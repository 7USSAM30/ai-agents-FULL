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
import asyncio
from datetime import datetime
from dotenv import load_dotenv
from contextlib import asynccontextmanager
from agents.news_agent import NewsAgent
from agents.research_agent import ResearchAgent
from agents.sentiment_agent import SentimentAgent
from agents.summarizer_agent import SummarizerAgent
from agents.decision_agent import DecisionAgent
from agents.frontend_agent import FrontendAgent
from agents.langgraph_orchestrator import LangGraphOrchestrator, WorkflowConfig
from agents.documentation_agent import DocumentationAgent
from agents.caching_agent import CachingAgent, CacheConfig
from agents.learning_agent import LearningAgent

# Load environment variables
load_dotenv()

# Helper function to validate agent results
def _validate_agent_result(agent_name: str, result: Dict[str, Any]) -> bool:
    """Validate agent result based on agent type."""
    if not result or result.get("error"):
        return False
    
    if agent_name == "news_agent":
        return result.get("articles") and len(result.get("articles", [])) > 0
    elif agent_name == "research_agent":
        summary = result.get("summary", "")
        return summary and "No relevant documents found" not in summary and len(summary) > 50
    elif agent_name == "sentiment_agent":
        return result.get("sentiment") is not None
    else:
        return True

# Initialize agents
news_agent = NewsAgent()
research_agent = ResearchAgent()
sentiment_agent = SentimentAgent()
summarizer_agent = SummarizerAgent()
decision_agent = DecisionAgent()
frontend_agent = FrontendAgent()
documentation_agent = DocumentationAgent()
learning_agent = LearningAgent()

# Initialize Caching Agent
cache_config = CacheConfig(
    max_size_mb=100,
    default_ttl_seconds=3600,  # 1 hour
    cleanup_interval_seconds=300,  # 5 minutes
    enable_compression=True,
    enable_persistence=True,
    cache_directory="cache"
)
caching_agent = CachingAgent(cache_config)

# Initialize LangGraph Orchestrator
workflow_config = WorkflowConfig(
    max_parallel_agents=3,
    timeout_seconds=60.0,
    enable_retry=True,
    enable_caching=True,
    enable_logging=True,
    state_persistence=True
)

