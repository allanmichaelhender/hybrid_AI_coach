RUNNING_LIBRARY = [
    {
        "title": "The 4x4 VO2 Max Ceiling",
        "modality": "Running",
        "focus": "VO2 Max",
        "description": "The Norwegian gold standard. 4 minutes at maximal sustainable aerobic effort (90-95% HR max) to expand the aerobic ceiling.",
        "structure": [
            {"name": "Progressive Warmup", "repeat_count": 1, "steps": [{"name": "Jog to Build", "duration_mins": 15, "intensity_factor": 0.5}]},
            {"name": "VO2 Blocks", "repeat_count": 4, "steps": [
                {"name": "Max Sustained Run", "duration_mins": 4, "intensity_factor": 1.15}, 
                {"name": "Active Recovery Walk", "duration_mins": 3, "intensity_factor": 0.3}
            ]},
            {"name": "Cool Down", "repeat_count": 1, "steps": [{"name": "Flush Jog", "duration_mins": 17, "intensity_factor": 0.4}]}
        ]
    },
    {
        "title": "Lactate Threshold Cruise",
        "modality": "Running",
        "focus": "Threshold",
        "description": "Building the 'Diesel Engine'. Sustained effort at 1-hour race pace (comfortably hard) to push back the fatigue point.",
        "structure": [
            {"name": "Ramp Up", "repeat_count": 1, "steps": [{"name": "Movement Prep", "duration_mins": 10, "intensity_factor": 0.4}]},
            {"name": "Threshold Blocks", "repeat_count": 2, "steps": [
                {"name": "Threshold Pace", "duration_mins": 20, "intensity_factor": 0.92}, 
                {"name": "Easy Jog Recovery", "duration_mins": 5, "intensity_factor": 0.4}
            ]}
        ]
    },
    {
        "title": "Hill Power Repeats",
        "modality": "Running",
        "focus": "Power",
        "description": "Strength work for runners. Short, steep hill sprints to build glute and calf power while sparing joint impact.",
        "structure": [
            {"name": "Warmup", "repeat_count": 1, "steps": [{"name": "Dynamic Mobility", "duration_mins": 15, "intensity_factor": 0.4}]},
            {"name": "Hill Sprints", "repeat_count": 10, "steps": [
                {"name": "Uphill Max Effort", "duration_mins": 1, "intensity_factor": 1.30}, 
                {"name": "Walk Down Recovery", "duration_mins": 3, "intensity_factor": 0.1}
            ]},
            {"name": "Cooldown", "repeat_count": 1, "steps": [{"name": "Flat Jog", "duration_mins": 5, "intensity_factor": 0.3}]}
        ]
    },
    {
        "title": "Nasal Breathing Base",
        "modality": "Running",
        "focus": "Aerobic Low",
        "description": "Pure Zone 2 endurance. Focus on nasal breathing and high cadence to build mitochondrial density without fatigue.",
        "structure": [
            {"name": "Base Run", "repeat_count": 1, "steps": [{"name": "Steady State Zone 2", "duration_mins": 60, "intensity_factor": 0.65}]}
        ]
    },
    {
        "title": "Anaerobic Shuttle Sprints",
        "modality": "Running",
        "focus": "Anaerobic",
        "description": "Speed endurance. 200m 'all out' repeats. Simulating the high-intensity bursts needed for functional fitness competitions.",
        "structure": [
            {"name": "Warmup", "repeat_count": 1, "steps": [{"name": "Drills & Strides", "duration_mins": 20, "intensity_factor": 0.5}]},
            {"name": "Shuttle Sets", "repeat_count": 8, "steps": [
                {"name": "Max Sprint", "duration_mins": 1, "intensity_factor": 1.40}, 
                {"name": "Full Rest", "duration_mins": 4, "intensity_factor": 0.0}
            ]}
        ]
    },
    {
        "title": "Tempo Progression",
        "modality": "Running",
        "focus": "Threshold",
        "description": "Start easy, finish hard. Every 15 minutes increase the pace until you hit 10k race intensity for the final block.",
        "structure": [
            {"name": "Progression Blocks", "repeat_count": 4, "steps": [
                {"name": "Escalating Pace", "duration_mins": 15, "intensity_factor": 0.85} 
            ]}
        ]
    },
    {
        "title": "Post-Leg Day Recovery Flush",
        "modality": "Running",
        "focus": "Recovery",
        "description": "The 'Shakeout'. Very low intensity jog to clear metabolic waste from heavy squats without adding impact stress.",
        "structure": [
            {"name": "Recovery Flush", "repeat_count": 1, "steps": [{"name": "Slow Social Pace", "duration_mins": 40, "intensity_factor": 0.4}]},
            {"name": "Mobility", "repeat_count": 1, "steps": [{"name": "Walk & Stretch", "duration_mins": 20, "intensity_factor": 0.2}]}
        ]
    },
    {
        "title": "Monash 1km Repeats",
        "modality": "Running",
        "focus": "Threshold",
        "description": "Building pacing discipline. 1000m repeats at 5k goal pace. Focus on consistent splits as the sets progress.",
        "structure": [
            {"name": "Warmup", "repeat_count": 1, "steps": [{"name": "Jog + Strides", "duration_mins": 10, "intensity_factor": 0.5}]},
            {"name": "K-Repeats", "repeat_count": 6, "steps": [
                {"name": "1km Interval", "duration_mins": 5, "intensity_factor": 1.05}, 
                {"name": "Standing Rest", "duration_mins": 3, "intensity_factor": 0.1}
            ]},
            {"name": "Cooldown", "repeat_count": 1, "steps": [{"name": "Slow Jog", "duration_mins": 2, "intensity_factor": 0.3}]}
        ]
    },
    {
        "title": "Strides & Skills",
        "modality": "Running",
        "focus": "Endurance",
        "description": "A light aerobic run punctuated by 20-second technique 'strides'. Focus on mid-foot strike and posture.",
        "structure": [
            {"name": "Aerobic Base", "repeat_count": 5, "steps": [
                {"name": "Easy Pace", "duration_mins": 10, "intensity_factor": 0.6}, 
                {"name": "Form Stride", "duration_mins": 2, "intensity_factor": 0.95}
            ]}
        ]
    },
    {
        "title": "Metcon Running: EMOM 60",
        "modality": "Running",
        "focus": "Conditioning",
        "description": "Every Minute On the Minute. 40 seconds of running, 20 seconds of rest. Constant stop-start builds high work capacity.",
        "structure": [
            {"name": "Warmup", "repeat_count": 1, "steps": [{"name": "Jog Prep", "duration_mins": 10, "intensity_factor": 0.4}]},
            {"name": "EMOM Work", "repeat_count": 50, "steps": [
                {"name": "Work Interval", "duration_mins": 0.66, "intensity_factor": 0.9}, 
                {"name": "Statue Rest", "duration_mins": 0.34, "intensity_factor": 0.0}
            ]}
        ]
    }
]
