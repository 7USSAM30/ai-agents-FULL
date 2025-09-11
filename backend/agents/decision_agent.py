"""
Enhanced Decision Agent for intelligent query routing and multi-agent coordination.
"""

import re
import asyncio
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import openai
import os
from datetime import datetime

class QueryIntent(Enum):
    NEWS = "news"
    RESEARCH = "research"
    SENTIMENT = "sentiment"
    MULTI_AGENT = "multi_agent"
    UNKNOWN = "unknown"

class QueryComplexity(Enum):
    SIMPLE = "simple"
    MODERATE = "moderate"
    COMPLEX = "complex"

@dataclass
class QueryAnalysis:
    intent: QueryIntent
    complexity: QueryComplexity
    confidence: float
    keywords: List[str]
    entities: List[str]
    suggested_agents: List[str]
    reasoning: str

@dataclass
class AgentCapability:
    name: str
    description: str
    keywords: List[str]
    max_complexity: QueryComplexity
    priority: int

class DecisionAgent:
    def __init__(self):
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        if self.openai_api_key:
            openai.api_key = self.openai_api_key
        
        # Define agent capabilities
        self.agent_capabilities = {
            "news_agent": AgentCapability(
                name="News Agent",
                description="Fetches and analyzes latest technology news and articles",
                keywords=["news", "latest", "recent", "technology", "tech", "ai", "artificial intelligence", "update", "announcement"],
                max_complexity=QueryComplexity.MODERATE,
                priority=1
            ),
            "research_agent": AgentCapability(
                name="Research Agent",
                description="Searches knowledge base and provides research insights",
                keywords=["research", "document", "knowledge", "find", "search", "what is", "how does", "explain", "tell me about", "information"],
                max_complexity=QueryComplexity.COMPLEX,
                priority=2
            ),
            "sentiment_agent": AgentCapability(
                name="Sentiment Agent",
                description="Analyzes sentiment, emotions, and opinions in text",
                keywords=["sentiment", "emotion", "feeling", "mood", "opinion", "attitude", "analyze", "analysis", "positive", "negative"],
                max_complexity=QueryComplexity.SIMPLE,
                priority=3
            )
        }
        
        # Query patterns for intent detection
        self.intent_patterns = {
            QueryIntent.NEWS: [
                r"\b(news|latest|recent|update|announcement|breaking)\b",
                r"\b(technology|tech|ai|artificial intelligence)\b.*\b(news|update|latest)\b",
                r"what.*happening.*(tech|ai|technology)",
                r"tell me.*latest.*(news|update)"
            ],
            QueryIntent.RESEARCH: [
                r"\b(what is|how does|explain|tell me about|research|find|search)\b",
                r"\b(knowledge|information|document|study|analysis)\b",
                r"can you.*(explain|describe|tell me)",
                r"i want to know.*about"
            ],
            QueryIntent.SENTIMENT: [
                r"\b(sentiment|emotion|feeling|mood|opinion|attitude)\b",
                r"\b(analyze|analysis|positive|negative|neutral)\b",
                r"how.*feel.*about",
                r"what.*opinion.*about"
            ]
        }

    async def analyze_query(self, query: str) -> QueryAnalysis:
        """Analyze query to determine intent, complexity, and suggested agents."""
        query_lower = query.lower()
        
        # Extract keywords and entities
        keywords = self._extract_keywords(query_lower)
        entities = self._extract_entities(query_lower)
        
        # Determine intent
        intent, intent_confidence = self._detect_intent(query_lower)
        
        # Determine complexity
        complexity = self._assess_complexity(query, keywords, entities)
        
        # Suggest agents
        suggested_agents = self._suggest_agents(intent, complexity, keywords)
        
        # Generate reasoning
        reasoning = self._generate_reasoning(intent, complexity, suggested_agents, keywords)
        
        return QueryAnalysis(
            intent=intent,
            complexity=complexity,
            confidence=intent_confidence,
            keywords=keywords,
            entities=entities,
            suggested_agents=suggested_agents,
            reasoning=reasoning
        )

    def _extract_keywords(self, query: str) -> List[str]:
        """Extract relevant keywords from query."""
        # Common stop words to filter out
        stop_words = {"the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", "of", "with", "by", "is", "are", "was", "were", "be", "been", "have", "has", "had", "do", "does", "did", "will", "would", "could", "should", "may", "might", "can", "this", "that", "these", "those", "i", "you", "he", "she", "it", "we", "they", "me", "him", "her", "us", "them"}
        
        # Extract words and filter out stop words
        words = re.findall(r'\b\w+\b', query)
        keywords = [word for word in words if word not in stop_words and len(word) > 2]
        
        return keywords

    def _extract_entities(self, query: str) -> List[str]:
        """Extract named entities from query."""
        # Simple entity extraction - can be enhanced with NER
        entities = []
        
        # Technology entities
        tech_entities = ["ai", "artificial intelligence", "machine learning", "deep learning", "neural network", "chatgpt", "openai", "google", "microsoft", "apple", "iphone", "android", "python", "javascript", "react", "node.js"]
        
        for entity in tech_entities:
            if entity in query:
                entities.append(entity)
        
        return entities

    def _detect_intent(self, query: str) -> Tuple[QueryIntent, float]:
        """Detect query intent using pattern matching and AI."""
        scores = {}
        
        # Pattern-based scoring
        for intent, patterns in self.intent_patterns.items():
            score = 0
            for pattern in patterns:
                matches = len(re.findall(pattern, query, re.IGNORECASE))
                score += matches
            scores[intent] = score
        
        # AI-based intent detection if OpenAI is available
        if self.openai_api_key:
            try:
                ai_intent = self._ai_intent_detection(query)
                if ai_intent:
                    scores[ai_intent] = scores.get(ai_intent, 0) + 2
            except Exception as e:
                print(f"AI intent detection failed: {e}")
        
        # Determine best intent
        if not scores or max(scores.values()) == 0:
            return QueryIntent.UNKNOWN, 0.0
        
        best_intent = max(scores, key=scores.get)
        confidence = min(scores[best_intent] / 3.0, 1.0)  # Normalize confidence
        
        return best_intent, confidence

    def _ai_intent_detection(self, query: str) -> Optional[QueryIntent]:
        """Use AI to detect query intent."""
        try:
            client = openai.OpenAI(api_key=self.openai_api_key)
            response = client.chat.completions.create(
                model="gpt-5",
                messages=[
                    {"role": "system", "content": "Analyze the query intent. Return only one of: news, research, sentiment, multi_agent, unknown"},
                    {"role": "user", "content": f"Query: {query}"}
                ],
                max_completion_tokens=50,
                temperature=0.1
            )
            
            intent_str = response.choices[0].message.content.strip().lower()
            intent_map = {
                "news": QueryIntent.NEWS,
                "research": QueryIntent.RESEARCH,
                "sentiment": QueryIntent.SENTIMENT,
                "multi_agent": QueryIntent.MULTI_AGENT,
                "unknown": QueryIntent.UNKNOWN
            }
            
            return intent_map.get(intent_str, QueryIntent.UNKNOWN)
        except Exception as e:
            print(f"AI intent detection error: {e}")
            return None

    def _assess_complexity(self, query: str, keywords: List[str], entities: List[str]) -> QueryComplexity:
        """Assess query complexity based on various factors."""
        complexity_score = 0
        
        # Length factor
        if len(query) > 100:
            complexity_score += 2
        elif len(query) > 50:
            complexity_score += 1
        
        # Keyword count
        complexity_score += len(keywords) * 0.5
        
        # Entity count
        complexity_score += len(entities) * 0.3
        
        # Question complexity indicators
        complex_indicators = ["compare", "analyze", "evaluate", "explain", "describe", "discuss", "pros and cons", "advantages and disadvantages"]
        for indicator in complex_indicators:
            if indicator in query.lower():
                complexity_score += 1
        
        # Multiple questions
        question_count = query.count("?")
        if question_count > 1:
            complexity_score += 1
        
        # Determine complexity level
        if complexity_score >= 4:
            return QueryComplexity.COMPLEX
        elif complexity_score >= 2:
            return QueryComplexity.MODERATE
        else:
            return QueryComplexity.SIMPLE

    def _suggest_agents(self, intent: QueryIntent, complexity: QueryComplexity, keywords: List[str]) -> List[str]:
        """Suggest appropriate agents based on intent and complexity."""
        suggestions = []
        
        # Intent-based suggestions
        if intent == QueryIntent.NEWS:
            suggestions.append("news_agent")
        elif intent == QueryIntent.RESEARCH:
            suggestions.append("research_agent")
        elif intent == QueryIntent.SENTIMENT:
            suggestions.append("sentiment_agent")
        elif intent == QueryIntent.MULTI_AGENT:
            suggestions = ["news_agent", "research_agent", "sentiment_agent"]
        
        # Keyword-based suggestions
        for agent_name, capability in self.agent_capabilities.items():
            if agent_name not in suggestions:
                for keyword in keywords:
                    if keyword in capability.keywords:
                        suggestions.append(agent_name)
                        break
        
        # Complexity-based filtering
        filtered_suggestions = []
        for agent_name in suggestions:
            capability = self.agent_capabilities.get(agent_name)
            if capability and self._can_handle_complexity(capability, complexity):
                filtered_suggestions.append(agent_name)
        
        # If no suggestions, default to research agent
        if not filtered_suggestions:
            filtered_suggestions = ["research_agent"]
        
        # Remove duplicates and sort by priority
        unique_suggestions = list(dict.fromkeys(filtered_suggestions))
        unique_suggestions.sort(key=lambda x: self.agent_capabilities.get(x, AgentCapability("", "", [], QueryComplexity.SIMPLE, 999)).priority)
        
        return unique_suggestions

    def _can_handle_complexity(self, capability: AgentCapability, complexity: QueryComplexity) -> bool:
        """Check if agent can handle the query complexity."""
        complexity_levels = {
            QueryComplexity.SIMPLE: 1,
            QueryComplexity.MODERATE: 2,
            QueryComplexity.COMPLEX: 3
        }
        
        return complexity_levels[complexity] <= complexity_levels[capability.max_complexity]

    def _generate_reasoning(self, intent: QueryIntent, complexity: QueryComplexity, suggested_agents: List[str], keywords: List[str]) -> str:
        """Generate human-readable reasoning for the decision."""
        reasoning_parts = []
        
        # Intent reasoning
        reasoning_parts.append(f"Intent detected: {intent.value}")
        
        # Complexity reasoning
        reasoning_parts.append(f"Complexity level: {complexity.value}")
        
        # Agent selection reasoning
        if suggested_agents:
            agent_names = [self.agent_capabilities.get(agent, AgentCapability(agent, "", [], QueryComplexity.SIMPLE, 0)).name for agent in suggested_agents]
            reasoning_parts.append(f"Selected agents: {', '.join(agent_names)}")
        
        # Keyword reasoning
        if keywords:
            reasoning_parts.append(f"Key terms: {', '.join(keywords[:5])}")  # Limit to 5 keywords
        
        return " | ".join(reasoning_parts)

    async def coordinate_agents(self, query: str, available_agents: Dict[str, Any]) -> Dict[str, Any]:
        """Coordinate multiple agents for complex queries."""
        analysis = await self.analyze_query(query)
        
        coordination_plan = {
            "query_analysis": analysis,
            "execution_plan": [],
            "parallel_execution": False,
            "fallback_strategy": "research_agent"
        }
        
        # Determine execution strategy
        if len(analysis.suggested_agents) > 1:
            coordination_plan["parallel_execution"] = True
            coordination_plan["execution_plan"] = [
                {
                    "agent": agent,
                    "priority": self.agent_capabilities.get(agent, AgentCapability("", "", [], QueryComplexity.SIMPLE, 0)).priority,
                    "expected_result_type": self._get_expected_result_type(agent)
                }
                for agent in analysis.suggested_agents
            ]
        else:
            coordination_plan["execution_plan"] = [
                {
                    "agent": analysis.suggested_agents[0],
                    "priority": 1,
                    "expected_result_type": self._get_expected_result_type(analysis.suggested_agents[0])
                }
            ]
        
        return coordination_plan

    def _get_expected_result_type(self, agent_name: str) -> str:
        """Get expected result type for agent."""
        result_types = {
            "news_agent": "news_summary",
            "research_agent": "knowledge_summary",
            "sentiment_agent": "sentiment_analysis"
        }
        return result_types.get(agent_name, "unknown")

    def get_agent_status(self) -> Dict[str, Any]:
        """Get decision agent status."""
        return {
            "status": "active",
            "capabilities": len(self.agent_capabilities),
            "intent_patterns": len(self.intent_patterns),
            "ai_enabled": bool(self.openai_api_key),
            "last_updated": datetime.now().isoformat()
        }
