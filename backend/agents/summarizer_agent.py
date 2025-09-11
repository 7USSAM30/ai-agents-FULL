"""
Summarizer Agent - Combines results from multiple agents to provide comprehensive answers
"""

import os
import asyncio
from typing import List, Dict, Any, Optional
from datetime import datetime
import json
from dotenv import load_dotenv
import httpx

# Load environment variables
load_dotenv()

class SummarizerAgent:
    """
    Summarizer Agent that combines results from multiple agents to provide comprehensive answers
    """
    
    def __init__(self):
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.base_url = "https://api.openai.com/v1"
        
    async def summarize_results(self, query: str, agent_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Combine results from multiple agents into a comprehensive summary
        
        Args:
            query: Original user query
            agent_results: List of results from different agents
            
        Returns:
            Comprehensive summary combining all agent results
        """
        if not agent_results:
            return {
                "type": "comprehensive_summary",
                "summary": "No results available to summarize.",
                "sources": [],
                "query": query
            }
        
        start_time = datetime.now()
        
        try:
            # Analyze and categorize results
            categorized_results = self._categorize_results(agent_results)
            
            # Generate comprehensive summary
            if self.openai_api_key:
                summary = await self._ai_powered_summary(query, categorized_results)
            else:
                summary = self._rule_based_summary(query, categorized_results)
            
            # Extract key insights
            insights = self._extract_insights(categorized_results)
            
            # Generate recommendations
            recommendations = self._generate_recommendations(query, categorized_results)
            
            processing_time = (datetime.now() - start_time).total_seconds()
            
            return {
                "type": "comprehensive_summary",
                "query": query,
                "summary": summary,
                "insights": insights,
                "recommendations": recommendations,
                "sources": self._extract_sources(categorized_results),
                "agent_contributions": self._get_agent_contributions(categorized_results),
                "processing_time": processing_time,
                "generated_at": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                "type": "comprehensive_summary",
                "error": f"Failed to generate summary: {str(e)}",
                "query": query,
                "summary": "Unable to generate comprehensive summary due to an error.",
                "sources": []
            }
    
    def _categorize_results(self, agent_results: List[Dict[str, Any]]) -> Dict[str, List[Dict]]:
        """
        Categorize results by agent type and content
        """
        categorized = {
            "news": [],
            "research": [],
            "sentiment": [],
            "other": []
        }
        
        for result in agent_results:
            agent_type = result.get("agent_type", "other")
            result_data = result.get("result", {})
            
            if agent_type == "news_agent" or result_data.get("type") == "news_summary":
                categorized["news"].append(result_data)
            elif agent_type == "research_agent" or result_data.get("type") in ["knowledge_summary", "research_results"]:
                categorized["research"].append(result_data)
            elif agent_type == "sentiment_agent" or result_data.get("type") == "sentiment_analysis":
                categorized["sentiment"].append(result_data)
            else:
                categorized["other"].append(result_data)
        
        return categorized
    
    async def _ai_powered_summary(self, query: str, categorized_results: Dict[str, List[Dict]]) -> str:
        """
        Generate AI-powered comprehensive summary
        """
        try:
            # Prepare context for AI
            context_parts = []
            
            if categorized_results["news"]:
                news_content = self._extract_news_content(categorized_results["news"])
                context_parts.append(f"NEWS INFORMATION:\n{news_content}")
            
            if categorized_results["research"]:
                research_content = self._extract_research_content(categorized_results["research"])
                context_parts.append(f"RESEARCH FINDINGS:\n{research_content}")
            
            if categorized_results["sentiment"]:
                sentiment_content = self._extract_sentiment_content(categorized_results["sentiment"])
                context_parts.append(f"SENTIMENT ANALYSIS:\n{sentiment_content}")
            
            context = "\n\n".join(context_parts)
            
            prompt = f"""
            You are an expert AI assistant that combines information from multiple sources to provide comprehensive, accurate, and insightful answers.
            
            USER QUERY: "{query}"
            
            AVAILABLE INFORMATION:
            {context}
            
            ⚠️ CRITICAL FORMATTING REQUIREMENT ⚠️
            You MUST format your response EXACTLY like this example:
            
            1. **Section Title Here:**
               - Sub-point 1
               - Sub-point 2
            
            2. **Another Section Title:**
               - Sub-point 1
               - Sub-point 2
            
            3. **Final Section Title:**
               - Sub-point 1
               - Sub-point 2
            
            RULES:
            - EVERY main section MUST start with a number (1., 2., 3., etc.)
            - NEVER use bold headings without numbers
            - Use bullet points (-) for sub-points
            - Organize information logically into numbered sections
            
            Please provide a comprehensive summary that:
            1. Directly answers the user's query
            2. Combines insights from all available sources
            3. Highlights key findings and trends
            4. Provides context and background information
            5. Is well-structured and easy to read
            6. Maintains accuracy and cites sources when relevant
            
            REMEMBER: Start every main section with a number. Format: 1. **Title**, 2. **Title**, 3. **Title**
            
            CRITICAL: Your response MUST start with "1. **" - do not use bold headings without numbers!
            """
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self.openai_api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": "gpt-5",
                        "messages": [
                            {"role": "user", "content": prompt}
                        ],
                        "max_completion_tokens": 2000,
                        "temperature": 0.3
                    },
                    timeout=15.0
                )
                
                if response.status_code == 200:
                    data = response.json()
                    raw_summary = data["choices"][0]["message"]["content"].strip()
                    # Post-process to ensure proper formatting
                    return self._fix_formatting(raw_summary)
                else:
                    return self._rule_based_summary(query, categorized_results)
                    
        except Exception as e:
            print(f"AI summary failed: {e}")
            return self._rule_based_summary(query, categorized_results)
    
    def _fix_formatting(self, summary: str) -> str:
        """
        Post-process the summary to ensure proper numbered formatting
        """
        import re
        
        # If the summary doesn't start with a number, fix it
        if not summary.startswith(('1.', '1. **')):
            # Find all bold headings and convert them to numbered format
            lines = summary.split('\n')
            fixed_lines = []
            counter = 1
            
            for line in lines:
                # Check if line is a bold heading without a number
                if line.strip().startswith('**') and line.strip().endswith('**') and not line.strip().startswith(f'{counter}.'):
                    # Convert to numbered format
                    fixed_lines.append(f"{counter}. {line.strip()}")
                    counter += 1
                else:
                    fixed_lines.append(line)
            
            return '\n'.join(fixed_lines)
        
        return summary
    
    def _rule_based_summary(self, query: str, categorized_results: Dict[str, List[Dict]]) -> str:
        """
        Generate rule-based comprehensive summary with numbered lists
        """
        summary_parts = []
        
        # Add query context
        summary_parts.append(f"Based on your query about '{query}', here's a comprehensive overview:")
        
        counter = 1
        
        # News information
        if categorized_results["news"]:
            news_summary = self._extract_news_content(categorized_results["news"])
            summary_parts.append(f"\n{counter}. **Latest News & Updates:**\n{news_summary}")
            counter += 1
        
        # Research findings
        if categorized_results["research"]:
            research_summary = self._extract_research_content(categorized_results["research"])
            summary_parts.append(f"\n{counter}. **Research & Knowledge:**\n{research_summary}")
            counter += 1
        
        # Sentiment analysis
        if categorized_results["sentiment"]:
            sentiment_summary = self._extract_sentiment_content(categorized_results["sentiment"])
            summary_parts.append(f"\n{counter}. **Sentiment Analysis:**\n{sentiment_summary}")
            counter += 1
        
        # Combine all parts
        return "\n".join(summary_parts)
    
    def _extract_news_content(self, news_results: List[Dict]) -> str:
        """
        Extract and format news content with numbered lists
        """
        if not news_results:
            return "No recent news available."
        
        content_parts = []
        for result in news_results:
            articles = result.get("articles", [])
            if articles:
                content_parts.append(f"Found {len(articles)} relevant articles:")
                for i, article in enumerate(articles[:3], 1):  # Top 3 articles
                    content_parts.append(f"{i}. {article.get('headline', 'No title')}")
                    if article.get('summary'):
                        content_parts.append(f"   {article.get('summary', '')[:150]}...")
        
        return "\n".join(content_parts) if content_parts else "No detailed news content available."
    
    def _extract_research_content(self, research_results: List[Dict]) -> str:
        """
        Extract and format research content with numbered lists
        """
        if not research_results:
            return "No research information available."
        
        content_parts = []
        for result in research_results:
            if result.get("summary"):
                content_parts.append(result["summary"])
            elif result.get("documents"):
                docs = result["documents"]
                content_parts.append(f"Found {len(docs)} relevant documents:")
                for i, doc in enumerate(docs[:2], 1):  # Top 2 documents
                    content_parts.append(f"{i}. {doc.get('title', 'No title')}")
                    if doc.get('content'):
                        content_parts.append(f"   {doc.get('content', '')[:150]}...")
        
        return "\n".join(content_parts) if content_parts else "No detailed research content available."
    
    def _extract_sentiment_content(self, sentiment_results: List[Dict]) -> str:
        """
        Extract and format sentiment content
        """
        if not sentiment_results:
            return "No sentiment analysis available."
        
        content_parts = []
        for result in sentiment_results:
            sentiment = result.get("sentiment", "unknown")
            confidence = result.get("confidence", 0)
            text = result.get("text", "")
            
            content_parts.append(f"Sentiment: {sentiment.title()} (Confidence: {confidence:.1%})")
            if text:
                content_parts.append(f"Analyzed text: {text[:100]}...")
        
        return "\n".join(content_parts) if content_parts else "No detailed sentiment information available."
    
    def _extract_insights(self, categorized_results: Dict[str, List[Dict]]) -> List[str]:
        """
        Extract key insights from all results
        """
        insights = []
        
        # News insights
        if categorized_results["news"]:
            total_articles = sum(len(result.get("articles", [])) for result in categorized_results["news"])
            if total_articles > 0:
                insights.append(f"Found {total_articles} relevant news articles")
        
        # Research insights
        if categorized_results["research"]:
            total_docs = sum(len(result.get("documents", [])) for result in categorized_results["research"])
            if total_docs > 0:
                insights.append(f"Retrieved {total_docs} research documents")
        
        # Sentiment insights
        if categorized_results["sentiment"]:
            sentiments = [result.get("sentiment") for result in categorized_results["sentiment"]]
            if sentiments:
                most_common = max(set(sentiments), key=sentiments.count)
                insights.append(f"Overall sentiment trend: {most_common}")
        
        return insights
    
    def _generate_recommendations(self, query: str, categorized_results: Dict[str, List[Dict]]) -> List[str]:
        """
        Generate actionable recommendations based on results
        """
        recommendations = []
        
        # News recommendations
        if categorized_results["news"]:
            recommendations.append("📰 Stay updated with the latest news on this topic")
        
        # Research recommendations
        if categorized_results["research"]:
            recommendations.append("🔍 Explore the research documents for deeper insights")
        
        # Sentiment recommendations
        if categorized_results["sentiment"]:
            recommendations.append("💭 Consider the sentiment analysis for decision making")
        
        # General recommendations
        recommendations.append("🔄 Ask follow-up questions for more specific information")
        
        return recommendations
    
    def _extract_sources(self, categorized_results: Dict[str, List[Dict]]) -> List[Dict[str, str]]:
        """
        Extract all sources from results
        """
        sources = []
        
        for category, results in categorized_results.items():
            for result in results:
                if category == "news" and result.get("articles"):
                    for article in result["articles"]:
                        sources.append({
                            "type": "news",
                            "title": article.get("headline", "News Article"),
                            "source": article.get("source", "Unknown"),
                            "url": article.get("url", "")
                        })
                elif category == "research" and result.get("sources"):
                    for source in result["sources"]:
                        sources.append({
                            "type": "research",
                            "title": source.get("title", "Research Document"),
                            "source": source.get("source", "Unknown"),
                            "similarity": source.get("similarity_score", 0)
                        })
        
        return sources
    
    def _get_agent_contributions(self, categorized_results: Dict[str, List[Dict]]) -> Dict[str, Any]:
        """
        Get contribution summary from each agent
        """
        contributions = {}
        
        for category, results in categorized_results.items():
            if results:
                contributions[category] = {
                    "count": len(results),
                    "status": "active",
                    "contribution": f"Provided {len(results)} result(s)"
                }
            else:
                contributions[category] = {
                    "count": 0,
                    "status": "inactive",
                    "contribution": "No results available"
                }
        
        return contributions
    
    async def get_agent_status(self) -> Dict[str, Any]:
        """
        Get the current status of the Summarizer Agent
        """
        return {
            "name": "summarizer_agent",
            "status": "active",
            "description": "Combines results from multiple agents to provide comprehensive answers",
            "last_used": datetime.now().isoformat(),
            "performance_metrics": {
                "openai_configured": bool(self.openai_api_key),
                "supported_input_types": ["news_summary", "knowledge_summary", "sentiment_analysis", "research_results"],
                "output_type": "comprehensive_summary",
                "capabilities": ["multi_agent_combination", "ai_powered_summarization", "insight_extraction", "recommendation_generation"]
            }
        }
