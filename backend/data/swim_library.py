SWIM_LIBRARY = [
    {
        "title": "CSS Baseline Threshold",
        "modality": "Swimming",
        "focus": "Aerobic High",
        "description": "The classic CSS builder. Sustained speed at your 1500m race pace. Minimal rest to build lactate clearance.",
        "structure": [
            {"name": "Warmup", "repeat_count": 1, "steps": [{"name": "Mixed Stroke Drill", "duration_mins": 10, "intensity_factor": 0.4}]},
            {"name": "Main Set", "repeat_count": 10, "steps": [
                {"name": "100m CSS Pace", "duration_mins": 4, "intensity_factor": 0.95}, 
                {"name": "Short Wall Rest", "duration_mins": 1, "intensity_factor": 0.1}
            ]}
        ]
    },
    {
        "title": "VO2 Max Burst: Redline",
        "modality": "Swimming",
        "focus": "VO2 Max",
        "description": "High-intensity bursts to expand aerobic ceiling. 50m sprints at 95% effort followed by full recovery.",
        "structure": [
            {"name": "Warmup", "repeat_count": 1, "steps": [{"name": "Build Sets", "duration_mins": 15, "intensity_factor": 0.5}]},
            {"name": "Redline Sprints", "repeat_count": 15, "steps": [
                {"name": "50m Max Effort", "duration_mins": 1, "intensity_factor": 1.25}, 
                {"name": "Rest & Breathe", "duration_mins": 2, "intensity_factor": 0.1}
            ]}
        ]
    },
    {
        "title": "Ironman Distance Steady",
        "modality": "Swimming",
        "focus": "Aerobic Low",
        "description": "Steady-state aerobic endurance. Focus on body position and 'the catch' without stopping.",
        "structure": [
            {"name": "Main Set", "repeat_count": 1, "steps": [{"name": "Continuous Zone 2", "duration_mins": 60, "intensity_factor": 0.65}]}
        ]
    },
    {
        "title": "Hypoxic Lung Buster",
        "modality": "Swimming",
        "focus": "Aerobic Low",
        "description": "Building CO2 tolerance. Every 3, 5, 7, then 9 strokes per breath to simulate race-start stress.",
        "structure": [
            {"name": "Warmup", "repeat_count": 1, "steps": [{"name": "Easy Flow", "duration_mins": 10, "intensity_factor": 0.4}]},
            {"name": "Breath Control", "repeat_count": 5, "steps": [
                {"name": "Hypoxic Ladder", "duration_mins": 8, "intensity_factor": 0.8}, 
                {"name": "Flush Recovery", "duration_mins": 2, "intensity_factor": 0.3}
            ]}
        ]
    },
    {
        "title": "Pull-Power Strength",
        "modality": "Swimming",
        "focus": "Aerobic High",
        "description": "Paddles and Pull-buoy focus. High resistance to build upper body pulling power for open water.",
        "structure": [
            {"name": "Activation", "repeat_count": 1, "steps": [{"name": "Sculling", "duration_mins": 10, "intensity_factor": 0.3}]},
            {"name": "Heavy Pull", "repeat_count": 4, "steps": [
                {"name": "400m Paddle Work", "duration_mins": 10, "intensity_factor": 0.85}, 
                {"name": "Rest", "duration_mins": 2, "intensity_factor": 0.2}
            ]}
        ]
    },
    {
        "title": "Anaerobic Kick Finish",
        "modality": "Swimming",
        "focus": "Anaerobic",
        "description": "Leg-focused intensity. High-cadence kicking to simulate the final 200m of a swim leg.",
        "structure": [
            {"name": "Prep", "repeat_count": 1, "steps": [{"name": "Mixed Bag", "duration_mins": 10, "intensity_factor": 0.5}]},
            {"name": "Kick Overload", "repeat_count": 8, "steps": [
                {"name": "Board Kicking Max", "duration_mins": 3, "intensity_factor": 1.1}, 
                {"name": "Easy Pull Recovery", "duration_mins": 3, "intensity_factor": 0.4}
            ]}
        ]
    },
    {
        "title": "Technique Recovery Flush",
        "modality": "Swimming",
        "focus": "Aerobic Low",
        "description": "Post-race or post-strength flush. Focus on glide, high-elbow, and relaxation.",
        "structure": [
            {"name": "Drills", "repeat_count": 1, "steps": [{"name": "Total Immersion Drills", "duration_mins": 45, "intensity_factor": 0.35}]},
            {"name": "Cooldown", "repeat_count": 1, "steps": [{"name": "Float", "duration_mins": 15, "intensity_factor": 0.2}]}
        ]
    },
    {
        "title": "70.3 Race Simulation",
        "modality": "Swimming",
        "focus": "Aerobic High",
        "description": "Broken 1900m at race intensity. Alternating pace between 'sighting' and 'settling' speed.",
        "structure": [
            {"name": "Warmup", "repeat_count": 1, "steps": [{"name": "Build 400", "duration_mins": 10, "intensity_factor": 0.5}]},
            {"name": "Race Blocks", "repeat_count": 4, "steps": [
                {"name": "Race Pace Sighting", "duration_mins": 10, "intensity_factor": 0.92}, 
                {"name": "Easy Wall Flow", "duration_mins": 2, "intensity_factor": 0.2}
            ]}
        ]
    },
    {
        "title": "Sprint Metcon: In/Out",
        "modality": "Swimming",
        "focus": "Aerobic High",
        "description": "Simulation of open-water beach starts. Sprint 25m, touch the wall, pull yourself out, jump back in.",
        "structure": [
            {"name": "Warmup", "repeat_count": 1, "steps": [{"name": "Mixed Drill", "duration_mins": 15, "intensity_factor": 0.4}]},
            {"name": "In-Out Sets", "repeat_count": 6, "steps": [
                {"name": "Sprints + Deck Work", "duration_mins": 5, "intensity_factor": 1.15}, 
                {"name": "Rest", "duration_mins": 2, "intensity_factor": 0.1}
            ]}
        ]
    },
    {
        "title": "Pyramid Power",
        "modality": "Swimming",
        "focus": "Aerobic High",
        "description": "25, 50, 75, 100... then back down. Building pacing discipline under cumulative fatigue.",
        "structure": [
            {"name": "Up-Ladder", "repeat_count": 1, "steps": [{"name": "Climb", "duration_mins": 25, "intensity_factor": 0.85}]},
            {"name": "Apex Rest", "repeat_count": 1, "steps": [{"name": "Wall Recovery", "duration_mins": 5, "intensity_factor": 0.1}]},
            {"name": "Down-Ladder", "repeat_count": 1, "steps": [{"name": "Descent", "duration_mins": 30, "intensity_factor": 0.9}]}
        ]
    }
]
