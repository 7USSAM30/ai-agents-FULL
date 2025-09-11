"""
Sentiment Analysis Agent - Analyzes text sentiment and provides scoring
"""

import os
import asyncio
from typing import List, Dict, Any, Optional
from datetime import datetime
import json
import re
from dotenv import load_dotenv
import httpx

# Load environment variables
load_dotenv()

class SentimentAgent:
    """
    Sentiment Analysis Agent that analyzes text sentiment using multiple approaches
    """
    
    def __init__(self):
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.base_url = "https://api.openai.com/v1"
        
        # Sentiment keywords for rule-based analysis
        self.positive_keywords = [
            "good", "great", "excellent", "amazing", "wonderful", "fantastic", "awesome",
            "love", "like", "enjoy", "happy", "pleased", "satisfied", "impressed",
            "outstanding", "brilliant", "perfect", "best", "superb", "marvelous",
            "positive", "optimistic", "hopeful", "confident", "successful", "winning"
        ]
        
        self.negative_keywords = [
            "bad", "terrible", "awful", "horrible", "disgusting", "hate", "dislike",
            "angry", "frustrated", "disappointed", "sad", "upset", "worried", "concerned",
            "negative", "pessimistic", "hopeless", "failing", "losing", "broken",
            "problem", "issue", "error", "mistake", "wrong", "failed", "poor"
        ]
        
        self.neutral_keywords = [
            "okay", "fine", "average", "normal", "standard", "typical", "regular",
            "neutral", "indifferent", "moderate", "balanced", "fair", "acceptable"
        ]
    
    async def analyze_sentiment(self, text: str, method: str = "hybrid") -> Dict[str, Any]:
        """
        Analyze sentiment of the given text
        
        Args:
            text: Text to analyze
            method: Analysis method ("rule_based", "openai", "hybrid")
            
        Returns:
            Sentiment analysis results
        """
        if not text or not text.strip():
            return {
                "error": "No text provided for analysis",
                "sentiment": "neutral",
                "confidence": 0.0
            }
        
        start_time = datetime.now()
        
        try:
            if method == "rule_based":
                result = self._rule_based_analysis(text)
            elif method == "openai":
                result = await self._openai_analysis(text)
            else:  # hybrid
                rule_result = self._rule_based_analysis(text)
                openai_result = await self._openai_analysis(text)
                result = self._combine_analyses(rule_result, openai_result)
            
            processing_time = (datetime.now() - start_time).total_seconds()
            
            return {
                "type": "sentiment_analysis",
                "text": text[:200] + "..." if len(text) > 200 else text,
                "sentiment": result["sentiment"],
                "confidence": result["confidence"],
                "scores": result.get("scores", {}),
                "method_used": method,
                "processing_time": processing_time,
                "analyzed_at": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                "error": f"Sentiment analysis failed: {str(e)}",
                "sentiment": "neutral",
                "confidence": 0.0,
                "method_used": method
            }
    
    def _rule_based_analysis(self, text: str) -> Dict[str, Any]:
        """
        Rule-based sentiment analysis using keyword matching
        """
        text_lower = text.lower()
        
        # Count keyword matches
        positive_count = sum(1 for word in self.positive_keywords if word in text_lower)
        negative_count = sum(1 for word in self.negative_keywords if word in text_lower)
        neutral_count = sum(1 for word in self.neutral_keywords if word in text_lower)
        
        # Calculate scores
        total_words = len(text.split())
        positive_score = positive_count / max(total_words, 1)
        negative_score = negative_count / max(total_words, 1)
        neutral_score = neutral_count / max(total_words, 1)
        
        # Determine sentiment
        if positive_score > negative_score and positive_score > neutral_score:
            sentiment = "positive"
            confidence = min(positive_score * 2, 1.0)
        elif negative_score > positive_score and negative_score > neutral_score:
            sentiment = "negative"
            confidence = min(negative_score * 2, 1.0)
        else:
            sentiment = "neutral"
            confidence = min(neutral_score * 2, 1.0)
        
        return {
            "sentiment": sentiment,
            "confidence": confidence,
            "scores": {
                "positive": positive_score,
                "negative": negative_score,
                "neutral": neutral_score
            },
            "keyword_counts": {
                "positive": positive_count,
                "negative": negative_count,
                "neutral": neutral_count
            }
        }
    
    async def _openai_analysis(self, text: str) -> Dict[str, Any]:
        """
        OpenAI-based sentiment analysis
        """
        if not self.openai_api_key:
            return {
                "sentiment": "neutral",
                "confidence": 0.0,
                "error": "OpenAI API key not configured"
            }
        
        try:
            prompt = f"""
            Analyze the sentiment of the following text and respond with a JSON object containing:
            - sentiment: "positive", "negative", or "neutral"
            - confidence: a number between 0 and 1
            - reasoning: brief explanation
            
            Text: "{text}"
            
            Respond only with valid JSON.
            """
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self.openai_api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": "gpt-4o-mini",
                        "messages": [
                            {"role": "user", "content": prompt}
                        ],
                        "max_completion_tokens": 300,
                        "temperature": 0.1
                    },
                    timeout=10.0
                )
                
                if response.status_code == 200:
                    data = response.json()
                    content = data["choices"][0]["message"]["content"]
                    
                    # Parse JSON response
                    try:
                        result = json.loads(content)
                        return {
                            "sentiment": result.get("sentiment", "neutral"),
                            "confidence": float(result.get("confidence", 0.5)),
                            "reasoning": result.get("reasoning", "")
                        }
                    except json.JSONDecodeError:
                        # Fallback parsing
                        sentiment = "neutral"
                        confidence = 0.5
                        
                        if "positive" in content.lower():
                            sentiment = "positive"
                        elif "negative" in content.lower():
                            sentiment = "negative"
                        
                        return {
                            "sentiment": sentiment,
                            "confidence": confidence,
                            "reasoning": content
                        }
                else:
                    return {
                        "sentiment": "neutral",
                        "confidence": 0.0,
                        "error": f"OpenAI API error: {response.status_code}"
                    }
                    
        except Exception as e:
            return {
                "sentiment": "neutral",
                "confidence": 0.0,
                "error": f"OpenAI analysis failed: {str(e)}"
            }
    
    def _combine_analyses(self, rule_result: Dict, openai_result: Dict) -> Dict[str, Any]:
        """
        Combine rule-based and OpenAI analysis results
        """
        # Weight the results (rule-based: 0.3, OpenAI: 0.7)
        rule_weight = 0.3
        openai_weight = 0.7
        
        # Map sentiments to numbers for calculation
        sentiment_map = {"negative": -1, "neutral": 0, "positive": 1}
        
        rule_score = sentiment_map.get(rule_result["sentiment"], 0) * rule_result["confidence"]
        openai_score = sentiment_map.get(openai_result["sentiment"], 0) * openai_result["confidence"]
        
        combined_score = (rule_score * rule_weight) + (openai_score * openai_weight)
        
        # Determine final sentiment
        if combined_score > 0.2:
            sentiment = "positive"
        elif combined_score < -0.2:
            sentiment = "negative"
        else:
            sentiment = "neutral"
        
        # Calculate combined confidence
        combined_confidence = (rule_result["confidence"] * rule_weight) + (openai_result["confidence"] * openai_weight)
        
        return {
            "sentiment": sentiment,
            "confidence": min(combined_confidence, 1.0),
            "scores": {
                "rule_based": rule_result,
                "openai": openai_result,
                "combined_score": combined_score
            }
        }
    
    async def analyze_batch(self, texts: List[str], method: str = "hybrid") -> Dict[str, Any]:
        """
        Analyze sentiment for multiple texts
        
        Args:
            texts: List of texts to analyze
            method: Analysis method
            
        Returns:
            Batch analysis results
        """
        if not texts:
            return {
                "error": "No texts provided for analysis",
                "results": [],
                "summary": {}
            }
        
        start_time = datetime.now()
        results = []
        
        # Analyze each text
        for i, text in enumerate(texts):
            result = await self.analyze_sentiment(text, method)
            result["index"] = i
            results.append(result)
        
        # Calculate summary statistics
        sentiments = [r["sentiment"] for r in results if "sentiment" in r]
        confidences = [r["confidence"] for r in results if "confidence" in r]
        
        sentiment_counts = {
            "positive": sentiments.count("positive"),
            "negative": sentiments.count("negative"),
            "neutral": sentiments.count("neutral")
        }
        
        processing_time = (datetime.now() - start_time).total_seconds()
        
        return {
            "type": "batch_sentiment_analysis",
            "total_texts": len(texts),
            "results": results,
            "summary": {
                "sentiment_distribution": sentiment_counts,
                "average_confidence": sum(confidences) / len(confidences) if confidences else 0,
                "dominant_sentiment": max(sentiment_counts, key=sentiment_counts.get),
                "processing_time": processing_time
            },
            "analyzed_at": datetime.now().isoformat()
        }
    
    async def get_agent_status(self) -> Dict[str, Any]:
        """
        Get the current status of the Sentiment Agent
        """
        return {
            "name": "sentiment_agent",
            "status": "active",
            "description": "Analyzes text sentiment using rule-based and AI methods",
            "last_used": datetime.now().isoformat(),
            "performance_metrics": {
                "openai_configured": bool(self.openai_api_key),
                "positive_keywords": len(self.positive_keywords),
                "negative_keywords": len(self.negative_keywords),
                "neutral_keywords": len(self.neutral_keywords),
                "supported_methods": ["rule_based", "openai", "hybrid"]
            }
        }
