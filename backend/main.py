from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import util

# ── App setup ──────────────────────────────────────────────
app = FastAPI(title="Bangalore Home Price Prediction API")

# CORS — Flask me manually header add kiya tha, yahan middleware se hoga
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Startup pe artifacts load karo ────────────────────────
@app.on_event("startup")
def startup_event():
    print("Starting FastAPI Server For Home Price Prediction...")
    util.load_saved_artifacts()

# ── Request schema (Flask me request.form tha, FastAPI me Pydantic) ──
class PredictRequest(BaseModel):
    total_sqft: float
    location: str
    bhk: int
    bath: int

# ── Routes ────────────────────────────────────────────────

# Flask: /get_location_names  →  FastAPI: same
@app.get("/get_location_names")
def get_location_names():
    return {
        "locations": util.get_location_names()
    }

# Flask: /predict_home_price  →  FastAPI: same
@app.post("/predict_home_price")
def predict_home_price(req: PredictRequest):
    estimated_price = util.get_estimated_price(
        req.location,
        req.total_sqft,
        req.bhk,
        req.bath
    )
    return {
        "estimated_price": estimated_price
    }