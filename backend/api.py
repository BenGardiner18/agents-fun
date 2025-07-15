from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import accounts, contacts, emails, calls, transcripts, relationships

# Create FastAPI app
app = FastAPI(
    title="CRM API", 
    description="A modular CRM API for managing accounts, contacts, emails, calls, and transcripts",
    version="2.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include all routers
app.include_router(accounts.router)
app.include_router(contacts.router)
app.include_router(emails.router)
app.include_router(calls.router)
app.include_router(transcripts.router)
app.include_router(relationships.router)

@app.get("/")
def root():
    return {
        "message": "CRM API v2.0 is running! Visit /docs for API documentation.",
        "version": "2.0.0",
        "features": [
            "Modular architecture",
            "Comprehensive testing",
            "Environment-based configuration",
            "Full CRUD operations",
            "Relationship endpoints"
        ]
    }

@app.get("/health")
def health_check():
    return {"status": "healthy", "version": "2.0.0"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 