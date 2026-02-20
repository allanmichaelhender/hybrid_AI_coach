from schemas.workout import Modality, Focus

INITIAL_WORKOUTS = [
    {
        "title": "Power Hour: Squat Focus",
        "modality": Modality.STRENGTH,
        "focus": Focus.STRENGTH,
        "rpe": 9,
        "description": "Maximal force production focused on the back squat. Low volume, high intensity with full recovery.",
        "structure": [
            {"name": "Warmup", "repeat_count": 1, "steps": [{"name": "Dynamic Prep", "duration_mins": 10, "intensity_factor": 0.4}]},
            {"name": "Main Set", "repeat_count": 5, "steps": [
                {"name": "Heavy Squats", "duration_mins": 6, "intensity_factor": 1.1}, 
                {"name": "Rest", "duration_mins": 4, "intensity_factor": 0.1}
            ]}
        ]
    },
    {
        "title": "Upper Body Hypertrophy",
        "modality": Modality.HYPERTROPHY,
        "focus": Focus.HYPERTROPHY,
        "rpe": 7,
        "description": "High volume metabolic stress for chest and back. Moderate rest periods and controlled eccentrics.",
        "structure": [
            {"name": "Warmup", "repeat_count": 1, "steps": [{"name": "Activation", "duration_mins": 10, "intensity_factor": 0.4}]},
            {"name": "Giant Sets", "repeat_count": 4, "steps": [
                {"name": "Push/Pull Duo", "duration_mins": 10, "intensity_factor": 0.85}, 
                {"name": "Rest", "duration_mins": 2, "intensity_factor": 0.2}
            ]},
            {"name": "Cooldown", "repeat_count": 1, "steps": [{"name": "Stretch", "duration_mins": 2, "intensity_factor": 0.2}]}
        ]
    },
    {
        "title": "The Oxygen Debt",
        "modality": Modality.RUNNING,
        "focus": Focus.VO2_MAX,
        "rpe": 10,
        "description": "4x4min maximal aerobic intervals. Designed to expand aerobic ceiling and lactate clearance.",
        "structure": [
            {"name": "Warmup", "repeat_count": 1, "steps": [{"name": "Progressive Jog", "duration_mins": 15, "intensity_factor": 0.5}]},
            {"name": "VO2 Intervals", "repeat_count": 4, "steps": [
                {"name": "Max Effort Run", "duration_mins": 4, "intensity_factor": 1.3}, 
                {"name": "Active Recovery Walk", "duration_mins": 4, "intensity_factor": 0.3}
            ]},
            {"name": "Cool Down", "repeat_count": 1, "steps": [{"name": "Easy Jog", "duration_mins": 13, "intensity_factor": 0.4}]}
        ]
    },
    {
        "title": "Sunrise Base Run",
        "modality": Modality.RUNNING,
        "focus": Focus.AEROBIC_LOW,
        "rpe": 4,
        "description": "Low impact, steady-state nasal breathing endurance run. Focus on efficiency and joint health.",
        "structure": [
            {"name": "Main Run", "repeat_count": 1, "steps": [{"name": "Zone 2 Steady", "duration_mins": 60, "intensity_factor": 0.6}]}
        ]
    },
    {
        "title": "Threshold Engine",
        "modality": Modality.CYCLING,
        "focus": Focus.AEROBIC_HIGH,
        "rpe": 8,
        "description": "Sustained effort at 1-hour race pace. Building the 'diesel' engine for long-distance power.",
        "structure": [
            {"name": "Warmup", "repeat_count": 1, "steps": [{"name": "Ramp Up", "duration_mins": 10, "intensity_factor": 0.5}]},
            {"name": "Threshold Blocks", "repeat_count": 2, "steps": [
                {"name": "Threshold Pull", "duration_mins": 20, "intensity_factor": 0.95}, 
                {"name": "Spin Recovery", "duration_mins": 5, "intensity_factor": 0.4}
            ]}
        ]
    },
    {
        "title": "Active Recovery Spin",
        "modality": Modality.CYCLING,
        "focus": Focus.AEROBIC_LOW,
        "rpe": 3,
        "description": "Low resistance, high cadence flush for the legs. Promoting blood flow without adding fatigue.",
        "structure": [
            {"name": "Flush", "repeat_count": 1, "steps": [{"name": "Easy Spin", "duration_mins": 45, "intensity_factor": 0.4}]}
        ]
    },
    {
        "title": "CSS Development",
        "modality": Modality.SWIMMING,
        "focus": Focus.VO2_MAX,
        "rpe": 9,
        "description": "Critical Swim Speed intervals. Sustaining high speed with minimal rest to build pacing skills.",
        "structure": [
            {"name": "Warmup", "repeat_count": 1, "steps": [{"name": "Mixed Strokes", "duration_mins": 10, "intensity_factor": 0.4}]},
            {"name": "Main Set", "repeat_count": 10, "steps": [
                {"name": "100m CSS Pace", "duration_mins": 4, "intensity_factor": 1.1}, 
                {"name": "Wall Rest", "duration_mins": 1, "intensity_factor": 0.1}
            ]}
        ]
    },
    {
        "title": "Technical Drill Flush",
        "modality": Modality.SWIMMING,
        "focus": Focus.AEROBIC_LOW,
        "rpe": 3,
        "description": "Low-intensity skill focus on catch and body position. Perfect for a deload day.",
        "structure": [
            {"name": "Drills", "repeat_count": 6, "steps": [
                {"name": "Technique Focus", "duration_mins": 8, "intensity_factor": 0.5}, 
                {"name": "Rest", "duration_mins": 2, "intensity_factor": 0.1}
            ]}
        ]
    },
    {
        "title": "The Burner Metcon",
        "modality": Modality.CONDITIONING,
        "focus": Focus.ANAEROBIC,
        "rpe": 10,
        "description": "High-intensity functional rounds. Burpees, KB swings, and sprints. Maximum caloric burn.",
        "structure": [
            {"name": "Warmup", "repeat_count": 1, "steps": [{"name": "Flow", "duration_mins": 10, "intensity_factor": 0.4}]},
            {"name": "Metcon", "repeat_count": 5, "steps": [
                {"name": "AMRAP Work", "duration_mins": 8, "intensity_factor": 1.2}, 
                {"name": "Total Rest", "duration_mins": 2, "intensity_factor": 0.0}
            ]}
        ]
    },
    {
        "title": "EMOM Mobility Flow",
        "modality": Modality.CONDITIONING,
        "focus": Focus.AEROBIC_LOW,
        "rpe": 2,
        "description": "Low intensity movement quality. Every minute on the minute transitions between yoga and mobility.",
        "structure": [
            {"name": "Flow", "repeat_count": 1, "steps": [{"name": "Mobility Steady State", "duration_mins": 40, "intensity_factor": 0.3}]}
        ]
    }
]
