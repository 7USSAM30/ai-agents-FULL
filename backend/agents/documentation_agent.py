"""
Documentation Agent for auto-documentation and system updates.
Automatically generates and maintains documentation for the multi-agent system.
"""

import os
import json
import asyncio
from typing import Dict, List, Any, Optional, Set
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
import openai
import os

@dataclass
class DocumentationSection:
    title: str
    content: str
    section_type: str  # "api", "agent", "workflow", "deployment", "usage"
    last_updated: str
    version: str = "1.0.0"

@dataclass
class AgentDocumentation:
    name: str
    description: str
    capabilities: List[str]
    endpoints: List[Dict[str, Any]]
    status: str
    last_updated: str
    version: str = "1.0.0"

@dataclass
class SystemDocumentation:
    title: str
    description: str
    version: str
    agents: List[AgentDocumentation]
    sections: List[DocumentationSection]
    last_updated: str
    generated_by: str = "Documentation Agent"

class DocumentationAgent:
    def __init__(self):
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        if self.openai_api_key:
            openai.api_key = self.openai_api_key
        
        self.docs_dir = Path("docs")
        self.docs_dir.mkdir(exist_ok=True)
        
        # Documentation templates
        self.templates = {
            "api": self._get_api_template(),
            "agent": self._get_agent_template(),
            "workflow": self._get_workflow_template(),
            "deployment": self._get_deployment_template(),
            "usage": self._get_usage_template()
        }

    async def generate_system_documentation(self, agents: Dict[str, Any]) -> SystemDocumentation:
        """Generate comprehensive system documentation."""
        try:
            # Generate agent documentation
            agent_docs = []
            for agent_name, agent in agents.items():
                agent_doc = await self._generate_agent_documentation(agent_name, agent)
                agent_docs.append(agent_doc)
            
            # Generate sections
            sections = [
                await self._generate_api_documentation(agents),
                await self._generate_workflow_documentation(),
                await self._generate_deployment_documentation(),
                await self._generate_usage_documentation()
            ]
            
            system_doc = SystemDocumentation(
                title="Multi-Agent AI System Documentation",
                description="Comprehensive documentation for the multi-agent AI system",
                version="2.0.0",
                agents=agent_docs,
                sections=sections,
                last_updated=datetime.now().isoformat(),
                generated_by="Documentation Agent v1.0.0"
            )
            
            return system_doc
            
        except Exception as e:
            print(f"Error generating system documentation: {e}")
            return self._create_error_documentation(str(e))

    async def _generate_agent_documentation(self, agent_name: str, agent: Any) -> AgentDocumentation:
        """Generate documentation for a specific agent."""
        try:
            # Get agent status
            if hasattr(agent, 'get_agent_status'):
                status_info = await agent.get_agent_status() if asyncio.iscoroutinefunction(agent.get_agent_status) else agent.get_agent_status()
            else:
                status_info = {"status": "unknown", "description": "No status available"}
            
            # Extract capabilities
            capabilities = self._extract_agent_capabilities(agent_name, agent)
            
            # Generate endpoints
            endpoints = self._generate_agent_endpoints(agent_name, agent)
            
            return AgentDocumentation(
                name=agent_name,
                description=status_info.get("description", f"{agent_name} agent"),
                capabilities=capabilities,
                endpoints=endpoints,
                status=status_info.get("status", "unknown"),
                last_updated=datetime.now().isoformat(),
                version="1.0.0"
            )
            
        except Exception as e:
            print(f"Error generating documentation for {agent_name}: {e}")
            return AgentDocumentation(
                name=agent_name,
                description=f"Error generating documentation: {str(e)}",
                capabilities=[],
                endpoints=[],
                status="error",
                last_updated=datetime.now().isoformat()
            )

    def _extract_agent_capabilities(self, agent_name: str, agent: Any) -> List[str]:
        """Extract capabilities from agent."""
        capabilities_map = {
            "news_agent": [
                "Fetch technology news",
                "Analyze news sentiment",
                "Filter news by category",
                "Provide news summaries"
            ],
            "research_agent": [
                "Search knowledge base",
                "Process web content",
                "Add documents to knowledge base",
                "Provide research summaries",
                "Vector similarity search"
            ],
            "sentiment_agent": [
                "Analyze text sentiment",
                "Batch sentiment analysis",
                "Confidence scoring",
                "Emotion detection"
            ],
            "summarizer_agent": [
                "Combine multiple agent results",
                "Generate comprehensive summaries",
                "Extract key insights",
                "Provide recommendations"
            ],
            "decision_agent": [
                "Query intent analysis",
                "Agent coordination",
                "Parallel execution planning",
                "Fallback strategies"
            ],
            "frontend_agent": [
                "Data formatting for UI",
                "Component type mapping",
                "UI props generation",
                "Response validation"
            ],
            "langgraph_orchestrator": [
                "Workflow orchestration",
                "State management",
                "Conditional execution",
                "Error handling",
                "Execution history"
            ]
        }
        
        return capabilities_map.get(agent_name, ["Unknown capabilities"])

    def _generate_agent_endpoints(self, agent_name: str, agent: Any) -> List[Dict[str, Any]]:
        """Generate API endpoints for agent."""
        endpoints_map = {
            "news_agent": [
                {"path": "/news/status", "method": "GET", "description": "Get news agent status"},
                {"path": "/news/fetch", "method": "POST", "description": "Fetch news articles"}
            ],
            "research_agent": [
                {"path": "/research/status", "method": "GET", "description": "Get research agent status"},
                {"path": "/research/add-document", "method": "POST", "description": "Add document to knowledge base"},
                {"path": "/research/process-url", "method": "POST", "description": "Process URL content"},
                {"path": "/research/search", "method": "POST", "description": "Search documents"}
            ],
            "sentiment_agent": [
                {"path": "/sentiment/status", "method": "GET", "description": "Get sentiment agent status"},
                {"path": "/sentiment/analyze", "method": "POST", "description": "Analyze text sentiment"},
                {"path": "/sentiment/batch", "method": "POST", "description": "Batch sentiment analysis"}
            ],
            "decision_agent": [
                {"path": "/decision/analyze", "method": "POST", "description": "Analyze query intent"}
            ],
            "frontend_agent": [
                {"path": "/frontend/status", "method": "GET", "description": "Get frontend agent status"},
                {"path": "/frontend/format", "method": "POST", "description": "Format data for frontend"},
                {"path": "/frontend/component-schema/{component_type}", "method": "GET", "description": "Get component schema"}
            ],
            "langgraph_orchestrator": [
                {"path": "/orchestrator/status", "method": "GET", "description": "Get orchestrator status"},
                {"path": "/orchestrator/execute", "method": "POST", "description": "Execute orchestrated workflow"},
                {"path": "/orchestrator/history", "method": "GET", "description": "Get workflow history"}
            ]
        }
        
        return endpoints_map.get(agent_name, [])

    async def _generate_api_documentation(self, agents: Dict[str, Any]) -> DocumentationSection:
        """Generate API documentation section."""
        content = self.templates["api"]
        
        # Add agent-specific endpoints
        for agent_name, agent in agents.items():
            endpoints = self._generate_agent_endpoints(agent_name, agent)
            if endpoints:
                content += f"\n## {agent_name.replace('_', ' ').title()} Endpoints\n\n"
                for endpoint in endpoints:
                    content += f"### {endpoint['method']} {endpoint['path']}\n"
                    content += f"{endpoint['description']}\n\n"
        
        return DocumentationSection(
            title="API Documentation",
            content=content,
            section_type="api",
            last_updated=datetime.now().isoformat()
        )

    async def _generate_workflow_documentation(self) -> DocumentationSection:
        """Generate workflow documentation section."""
        content = self.templates["workflow"]
        
        # Add workflow steps
        workflow_steps = [
            "1. **Initialize**: Set up workflow state and metadata",
            "2. **Analyze Query**: Use decision agent to analyze query intent",
            "3. **Execute Agents**: Run appropriate agents in parallel or sequence",
            "4. **Combine Results**: Use summarizer agent to combine results",
            "5. **Format Response**: Use frontend agent to format for UI",
            "6. **Finalize**: Complete workflow and return results"
        ]
        
        content += "\n## Workflow Steps\n\n"
        for step in workflow_steps:
            content += f"{step}\n"
        
        return DocumentationSection(
            title="Workflow Documentation",
            content=content,
            section_type="workflow",
            last_updated=datetime.now().isoformat()
        )

    async def _generate_deployment_documentation(self) -> DocumentationSection:
        """Generate deployment documentation section."""
        content = self.templates["deployment"]
        
        # Add environment variables
        env_vars = [
            "OPENAI_API_KEY - OpenAI API key for AI models",
            "NEWS_API_KEY - NewsAPI key for news fetching",
            "WEAVIATE_URL - Weaviate vector database URL",
            "WEAVIATE_API_KEY - Weaviate API key"
        ]
        
        content += "\n## Environment Variables\n\n"
        for env_var in env_vars:
            content += f"- {env_var}\n"
        
        return DocumentationSection(
            title="Deployment Documentation",
            content=content,
            section_type="deployment",
            last_updated=datetime.now().isoformat()
        )

    async def _generate_usage_documentation(self) -> DocumentationSection:
        """Generate usage documentation section."""
        content = self.templates["usage"]
        
        # Add example queries
        examples = [
            "What are the latest AI news?",
            "Analyze the sentiment of this text: 'I love this new AI technology!'",
            "Research information about machine learning",
            "Get a comprehensive analysis of recent tech developments"
        ]
        
        content += "\n## Example Queries\n\n"
        for i, example in enumerate(examples, 1):
            content += f"{i}. {example}\n"
        
        return DocumentationSection(
            title="Usage Documentation",
            content=content,
            section_type="usage",
            last_updated=datetime.now().isoformat()
        )

    def _get_api_template(self) -> str:
        """Get API documentation template."""
        return """# API Documentation

## Base URL
```
http://localhost:8000
```

## Authentication
Currently no authentication is required.

## Common Endpoints

### Health Check
- **GET** `/health` - Check system health

### System Status
- **GET** `/` - Get system information
- **GET** `/agents/status` - Get all agents status

### Query Processing
- **POST** `/query` - Process user queries
- **POST** `/orchestrator/execute` - Execute orchestrated workflow

## Response Format
All responses follow a consistent JSON format:

```json
{
  "query": "user query",
  "result": {
    "type": "result_type",
    "data": {...}
  },
  "agents_used": ["agent1", "agent2"],
  "timestamp": "2024-01-01T00:00:00Z"
}
```"""

    def _get_agent_template(self) -> str:
        """Get agent documentation template."""
        return """# Agent Documentation

## Agent Architecture
The system consists of multiple specialized agents, each handling specific tasks:

- **News Agent**: Fetches and analyzes technology news
- **Research Agent**: Searches knowledge base and processes documents
- **Sentiment Agent**: Analyzes text sentiment and emotions
- **Summarizer Agent**: Combines results from multiple agents
- **Decision Agent**: Routes queries to appropriate agents
- **Frontend Agent**: Formats data for UI display
- **LangGraph Orchestrator**: Manages complex workflows

## Agent Communication
Agents communicate through standardized interfaces and can work in parallel or sequence based on query requirements."""

    def _get_workflow_template(self) -> str:
        """Get workflow documentation template."""
        return """# Workflow Documentation

## Multi-Agent Workflow
The system uses a sophisticated workflow to process user queries:

### Standard Workflow
1. Query analysis and intent detection
2. Agent selection and coordination
3. Parallel or sequential execution
4. Result combination and summarization
5. Frontend formatting and response

### LangGraph Orchestration
For complex queries, the system can use LangGraph for advanced workflow orchestration with:
- State management
- Conditional execution
- Error handling and retries
- Execution history tracking"""

    def _get_deployment_template(self) -> str:
        """Get deployment documentation template."""
        return """# Deployment Documentation

## Prerequisites
- Python 3.8+
- Node.js 16+
- Docker (optional)

## Local Development

### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate
pip install -r requirements.txt
python main.py
```

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

## Production Deployment
Use Docker Compose for production deployment:

```bash
docker-compose up -d
```"""

    def _get_usage_template(self) -> str:
        """Get usage documentation template."""
        return """# Usage Documentation

## Getting Started
1. Start the backend server: `python main.py`
2. Start the frontend: `npm run dev`
3. Open http://localhost:3000 in your browser

## Query Types
The system can handle various types of queries:

### News Queries
- "What are the latest AI news?"
- "Show me recent technology updates"

### Research Queries
- "What is machine learning?"
- "Research information about neural networks"

### Sentiment Analysis
- "Analyze the sentiment of this text"
- "How do people feel about AI?"

### Complex Queries
- "Give me a comprehensive analysis of recent AI developments"
- "What's the sentiment around the latest tech news?"
"""

    async def save_documentation(self, system_doc: SystemDocumentation, format: str = "markdown") -> Dict[str, str]:
        """Save documentation to files."""
        saved_files = {}
        
        try:
            if format == "markdown":
                # Save main documentation
                main_file = self.docs_dir / "README.md"
                main_content = self._generate_markdown_documentation(system_doc)
                main_file.write_text(main_content)
                saved_files["main"] = str(main_file)
                
                # Save individual agent documentation
                for agent_doc in system_doc.agents:
                    agent_file = self.docs_dir / f"{agent_doc.name}.md"
                    agent_content = self._generate_agent_markdown(agent_doc)
                    agent_file.write_text(agent_content)
                    saved_files[agent_doc.name] = str(agent_file)
                
                # Save sections
                for section in system_doc.sections:
                    section_file = self.docs_dir / f"{section.section_type}.md"
                    section_file.write_text(section.content)
                    saved_files[section.section_type] = str(section_file)
            
            elif format == "json":
                # Save as JSON
                json_file = self.docs_dir / "documentation.json"
                json_content = self._system_doc_to_json(system_doc)
                json_file.write_text(json.dumps(json_content, indent=2))
                saved_files["json"] = str(json_file)
            
            return saved_files
            
        except Exception as e:
            print(f"Error saving documentation: {e}")
            return {"error": str(e)}

    def _generate_markdown_documentation(self, system_doc: SystemDocumentation) -> str:
        """Generate markdown documentation."""
        content = f"""# {system_doc.title}

{system_doc.description}

**Version**: {system_doc.version}  
**Last Updated**: {system_doc.last_updated}  
**Generated By**: {system_doc.generated_by}

## Table of Contents
- [Agents](#agents)
- [API Documentation](#api-documentation)
- [Workflow Documentation](#workflow-documentation)
- [Deployment Documentation](#deployment-documentation)
- [Usage Documentation](#usage-documentation)

## Agents

"""
        
        for agent_doc in system_doc.agents:
            content += f"""### {agent_doc.name.replace('_', ' ').title()}

**Status**: {agent_doc.status}  
**Description**: {agent_doc.description}

**Capabilities**:
"""
            for capability in agent_doc.capabilities:
                content += f"- {capability}\n"
            
            if agent_doc.endpoints:
                content += "\n**Endpoints**:\n"
                for endpoint in agent_doc.endpoints:
                    content += f"- `{endpoint['method']} {endpoint['path']}` - {endpoint['description']}\n"
            
            content += "\n"
        
        # Add sections
        for section in system_doc.sections:
            content += f"\n## {section.title}\n\n{section.content}\n"
        
        return content

    def _generate_agent_markdown(self, agent_doc: AgentDocumentation) -> str:
        """Generate markdown for individual agent."""
        content = f"""# {agent_doc.name.replace('_', ' ').title()}

**Status**: {agent_doc.status}  
**Version**: {agent_doc.version}  
**Last Updated**: {agent_doc.last_updated}

## Description
{agent_doc.description}

## Capabilities
"""
        for capability in agent_doc.capabilities:
            content += f"- {capability}\n"
        
        if agent_doc.endpoints:
            content += "\n## API Endpoints\n\n"
            for endpoint in agent_doc.endpoints:
                content += f"### {endpoint['method']} {endpoint['path']}\n"
                content += f"{endpoint['description']}\n\n"
        
        return content

    def _system_doc_to_json(self, system_doc: SystemDocumentation) -> Dict[str, Any]:
        """Convert system documentation to JSON."""
        return {
            "title": system_doc.title,
            "description": system_doc.description,
            "version": system_doc.version,
            "last_updated": system_doc.last_updated,
            "generated_by": system_doc.generated_by,
            "agents": [
                {
                    "name": agent.name,
                    "description": agent.description,
                    "capabilities": agent.capabilities,
                    "endpoints": agent.endpoints,
                    "status": agent.status,
                    "last_updated": agent.last_updated,
                    "version": agent.version
                }
                for agent in system_doc.agents
            ],
            "sections": [
                {
                    "title": section.title,
                    "content": section.content,
                    "section_type": section.section_type,
                    "last_updated": section.last_updated,
                    "version": section.version
                }
                for section in system_doc.sections
            ]
        }

    def _create_error_documentation(self, error_message: str) -> SystemDocumentation:
        """Create error documentation."""
        return SystemDocumentation(
            title="Multi-Agent AI System Documentation",
            description=f"Error generating documentation: {error_message}",
            version="2.0.0",
            agents=[],
            sections=[],
            last_updated=datetime.now().isoformat(),
            generated_by="Documentation Agent v1.0.0 (Error)"
        )

    async def get_agent_status(self) -> Dict[str, Any]:
        """Get documentation agent status."""
        return {
            "status": "active",
            "templates_available": len(self.templates),
            "docs_directory": str(self.docs_dir),
            "openai_enabled": bool(self.openai_api_key),
            "last_updated": datetime.now().isoformat()
        }

    async def update_documentation(self, agents: Dict[str, Any], format: str = "markdown") -> Dict[str, Any]:
        """Update system documentation."""
        try:
            # Generate new documentation
            system_doc = await self.generate_system_documentation(agents)
            
            # Save documentation
            saved_files = await self.save_documentation(system_doc, format)
            
            return {
                "status": "success",
                "message": "Documentation updated successfully",
                "files_saved": saved_files,
                "documentation": {
                    "title": system_doc.title,
                    "version": system_doc.version,
                    "agents_count": len(system_doc.agents),
                    "sections_count": len(system_doc.sections),
                    "last_updated": system_doc.last_updated
                }
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to update documentation: {str(e)}",
                "files_saved": {},
                "documentation": None
            }
