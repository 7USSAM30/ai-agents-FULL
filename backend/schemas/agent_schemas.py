"""
Agent-specific schemas for the Multi-Agent AI System
Defines response models for each specialized agent
"""

from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
from enum import Enum

class DocumentSource(BaseModel):
    """Document source information"""
    title: str = Field(..., description="Document title")
    url: Optional[str] = Field(None, description="Document URL")
    page_number: Optional[int] = Field(None, description="Page number if applicable")
    confidence: float = Field(..., description="Relevance confidence score", ge=0.0, le=1.0)

class ResearchAgentResponse(BaseModel):
    """Response from the Research Agent (RAG)"""
    type: str = Field(default="document_answer", description="Response type")
    answer: str = Field(..., description="Generated answer from documents")
    sources: List[DocumentSource] = Field(..., description="Source documents used")
    confidence: float = Field(..., description="Overall confidence score", ge=0.0, le=1.0)
    processing_time: Optional[float] = Field(None, description="Processing time in seconds")
    
    class Config:
        json_schema_extra = {
            "example": {
                "type": "document_answer",
                "answer": "Based on the documents, AI sentiment analysis shows...",
                "sources": [
                    {
                        "title": "AI Research Paper 2024",
                        "url": "https://example.com/paper.pdf",
                        "page_number": 15,
                        "confidence": 0.95
                    }
                ],
                "confidence": 0.87,
                "processing_time": 1.2
            }
        }

class NewsArticle(BaseModel):
    """News article information"""
    headline: str = Field(..., description="Article headline")
    summary: str = Field(..., description="Article summary")
    url: str = Field(..., description="Article URL")
    published_at: str = Field(..., description="Publication timestamp")
    source: str = Field(..., description="News source")
    relevance_score: float = Field(..., description="Relevance to query", ge=0.0, le=1.0)

class NewsAgentResponse(BaseModel):
    """Response from the News Agent"""
    type: str = Field(default="news_summary", description="Response type")
    articles: List[NewsArticle] = Field(..., description="List of relevant news articles")
    total_articles: int = Field(..., description="Total number of articles found")
    query_used: str = Field(..., description="Search query used")
    processing_time: Optional[float] = Field(None, description="Processing time in seconds")
    
    class Config:
        json_schema_extra = {
            "example": {
                "type": "news_summary",
                "articles": [
                    {
                        "headline": "AI Breakthrough in Natural Language Processing",
                        "summary": "Researchers have achieved new milestones...",
                        "url": "https://example.com/news/ai-breakthrough",
                        "published_at": "2024-01-15T08:00:00Z",
                        "source": "TechCrunch",
                        "relevance_score": 0.92
                    }
                ],
                "total_articles": 15,
                "query_used": "AI news",
                "processing_time": 0.8
            }
        }

class SentimentData(BaseModel):
    """Sentiment analysis data point"""
    label: str = Field(..., description="Sentiment label (Positive, Negative, Neutral)")
    value: int = Field(..., description="Number of items with this sentiment")
    percentage: float = Field(..., description="Percentage of total", ge=0.0, le=100.0)

class SentimentAgentResponse(BaseModel):
    """Response from the Sentiment Analysis Agent"""
    type: str = Field(default="sentiment_chart", description="Response type")
    data: List[SentimentData] = Field(..., description="Sentiment distribution data")
    overall_sentiment: str = Field(..., description="Overall sentiment classification")
    confidence: float = Field(..., description="Confidence in overall sentiment", ge=0.0, le=1.0)
    total_items_analyzed: int = Field(..., description="Total number of items analyzed")
    processing_time: Optional[float] = Field(None, description="Processing time in seconds")
    
    class Config:
        json_schema_extra = {
            "example": {
                "type": "sentiment_chart",
                "data": [
                    {"label": "Positive", "value": 10, "percentage": 50.0},
                    {"label": "Negative", "value": 5, "percentage": 25.0},
                    {"label": "Neutral", "value": 5, "percentage": 25.0}
                ],
                "overall_sentiment": "Positive",
                "confidence": 0.75,
                "total_items_analyzed": 20,
                "processing_time": 1.5
            }
        }

class SummarizerAgentResponse(BaseModel):
    """Response from the Summarizer Agent"""
    type: str = Field(default="summary", description="Response type")
    summary: str = Field(..., description="Condensed summary of all inputs")
    key_points: List[str] = Field(..., description="Key points extracted")
    insights: List[str] = Field(..., description="Generated insights")
    sources_used: List[str] = Field(..., description="Sources that contributed to the summary")
    processing_time: Optional[float] = Field(None, description="Processing time in seconds")
    
    class Config:
        json_schema_extra = {
            "example": {
                "type": "summary",
                "summary": "Based on recent news and research, AI sentiment is generally positive...",
                "key_points": [
                    "AI adoption is increasing across industries",
                    "Public sentiment is mostly positive",
                    "Concerns about job displacement remain"
                ],
                "insights": [
                    "The AI market is showing strong growth indicators",
                    "Ethical considerations are becoming more prominent"
                ],
                "sources_used": ["news_agent", "research_agent"],
                "processing_time": 2.1
            }
        }

class WidgetData(BaseModel):
    """Widget data for frontend display"""
    type: str = Field(..., description="Widget type (chart, text, table, etc.)")
    title: str = Field(..., description="Widget title")
    data: Dict[str, Any] = Field(..., description="Widget data")
    config: Optional[Dict[str, Any]] = Field(None, description="Widget configuration")

class FrontendAgentResponse(BaseModel):
    """Response from the Frontend Agent"""
    type: str = Field(default="dashboard_payload", description="Response type")
    widgets: List[WidgetData] = Field(..., description="List of widgets for the dashboard")
    layout: Dict[str, Any] = Field(..., description="Dashboard layout configuration")
    metadata: Dict[str, Any] = Field(..., description="Additional metadata")
    processing_time: Optional[float] = Field(None, description="Processing time in seconds")
    
    class Config:
        json_schema_extra = {
            "example": {
                "type": "dashboard_payload",
                "widgets": [
                    {
                        "type": "sentiment_chart",
                        "title": "AI News Sentiment",
                        "data": {"positive": 10, "negative": 5, "neutral": 5},
                        "config": {"chart_type": "pie", "colors": ["green", "red", "gray"]}
                    }
                ],
                "layout": {"columns": 2, "rows": 1},
                "metadata": {"query": "AI news sentiment", "timestamp": "2024-01-15T10:30:00Z"},
                "processing_time": 0.3
            }
        }