orchestrator = LangGraphOrchestrator({
    "news_agent": news_agent,
    "research_agent": research_agent,
    "sentiment_agent": sentiment_agent,
    "summarizer_agent": summarizer_agent,
    "decision_agent": decision_agent,
    "frontend_agent": frontend_agent,
    "documentation_agent": documentation_agent
}, workflow_config)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan event handler for startup and shutdown."""
    # Startup
    await caching_agent.start_cleanup_task()
    yield
    # Shutdown
    if caching_agent.cleanup_task:
        caching_agent.cleanup_task.cancel()
        try:
            await caching_agent.cleanup_task
        except asyncio.CancelledError:
            pass

# Initialize FastAPI app
app = FastAPI(
    title="Multi-Agent AI System",
    description="A sophisticated multi-agent AI system with 8 specialized agents",
    version="2.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Root endpoint with system information"""
    return {
        "message": "Multi-Agent AI System API",
        "version": "2.0.0",
        "status": "operational",
        "agents": ["news_agent", "research_agent", "sentiment_agent", "summarizer_agent", "decision_agent", "frontend_agent", "documentation_agent", "caching_agent"],
        "endpoints": {
            "query": "/query",
            "health": "/health",
            "agents_status": "/agents/status",
            "decision_analyze": "/decision/analyze",
            "orchestrator_execute": "/orchestrator/execute",
            "orchestrator_status": "/orchestrator/status",
            "frontend_format": "/frontend/format",
            "documentation_generate": "/documentation/generate",
            "documentation_agents": "/documentation/agents",
            "cache_status": "/cache/status",
            "cache_stats": "/cache/stats",
            "cache_clear": "/cache/clear"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "system": "multi_agent_ai"
    }

@app.post("/query")
async def process_query(query_data: Dict[str, Any]):
    """
    Process a query using the multi-agent system with enhanced decision agent.
    
    Expected input:
    {
        "query": "What is the sentiment of recent AI news?",
        "user_id": "optional_user_id",
        "use_orchestrator": false  # Optional: use LangGraph orchestrator
    }
    """
    try:
        query = query_data.get("query", "")
        user_id = query_data.get("user_id", "anonymous")
        use_orchestrator = query_data.get("use_orchestrator", False)
        
        if not query:
            raise HTTPException(status_code=400, detail="Query is required")
        
        # Check cache first (but skip for sentiment queries to ensure fresh analysis)
        if not any(keyword in query.lower() for keyword in ["sentiment", "emotion", "feeling", "mood", "opinion", "attitude", "analyze"]):
            cached_result = await caching_agent.get_cached_query_result(query)
            if cached_result:
                return {
                    "query": query,
                    "agents_used": ["caching_agent"],
                    "processing_time": 0.0,
                    "timestamp": datetime.now().isoformat(),
                    "result": cached_result,
                    "cached": True
                }
        
        # Use LangGraph Orchestrator if requested
        if use_orchestrator:
            result = await orchestrator.execute_workflow(query, user_id)
            # Cache the result
            await caching_agent.cache_query_result(query, result.get("result", {}))
            return result
        
        # Enhanced decision agent processing
        agents_used = []
        agent_results = []

        # Use decision agent to analyze query and coordinate agents
        coordination_plan = await decision_agent.coordinate_agents(query, {
            "news_agent": news_agent,
            "research_agent": research_agent,
            "sentiment_agent": sentiment_agent
        })
        
        query_analysis = coordination_plan["query_analysis"]
        execution_plan = coordination_plan["execution_plan"]
        
        # For sentiment queries, prioritize sentiment agent only
        if query_analysis.intent.value == "sentiment":
            execution_plan = [{"agent": "sentiment_agent", "priority": 1}]
            print(f"🎯 Sentiment query detected - running sentiment agent only")
    
        # Execute agents based on decision agent coordination plan
        if coordination_plan["parallel_execution"]:
            # Execute agents in parallel for better performance
            tasks = []
            for plan_item in execution_plan:
                agent_name = plan_item["agent"]
                if agent_name == "news_agent":
                    tasks.append(news_agent.fetch_tech_news(query))
                elif agent_name == "research_agent":
                    tasks.append(research_agent.get_knowledge_summary(query))
                elif agent_name == "sentiment_agent":
                    tasks.append(sentiment_agent.analyze_sentiment(query))
            
            # Execute all tasks in parallel
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Process results
            for i, result in enumerate(results):
                if not isinstance(result, Exception):
                    plan_item = execution_plan[i]
                    agent_name = plan_item["agent"]
                    
                    # Validate result based on agent type
                    if _validate_agent_result(agent_name, result):
                        agents_used.append(agent_name)
                        agent_results.append({
                            "agent_type": agent_name,
                            "result": result
                        })
                    else:
                        print(f"{agent_name}: No valid results for query: {query}")
                else:
                    print(f"Agent execution error: {result}")
        else:
            # Execute agents sequentially
            for plan_item in execution_plan:
                agent_name = plan_item["agent"]
                try:
                    if agent_name == "news_agent":
                        result = await news_agent.fetch_tech_news(query)
                    elif agent_name == "research_agent":
                        result = await research_agent.get_knowledge_summary(query)
                    elif agent_name == "sentiment_agent":
                        result = await sentiment_agent.analyze_sentiment(query)
                    else:
                        continue
                    
                    # Validate result
                    if _validate_agent_result(agent_name, result):
                        agents_used.append(agent_name)
                        agent_results.append({
                            "agent_type": agent_name,
                            "result": result
                        })
                    else:
                        print(f"{agent_name}: No valid results for query: {query}")
                except Exception as e:
                    print(f"{agent_name} error: {e}")
        
        # Use Summarizer Agent to combine results (but prioritize sentiment results)
        if agent_results:
            # Check if we have a sentiment result and prioritize it
            sentiment_result = None
            for agent_result in agent_results:
                if agent_result["agent_type"] == "sentiment_agent" and agent_result["result"].get("type") == "sentiment_analysis":
                    sentiment_result = agent_result["result"]
                    break
            
            if sentiment_result:
                # Use sentiment result directly for sentiment queries
                result = sentiment_result
                print(f"🎯 Using sentiment result: {sentiment_result.get('sentiment')} (confidence: {sentiment_result.get('confidence')})")
            else:
                # Use summarizer for other types of queries
                try:
                    result = await summarizer_agent.summarize_results(query, agent_results)
                    agents_used.append("summarizer_agent")
                except Exception as e:
                    print(f"Summarizer Agent error: {e}")
                    # Fallback to first available result
                    result = agent_results[0]["result"] if agent_results else {
                        "type": "error",
                        "error": "No agents were able to process the query"
                    }
        else:
            result = {
                "type": "error",
                "error": "No agents were able to process the query"
            }
        
        # Learn from this query (run in background)
        try:
            learning_result = await learning_agent.learn_from_query(query, max_articles=3)
            if learning_result.get("learning_successful"):
                print(f"🧠 Learned from query: {learning_result['articles_stored']} articles stored")
                agents_used.append("learning_agent")
        except Exception as e:
            print(f"Learning Agent error: {e}")
        
        # Use Frontend Agent to format response for UI
        try:
            formatted_response = await frontend_agent.format_response(result, query)
            agents_used.append("frontend_agent")
            
            # Add formatted response to result
            result["formatted"] = {
                "component_type": formatted_response.component_type.value,
                "formatted_data": formatted_response.formatted_data,
                "ui_props": formatted_response.ui_props,
                "metadata": formatted_response.metadata
            }
        except Exception as e:
            print(f"Frontend Agent error: {e}")
            # Continue without formatting
        
        # If no agents returned results, try fallback
        if not agent_results:
            print("No agents returned results, trying fallback...")
            try:
                # Try research agent as fallback
                research_result = await research_agent.get_knowledge_summary(query)
                if research_result:
                    result = research_result
                    agents_used.append("research_agent")
                else:
                    result = {
                        "type": "placeholder",
                        "data": f"I understand you're asking about '{query}'. While I don't have specific information about this topic in my knowledge base, I can help you with technology news, research documents, or sentiment analysis. Please try rephrasing your question or ask about a specific topic."
                    }
            except Exception as e:
                print(f"Fallback error: {e}")
                result = {
                    "type": "error",
                    "error": "Unable to process your query at this time. Please try again or rephrase your question."
                }
        
        # Cache the final result
        await caching_agent.cache_query_result(query, result)
        
        # Return response
        return {
            "query": query,
            "agents_used": agents_used,
            "processing_time": 0.0,  # TODO: Add timing
            "timestamp": datetime.now().isoformat(),
            "result": result,
            "cached": False
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.post("/decision/analyze")
async def analyze_query(query_data: Dict[str, Any]):
    """Analyze query using decision agent"""
    query = query_data.get("query", "")
    if not query:
        raise HTTPException(status_code=400, detail="Query is required")
    
    analysis = await decision_agent.analyze_query(query)
    return {
        "query": query,
        "analysis": {
            "intent": analysis.intent.value,
            "complexity": analysis.complexity.value,
            "confidence": analysis.confidence,
            "keywords": analysis.keywords,
            "entities": analysis.entities,
            "suggested_agents": analysis.suggested_agents,
            "reasoning": analysis.reasoning
        }
    }

@app.get("/agents/status")
async def get_agents_status():
    """Get status of all agents in the system"""
    # Get agent statuses
    news_status = await news_agent.get_agent_status()
    research_status = await research_agent.get_agent_status()
    sentiment_status = await sentiment_agent.get_agent_status()
    summarizer_status = await summarizer_agent.get_agent_status()
    
    agents = {
        "decision_agent": decision_agent.get_agent_status(),
        "research_agent": research_status,
        "news_agent": news_status,
        "sentiment_agent": sentiment_status,
        "summarizer_agent": summarizer_status,
        "frontend_agent": await frontend_agent.get_agent_status(),
        "documentation_agent": await documentation_agent.get_agent_status(),
        "caching_agent": await caching_agent.get_agent_status(),
        "learning_agent": await learning_agent.get_agent_status()
    }
    
    return {
        "status": "system_initialized",
        "agents": agents,
        "message": "Enhanced Decision Agent, News Agent, Research Agent, Sentiment Agent, and Summarizer Agent are now active! Multi-agent orchestration with intelligent routing is working!",
        "timestamp": datetime.now().isoformat()
    }

# News Agent endpoints
@app.get("/news/status")
async def get_news_status():
    """Get News Agent status"""
    return await news_agent.get_agent_status()

@app.post("/news/fetch")
async def fetch_news(query_data: Dict[str, Any]):
    """Fetch news using News Agent"""
    query = query_data.get("query", "")
    if not query:
        raise HTTPException(status_code=400, detail="Query is required")
    
    result = await news_agent.fetch_tech_news(query)
    return result

# Research Agent endpoints
@app.get("/research/status")
async def get_research_status():
    """Get Research Agent status"""
    return await research_agent.get_agent_status()

@app.post("/research/add-document")
async def add_document(document_data: Dict[str, Any]):
    """Add document to Research Agent knowledge base"""
    title = document_data.get("title", "")
    content = document_data.get("content", "")
    source = document_data.get("source", "manual")
    
    if not title or not content:
        raise HTTPException(status_code=400, detail="Title and content are required")
    
    result = await research_agent.add_document(title, content, source)
    return result

@app.post("/research/process-url")
async def process_url(url_data: Dict[str, Any]):
    """Process URL content and add to knowledge base"""
    url = url_data.get("url", "")
    if not url:
        raise HTTPException(status_code=400, detail="URL is required")
    
    result = await research_agent.process_web_content(url)
    return result

@app.post("/research/search")
async def search_documents(search_data: Dict[str, Any]):
    """Search documents in knowledge base"""
    query = search_data.get("query", "")
    limit = search_data.get("limit", 5)
    
    if not query:
        raise HTTPException(status_code=400, detail="Query is required")
    
    result = await research_agent.search_documents(query, limit)
    return result

# Sentiment Agent endpoints
@app.get("/sentiment/status")
async def get_sentiment_status():
    """Get Sentiment Agent status"""
    return await sentiment_agent.get_agent_status()

@app.post("/sentiment/analyze")
async def analyze_sentiment(sentiment_data: Dict[str, Any]):
    """Analyze sentiment using Sentiment Agent"""
    text = sentiment_data.get("text", "")
    if not text:
        raise HTTPException(status_code=400, detail="Text is required")
    
    result = await sentiment_agent.analyze_sentiment(text)
    return result

@app.post("/sentiment/batch")
async def analyze_batch_sentiment(batch_data: Dict[str, Any]):
    """Analyze sentiment for multiple texts"""
    texts = batch_data.get("texts", [])
    if not texts:
        raise HTTPException(status_code=400, detail="Texts array is required")
    
    result = await sentiment_agent.analyze_batch(texts)
    return result

# Frontend Agent endpoints
@app.get("/frontend/status")
async def get_frontend_status():
    """Get Frontend Agent status"""
    return await frontend_agent.get_agent_status()

@app.post("/frontend/format")
async def format_for_frontend(format_data: Dict[str, Any]):
    """Format data for frontend display"""
    result = format_data.get("result", {})
    query = format_data.get("query", "")
    
    if not result:
        raise HTTPException(status_code=400, detail="Result data is required")
    
    formatted_response = await frontend_agent.format_response(result, query)
    return {
        "component_type": formatted_response.component_type.value,
        "formatted_data": formatted_response.formatted_data,
        "ui_props": formatted_response.ui_props,
        "metadata": formatted_response.metadata,
        "timestamp": formatted_response.timestamp
    }

@app.get("/frontend/component-schema/{component_type}")
async def get_component_schema(component_type: str):
    """Get schema for a specific component type"""
    from agents.frontend_agent import ComponentType
    
    try:
        comp_type = ComponentType(component_type)
        schema = await frontend_agent.get_component_schema(comp_type)
        return schema
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Invalid component type: {component_type}")

# LangGraph Orchestrator endpoints
@app.get("/orchestrator/status")
async def get_orchestrator_status():
    """Get LangGraph Orchestrator status"""
    return await orchestrator.get_workflow_status()

@app.post("/orchestrator/execute")
async def execute_orchestrated_workflow(workflow_data: Dict[str, Any]):
    """Execute a workflow using LangGraph Orchestrator"""
    query = workflow_data.get("query", "")
    user_id = workflow_data.get("user_id", "anonymous")
    
    if not query:
        raise HTTPException(status_code=400, detail="Query is required")
    
    result = await orchestrator.execute_workflow(query, user_id)
    return result

@app.get("/orchestrator/history")
async def get_workflow_history(limit: int = 10):
    """Get workflow execution history"""
    if limit > 100:
        limit = 100  # Cap at 100 for performance
    
    history = await orchestrator.get_workflow_history(limit)
    return {
        "history": history,
        "count": len(history),
        "limit": limit
    }

# Documentation Agent endpoints
@app.get("/documentation/status")
async def get_documentation_status():
    """Get Documentation Agent status"""
    return await documentation_agent.get_agent_status()

@app.post("/documentation/generate")
async def generate_documentation(format: str = "markdown"):
    """Generate system documentation"""
    agents = {
        "news_agent": news_agent,
        "research_agent": research_agent,
        "sentiment_agent": sentiment_agent,
        "summarizer_agent": summarizer_agent,
        "decision_agent": decision_agent,
        "frontend_agent": frontend_agent,
        "documentation_agent": documentation_agent
    }
    
    result = await documentation_agent.update_documentation(agents, format)
    return result

@app.get("/documentation/agents")
async def get_agent_documentation():
    """Get documentation for all agents"""
    agents = {
        "news_agent": news_agent,
        "research_agent": research_agent,
        "sentiment_agent": sentiment_agent,
        "summarizer_agent": summarizer_agent,
        "decision_agent": decision_agent,
        "frontend_agent": frontend_agent,
        "documentation_agent": documentation_agent
    }
    
    system_doc = await documentation_agent.generate_system_documentation(agents)
    return {
        "agents": [
            {
                "name": agent.name,
                "description": agent.description,
                "capabilities": agent.capabilities,
                "endpoints": agent.endpoints,
                "status": agent.status
            }
            for agent in system_doc.agents
        ],
        "last_updated": system_doc.last_updated
    }

# Caching Agent endpoints
@app.get("/cache/status")
async def get_cache_status():
    """Get Caching Agent status and statistics"""
    return await caching_agent.get_agent_status()

@app.get("/cache/stats")
async def get_cache_stats():
    """Get detailed cache statistics"""
    return await caching_agent.get_cache_stats()

@app.post("/cache/clear")
async def clear_cache(cache_type: str = None):
    """Clear cache entries"""
    from agents.caching_agent import CacheType
    
    if cache_type:
        try:
            cache_type_enum = CacheType(cache_type)
            cleared_count = await caching_agent.clear(cache_type_enum)
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid cache type: {cache_type}")
    else:
        cleared_count = await caching_agent.clear()
    
    return {
        "message": f"Cleared {cleared_count} cache entries",
        "cleared_count": cleared_count,
        "cache_type": cache_type
    }

@app.post("/cache/invalidate")
async def invalidate_cache(invalidation_data: Dict[str, Any]):
    """Invalidate cache entries by pattern or type"""
    pattern = invalidation_data.get("pattern")
    cache_type = invalidation_data.get("cache_type")
    
    from agents.caching_agent import CacheType
    
    if cache_type:
        try:
            cache_type_enum = CacheType(cache_type)
            invalidated_count = await caching_agent.invalidate_cache(cache_type=cache_type_enum)
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid cache type: {cache_type}")
    else:
        invalidated_count = await caching_agent.invalidate_cache(pattern=pattern)
    
    return {
        "message": f"Invalidated {invalidated_count} cache entries",
        "invalidated_count": invalidated_count,
        "pattern": pattern,
        "cache_type": cache_type
    }

@app.post("/cache/warm")
async def warm_cache(warm_data: Dict[str, Any]):
    """Warm up cache with common queries"""
    queries = warm_data.get("queries", [])
    
    if not queries:
        # Default warm-up queries
        queries = [
            "What are the latest AI news?",
            "Analyze the sentiment of this text",
            "Research information about machine learning",
            "What is artificial intelligence?"
        ]
    
    agents = {
        "news_agent": news_agent,
        "research_agent": research_agent,
        "sentiment_agent": sentiment_agent,
        "summarizer_agent": summarizer_agent,
        "decision_agent": decision_agent,
        "frontend_agent": frontend_agent,
        "documentation_agent": documentation_agent
    }
    
    result = await caching_agent.warm_cache(queries, agents)
    return result

# Learning Agent endpoints
@app.get("/learning/stats")
async def get_learning_stats():
    """Get learning statistics"""
    return await learning_agent.get_learning_stats()

@app.post("/learning/learn")
async def manual_learn(learn_data: Dict[str, Any]):
    """Manually trigger learning from a query"""
    query = learn_data.get("query", "")
    max_articles = learn_data.get("max_articles", 5)
    
    if not query:
        raise HTTPException(status_code=400, detail="Query is required")
    
    result = await learning_agent.learn_from_query(query, max_articles)
    return result

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)