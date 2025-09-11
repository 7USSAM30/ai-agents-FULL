"""
LangGraph Orchestrator for advanced workflow orchestration and state management.
Provides sophisticated multi-agent coordination with state persistence and conditional workflows.
"""

import asyncio
from typing import Dict, List, Any, Optional, TypedDict, Annotated
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
import json
import os

try:
    from langgraph.graph import StateGraph, END
    from langgraph.graph.message import add_messages
    from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
    LANGGRAPH_AVAILABLE = True
except ImportError:
    LANGGRAPH_AVAILABLE = False
    print("LangGraph not available. Install with: pip install langgraph")

class WorkflowState(TypedDict):
    """State for the multi-agent workflow."""
    messages: Annotated[List[BaseMessage], add_messages]
    query: str
    user_id: str
    current_step: str
    agent_results: Dict[str, Any]
    final_result: Optional[Dict[str, Any]]
    error: Optional[str]
    metadata: Dict[str, Any]

class WorkflowStep(Enum):
    INITIALIZE = "initialize"
    ANALYZE_QUERY = "analyze_query"
    EXECUTE_AGENTS = "execute_agents"
    COMBINE_RESULTS = "combine_results"
    FORMAT_RESPONSE = "format_response"
    FINALIZE = "finalize"
    ERROR_HANDLING = "error_handling"

@dataclass
class AgentNode:
    name: str
    agent: Any
    condition: Optional[str] = None
    priority: int = 1
    timeout: float = 30.0
    retry_count: int = 3

@dataclass
class WorkflowConfig:
    max_parallel_agents: int = 3
    timeout_seconds: float = 60.0
    enable_retry: bool = True
    enable_caching: bool = True
    enable_logging: bool = True
    state_persistence: bool = True

