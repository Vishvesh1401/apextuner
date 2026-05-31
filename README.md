# ApexTuner — AI Parameter Optimizer for Autonomous Racing

## Demo Video
[https://drive.google.com/drive/folders/1U99Ni7Ud6NsT88F61sH371FJsDviyNdd?usp=sharing]

## The Problem
Tuning an autonomous racing AI is pure trial and error. You change 
parameters blindly, run laps, crash, repeat. There is no system that 
looks at your results and tells you why one configuration crashed but 
another didn't, or what to change next to go faster.

## The Solution
ApexTuner uses IBM Granite to analyze TORCS autonomous driver experiment 
results and recommend the next parameter configuration to try, with a 
predicted lap time. The feedback loop is closed — AI makes a prediction, 
you validate it in a real simulator, the result proves or disproves the 
recommendation.

## Results
- Starting lap time: 62.05 seconds
- Human best after 6 experiments: 57.49 seconds  
- AI recommendation 1: predicted 55.94s → actual 53.56s ✅
- AI recommendation 2: predicted 52.0s → actual 53.52s ✅
- Total improvement: 8.53 seconds faster than first run

## IBM Technologies Used

**IBM Granite (granite3.1-dense:2b via Ollama)**
Analyzes experiment history, identifies which parameter changes had the 
most impact, and recommends the next configuration with predicted lap time.
Runs fully locally, no API key required.

**IBM Docling**
Parses the TORCS SCR Server manual PDF into 79 knowledge chunks. These 
chunks are retrieved and injected into Granite's prompt to ground its 
reasoning in actual simulator documentation — sensor behavior, actuator 
ranges, and control system architecture.

## How the Feedback Loop Works
1. Run TORCS with a parameter configuration
2. Record the lap time and crash status
3. IBM Granite analyzes all experiment history grounded in TORCS documentation
4. Granite recommends exact next values for target_speed, steer_gain, 
   brake_threshold with predicted lap time
5. Run that configuration, add the real result back
6. Repeat — each run makes the analysis more accurate

## Tech Stack
- IBM Granite via Ollama (local inference)
- IBM Docling (PDF knowledge extraction)
- FastAPI (Python backend)
- Vanilla HTML/JS (frontend)
- TORCS + SCR server via Docker (racing simulator)

## Setup

**Requirements:** Python 3.11+, Ollama, Node.js not required

**1. Install and start Ollama**
```bash
brew install ollama
ollama serve
ollama pull granite3.1-dense:2b
```

**2. Backend**
```bash
cd backend
pip install fastapi uvicorn ollama docling
uvicorn api:app --reload --port 8000
```

**3. Frontend**
```bash
cd frontend
python3 -m http.server 3000
```

Open http://localhost:3000

## Project Structure
```
apextuner/
├── backend/
│   ├── api.py              # FastAPI endpoints
│   ├── knowledge.py        # Docling PDF parser
│   ├── experiments.json    # Experiment history
│   └── 1304_1672v2.pdf     # TORCS SCR manual
└── frontend/
    └── index.html          # Dashboard
```
