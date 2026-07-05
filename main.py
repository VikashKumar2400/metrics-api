import time
import uuid
from typing import List
from fastapi import FastAPI, Query, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# --- CONSTANTS ---
ALLOWED_ORIGIN = "https://dash-pr91e6.example.com"
YOUR_EMAIL = "your-email@example.com"  # <-- Replace with your logged-in address

# --- CORS MIDDLEWARE ---
# We explicitly allow ONLY your assigned origin. FastAPI handles preflight 
# OPTIONS automatically, ensuring other origins do not receive the ACAO header.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[ALLOWED_ORIGIN],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- CUSTOM MIDDLEWARE ---
# Captures processing time and injects required tracking headers
@app.middleware("http")
async def add_custom_headers(request: Request, call_next):
    start_time = time.perf_counter()
    
    response: Response = await call_next(request)
    
    process_time = time.perf_counter() - start_time
    
    # Inject required headers
    response.headers["X-Request-ID"] = str(uuid.uuid4())
    response.headers["X-Process-Time"] = f"{process_time:.6f}"
    
    return response

# --- RESPONSE SCHEMA ---
class StatsResponse(BaseModel):
    email: str
    count: int
    sum: int
    min: int
    max: int
    mean: float

# --- ENDPOINT ---
@app.get("/stats", response_model=StatsResponse)
async def get_stats(values: str = Query(..., description="Comma-separated integers")):
    # Parse comma-separated string into a list of integers
    int_list: List[int] = [int(x.strip()) for x in values.split(",") if x.strip()]
    
    if not int_list:
        return {
            "email": YOUR_EMAIL,
            "count": 0,
            "sum": 0,
            "min": 0,
            "max": 0,
            "mean": 0.0
        }
    
    count_val = len(int_list)
    sum_val = sum(int_list)
    min_val = min(int_list)
    max_val = max(int_list)
    mean_val = float(sum_val / count_val)
    
    return {
        "email":"23f3003537@ds.study.iitm.ac.in",
        "count": count_val,
        "sum": sum_val,
        "min": min_val,
        "max": max_val,
        "mean": round(mean_val, 4)  # Well within the ±0.01 tolerance
    }
