from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import engine, get_db, Base
from app import models
from app.schemas import PractitionerCreate

# Create all tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI
app = FastAPI(
    title="🏥 PracStart API",
    description="Medical practice management and claims automation",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Root endpoint
@app.get("/", tags=["Root"])
async def read_root():
    return {
        "app": "PracStart API",
        "status": "🟢 Running",
        "version": "0.1.0",
        "message": "Medical practice management system",
        "links": {
            "documentation": "/docs",
            "alternative_docs": "/redoc",
            "health_check": "/health"
        }
    }

# Health check
@app.get("/health", tags=["System"])
async def health_check():
    return {
        "status": "healthy",
        "database": "connected",
        "api": "operational"
    }

# Register practitioner

@app.post("/practitioners/register", tags=["Practitioners"])
def register_practitioner(
    data: PractitionerCreate,
    db: Session = Depends(get_db)
):
    # Check for duplicate
    existing = db.query(Practitioner).filter(
        Practitioner.hpcsa_number == data.hpcsa_number
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=400,
            detail=f"Practitioner with HPCSA {data.hpcsa_number} already registered"
        )

    # Create new practitioner
    practitioner = Practitioner(
        full_name=data.full_name,
        hpcsa_number=data.hpcsa_number,
        practice_number=data.practice_number,
        practice_type=data.practice_type,
        verified=False,
        verification_source="pending"
    )

    db.add(practitioner)
    db.commit()
    db.refresh(practitioner)

    return {
        "success": True,
        "message": "✅ Practitioner registered successfully",
        "status": "pending_verification",
        "data": {
            "practitioner_id": practitioner.id,
            "full_name": practitioner.full_name,
            "hpcsa_number": practitioner.hpcsa_number,
            "practice_type": practitioner.practice_type
        }
    }

# List all practitioners
@app.get("/practitioners", tags=["Practitioners"])
def list_practitioners(db: Session = Depends(get_db)):
    practitioners = db.query(Practitioner).all()  # ✅ Changed
    return {
        "count": len(practitioners),
        "practitioners": practitioners
    }

# Get single practitioner
@app.get("/practitioners/{practitioner_id}", tags=["Practitioners"])
def get_practitioner(practitioner_id: int, db: Session = Depends(get_db)):
    practitioner = db.query(Practitioner).filter(  # ✅ Changed
        Practitioner.id == practitioner_id
    ).first()
    
    if not practitioner:
        raise HTTPException(
            status_code=404,
            detail=f"Practitioner with ID {practitioner_id} not found"
        )
    
    return practitioner
# Debug: List all routes
@app.get("/debug/routes", tags=["Debug"])
async def list_routes():
    routes = []
    for route in app.routes:
        if hasattr(route, 'methods'):
            routes.append({
                "path": route.path,
                "name": route.name,
                "methods": list(route.methods)
            })
    return {"total_routes": len(routes), "routes": routes}