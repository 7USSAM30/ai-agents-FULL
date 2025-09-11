"""
Frontend Agent for data formatting and UI component mapping.
Handles data transformation and component selection for the frontend.
"""

import json
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass
from enum import Enum
from datetime import datetime

class ComponentType(Enum):
    NEWS_CARDS = "news_cards"
    RESEARCH_SUMMARY = "research_summary"
    SENTIMENT_ANALYSIS = "sentiment_analysis"
    COMPREHENSIVE_SUMMARY = "comprehensive_summary"
    ERROR_MESSAGE = "error_message"
    LOADING_SPINNER = "loading_spinner"
    PLACEHOLDER = "placeholder"

class DataFormat(Enum):
    JSON = "json"
    HTML = "html"
    MARKDOWN = "markdown"
    PLAIN_TEXT = "plain_text"

@dataclass
class UIComponent:
    type: ComponentType
    data: Dict[str, Any]
    props: Dict[str, Any]
    metadata: Dict[str, Any]

@dataclass
class FormattedResponse:
    component_type: ComponentType
    formatted_data: Dict[str, Any]
    ui_props: Dict[str, Any]
    metadata: Dict[str, Any]
    timestamp: str

class FrontendAgent:
    def __init__(self):
        self.component_mappings = {
            "news_summary": ComponentType.NEWS_CARDS,
            "knowledge_summary": ComponentType.RESEARCH_SUMMARY,
            "research_results": ComponentType.RESEARCH_SUMMARY,
            "sentiment_analysis": ComponentType.SENTIMENT_ANALYSIS,
            "comprehensive_summary": ComponentType.COMPREHENSIVE_SUMMARY,
            "error": ComponentType.ERROR_MESSAGE,
            "placeholder": ComponentType.PLACEHOLDER
        }
        
        # UI component configurations
        self.component_configs = {
            ComponentType.NEWS_CARDS: {
                "max_items": 10,
                "show_images": True,
                "show_sources": True,
                "show_timestamps": True,
                "layout": "grid"
            },
            ComponentType.RESEARCH_SUMMARY: {
                "max_sources": 5,
                "show_similarity_scores": True,
                "expandable": True,
                "highlight_keywords": True
            },
            ComponentType.SENTIMENT_ANALYSIS: {
                "show_confidence": True,
                "show_breakdown": True,
                "color_coded": True,
                "show_emotions": True
            },
            ComponentType.COMPREHENSIVE_SUMMARY: {
                "show_insights": True,
                "show_recommendations": True,
                "show_agent_contributions": True,
                "show_sources": True,
                "collapsible_sections": True
            }
        }

    async def format_response(self, result: Dict[str, Any], query: str = "") -> FormattedResponse:
        """Format agent result for frontend display."""
        try:
            result_type = result.get("type", "unknown")
            
            # Map result type to component type
            component_type = self.component_mappings.get(result_type, ComponentType.PLACEHOLDER)
            
            # Get component configuration
            config = self.component_configs.get(component_type, {})
            
            # Format data based on component type
            formatted_data = await self._format_data_for_component(component_type, result, config)
            
            # Generate UI props
            ui_props = await self._generate_ui_props(component_type, formatted_data, config)
            
            # Generate metadata
            metadata = await self._generate_metadata(result, query, component_type)
            
            return FormattedResponse(
                component_type=component_type,
                formatted_data=formatted_data,
                ui_props=ui_props,
                metadata=metadata,
                timestamp=datetime.now().isoformat()
            )
            
        except Exception as e:
            print(f"Frontend Agent formatting error: {e}")
            return self._create_error_response(str(e))

    async def _format_data_for_component(self, component_type: ComponentType, result: Dict[str, Any], config: Dict[str, Any]) -> Dict[str, Any]:
        """Format data specifically for the component type."""
        data = result.get("data", result)
        
        if component_type == ComponentType.NEWS_CARDS:
            return await self._format_news_cards(data, config)
        elif component_type == ComponentType.RESEARCH_SUMMARY:
            return await self._format_research_summary(data, config)
        elif component_type == ComponentType.SENTIMENT_ANALYSIS:
            return await self._format_sentiment_analysis(data, config)
        elif component_type == ComponentType.COMPREHENSIVE_SUMMARY:
            return await self._format_comprehensive_summary(data, config)
        elif component_type == ComponentType.ERROR_MESSAGE:
            return await self._format_error_message(data, config)
        else:
            return await self._format_placeholder(data, config)

    async def _format_news_cards(self, data: Dict[str, Any], config: Dict[str, Any]) -> Dict[str, Any]:
        """Format news data for news cards component."""
        articles = data.get("articles", [])
        max_items = config.get("max_items", 10)
        
        formatted_articles = []
        for article in articles[:max_items]:
            formatted_article = {
                "id": self._generate_id(article.get("headline", "")),
                "title": article.get("headline", "No title"),
                "summary": article.get("summary", "No summary available"),
                "source": article.get("source", "Unknown source"),
                "published_at": article.get("published_at", ""),
                "url": article.get("url", ""),
                "image_url": article.get("image_url", ""),
                "category": article.get("category", "General"),
                "sentiment": article.get("sentiment", "neutral"),
                "relevance_score": article.get("relevance_score", 0.0)
            }
            formatted_articles.append(formatted_article)
        
        return {
            "articles": formatted_articles,
            "total_count": len(articles),
            "displayed_count": len(formatted_articles),
            "has_more": len(articles) > max_items
        }

    async def _format_research_summary(self, data: Dict[str, Any], config: Dict[str, Any]) -> Dict[str, Any]:
        """Format research data for research summary component."""
        summary = data.get("summary", "No summary available")
        sources = data.get("sources", [])
        documents = data.get("documents", [])
        max_sources = config.get("max_sources", 5)
        
        # Format sources
        formatted_sources = []
        for source in sources[:max_sources]:
            formatted_source = {
                "id": self._generate_id(source.get("title", "")),
                "title": source.get("title", "Unknown source"),
                "similarity_score": source.get("similarity_score", 0.0),
                "url": source.get("url", ""),
                "type": source.get("type", "document")
            }
            formatted_sources.append(formatted_source)
        
        # Format documents
        formatted_documents = []
        for doc in documents[:max_sources]:
            formatted_doc = {
                "id": self._generate_id(doc.get("title", "")),
                "title": doc.get("title", "Unknown document"),
                "content": doc.get("content", ""),
                "source": doc.get("source", "Unknown"),
                "similarity_score": doc.get("similarity_score", 0.0),
                "preview": doc.get("content", "")[:200] + "..." if len(doc.get("content", "")) > 200 else doc.get("content", "")
            }
            formatted_documents.append(formatted_doc)
        
        return {
            "summary": summary,
            "sources": formatted_sources,
            "documents": formatted_documents,
            "total_sources": len(sources),
            "total_documents": len(documents),
            "has_more_sources": len(sources) > max_sources,
            "has_more_documents": len(documents) > max_sources
        }

    async def _format_sentiment_analysis(self, data: Dict[str, Any], config: Dict[str, Any]) -> Dict[str, Any]:
        """Format sentiment data for sentiment analysis component."""
        sentiment = data.get("sentiment", "neutral")
        confidence = data.get("confidence", 0.0)
        text = data.get("text", "")
        breakdown = data.get("breakdown", {})
        emotions = data.get("emotions", {})
        
        # Determine sentiment color and icon
        sentiment_info = self._get_sentiment_info(sentiment)
        
        return {
            "sentiment": sentiment,
            "confidence": confidence,
            "confidence_percentage": round(confidence * 100, 1),
            "text": text,
            "breakdown": breakdown,
            "emotions": emotions,
            "color": sentiment_info["color"],
            "icon": sentiment_info["icon"],
            "description": sentiment_info["description"]
        }

    async def _format_comprehensive_summary(self, data: Dict[str, Any], config: Dict[str, Any]) -> Dict[str, Any]:
        """Format comprehensive summary data."""
        summary = data.get("summary", "No summary available")
        insights = data.get("insights", [])
        recommendations = data.get("recommendations", [])
        agent_contributions = data.get("agent_contributions", {})
        sources = data.get("sources", [])
        
        # Format insights
        formatted_insights = []
        for i, insight in enumerate(insights):
            formatted_insights.append({
                "id": f"insight_{i}",
                "text": insight,
                "type": "insight",
                "priority": "high" if i < 3 else "medium"
            })
        
        # Format recommendations
        formatted_recommendations = []
        for i, recommendation in enumerate(recommendations):
            formatted_recommendations.append({
                "id": f"recommendation_{i}",
                "text": recommendation,
                "type": "recommendation",
                "priority": "high" if i < 3 else "medium"
            })
        
        # Format agent contributions
        formatted_contributions = []
        for agent, info in agent_contributions.items():
            formatted_contributions.append({
                "agent": agent,
                "contribution": info.get("contribution", ""),
                "status": info.get("status", "unknown"),
                "confidence": info.get("confidence", 0.0)
            })
        
        # Format sources
        formatted_sources = []
        for i, source in enumerate(sources[:5]):  # Limit to 5 sources
            formatted_sources.append({
                "id": f"source_{i}",
                "title": source.get("title", "Unknown source"),
                "source": source.get("source", ""),
                "relevance": source.get("similarity_score", 0.0)
            })
        
        return {
            "summary": summary,
            "insights": formatted_insights,
            "recommendations": formatted_recommendations,
            "agent_contributions": formatted_contributions,
            "sources": formatted_sources,
            "total_insights": len(insights),
            "total_recommendations": len(recommendations),
            "total_contributions": len(agent_contributions)
        }

    async def _format_error_message(self, data: Dict[str, Any], config: Dict[str, Any]) -> Dict[str, Any]:
        """Format error data for error message component."""
        error = data.get("error", "An unknown error occurred")
        
        return {
            "error": error,
            "type": "error",
            "severity": "high",
            "suggestions": [
                "Try rephrasing your question",
                "Check your internet connection",
                "Try again in a few moments"
            ]
        }

    async def _format_placeholder(self, data: Dict[str, Any], config: Dict[str, Any]) -> Dict[str, Any]:
        """Format placeholder data."""
        message = data.get("data", "No data available")
        
        return {
            "message": message,
            "type": "placeholder",
            "suggestions": [
                "Ask about technology news",
                "Request research information",
                "Analyze sentiment of text"
            ]
        }

    async def _generate_ui_props(self, component_type: ComponentType, formatted_data: Dict[str, Any], config: Dict[str, Any]) -> Dict[str, Any]:
        """Generate UI-specific properties for the component."""
        base_props = {
            "className": f"component-{component_type.value}",
            "data-testid": f"component-{component_type.value}",
            "aria-label": f"{component_type.value.replace('_', ' ')} component"
        }
        
        if component_type == ComponentType.NEWS_CARDS:
            base_props.update({
                "layout": config.get("layout", "grid"),
                "showImages": config.get("show_images", True),
                "showSources": config.get("show_sources", True),
                "showTimestamps": config.get("show_timestamps", True)
            })
        elif component_type == ComponentType.RESEARCH_SUMMARY:
            base_props.update({
                "expandable": config.get("expandable", True),
                "showSimilarityScores": config.get("show_similarity_scores", True),
                "highlightKeywords": config.get("highlight_keywords", True)
            })
        elif component_type == ComponentType.SENTIMENT_ANALYSIS:
            base_props.update({
                "showConfidence": config.get("show_confidence", True),
                "showBreakdown": config.get("show_breakdown", True),
                "colorCoded": config.get("color_coded", True),
                "showEmotions": config.get("show_emotions", True)
            })
        elif component_type == ComponentType.COMPREHENSIVE_SUMMARY:
            base_props.update({
                "showInsights": config.get("show_insights", True),
                "showRecommendations": config.get("show_recommendations", True),
                "showAgentContributions": config.get("show_agent_contributions", True),
                "showSources": config.get("show_sources", True),
                "collapsibleSections": config.get("collapsible_sections", True)
            })
        
        return base_props

    async def _generate_metadata(self, result: Dict[str, Any], query: str, component_type: ComponentType) -> Dict[str, Any]:
        """Generate metadata for the formatted response."""
        return {
            "query": query,
            "original_type": result.get("type", "unknown"),
            "component_type": component_type.value,
            "data_size": len(str(result)),
            "processing_time": 0.0,  # TODO: Add actual processing time
            "version": "1.0.0"
        }

    def _get_sentiment_info(self, sentiment: str) -> Dict[str, str]:
        """Get sentiment-specific information."""
        sentiment_map = {
            "positive": {
                "color": "green",
                "icon": "😊",
                "description": "Positive sentiment detected"
            },
            "negative": {
                "color": "red",
                "icon": "😞",
                "description": "Negative sentiment detected"
            },
            "neutral": {
                "color": "gray",
                "icon": "😐",
                "description": "Neutral sentiment detected"
            }
        }
        
        return sentiment_map.get(sentiment.lower(), sentiment_map["neutral"])

    def _generate_id(self, text: str) -> str:
        """Generate a simple ID from text."""
        import hashlib
        return hashlib.md5(text.encode()).hexdigest()[:8]

    def _create_error_response(self, error_message: str) -> FormattedResponse:
        """Create an error response."""
        return FormattedResponse(
            component_type=ComponentType.ERROR_MESSAGE,
            formatted_data={
                "error": error_message,
                "type": "error",
                "severity": "high"
            },
            ui_props={
                "className": "component-error-message",
                "data-testid": "component-error-message"
            },
            metadata={
                "error": True,
                "timestamp": datetime.now().isoformat()
            },
            timestamp=datetime.now().isoformat()
        )

    async def get_agent_status(self) -> Dict[str, Any]:
        """Get frontend agent status."""
        return {
            "status": "active",
            "component_types": len(self.component_mappings),
            "supported_formats": [fmt.value for fmt in DataFormat],
            "last_updated": datetime.now().isoformat()
        }

    async def format_multiple_responses(self, results: List[Dict[str, Any]], query: str = "") -> List[FormattedResponse]:
        """Format multiple agent results for frontend display."""
        formatted_responses = []
        
        for result in results:
            formatted_response = await self.format_response(result, query)
            formatted_responses.append(formatted_response)
        
        return formatted_responses

    async def get_component_schema(self, component_type: ComponentType) -> Dict[str, Any]:
        """Get schema for a specific component type."""
        schemas = {
            ComponentType.NEWS_CARDS: {
                "type": "object",
                "properties": {
                    "articles": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "id": {"type": "string"},
                                "title": {"type": "string"},
                                "summary": {"type": "string"},
                                "source": {"type": "string"},
                                "published_at": {"type": "string"},
                                "url": {"type": "string"},
                                "image_url": {"type": "string"},
                                "category": {"type": "string"},
                                "sentiment": {"type": "string"},
                                "relevance_score": {"type": "number"}
                            }
                        }
                    }
                }
            },
            ComponentType.SENTIMENT_ANALYSIS: {
                "type": "object",
                "properties": {
                    "sentiment": {"type": "string"},
                    "confidence": {"type": "number"},
                    "confidence_percentage": {"type": "number"},
                    "text": {"type": "string"},
                    "color": {"type": "string"},
                    "icon": {"type": "string"},
                    "description": {"type": "string"}
                }
            }
        }
        
        return schemas.get(component_type, {"type": "object", "properties": {}})
