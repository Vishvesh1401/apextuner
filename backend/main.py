import ollama

experiments = [
    {"experiment": 1, "target_speed": 100, "steer_gain": 30, "brake_threshold": 0.9, "lap_time": None, "crashed": False, "notes": "Smooth, no crashes, stable"},
    {"experiment": 2, "target_speed": 70, "steer_gain": 30, "brake_threshold": 0.9, "lap_time": None, "crashed": False, "notes": "Smooth, stable, slow"},
    {"experiment": 3, "target_speed": 120, "steer_gain": 15, "brake_threshold": 0.9, "lap_time": 62.05, "crashed": False, "notes": "Smooth, improving consistency"},
    {"experiment": 4, "target_speed": 120, "steer_gain": 15, "brake_threshold": 0.4, "lap_time": 67.00, "crashed": False, "notes": "Earlier braking, safer but slower"},
    {"experiment": 5, "target_speed": 150, "steer_gain": 12, "brake_threshold": 0.6, "lap_time": None, "crashed": True, "notes": "Crashed, too aggressive"},
    {"experiment": 6, "target_speed": 130, "steer_gain": 12, "brake_threshold": 0.5, "lap_time": 57.49, "crashed": False, "notes": "Best result, consistent improvement"},
]

prompt = f"""You are an expert autonomous racing AI tuner analyzing TORCS simulator experiments.

Here are the results of parameter tuning experiments on an autonomous racing driver:

{experiments}

Parameters explained:
- target_speed: The speed the car tries to maintain in km/h
- steer_gain: Steering sensitivity, higher = more aggressive turning
- brake_threshold: Angle at which braking triggers, lower = brakes earlier
- crashed: Whether the car lost control

Analyze:
1. Which parameter changes had the most impact on lap time
2. Why experiment 5 crashed but experiment 6 did not
3. What the relationship is between steer_gain and target_speed stability

Then recommend the exact next configuration to try. Give specific numbers for target_speed, steer_gain, brake_threshold. Predict the lap time this configuration will achieve and explain your reasoning."""

response = ollama.chat(
    model="granite3.1-dense:2b",
    messages=[{"role": "user", "content": prompt}]
)

print(response["message"]["content"])