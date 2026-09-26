from contextlib import asynccontextmanager
import logging

from fastapi import Depends, FastAPI, HTTPException,status,Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from logging_config import setup_logging
from models import Customer
from schemas import CustomerCreate, CustomerResponse
from middleware import request_logging_middleware
from request_context import request_id_context
from database import Base, engine, get_db, check_database_connection
from app.services.customer_service import find_customer
from app.services.customer_service import (
    create_customer as create_customer_service,
    update_customer as update_customer_service,
    patch_customer as patch_customer_service
)
from schemas import CustomerCreate, CustomerResponse, CustomerUpdate, CustomerPatch
from app.services.customer_service import delete_customer as delete_customer_service
from app.services.external_client import check_external_service


# Configure application logging
setup_logging()

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application startup and shutdown lifecycle.
    """
    logger.info("FDE Customer Platform started")

    yield

    logger.info("FDE Customer Platform shutting down")


# Create database tables
Base.metadata.create_all(bind=engine)


# Create FastAPI application
app = FastAPI(
    title="FDE Customer Platform",
    lifespan=lifespan
)

app.middleware("http")(request_logging_middleware)


@app.get("/")
def home():
    return {
        "message": "FDE Customer Platform is running"
    }

@app.get("/live")
def liveness_check():
    return {
        "status": "alive"
    }

@app.get("/ready")
def readiness_check():
    database_healthy = check_database_connection()

    if not database_healthy:
        raise HTTPException(
            status_code=503,
            detail={
                "status": "not_ready",
                "database": "unavailable"
            }
        )

    return {
        "status": "ready",
        "database": "healthy"
    }

@app.get("/health")
def health_check():
    database_healthy = check_database_connection()

    if not database_healthy:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={
                "status": "unhealthy",
                "database": "unhealthy"
            }
        )

    return {
        "status": "healthy",
        "database": "healthy"
    }

@app.post(
    "/customers",
    status_code=201,
    response_model=CustomerResponse
)
def create_customer(
    customer: CustomerCreate,
    db: Session = Depends(get_db)
):
    logger.info(
        "%s | Creating customer: %s",
        request_id_context.get(),
        customer.name
    )

    try:
        new_customer = create_customer_service(
            db=db,
            name=customer.name,
            role=customer.role
        )

        logger.info(
            "%s | Customer created successfully: id=%s",
            request_id_context.get(),
            new_customer.id
        )

        return new_customer

    except Exception:
        logger.exception(
            "%s | Failed to create customer",
            request_id_context.get()
        )

        raise HTTPException(
            status_code=500,
            detail="Unable to create customer"
        )
    
@app.get(
    "/customers",
    response_model=list[CustomerResponse]
)
def get_customers(
    db: Session = Depends(get_db)
):
    customers = db.query(Customer).all()
    return customers

@app.get(
    "/customers/{customer_id}",
    response_model=CustomerResponse
)
def get_customer(
    customer_id: int,
    db: Session = Depends(get_db)
):
    customer = find_customer(
        db=db,
        customer_id=customer_id
    )

    if customer is None:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    return customer
@app.exception_handler(Exception)
async def global_exception_handler(
    request: Request,
    exc: Exception
):
    request_id = request_id_context.get()

    logger.exception(
        "%s | Unhandled exception | %s %s",
        request_id,
        request.method,
        request.url.path
    )

    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error",
            "request_id": request_id
        }
    )

@app.put("/customers/{customer_id}", response_model=CustomerResponse)
def update_customer(
    customer_id: int,
    customer: CustomerUpdate,
    db: Session = Depends(get_db)
):
    updated_customer = update_customer_service(
        db=db,
        customer_id=customer_id,
        name=customer.name,
        role=customer.role
    )

    if updated_customer is None:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    return updated_customer

##patch customer
@app.patch("/customers/{customer_id}", response_model=CustomerResponse)
def patch_customer(
    customer_id: int,
    customer: CustomerPatch,
    db: Session = Depends(get_db)
):
    patched_customer = patch_customer_service(
        db=db,
        customer_id=customer_id,
        name=customer.name,
        role=customer.role
    )

    if patched_customer is None:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    return patched_customer

##delete customer
@app.delete("/customers/{customer_id}")
def delete_customer(
    customer_id: int,
    db: Session = Depends(get_db)
):
    deleted_customer = delete_customer_service(
        db=db,
        customer_id=customer_id
    )

    if deleted_customer is None:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    return {
        "message": "Customer deleted successfully",
        "customer_id": customer_id
    }

@app.get("/external-check")
def external_check():
    try:
        result = check_external_service()

        return {
            "status": "success",
            "external_response": result
        }

    except RuntimeError:
        request_id = request_id_context.get()

        logger.error(
            "%s | External service unavailable",
            request_id
        )

        return JSONResponse(
            status_code=503,
            content={
                "status": "unavailable",
                "message": "External service temporarily unavailable",
                "request_id": request_id
            }
        )