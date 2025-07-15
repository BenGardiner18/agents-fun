#!/usr/bin/env python3
"""
FastAPI CRM Server Startup Script
"""

import uvicorn
from api import app

if __name__ == "__main__":
    print("🚀 Starting CRM FastAPI Server...")
    print("📖 API Documentation: http://localhost:8000/docs")
    print("🔍 Alternative docs: http://localhost:8000/redoc")
    print("⚡ Server running on: http://localhost:8000")
    print("-" * 50)
    
    uvicorn.run(
        "api:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Auto-reload on code changes
        log_level="info"
    ) 