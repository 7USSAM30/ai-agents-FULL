"""
Multi-Agent AI System - FastAPI Backend
Main application entry point with API endpoints
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
from typing import Dict, Any
import os
from dotenv import load_dotenv
from agents.news_agent import NewsAgent
from agents.research_agent import ResearchAgent
from agents.sentiment_agent import SentimentAgent

# Load environment variables
load_dotenv()

# Initialize agents
news_agent = NewsAgent()
research_agent = ResearchAgent()
sentiment_agent = SentimentAgent()

# Initialize FastAPI app
app = FastAPI(
    title="Multi-Agent AI System",
    description="A sophisticated multi-agent AI system with 7 specialized agents",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],  # Next.js dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring"""
    return {
        "status": "healthy",
        "message": "Multi-Agent AI System is running",
        "version": "1.0.0"
    }

# Main query endpoint
@app.post("/query")
async def process_query(query_data: Dict[str, Any]):
    """
    Main endpoint for processing user queries through the multi-agent system
    
    Expected input:
    {
        "query": "What is the sentiment of recent AI news?",
        "user_id": "optional_user_id"
    }
    """
    try:
        query = query_data.get("query", "")
        user_id = query_data.get("user_id", "anonymous")
        
        if not query:
            raise HTTPException(status_code=400, detail="Query is required")
        
        # Enhanced agent routing logic
        agents_used = []
        result = None
        
        # Check if query is about news or technology
        query_lower = query.lower()
        if any(keyword in query_lower for keyword in ["news", "latest", "recent", "technology", "tech", "ai", "artificial intelligence"]):
            # Use News Agent
            news_result = await news_agent.fetch_tech_news(query)
            agents_used.append("news_agent")
            result = news_result
        elif any(keyword in query_lower for keyword in ["research", "document", "knowledge", "find", "search", "what is", "how does", "explain"]):
            # Use Research Agent
            research_result = await research_agent.get_knowledge_summary(query)
            agents_used.append("research_agent")
            result = research_result
        elif any(keyword in query_lower for keyword in ["sentiment", "emotion", "feeling", "mood", "opinion", "attitude", "analyze", "analysis"]):
            # Use Sentiment Agent
            sentiment_result = await sentiment_agent.analyze_sentiment(query)
            agents_used.append("sentiment_agent")
            result = sentiment_result
        else:
            # Try Research Agent as fallback for general queries
            research_result = await research_agent.get_knowledge_summary(query)
            if research_result.get("documents") or research_result.get("summary"):
                agents_used.append("research_agent")
                result = research_result
            else:
                # Placeholder for other queries
                result = {
                    "type": "placeholder",
                    "data": "This is a placeholder response. The multi-agent system will be implemented in subsequent phases."
                }
        
        response = {
            "status": "success",
            "query": query,
            "user_id": user_id,
            "message": "Query processed successfully",
            "agents_used": agents_used,
            "result": result
        }
        
        return JSONResponse(content=response)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

# Agent status endpoint
@app.get("/agents/status")
async def get_agents_status():
    """Get status of all agents in the system"""
    # Get agent statuses
    news_status = await news_agent.get_agent_status()
    research_status = await research_agent.get_agent_status()
    sentiment_status = await sentiment_agent.get_agent_status()
    
    agents = {
        "decision_agent": {"status": "active", "description": "Routes queries to appropriate agents"},
        "research_agent": research_status,
        "news_agent": news_status,
        "sentiment_agent": sentiment_status,
        "summarizer_agent": {"status": "not_implemented", "description": "Condenses outputs into insights"},
        "frontend_agent": {"status": "not_implemented", "description": "Formats results for UI"},
        "documentation_agent": {"status": "not_implemented", "description": "Auto-updates documentation"}
    }
    
    return {
        "status": "system_initialized",
        "agents": agents,
        "message": "News Agent, Research Agent, and Sentiment Agent are now active! Phase 2 implementation in progress."
    }

# Research Agent endpoints
@app.post("/research/add-document")
async def add_document(document_data: Dict[str, Any]):
    """Add a document to the research knowledge base"""
    try:
        title = document_data.get("title", "")
        content = document_data.get("content", "")
        source = document_data.get("source", "")
        document_type = document_data.get("document_type", "text")
        metadata = document_data.get("metadata", {})
        
        if not title or not content:
            raise HTTPException(status_code=400, detail="Title and content are required")
        
        success = await research_agent.add_document(
            title=title,
            content=content,
            source=source,
            document_type=document_type,
            metadata=metadata
        )
        
        return {
            "success": success,
            "message": "Document added successfully" if success else "Failed to add document"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error adding document: {str(e)}")

@app.post("/research/process-url")
async def process_url(url_data: Dict[str, Any]):
    """Process a URL and add its content to the knowledge base"""
    try:
        url = url_data.get("url", "")
        if not url:
            raise HTTPException(status_code=400, detail="URL is required")
        
        result = await research_agent.process_web_content(url)
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing URL: {str(e)}")

@app.get("/research/search")
async def search_knowledge_base(query: str, limit: int = 5):
    """Search the knowledge base for relevant documents"""
    try:
        if not query:
            raise HTTPException(status_code=400, detail="Query is required")
        
        results = await research_agent.search_documents(query, limit=limit)
        return results
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching knowledge base: {str(e)}")

# Sentiment Analysis endpoints
@app.post("/sentiment/analyze")
async def analyze_sentiment(sentiment_data: Dict[str, Any]):
    """Analyze sentiment of provided text"""
    try:
        text = sentiment_data.get("text", "")
        method = sentiment_data.get("method", "hybrid")
        
        if not text:
            raise HTTPException(status_code=400, detail="Text is required")
        
        result = await sentiment_agent.analyze_sentiment(text, method)
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing sentiment: {str(e)}")

@app.post("/sentiment/batch")
async def analyze_batch_sentiment(batch_data: Dict[str, Any]):
    """Analyze sentiment for multiple texts"""
    try:
        texts = batch_data.get("texts", [])
        method = batch_data.get("method", "hybrid")
        
        if not texts or not isinstance(texts, list):
            raise HTTPException(status_code=400, detail="Texts array is required")
        
        result = await sentiment_agent.analyze_batch(texts, method)
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing batch sentiment: {str(e)}")

# System configuration endpoint
@app.get("/config")
async def get_system_config():
    """Get system configuration and environment info"""
    return {
        "environment": os.getenv("ENVIRONMENT", "development"),
        "openai_api_key_configured": bool(os.getenv("OPENAI_API_KEY")),
        "weaviate_url_configured": bool(os.getenv("WEAVIATE_URL")),
        "news_api_key_configured": bool(os.getenv("NEWS_API_KEY")),
        "cors_origins": ["http://localhost:3000", "http://127.0.0.1:3000"]
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
