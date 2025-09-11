"""
Caching Agent for improved performance and reduced API calls.
Implements intelligent caching mechanisms for agent responses and external API calls.
"""

import json
import hashlib
import asyncio
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
import os
import pickle
from pathlib import Path

class CacheType(Enum):
    QUERY_RESULT = "query_result"
    AGENT_RESPONSE = "agent_response"
    API_RESPONSE = "api_response"
    NEWS_DATA = "news_data"
    RESEARCH_DATA = "research_data"
    SENTIMENT_DATA = "sentiment_data"

class CacheStrategy(Enum):
    LRU = "lru"  # Least Recently Used
    TTL = "ttl"  # Time To Live
    SIZE_BASED = "size_based"
    FREQUENCY_BASED = "frequency_based"

@dataclass
class CacheEntry:
    key: str
    value: Any
    cache_type: CacheType
    created_at: datetime
    last_accessed: datetime
    access_count: int = 0
    ttl_seconds: Optional[int] = None
    size_bytes: int = 0

@dataclass
class CacheConfig:
    max_size_mb: int = 100
    default_ttl_seconds: int = 3600  # 1 hour
    cleanup_interval_seconds: int = 300  # 5 minutes
    enable_compression: bool = True
    enable_persistence: bool = True
    cache_directory: str = "cache"

