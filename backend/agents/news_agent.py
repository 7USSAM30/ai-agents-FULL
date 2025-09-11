"""
News Agent - Fetches and processes technology news from NewsAPI
"""

import httpx
import os
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import asyncio
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class NewsAgent:
    """
    News Agent that fetches technology news from NewsAPI
    """
    
    def __init__(self):
        self.api_key = os.getenv("NEWS_API_KEY")
        self.base_url = "https://newsapi.org/v2"
        self.tech_keywords = [
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
        
    async def fetch_tech_news(self, query: str = "technology", max_articles: int = 10) -> Dict[str, Any]:
        """
        Fetch technology news from NewsAPI
        
        Args:
            query: Search query for news
            max_articles: Maximum number of articles to return
            
        Returns:
            Dictionary containing news articles and metadata
        """
        if not self.api_key:
            return {
                "error": "NewsAPI key not configured",
                "articles": [],
                "total_articles": 0,
                "query_used": query,
                "processing_time": 0
            }
        
        start_time = datetime.now()
        
        try:
            # Build search query with technology focus
            tech_query = self._build_tech_query(query)
            
            # Fetch news from multiple sources
            articles = []
            
            # Try different endpoints for comprehensive coverage
            endpoints = [
                f"/everything?q={tech_query}&sortBy=publishedAt&pageSize={max_articles}",
                f"/top-headlines?category=technology&pageSize={max_articles}",
                f"/everything?q=technology OR tech OR software&sortBy=publishedAt&pageSize={max_articles//2}",
                f"/everything?q=startup OR innovation OR programming&sortBy=publishedAt&pageSize={max_articles//2}"
            ]
            
            async with httpx.AsyncClient() as client:
                for endpoint in endpoints:
                    try:
                        url = f"{self.base_url}{endpoint}&apiKey={self.api_key}"
                        response = await client.get(url, timeout=10.0)
                        
                        if response.status_code == 200:
                            data = response.json()
                            if data.get("status") == "ok":
                                articles.extend(data.get("articles", []))
                        else:
                            print(f"NewsAPI error: {response.status_code}")
                            
                    except Exception as e:
                        print(f"Error fetching from {endpoint}: {e}")
                        continue
            
            # Remove duplicates and filter for tech relevance
            unique_articles = self._deduplicate_articles(articles)
            tech_articles = self._filter_tech_articles(unique_articles)
            
            # Process and format articles
            processed_articles = self._process_articles(tech_articles[:max_articles])
            
            processing_time = (datetime.now() - start_time).total_seconds()
            
            return {
                "type": "news_summary",
                "articles": processed_articles,
                "total_articles": len(processed_articles),
                "query_used": tech_query,
                "processing_time": processing_time,
                "sources_checked": len(endpoints)
            }
            
        except Exception as e:
            processing_time = (datetime.now() - start_time).total_seconds()
            return {
                "error": f"Failed to fetch news: {str(e)}",
                "articles": [],
                "total_articles": 0,
                "query_used": query,
                "processing_time": processing_time
            }
    
    def _build_tech_query(self, query: str) -> str:
        """
        Build a technology-focused search query
        """
        query_lower = query.lower()
        
        # If query is already tech-focused, use it as is
        if any(keyword.lower() in query_lower for keyword in self.tech_keywords):
            return query
        
        # Otherwise, add comprehensive tech context
        tech_context = "technology OR tech OR software OR programming OR AI OR artificial intelligence OR machine learning OR startup OR innovation OR digital"
        return f"({query}) AND ({tech_context})"
    
    def _deduplicate_articles(self, articles: List[Dict]) -> List[Dict]:
        """
        Remove duplicate articles based on title and URL
        """
        seen_titles = set()
        seen_urls = set()
        unique_articles = []
        
        for article in articles:
            title = article.get("title", "").lower().strip()
            url = article.get("url", "").strip()
            
            if title and url and title not in seen_titles and url not in seen_urls:
                seen_titles.add(title)
                seen_urls.add(url)
                unique_articles.append(article)
        
        return unique_articles
    
    def _filter_tech_articles(self, articles: List[Dict]) -> List[Dict]:
        """
        Filter articles to ensure they're technology-related
        """
        tech_articles = []
        
        for article in articles:
            title = article.get("title", "") or ""
            description = article.get("description", "") or ""
            content = article.get("content", "") or ""
            
            # Convert to lowercase safely
            title = title.lower() if title else ""
            description = description.lower() if description else ""
            content = content.lower() if content else ""
            
            # Check if article contains tech keywords
            text_to_check = f"{title} {description} {content}"
            
            if any(keyword.lower() in text_to_check for keyword in self.tech_keywords):
                tech_articles.append(article)
        
        return tech_articles
    
    def _process_articles(self, articles: List[Dict]) -> List[Dict]:
        """
        Process and format articles for the frontend
        """
        processed = []
        
        for article in articles:
            # Calculate relevance score based on tech keywords
            relevance_score = self._calculate_relevance_score(article)
            
            processed_article = {
                "headline": article.get("title", "No title"),
                "summary": self._generate_summary(article),
                "url": article.get("url", ""),
                "published_at": article.get("publishedAt", ""),
                "source": article.get("source", {}).get("name", "Unknown"),
                "relevance_score": relevance_score,
                "image_url": article.get("urlToImage", ""),
                "author": article.get("author", "Unknown")
            }
            
            processed.append(processed_article)
        
        # Sort by relevance score
        processed.sort(key=lambda x: x["relevance_score"], reverse=True)
        
        return processed
    
    def _calculate_relevance_score(self, article: Dict) -> float:
        """
        Calculate relevance score for technology content
        """
        title = article.get("title", "") or ""
        description = article.get("description", "") or ""
        content = article.get("content", "") or ""
        
        # Convert to lowercase safely
        title = title.lower() if title else ""
        description = description.lower() if description else ""
        content = content.lower() if content else ""
        
        text = f"{title} {description} {content}"
        
        # Count tech keyword matches
        matches = sum(1 for keyword in self.tech_keywords if keyword.lower() in text)
        
        # Base score from keyword matches
        score = min(matches * 0.1, 1.0)
        
        # Boost score for recent articles (within last 24 hours)
        try:
            published_at = datetime.fromisoformat(article.get("publishedAt", "").replace("Z", "+00:00"))
            hours_old = (datetime.now(published_at.tzinfo) - published_at).total_seconds() / 3600
            
            if hours_old < 24:
                score += 0.2
            elif hours_old < 168:  # 1 week
                score += 0.1
        except:
            pass
        
        return min(score, 1.0)
    
    def _generate_summary(self, article: Dict) -> str:
        """
        Generate a summary from article content
        """
        description = article.get("description", "")
        content = article.get("content", "")
        
        # Use description if available and not too long
        if description and len(description) < 300:
            return description
        
        # Use content if available
        if content:
            # Take first 200 characters and add ellipsis
            summary = content[:200].strip()
            if len(content) > 200:
                summary += "..."
            return summary
        
        # Fallback to title
        return article.get("title", "No summary available")
    
    async def get_agent_status(self) -> Dict[str, Any]:
        """
        Get the current status of the News Agent
        """
        return {
            "name": "news_agent",
            "status": "active" if self.api_key else "inactive",
            "description": "Fetches live technology news data",
            "last_used": datetime.now().isoformat(),
            "performance_metrics": {
                "api_key_configured": bool(self.api_key),
                "tech_keywords_count": len(self.tech_keywords),
                "supported_sources": ["NewsAPI"]
            }
        }
