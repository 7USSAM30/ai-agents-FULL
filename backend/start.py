#!/usr/bin/env python3
"""
Production startup script for Multi-Agent AI System
Handles Railway deployment and production configuration
"""

import os
import sys
import uvicorn
from pathlib import Path

def main():
    """Main startup function with production configuration."""
    
    # Set production environment variables
    os.environ.setdefault("ENVIRONMENT", "production")
    os.environ.setdefault("DEBUG", "false")
    
    # Get port from Railway environment variable
    port = int(os.environ.get("PORT", 8000))
    
    # Production configuration
    config = {
        "app": "main:app",
        "host": "0.0.0.0",
        "port": port,
        "workers": 1,  # Single worker for Railway
        "log_level": "info",
        "access_log": True,
        "use_colors": False,  # Disable colors for production logs
        "loop": "asyncio",
        "http": "httptools",
        "ws": "websockets",
        "lifespan": "on",
        "reload": False,  # Disable reload in production
        "reload_dirs": [],
        "reload_includes": [],
        "reload_excludes": [],
        "reload_delay": 0.25,
    }
    
    print(f"🚀 Starting Multi-Agent AI System on port {port}")
    print(f"🌍 Environment: {os.environ.get('ENVIRONMENT', 'development')}")
    print(f"🔧 Debug mode: {os.environ.get('DEBUG', 'false')}")
    
    try:
        uvicorn.run(**config)
    except Exception as e:
        print(f"❌ Failed to start application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
