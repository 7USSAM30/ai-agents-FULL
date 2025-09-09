"""
Query schemas for the Multi-Agent AI System
Defines request and response models for API endpoints
"""

from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
from enum import Enum

class QueryType(str, Enum):
    """Types of queries the system can handle"""
    RESEARCH = "research"
    NEWS = "news"
    SENTIMENT = "sentiment"
    COMBINED = "combined"
    GENERAL = "general"

class QueryRequest(BaseModel):
    """Request model for user queries"""
    query: str = Field(..., description="The user's query", min_length=1, max_length=1000)
    user_id: Optional[str] = Field(None, description="Optional user identifier")
    query_type: Optional[QueryType] = Field(None, description="Optional query type hint")
    context: Optional[Dict[str, Any]] = Field(None, description="Additional context for the query")
    
    class Config:
        json_schema_extra = {
            "example": {
                "query": "What is the sentiment of recent AI news?",
                "user_id": "user123",
                "query_type": "combined",
                "context": {"preferred_sources": ["techcrunch", "wired"]}
            }
        }

class AgentStatus(BaseModel):
    """Status information for an agent"""
    name: str = Field(..., description="Agent name")
    status: str = Field(..., description="Agent status (active, inactive, error)")
    description: str = Field(..., description="Agent description")
    last_used: Optional[str] = Field(None, description="Last time agent was used")
    performance_metrics: Optional[Dict[str, Any]] = Field(None, description="Performance metrics")

class QueryResponse(BaseModel):
    """Response model for processed queries"""
    status: str = Field(..., description="Response status")
    query: str = Field(..., description="Original query")
    user_id: Optional[str] = Field(None, description="User identifier")
    agents_used: List[str] = Field(..., description="List of agents that processed the query")
    result: Dict[str, Any] = Field(..., description="The processed result")
    processing_time: Optional[float] = Field(None, description="Processing time in seconds")
    timestamp: Optional[str] = Field(None, description="Response timestamp")
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "success",
                "query": "What is the sentiment of recent AI news?",
                "user_id": "user123",
                "agents_used": ["decision_agent", "news_agent", "sentiment_agent"],
                "result": {
                    "type": "sentiment_analysis",
                    "data": {
                        "positive": 15,
                        "negative": 3,
                        "neutral": 7
                    }
                },
                "processing_time": 2.5,
                "timestamp": "2024-01-15T10:30:00Z"
            }
        }
