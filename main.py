import time
import uuid
from typing import List
from fastapi import FastAPI, Query, Request, Response
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

ALLOWED_ORIGIN = "https://dash-pr91e6.example.com"
YOUR_EMAIL = "23f3003537@ds.study.iitm.ac.in"

# Strict CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[ALLOWED_ORIGIN],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def add_custom_headers(request: Request, call_next):
    # CRITICAL: Preflight OPTIONS requests must bypass custom middleware
    if request.method == "OPTIONS":
        return await call_next(request)
        
    start_time = time.perf_counter()
    response: Response = await call_next(request)
    process_time = time.perf_counter() - start_time
    
    # Inject mandatory tracking headers for GET requests
    response.headers["X-Request-ID"] = str(uuid.uuid4())
    response.headers["X-Process-Time"] = f"{process_time:.6f}"
    return response

@app.get("/stats")
async def get_stats(values: str = Query(..., description="Comma-separated integers")):
    # Split raw string and convert items explicitly into integers
    int_list: List[int] = [int(x.strip()) for x in values.split(",") if x.strip()]
    
    count_val = len(int_list)
    sum_val = sum(int_list)
    min_val = min(int_list)
    max_val = max(int_list)
    mean_val = float(sum_val / count_val)
    
    return {
        "email": YOUR_EMAIL,
        "count": count_val,
        "sum": sum_val,
        "min": min_val,
        "max": max_val,
        "mean": round(mean_val, 4)
    }
