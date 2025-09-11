"""
Learning Agent - Automatically learns from queries and populates knowledge base
"""

import asyncio
import os
from typing import Dict, List, Any, Optional
from datetime import datetime
import json
from dotenv import load_dotenv
from .news_agent import NewsAgent
from .research_agent import ResearchAgent

# Load environment variables
load_dotenv()

class LearningAgent:
    """
    Learning Agent that automatically learns from queries by:
    1. Fetching relevant news/articles
    2. Processing and storing them in the knowledge base
    3. Building a comprehensive knowledge base over time
    """
    
    def __init__(self):
        self.news_agent = NewsAgent()
        self.research_agent = ResearchAgent()
        self.learning_keywords = [
            # AI & Machine Learning
            "artificial intelligence", "AI", "machine learning", "ML", "deep learning",
            "neural networks", "computer vision", "natural language processing", "NLP",
            "GPT", "ChatGPT", "OpenAI", "generative AI", "LLM", "large language model",
            
            # Technology & Software
            "technology", "tech", "software", "programming", "coding", "development",
            "startup", "innovation", "digital", "cyber", "cybersecurity", "data science",
            "big data", "analytics", "database", "API", "web development",
            
            # Programming Languages & Frameworks
            "Python", "JavaScript", "Java", "C++", "C#", "React", "Vue", "Angular",
            "Node.js", "Django", "Flask", "Spring", "Laravel", "PHP", "Ruby",
            "Swift", "Kotlin", "Go", "Rust", "TypeScript", "HTML", "CSS",
            
            # Cloud & Infrastructure
            "cloud computing", "AWS", "Azure", "Google Cloud", "GCP", "Docker",
            "Kubernetes", "DevOps", "CI/CD", "microservices", "serverless",
            "edge computing", "distributed systems", "scalability",
            
            # Mobile & Web
            "mobile app", "iOS", "Android", "React Native", "Flutter", "Xamarin",
            "web app", "responsive design", "PWA", "mobile development",
            
            # Emerging Technologies
            "blockchain", "cryptocurrency", "bitcoin", "ethereum", "Web3", "DeFi",
            "NFT", "smart contracts", "virtual reality", "VR", "augmented reality", "AR",
            "metaverse", "IoT", "internet of things", "smart home", "automation",
            "robotics", "quantum computing", "5G", "6G", "autonomous vehicles",
            "self-driving", "Tesla", "electric vehicles", "EV",
            
            # Companies & Platforms
            "Google", "Microsoft", "Meta", "Facebook", "Apple", "Amazon", "Netflix",
            "Twitter", "X", "LinkedIn", "GitHub", "GitLab", "Slack", "Discord",
            "Zoom", "Teams", "Spotify", "YouTube", "TikTok", "Instagram",
            
            # Gaming & Entertainment
            "gaming", "video games", "esports", "streaming", "Twitch", "Steam",
            "PlayStation", "Xbox", "Nintendo", "Unity", "Unreal Engine",
            
            # Business & Finance Tech
            "fintech", "payments", "digital banking", "cryptocurrency", "trading",
            "investment", "venture capital", "IPO", "startup funding",
            
            # Health & Biotech
            "healthtech", "biotech", "medical technology", "telemedicine",
            "digital health", "wearables", "fitness tech", "health monitoring"
        ]
    
    async def learn_from_query(self, query: str, max_articles: int = 5) -> Dict[str, Any]:
        """
        Learn from a query by fetching relevant information and storing it
        
        Args:
            query: The user's query
            max_articles: Maximum number of articles to fetch and store
            
        Returns:
            Learning result with statistics
        """
        learning_result = {
            "query": query,
            "articles_fetched": 0,
            "articles_stored": 0,
            "learning_successful": False,
            "timestamp": datetime.now().isoformat()
        }
        
        try:
            # Check if query is worth learning from
            if not self._is_worth_learning(query):
                learning_result["reason"] = "Query not suitable for learning"
                return learning_result
            
            # Fetch news articles related to the query
            print(f"🧠 Learning from query: '{query}'")
            news_result = await self.news_agent.fetch_tech_news(query, max_articles)
            
            if news_result.get("error"):
                learning_result["error"] = news_result["error"]
                return learning_result
            
            articles = news_result.get("articles", [])
            learning_result["articles_fetched"] = len(articles)
            
            if not articles:
                learning_result["reason"] = "No relevant articles found"
                return learning_result
            
            # Store articles in knowledge base
            stored_count = 0
            for article in articles:
                try:
                    # Create a comprehensive document from the article
                    document_title = f"News: {article.get('headline', 'Untitled')}"
                    document_content = self._create_document_content(article)
                    
                    # Store in research agent's knowledge base
                    success = await self.research_agent.add_document(
                        title=document_title,
                        content=document_content,
                        source=article.get('url', 'news_api'),
                        document_type="news_article",
                        metadata={
                            "source": article.get('source', 'Unknown'),
                            "published_at": article.get('published_at', ''),
                            "relevance_score": article.get('relevance_score', 0),
                            "author": article.get('author', 'Unknown'),
                            "learning_timestamp": datetime.now().isoformat(),
                            "original_query": query
                        }
                    )
                    
                    if success:
                        stored_count += 1
                        print(f"✅ Learned from: {article.get('headline', 'Untitled')[:50]}...")
                    
                except Exception as e:
                    print(f"❌ Error storing article: {e}")
                    continue
            
            learning_result["articles_stored"] = stored_count
            learning_result["learning_successful"] = stored_count > 0
            
            if stored_count > 0:
                print(f"🎉 Successfully learned from {stored_count} articles!")
            
            return learning_result
            
        except Exception as e:
            learning_result["error"] = str(e)
            return learning_result
    
    def _is_worth_learning(self, query: str) -> bool:
        """
        Determine if a query is worth learning from
        """
        query_lower = query.lower()
        
        # Check if query contains learning keywords
        has_keywords = any(keyword.lower() in query_lower for keyword in self.learning_keywords)
        
        # Check if query is not too short or too long
        appropriate_length = 2 <= len(query.split()) <= 20
        
        # Check if query is not a command or greeting
        not_command = not any(cmd in query_lower for cmd in [
            "hello", "hi", "hey", "thanks", "thank you", "bye", "goodbye",
            "help", "what can you do", "status", "test"
        ])
        
        print(f"🔍 Learning check for '{query}': keywords={has_keywords}, length={appropriate_length}, not_command={not_command}")
        
        return has_keywords and appropriate_length and not_command
    
    def _create_document_content(self, article: Dict) -> str:
        """
        Create comprehensive document content from an article
        """
        headline = article.get('headline', '')
        summary = article.get('summary', '')
        source = article.get('source', 'Unknown')
        published_at = article.get('published_at', '')
        author = article.get('author', 'Unknown')
        
        # Create structured content
        content_parts = [
            f"Title: {headline}",
            f"Source: {source}",
            f"Author: {author}",
            f"Published: {published_at}",
            "",
            "Summary:",
            summary,
            "",
            "This article provides insights into current developments in technology and artificial intelligence."
        ]
        
        return "\n".join(content_parts)
    
    async def get_learning_stats(self) -> Dict[str, Any]:
        """
        Get statistics about what the system has learned
        """
        try:
            if not self.research_agent.client:
                return {
                    "status": "inactive",
                    "reason": "Research Agent not connected to Weaviate"
                }
            
            # Get document count
            collection = self.research_agent.client.collections.get(self.research_agent.class_name)
            result = collection.aggregate.over_all(total_count=True)
            total_documents = result.total_count
            
            # Get recent learning activity (last 24 hours) - simplified for now
            recent_documents = 0  # TODO: Implement proper recent document filtering
            
            return {
                "status": "active",
                "total_documents_learned": total_documents,
                "recent_learning_activity": recent_documents,
                "learning_keywords": len(self.learning_keywords),
                "last_updated": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }
    
    async def get_agent_status(self) -> Dict[str, Any]:
        """
        Get the current status of the Learning Agent
        """
        return {
            "name": "learning_agent",
            "status": "active",
            "description": "Automatically learns from queries and populates knowledge base",
            "last_used": datetime.now().isoformat(),
            "performance_metrics": {
                "learning_keywords_count": len(self.learning_keywords),
                "news_agent_available": bool(self.news_agent.api_key),
                "research_agent_available": bool(self.research_agent.client),
                "auto_learning_enabled": True
            }
        }
