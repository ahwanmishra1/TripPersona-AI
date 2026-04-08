from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.schemas.request import TripRequest
from src.graph.builder import build_graph

app = FastAPI(title="TripPersona API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

graph = build_graph()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/plan")
def plan_trip(request: TripRequest):
    state = {"request": request.model_dump()}
    result = graph.invoke(state)
    return result["response"]