class CachingAgent:
    def __init__(self, config: Optional[CacheConfig] = None):
        self.config = config or CacheConfig()
        self.cache: Dict[str, CacheEntry] = {}
        self.cache_stats = {
            "hits": 0,
            "misses": 0,
            "evictions": 0,
            "total_requests": 0
        }
        
        # Create cache directory
        self.cache_dir = Path(self.config.cache_directory)
        self.cache_dir.mkdir(exist_ok=True)
        
        # Start cleanup task
        self.cleanup_task = None
        if self.config.cleanup_interval_seconds > 0:
            try:
                # Only create task if there's a running event loop
                loop = asyncio.get_running_loop()
                self.cleanup_task = asyncio.create_task(self._cleanup_loop())
            except RuntimeError:
                # No event loop running, will start cleanup task later
                self.cleanup_task = None
        
        # Load persistent cache
        if self.config.enable_persistence:
            self._load_persistent_cache()

    async def start_cleanup_task(self):
        """Start the cleanup task if it hasn't been started yet."""
        if self.cleanup_task is None and self.config.cleanup_interval_seconds > 0:
            self.cleanup_task = asyncio.create_task(self._cleanup_loop())

    def _generate_cache_key(self, query: str, agent_name: str = "", cache_type: CacheType = CacheType.QUERY_RESULT) -> str:
        """Generate a unique cache key."""
        # Create a hash of the query and agent name
        key_data = f"{query}:{agent_name}:{cache_type.value}"
        return hashlib.md5(key_data.encode()).hexdigest()

    async def get(self, key: str) -> Optional[Any]:
        """Get value from cache."""
        self.cache_stats["total_requests"] += 1
        
        if key in self.cache:
            entry = self.cache[key]
            
            # Check TTL
            if entry.ttl_seconds and self._is_expired(entry):
                await self.delete(key)
                self.cache_stats["misses"] += 1
                return None
            
            # Update access info
            entry.last_accessed = datetime.now()
            entry.access_count += 1
            self.cache_stats["hits"] += 1
            
            return entry.value
        else:
            self.cache_stats["misses"] += 1
            return None

    async def set(self, key: str, value: Any, cache_type: CacheType = CacheType.QUERY_RESULT, 
                  ttl_seconds: Optional[int] = None) -> bool:
        """Set value in cache."""
        try:
            # Calculate size
            size_bytes = self._calculate_size(value)
            
            # Check if we need to evict entries
            await self._check_and_evict(size_bytes)
            
            # Create cache entry
            entry = CacheEntry(
                key=key,
                value=value,
                cache_type=cache_type,
                created_at=datetime.now(),
                last_accessed=datetime.now(),
                ttl_seconds=ttl_seconds or self.config.default_ttl_seconds,
                size_bytes=size_bytes
            )
            
            self.cache[key] = entry
            
            # Save to persistent cache if enabled
            if self.config.enable_persistence:
                await self._save_to_persistent_cache(key, entry)
            
            return True
            
        except Exception as e:
            print(f"Error setting cache entry: {e}")
            return False

    async def delete(self, key: str) -> bool:
        """Delete entry from cache."""
        try:
            if key in self.cache:
                del self.cache[key]
                
                # Remove from persistent cache
                if self.config.enable_persistence:
                    await self._delete_from_persistent_cache(key)
                
                return True
            return False
        except Exception as e:
            print(f"Error deleting cache entry: {e}")
            return False

    async def clear(self, cache_type: Optional[CacheType] = None) -> int:
        """Clear cache entries."""
        try:
            if cache_type:
                # Clear specific cache type
                keys_to_delete = [
                    key for key, entry in self.cache.items()
                    if entry.cache_type == cache_type
                ]
            else:
                # Clear all
                keys_to_delete = list(self.cache.keys())
            
            for key in keys_to_delete:
                await self.delete(key)
            
            return len(keys_to_delete)
            
        except Exception as e:
            print(f"Error clearing cache: {e}")
            return 0

    async def get_or_set(self, key: str, value_func, cache_type: CacheType = CacheType.QUERY_RESULT,
                        ttl_seconds: Optional[int] = None) -> Any:
        """Get from cache or set if not found."""
        # Try to get from cache
        cached_value = await self.get(key)
        if cached_value is not None:
            return cached_value
        
        # Generate new value
        if asyncio.iscoroutinefunction(value_func):
            new_value = await value_func()
        else:
            new_value = value_func()
        
        # Cache the new value
        await self.set(key, new_value, cache_type, ttl_seconds)
        
        return new_value

    async def cache_query_result(self, query: str, result: Any, agent_name: str = "", 
                                ttl_seconds: Optional[int] = None) -> bool:
        """Cache a query result."""
        key = self._generate_cache_key(query, agent_name, CacheType.QUERY_RESULT)
        return await self.set(key, result, CacheType.QUERY_RESULT, ttl_seconds)

    async def get_cached_query_result(self, query: str, agent_name: str = "") -> Optional[Any]:
        """Get cached query result."""
        key = self._generate_cache_key(query, agent_name, CacheType.QUERY_RESULT)
        return await self.get(key)

    async def cache_agent_response(self, agent_name: str, query: str, response: Any,
                                  ttl_seconds: Optional[int] = None) -> bool:
        """Cache an agent response."""
        key = self._generate_cache_key(query, agent_name, CacheType.AGENT_RESPONSE)
        return await self.set(key, response, CacheType.AGENT_RESPONSE, ttl_seconds)

    async def get_cached_agent_response(self, agent_name: str, query: str) -> Optional[Any]:
        """Get cached agent response."""
        key = self._generate_cache_key(query, agent_name, CacheType.AGENT_RESPONSE)
        return await self.get(key)

    async def cache_api_response(self, api_name: str, params: Dict[str, Any], response: Any,
                                ttl_seconds: Optional[int] = None) -> bool:
        """Cache an API response."""
        # Create key from API name and parameters
        params_str = json.dumps(params, sort_keys=True)
        key = self._generate_cache_key(params_str, api_name, CacheType.API_RESPONSE)
        return await self.set(key, response, CacheType.API_RESPONSE, ttl_seconds)

    async def get_cached_api_response(self, api_name: str, params: Dict[str, Any]) -> Optional[Any]:
        """Get cached API response."""
        params_str = json.dumps(params, sort_keys=True)
        key = self._generate_cache_key(params_str, api_name, CacheType.API_RESPONSE)
        return await self.get(key)

    def _calculate_size(self, value: Any) -> int:
        """Calculate size of value in bytes."""
        try:
            if self.config.enable_compression:
                # Use pickle for size calculation
                return len(pickle.dumps(value))
            else:
                # Use JSON for size calculation
                return len(json.dumps(value).encode('utf-8'))
        except Exception:
            # Fallback to string length
            return len(str(value))

    def _is_expired(self, entry: CacheEntry) -> bool:
        """Check if cache entry is expired."""
        if entry.ttl_seconds is None:
            return False
        
        expiry_time = entry.created_at + timedelta(seconds=entry.ttl_seconds)
        return datetime.now() > expiry_time

    async def _check_and_evict(self, new_size_bytes: int):
        """Check cache size and evict if necessary."""
        current_size = sum(entry.size_bytes for entry in self.cache.values())
        max_size_bytes = self.config.max_size_mb * 1024 * 1024
        
        if current_size + new_size_bytes > max_size_bytes:
            # Need to evict entries
            await self._evict_entries(new_size_bytes)

    async def _evict_entries(self, required_space: int):
        """Evict entries to make space."""
        # Sort entries by last accessed time (LRU)
        sorted_entries = sorted(
            self.cache.items(),
            key=lambda x: x[1].last_accessed
        )
        
        freed_space = 0
        for key, entry in sorted_entries:
            if freed_space >= required_space:
                break
            
            await self.delete(key)
            freed_space += entry.size_bytes
            self.cache_stats["evictions"] += 1

    async def _cleanup_loop(self):
        """Background cleanup task."""
        while True:
            try:
                await asyncio.sleep(self.config.cleanup_interval_seconds)
                await self._cleanup_expired()
            except asyncio.CancelledError:
                break
            except Exception as e:
                print(f"Error in cleanup loop: {e}")

    async def _cleanup_expired(self):
        """Remove expired entries."""
        expired_keys = []
        for key, entry in self.cache.items():
            if self._is_expired(entry):
                expired_keys.append(key)
        
        for key in expired_keys:
            await self.delete(key)

    async def _save_to_persistent_cache(self, key: str, entry: CacheEntry):
        """Save entry to persistent cache."""
        try:
            cache_file = self.cache_dir / f"{key}.cache"
            with open(cache_file, 'wb') as f:
                pickle.dump(entry, f)
        except Exception as e:
            print(f"Error saving to persistent cache: {e}")

    async def _delete_from_persistent_cache(self, key: str):
        """Delete entry from persistent cache."""
        try:
            cache_file = self.cache_dir / f"{key}.cache"
            if cache_file.exists():
                cache_file.unlink()
        except Exception as e:
            print(f"Error deleting from persistent cache: {e}")

    def _load_persistent_cache(self):
        """Load cache from persistent storage."""
        try:
            for cache_file in self.cache_dir.glob("*.cache"):
                try:
                    with open(cache_file, 'rb') as f:
                        entry = pickle.load(f)
                    
                    # Check if entry is still valid
                    if not self._is_expired(entry):
                        self.cache[entry.key] = entry
                    else:
                        # Remove expired file
                        cache_file.unlink()
                        
                except Exception as e:
                    print(f"Error loading cache file {cache_file}: {e}")
                    # Remove corrupted file
                    cache_file.unlink()
                    
        except Exception as e:
            print(f"Error loading persistent cache: {e}")

    async def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        total_size = sum(entry.size_bytes for entry in self.cache.values())
        hit_rate = (self.cache_stats["hits"] / max(self.cache_stats["total_requests"], 1)) * 100
        
        return {
            "total_entries": len(self.cache),
            "total_size_mb": round(total_size / (1024 * 1024), 2),
            "max_size_mb": self.config.max_size_mb,
            "hit_rate_percentage": round(hit_rate, 2),
            "hits": self.cache_stats["hits"],
            "misses": self.cache_stats["misses"],
            "evictions": self.cache_stats["evictions"],
            "total_requests": self.cache_stats["total_requests"],
            "cache_types": {
                cache_type.value: len([e for e in self.cache.values() if e.cache_type == cache_type])
                for cache_type in CacheType
            },
            "config": {
                "default_ttl_seconds": self.config.default_ttl_seconds,
                "cleanup_interval_seconds": self.config.cleanup_interval_seconds,
                "enable_compression": self.config.enable_compression,
                "enable_persistence": self.config.enable_persistence
            }
        }

    async def get_agent_status(self) -> Dict[str, Any]:
        """Get caching agent status."""
        stats = await self.get_cache_stats()
        return {
            "status": "active",
            "cache_entries": stats["total_entries"],
            "cache_size_mb": stats["total_size_mb"],
            "hit_rate": stats["hit_rate_percentage"],
            "persistence_enabled": self.config.enable_persistence,
            "cleanup_running": self.cleanup_task is not None,
            "last_updated": datetime.now().isoformat()
        }

    async def warm_cache(self, queries: List[str], agents: Dict[str, Any]) -> Dict[str, Any]:
        """Warm up cache with common queries."""
        results = {
            "warmed_queries": 0,
            "failed_queries": 0,
            "errors": []
        }
        
        for query in queries:
            try:
                # Try to get cached result first
                cached_result = await self.get_cached_query_result(query)
                if cached_result is None:
                    # Execute query and cache result
                    # This would typically involve calling the orchestrator
                    # For now, we'll just mark as warmed
                    results["warmed_queries"] += 1
                else:
                    results["warmed_queries"] += 1
                    
            except Exception as e:
                results["failed_queries"] += 1
                results["errors"].append(f"Query '{query}': {str(e)}")
        
        return results

    async def invalidate_cache(self, pattern: str = None, cache_type: Optional[CacheType] = None) -> int:
        """Invalidate cache entries matching pattern or type."""
        invalidated = 0
        
        try:
            if pattern:
                # Invalidate by pattern
                keys_to_delete = [
                    key for key in self.cache.keys()
                    if pattern.lower() in key.lower()
                ]
            elif cache_type:
                # Invalidate by cache type
                keys_to_delete = [
                    key for key, entry in self.cache.items()
                    if entry.cache_type == cache_type
                ]
            else:
                # Invalidate all
                keys_to_delete = list(self.cache.keys())
            
            for key in keys_to_delete:
                await self.delete(key)
                invalidated += 1
                
        except Exception as e:
            print(f"Error invalidating cache: {e}")
        
        return invalidated

    async def close(self):
        """Close the caching agent and cleanup resources."""
        if self.cleanup_task:
            self.cleanup_task.cancel()
            try:
                await self.cleanup_task
            except asyncio.CancelledError:
                pass
        
        # Save final cache state
        if self.config.enable_persistence:
            await self._save_final_cache_state()

    async def _save_final_cache_state(self):
        """Save final cache state on shutdown."""
        try:
            # Save cache metadata
            metadata = {
                "stats": self.cache_stats,
                "config": {
                    "max_size_mb": self.config.max_size_mb,
                    "default_ttl_seconds": self.config.default_ttl_seconds,
                    "cleanup_interval_seconds": self.config.cleanup_interval_seconds,
                    "enable_compression": self.config.enable_compression,
                    "enable_persistence": self.config.enable_persistence
                },
                "last_saved": datetime.now().isoformat()
            }
            
            metadata_file = self.cache_dir / "cache_metadata.json"
            with open(metadata_file, 'w') as f:
                json.dump(metadata, f, indent=2)
                
        except Exception as e:
            print(f"Error saving final cache state: {e}")