class LangGraphOrchestrator:
    def __init__(self, agents: Dict[str, Any], config: Optional[WorkflowConfig] = None):
        self.agents = agents
        self.config = config or WorkflowConfig()
        self.workflow_graph = None
        self.state_history: List[WorkflowState] = []
        
        if LANGGRAPH_AVAILABLE:
            self._build_workflow_graph()
        else:
            print("LangGraph not available. Using fallback orchestration.")

    def _build_workflow_graph(self):
        """Build the LangGraph workflow graph."""
        if not LANGGRAPH_AVAILABLE:
            return
            
        # Create the state graph
        workflow = StateGraph(WorkflowState)
        
        # Add nodes
        workflow.add_node("initialize", self._initialize_node)
        workflow.add_node("analyze_query", self._analyze_query_node)
        workflow.add_node("execute_agents", self._execute_agents_node)
        workflow.add_node("combine_results", self._combine_results_node)
        workflow.add_node("format_response", self._format_response_node)
        workflow.add_node("finalize", self._finalize_node)
        workflow.add_node("error_handling", self._error_handling_node)
        
        # Add edges
        workflow.set_entry_point("initialize")
        workflow.add_edge("initialize", "analyze_query")
        workflow.add_edge("analyze_query", "execute_agents")
        workflow.add_edge("execute_agents", "combine_results")
        workflow.add_edge("combine_results", "format_response")
        workflow.add_edge("format_response", "finalize")
        workflow.add_edge("finalize", END)
        
        # Add conditional edges for error handling
        workflow.add_conditional_edges(
            "initialize",
            self._should_continue,
            {
                "continue": "analyze_query",
                "error": "error_handling"
            }
        )
        
        workflow.add_conditional_edges(
            "analyze_query",
            self._should_continue,
            {
                "continue": "execute_agents",
                "error": "error_handling"
            }
        )
        
        workflow.add_conditional_edges(
            "execute_agents",
            self._should_continue,
            {
                "continue": "combine_results",
                "error": "error_handling"
            }
        )
        
        workflow.add_conditional_edges(
            "combine_results",
            self._should_continue,
            {
                "continue": "format_response",
                "error": "error_handling"
            }
        )
        
        workflow.add_conditional_edges(
            "format_response",
            self._should_continue,
            {
                "continue": "finalize",
                "error": "error_handling"
            }
        )
        
        workflow.add_edge("error_handling", END)
        
        # Compile the graph
        self.workflow_graph = workflow.compile()

    async def _initialize_node(self, state: WorkflowState) -> WorkflowState:
        """Initialize the workflow state."""
        try:
            state["current_step"] = WorkflowStep.INITIALIZE.value
            state["agent_results"] = {}
            state["metadata"] = {
                "start_time": datetime.now().isoformat(),
                "workflow_id": self._generate_workflow_id(),
                "version": "1.0.0"
            }
            
            # Add system message
            system_msg = SystemMessage(content="You are a multi-agent AI system orchestrator. Coordinate agents to provide comprehensive responses.")
            state["messages"].append(system_msg)
            
            return state
        except Exception as e:
            state["error"] = f"Initialization error: {str(e)}"
            return state

    async def _analyze_query_node(self, state: WorkflowState) -> WorkflowState:
        """Analyze the query using decision agent."""
        try:
            state["current_step"] = WorkflowStep.ANALYZE_QUERY.value
            
            if "decision_agent" in self.agents:
                decision_agent = self.agents["decision_agent"]
                analysis = await decision_agent.analyze_query(state["query"])
                
                state["metadata"]["query_analysis"] = {
                    "intent": analysis.intent.value,
                    "complexity": analysis.complexity.value,
                    "confidence": analysis.confidence,
                    "suggested_agents": analysis.suggested_agents,
                    "reasoning": analysis.reasoning
                }
                
                # Add analysis message
                analysis_msg = AIMessage(content=f"Query analysis: {analysis.reasoning}")
                state["messages"].append(analysis_msg)
            else:
                # Fallback analysis
                state["metadata"]["query_analysis"] = {
                    "intent": "unknown",
                    "complexity": "moderate",
                    "confidence": 0.5,
                    "suggested_agents": ["research_agent"],
                    "reasoning": "Fallback analysis - decision agent not available"
                }
            
            return state
        except Exception as e:
            state["error"] = f"Query analysis error: {str(e)}"
            return state

    async def _execute_agents_node(self, state: WorkflowState) -> WorkflowState:
        """Execute agents based on analysis."""
        try:
            state["current_step"] = WorkflowStep.EXECUTE_AGENTS.value
            
            query_analysis = state["metadata"].get("query_analysis", {})
            suggested_agents = query_analysis.get("suggested_agents", ["research_agent"])
            
            # Execute agents in parallel
            tasks = []
            agent_names = []
            
            for agent_name in suggested_agents:
                if agent_name in self.agents:
                    agent = self.agents[agent_name]
                    if agent_name == "news_agent":
                        tasks.append(agent.fetch_tech_news(state["query"]))
                    elif agent_name == "research_agent":
                        tasks.append(agent.get_knowledge_summary(state["query"]))
                    elif agent_name == "sentiment_agent":
                        tasks.append(agent.analyze_sentiment(state["query"]))
                    agent_names.append(agent_name)
            
            if tasks:
                # Execute with timeout
                results = await asyncio.wait_for(
                    asyncio.gather(*tasks, return_exceptions=True),
                    timeout=self.config.timeout_seconds
                )
                
                # Process results
                for i, result in enumerate(results):
                    if not isinstance(result, Exception):
                        state["agent_results"][agent_names[i]] = result
                    else:
                        state["agent_results"][agent_names[i]] = {
                            "error": str(result),
                            "type": "error"
                        }
                
                # Add execution message
                execution_msg = AIMessage(content=f"Executed {len(agent_names)} agents: {', '.join(agent_names)}")
                state["messages"].append(execution_msg)
            else:
                state["error"] = "No agents available for execution"
            
            return state
        except asyncio.TimeoutError:
            state["error"] = f"Agent execution timeout after {self.config.timeout_seconds} seconds"
            return state
        except Exception as e:
            state["error"] = f"Agent execution error: {str(e)}"
            return state

    async def _combine_results_node(self, state: WorkflowState) -> WorkflowState:
        """Combine results using summarizer agent."""
        try:
            state["current_step"] = WorkflowStep.COMBINE_RESULTS.value
            
            if "summarizer_agent" in self.agents and state["agent_results"]:
                summarizer_agent = self.agents["summarizer_agent"]
                
                # Prepare agent results for summarizer
                agent_results = []
                for agent_name, result in state["agent_results"].items():
                    if not result.get("error"):
                        agent_results.append({
                            "agent_type": agent_name,
                            "result": result
                        })
                
                if agent_results:
                    combined_result = await summarizer_agent.summarize_results(
                        state["query"], 
                        agent_results
                    )
                    state["final_result"] = combined_result
                    
                    # Add combination message
                    combination_msg = AIMessage(content="Results combined successfully")
                    state["messages"].append(combination_msg)
                else:
                    state["error"] = "No valid agent results to combine"
            else:
                # Fallback: use first available result
                if state["agent_results"]:
                    first_result = next(iter(state["agent_results"].values()))
                    if not first_result.get("error"):
                        state["final_result"] = first_result
                    else:
                        state["error"] = "All agent results contain errors"
                else:
                    state["error"] = "No agent results available"
            
            return state
        except Exception as e:
            state["error"] = f"Result combination error: {str(e)}"
            return state

    async def _format_response_node(self, state: WorkflowState) -> WorkflowState:
        """Format response using frontend agent."""
        try:
            state["current_step"] = WorkflowStep.FORMAT_RESPONSE.value
            
            if "frontend_agent" in self.agents and state["final_result"]:
                frontend_agent = self.agents["frontend_agent"]
                formatted_response = await frontend_agent.format_response(
                    state["final_result"], 
                    state["query"]
                )
                
                # Add formatted response to final result
                state["final_result"]["formatted"] = {
                    "component_type": formatted_response.component_type.value,
                    "formatted_data": formatted_response.formatted_data,
                    "ui_props": formatted_response.ui_props,
                    "metadata": formatted_response.metadata
                }
                
                # Add formatting message
                formatting_msg = AIMessage(content="Response formatted for frontend")
                state["messages"].append(formatting_msg)
            
            return state
        except Exception as e:
            state["error"] = f"Response formatting error: {str(e)}"
            return state

    async def _finalize_node(self, state: WorkflowState) -> WorkflowState:
        """Finalize the workflow."""
        try:
            state["current_step"] = WorkflowStep.FINALIZE.value
            
            # Add completion metadata
            state["metadata"]["end_time"] = datetime.now().isoformat()
            state["metadata"]["status"] = "completed"
            
            # Add final message
            final_msg = AIMessage(content="Workflow completed successfully")
            state["messages"].append(final_msg)
            
            return state
        except Exception as e:
            state["error"] = f"Finalization error: {str(e)}"
            return state

    async def _error_handling_node(self, state: WorkflowState) -> WorkflowState:
        """Handle errors in the workflow."""
        try:
            state["current_step"] = WorkflowStep.ERROR_HANDLING.value
            
            # Add error metadata
            state["metadata"]["end_time"] = datetime.now().isoformat()
            state["metadata"]["status"] = "error"
            state["metadata"]["error_details"] = state.get("error", "Unknown error")
            
            # Create error result
            if not state.get("final_result"):
                state["final_result"] = {
                    "type": "error",
                    "error": state.get("error", "Workflow execution failed"),
                    "timestamp": datetime.now().isoformat()
                }
            
            # Add error message
            error_msg = AIMessage(content=f"Workflow error: {state.get('error', 'Unknown error')}")
            state["messages"].append(error_msg)
            
            return state
        except Exception as e:
            # Last resort error handling
            state["final_result"] = {
                "type": "error",
                "error": f"Critical workflow error: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }
            return state

    def _should_continue(self, state: WorkflowState) -> str:
        """Determine if workflow should continue or handle error."""
        if state.get("error"):
            return "error"
        return "continue"

    def _generate_workflow_id(self) -> str:
        """Generate a unique workflow ID."""
        import uuid
        return str(uuid.uuid4())[:8]

    async def execute_workflow(self, query: str, user_id: str = "anonymous") -> Dict[str, Any]:
        """Execute the complete workflow."""
        if not LANGGRAPH_AVAILABLE:
            return await self._fallback_orchestration(query, user_id)
        
        # Initialize state
        initial_state = WorkflowState(
            messages=[],
            query=query,
            user_id=user_id,
            current_step="",
            agent_results={},
            final_result=None,
            error=None,
            metadata={}
        )
        
        try:
            # Execute workflow
            final_state = await self.workflow_graph.ainvoke(initial_state)
            
            # Store state history
            if self.config.state_persistence:
                self.state_history.append(final_state)
            
            # Return result
            return {
                "query": query,
                "user_id": user_id,
                "result": final_state.get("final_result", {}),
                "metadata": final_state.get("metadata", {}),
                "messages": [msg.content for msg in final_state.get("messages", [])],
                "workflow_id": final_state.get("metadata", {}).get("workflow_id"),
                "status": final_state.get("metadata", {}).get("status", "unknown")
            }
            
        except Exception as e:
            return {
                "query": query,
                "user_id": user_id,
                "result": {
                    "type": "error",
                    "error": f"Workflow execution failed: {str(e)}",
                    "timestamp": datetime.now().isoformat()
                },
                "metadata": {"status": "error", "error_details": str(e)},
                "messages": [],
                "workflow_id": None,
                "status": "error"
            }

    async def _fallback_orchestration(self, query: str, user_id: str) -> Dict[str, Any]:
        """Fallback orchestration when LangGraph is not available."""
        try:
            # Simple sequential execution
            results = {}
            
            # Try research agent first
            if "research_agent" in self.agents:
                try:
                    research_result = await self.agents["research_agent"].get_knowledge_summary(query)
                    results["research_agent"] = research_result
                except Exception as e:
                    results["research_agent"] = {"error": str(e)}
            
            # Try news agent
            if "news_agent" in self.agents:
                try:
                    news_result = await self.agents["news_agent"].fetch_tech_news(query)
                    results["news_agent"] = news_result
                except Exception as e:
                    results["news_agent"] = {"error": str(e)}
            
            # Combine results
            final_result = None
            if results:
                # Use first successful result
                for agent_name, result in results.items():
                    if not result.get("error"):
                        final_result = result
                        break
            
            if not final_result:
                final_result = {
                    "type": "error",
                    "error": "No agents were able to process the query",
                    "timestamp": datetime.now().isoformat()
                }
            
            return {
                "query": query,
                "user_id": user_id,
                "result": final_result,
                "metadata": {"status": "completed", "fallback": True},
                "messages": ["Fallback orchestration used"],
                "workflow_id": self._generate_workflow_id(),
                "status": "completed"
            }
            
        except Exception as e:
            return {
                "query": query,
                "user_id": user_id,
                "result": {
                    "type": "error",
                    "error": f"Fallback orchestration failed: {str(e)}",
                    "timestamp": datetime.now().isoformat()
                },
                "metadata": {"status": "error", "error_details": str(e)},
                "messages": [],
                "workflow_id": None,
                "status": "error"
            }

    async def get_workflow_status(self) -> Dict[str, Any]:
        """Get orchestrator status."""
        return {
            "status": "active",
            "langgraph_available": LANGGRAPH_AVAILABLE,
            "workflow_graph_compiled": self.workflow_graph is not None,
            "state_history_count": len(self.state_history),
            "config": {
                "max_parallel_agents": self.config.max_parallel_agents,
                "timeout_seconds": self.config.timeout_seconds,
                "enable_retry": self.config.enable_retry,
                "enable_caching": self.config.enable_caching,
                "enable_logging": self.config.enable_logging,
                "state_persistence": self.config.state_persistence
            },
            "last_updated": datetime.now().isoformat()
        }

    async def get_workflow_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get workflow execution history."""
        history = []
        for state in self.state_history[-limit:]:
            history.append({
                "workflow_id": state.get("metadata", {}).get("workflow_id"),
                "query": state.get("query"),
                "user_id": state.get("user_id"),
                "status": state.get("metadata", {}).get("status"),
                "start_time": state.get("metadata", {}).get("start_time"),
                "end_time": state.get("metadata", {}).get("end_time"),
                "current_step": state.get("current_step"),
                "error": state.get("error")
            })
        return history
