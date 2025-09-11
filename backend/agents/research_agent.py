"""
Research Agent - RAG (Retrieval-Augmented Generation) with Weaviate integration
Handles document processing, vector search, and knowledge retrieval
"""

import weaviate
import os
import asyncio
from typing import List, Dict, Any, Optional
from datetime import datetime
import json
from dotenv import load_dotenv
import httpx
import re

# Load environment variables
load_dotenv()

class ResearchAgent:
    """
    Research Agent that provides RAG functionality using Weaviate vector database
    """
    
    def __init__(self):
        self.weaviate_url = os.getenv("WEAVIATE_URL")
        self.weaviate_api_key = os.getenv("WEAVIATE_API_KEY")
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.client = None
        self.class_name = "ResearchDocument"
        self._initialize_weaviate()
        
    def _initialize_weaviate(self):
        """
        Initialize Weaviate client connection
        """
        if not self.weaviate_url or not self.weaviate_api_key:
            print("Warning: Weaviate credentials not configured. Research Agent will be limited.")
            return
            
        try:
            # Ensure URL has proper scheme
            weaviate_url = self.weaviate_url
            if not weaviate_url.startswith(('http://', 'https://')):
                weaviate_url = f"https://{weaviate_url}"
            
            # Initialize Weaviate client with timeout and error handling
            # Using v4 client syntax
            from weaviate.classes.init import Auth
            self.client = weaviate.connect_to_weaviate_cloud(
                cluster_url=weaviate_url,
                auth_credentials=Auth.api_key(self.weaviate_api_key),
                skip_init_checks=True,
                headers={"X-OpenAI-Api-Key": self.openai_api_key} if self.openai_api_key else None
            )
            
            
            # Test connection before creating schema
            if self.client.is_ready():
                print("✅ Connected to Weaviate successfully!")
                # Create schema if it doesn't exist
                self._create_schema()
            else:
                print("❌ Failed to connect to Weaviate")
                self.client = None
            
        except Exception as e:
            print(f"Warning: Could not connect to Weaviate: {e}")
            print("Research Agent will work in limited mode without vector search.")
            self.client = None
    
    def _create_schema(self):
        """
        Create Weaviate schema for research documents
        """
        if not self.client:
            return
            
        try:
            # Check if class already exists (v4 syntax)
            existing_classes = self.client.collections.list_all()
            if self.class_name in existing_classes:
                print(f"Schema {self.class_name} already exists")
                return
                
            # Create collection with v4 syntax
            from weaviate.classes.config import Property, DataType, Configure
            
            self.client.collections.create(
                name=self.class_name,
                description="Research documents for RAG functionality",
                properties=[
                    Property(name="title", data_type=DataType.TEXT, description="Document title"),
                    Property(name="content", data_type=DataType.TEXT, description="Document content"),
                    Property(name="source", data_type=DataType.TEXT, description="Document source URL or file path"),
                    Property(name="document_type", data_type=DataType.TEXT, description="Type of document (pdf, txt, web, etc.)"),
                    Property(name="uploaded_at", data_type=DataType.DATE, description="When the document was uploaded"),
                    Property(name="metadata", data_type=DataType.TEXT, description="Additional metadata as JSON string")
                ],
                vectorizer_config=Configure.Vectorizer.text2vec_openai() if self.openai_api_key else None
            )
            print(f"Created Weaviate schema for {self.class_name}")
            
        except Exception as e:
            print(f"Error creating schema: {e}")
    
    async def add_document(self, title: str, content: str, source: str, 
                          document_type: str = "text", metadata: Dict = None) -> bool:
        """
        Add a document to the vector database
        
        Args:
            title: Document title
            content: Document content
            source: Source URL or file path
            document_type: Type of document
            metadata: Additional metadata
            
        Returns:
            True if successful, False otherwise
        """
        if not self.client:
            return False
            
        try:
            # Prepare document data
            document_data = {
                "title": title,
                "content": content,
                "source": source,
                "document_type": document_type,
                "uploaded_at": datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                "metadata": json.dumps(metadata or {})
            }
            
            # Add to Weaviate (v4 syntax)
            collection = self.client.collections.get(self.class_name)
            result = collection.data.insert(document_data)
            
            return result is not None
            
        except Exception as e:
            print(f"Error adding document: {e}")
            return False
    
    async def search_documents(self, query: str, limit: int = 5, 
                             similarity_threshold: float = 0.7) -> Dict[str, Any]:
        """
        Search for relevant documents using vector similarity
        
        Args:
            query: Search query
            limit: Maximum number of results
            similarity_threshold: Minimum similarity score
            
        Returns:
            Dictionary containing search results and metadata
        """
        if not self.client:
            return {
                "error": "Weaviate not configured",
                "documents": [],
                "total_found": 0,
                "query": query
            }
        
        try:
            # Perform vector search (v4 syntax)
            collection = self.client.collections.get(self.class_name)
            result = collection.query.near_text(
                query=query,
                limit=limit,
                return_metadata=["certainty"]
            )
            
            # Process results (v4 syntax)
            documents = []
            for item in result.objects:
                certainty = item.metadata.certainty if item.metadata else 0
                
                # Filter by similarity threshold
                if certainty >= similarity_threshold:
                    doc = {
                        "title": item.properties.get("title", ""),
                        "content": item.properties.get("content", ""),
                        "source": item.properties.get("source", ""),
                        "document_type": item.properties.get("document_type", ""),
                        "similarity_score": certainty,
                        "metadata": json.loads(item.properties.get("metadata", "{}"))
                    }
                    documents.append(doc)
            
            return {
                "type": "research_results",
                "documents": documents,
                "total_found": len(documents),
                "query": query,
                "similarity_threshold": similarity_threshold
            }
            
        except Exception as e:
            return {
                "error": f"Search failed: {str(e)}",
                "documents": [],
                "total_found": 0,
                "query": query
            }
    
    async def process_web_content(self, url: str) -> Dict[str, Any]:
        """
        Process web content and add it to the knowledge base
        
        Args:
            url: URL to process
            
        Returns:
            Processing result
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, timeout=10.0)
                response.raise_for_status()
                
                # Extract text content (basic implementation)
                content = response.text
                
                # Simple text extraction (in production, use BeautifulSoup or similar)
                title_match = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE)
                title = title_match.group(1) if title_match else "Web Document"
                
                # Remove HTML tags (basic)
                text_content = re.sub(r'<[^>]+>', ' ', content)
                text_content = re.sub(r'\s+', ' ', text_content).strip()
                
                # Add to knowledge base
                success = await self.add_document(
                    title=title,
                    content=text_content[:5000],  # Limit content length
                    source=url,
                    document_type="web",
                    metadata={"url": url, "processed_at": datetime.now().isoformat()}
                )
                
                return {
                    "success": success,
                    "title": title,
                    "content_length": len(text_content),
                    "source": url
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "source": url
            }
    
    async def get_knowledge_summary(self, query: str) -> Dict[str, Any]:
        """
        Get a comprehensive knowledge summary for a query
        
        Args:
            query: Query to summarize
            
        Returns:
            Knowledge summary with sources
        """
        # If Weaviate is not configured, provide a helpful response
        if not self.client:
            return {
                "type": "knowledge_summary",
                "summary": f"I understand you're asking about '{query}'. While I don't have access to a vector database for document retrieval, I can still help you with research. To enable full document search capabilities, please configure Weaviate in your environment variables.",
                "sources": [],
                "query": query,
                "status": "limited_mode",
                "suggestion": "Configure WEAVIATE_URL and WEAVIATE_API_KEY in your .env file to enable full document search"
            }
        
        # Search for relevant documents
        search_results = await self.search_documents(query, limit=10)
        
        if not search_results.get("documents"):
            return {
                "type": "knowledge_summary",
                "summary": "No relevant documents found in the knowledge base.",
                "sources": [],
                "query": query
            }
        
        # Create summary from top documents
        documents = search_results["documents"]
        summary_parts = []
        sources = []
        
        for doc in documents[:3]:  # Use top 3 documents
            summary_parts.append(f"**{doc['title']}**: {doc['content'][:300]}...")
            sources.append({
                "title": doc["title"],
                "source": doc["source"],
                "similarity_score": doc["similarity_score"]
            })
        
        summary = "\n\n".join(summary_parts)
        
        return {
            "type": "knowledge_summary",
            "summary": summary,
            "sources": sources,
            "total_documents": len(documents),
            "query": query
        }
    
    async def get_agent_status(self) -> Dict[str, Any]:
        """
        Get the current status of the Research Agent
        """
        is_connected = self.client is not None
        
        # Get document count if connected (v4 syntax)
        document_count = 0
        if is_connected:
            try:
                collection = self.client.collections.get(self.class_name)
                result = collection.aggregate.over_all(total_count=True)
                document_count = result.total_count
            except:
                pass
        
        return {
            "name": "research_agent",
            "status": "active" if is_connected else "limited_mode",
            "description": "RAG with document retrieval and vector search" if is_connected else "Research agent in limited mode (Weaviate not configured)",
            "last_used": datetime.now().isoformat(),
            "performance_metrics": {
                "weaviate_connected": is_connected,
                "documents_stored": document_count,
                "openai_configured": bool(self.openai_api_key),
                "supported_formats": ["text", "web", "pdf"] if is_connected else ["basic_research"],
                "configuration_needed": not is_connected
            }
        }
