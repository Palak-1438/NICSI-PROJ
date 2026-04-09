from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.auth import router as auth_router
from routes.complaints import router as complaints_router

app = FastAPI(
    title="Public Service Complaint Management System",
    description="A complete MVP for managing public service complaints with AI tagging and RBAC",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router, prefix="/api", tags=["authentication"])
app.include_router(complaints_router, prefix="/api", tags=["complaints"])

@app.get("/")
async def root():
    return {"message": "Public Service Complaint Management System API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}