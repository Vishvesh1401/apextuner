from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import ollama
import json
import os

os.environ["DOCLING_DEVICE"] = "cpu"
from knowledge import build_knowledge_base, get_relevant_chunks

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Build knowledge base once on startup
print("Loading TORCS knowledge base...")
KNOWLEDGE_CHUNKS = build_knowledge_base()
print(f"Knowledge base ready: {len(KNOWLEDGE_CHUNKS)} chunks")

def load_experiments():
    with open("experiments.json", "r") as f:
        return json.load(f)

def save_experiments(data):
    with open("experiments.json", "w") as f:
        json.dump(data, f, indent=2)

@app.get("/experiments")
def get_experiments():
    return load_experiments()

@app.post("/analyze")
def analyze():
    data = load_experiments()
    experiments = data["experiments"]

    relevant = get_relevant_chunks(
        KNOWLEDGE_CHUNKS,
        ["speed", "steering", "brake", "actuator", "sensor", "control"]
    )
    knowledge_context = "\n\n".join(relevant)

    prompt = f"""You are an expert autonomous racing AI tuner analyzing TORCS simulator experiments.

TORCS Technical Reference:
{knowledge_context}

Experiment results ordered by performance:
{sorted([e for e in experiments if not e['crashed'] and e['lap_time']], key=lambda x: x['lap_time'])}

Crashed experiments (avoid these parameter combinations):
{[e for e in experiments if e['crashed']]}

Current best lap time is {min([e['lap_time'] for e in experiments if e['lap_time']], default=999)} seconds.

Your goal is to recommend a configuration that beats the current best without crashing.
Rules:
- target_speed above 150 crashed, stay below that
- lower brake_threshold than 0.4 with high speed caused instability
- steer_gain of 30 is too sensitive at high speeds

Give exactly:
1. Recommended target_speed (number only)
2. Recommended steer_gain (number only)
3. Recommended brake_threshold (number only)
4. Predicted lap time (number only)
5. One paragraph explanation grounded in TORCS sensor and actuator behavior"""

    response = ollama.chat(
        model="granite3.1-dense:2b",
        messages=[{"role": "user", "content": prompt}]
    )

    return {"analysis": response["message"]["content"]}

@app.post("/add-experiment")
def add_experiment(experiment: dict):
    data = load_experiments()
    experiment["id"] = len(data["experiments"]) + 1
    data["experiments"].append(experiment)
    save_experiments(data)
    return {"status": "saved", "experiment": experiment}

@app.get("/health")
def health():
    return {"status": "running", "knowledge_chunks": len(KNOWLEDGE_CHUNKS)}