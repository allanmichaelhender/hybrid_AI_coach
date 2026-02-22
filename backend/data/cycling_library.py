CYCLING_LIBRARY = [
    {
        "title": "The Hour of Power: FTP Build",
        "modality": "Cycling",
        "focus": "Threshold",
        "description": "The ultimate threshold builder. 2x20 minute blocks at 95-100% of FTP. Designed to increase your sustained power output.",
        "structure": [
            {"name": "Progressive Ramp", "repeat_count": 1, "steps": [{"name": "Warmup Spin", "duration_mins": 10, "intensity_factor": 0.5}]},
            {"name": "Sustained Power", "repeat_count": 2, "steps": [
                {"name": "Threshold Pull", "duration_mins": 20, "intensity_factor": 0.98}, 
                {"name": "Spin Recovery", "duration_mins": 5, "intensity_factor": 0.4}
            ]}
        ]
    },
    {
        "title": "VO2 Max Micro-Intervals",
        "modality": "Cycling",
        "focus": "VO2 Max",
        "description": "Short, sharp 30/30s. 30 seconds at 120% FTP followed by 30 seconds of rest. Rapidly increases aerobic ceiling while maintaining high cadence.",
        "structure": [
            {"name": "Activation", "repeat_count": 1, "steps": [{"name": "Ramp Up", "duration_mins": 15, "intensity_factor": 0.5}]},
            {"name": "30/30 Blocks", "repeat_count": 30, "steps": [
                {"name": "Max Power Burst", "duration_mins": 0.5, "intensity_factor": 1.25}, 
                {"name": "Total Recovery", "duration_mins": 0.5, "intensity_factor": 0.2}
            ]},
            {"name": "Flush", "repeat_count": 1, "steps": [{"name": "Easy Spin", "duration_mins": 15, "intensity_factor": 0.4}]}
        ]
    },
    {
        "title": "Low Cadence Grinds: Torque",
        "modality": "Cycling",
        "focus": "Strength",
        "description": "Strength work on the bike. 50-60 RPM at high resistance. Simulates heavy climbing and builds sport-specific leg strength.",
        "structure": [
            {"name": "Prep", "repeat_count": 1, "steps": [{"name": "Spin Up", "duration_mins": 10, "intensity_factor": 0.4}]},
            {"name": "Big Gear Blocks", "repeat_count": 4, "steps": [
                {"name": "Torque Grind", "duration_mins": 8, "intensity_factor": 0.85}, 
                {"name": "High Cadence Flush", "duration_mins": 2, "intensity_factor": 0.4}
            ]},
            {"name": "Cooldown", "repeat_count": 1, "steps": [{"name": "Easy Spin", "duration_mins": 10, "intensity_factor": 0.3}]}
        ]
    },
    {
        "title": "Zone 2 Fat Oxidation",
        "modality": "Cycling",
        "focus": "Aerobic Low",
        "description": "Steady-state endurance. Maintaining a conversational pace to build mitochondrial density and improve fat metabolism.",
        "structure": [
            {"name": "Main Set", "repeat_count": 1, "steps": [{"name": "Steady Endurance", "duration_mins": 60, "intensity_factor": 0.62}]}
        ]
    },
    {
        "title": "Tabata Spin: Anaerobic",
        "modality": "Cycling",
        "focus": "Anaerobic",
        "description": "20 seconds on, 10 seconds off. Maximum anaerobic power. Short, brutal, and highly effective for sprint speed.",
        "structure": [
            {"name": "Warmup", "repeat_count": 1, "steps": [{"name": "Build Sprints", "duration_mins": 20, "intensity_factor": 0.5}]},
            {"name": "Tabata Set", "repeat_count": 8, "steps": [
                {"name": "All-Out Sprint", "duration_mins": 0.33, "intensity_factor": 1.50}, 
                {"name": "Pedal Stop", "duration_mins": 0.17, "intensity_factor": 0.0}
            ]},
            {"name": "Cooldown", "repeat_count": 1, "steps": [{"name": "Slow Spin", "duration_mins": 36, "intensity_factor": 0.3}]}
        ]
    },
    {
        "title": "Sweet Spot: The Over-Under",
        "modality": "Cycling",
        "focus": "Threshold",
        "description": "Alternating just above and just below FTP. Clears lactate during the 'under' while building power during the 'over'.",
        "structure": [
            {"name": "Warmup", "repeat_count": 1, "steps": [{"name": "Progressive", "duration_mins": 10, "intensity_factor": 0.5}]},
            {"name": "Over-Under Set", "repeat_count": 6, "steps": [
                {"name": "Over (105% FTP)", "duration_mins": 2, "intensity_factor": 1.05}, 
                {"name": "Under (90% FTP)", "duration_mins": 2, "intensity_factor": 0.90}
            ]},
            {"name": "Spin", "repeat_count": 1, "steps": [{"name": "Easy", "duration_mins": 26, "intensity_factor": 0.4}]}
        ]
    },
    {
        "title": "Post-Squat Leg Flush",
        "modality": "Cycling",
        "focus": "Recovery",
        "description": "Minimal resistance, high cadence (90+ RPM). Focused on blood flow to assist recovery after a heavy lower body lifting session.",
        "structure": [
            {"name": "Recovery Spin", "repeat_count": 1, "steps": [{"name": "High Cadence Easy", "duration_mins": 45, "intensity_factor": 0.4}]},
            {"name": "Stretch", "repeat_count": 1, "steps": [{"name": "Off-Bike Mobility", "duration_mins": 15, "intensity_factor": 0.1}]}
        ]
    },
    {
        "title": "Pyramid Sprints",
        "modality": "Cycling",
        "focus": "Anaerobic",
        "description": "Sprints of 15s, 30s, 45s, 60s, and back down. Building the ability to repeat high-power efforts under fatigue.",
        "structure": [
            {"name": "Ramp Up", "repeat_count": 1, "steps": [{"name": "Build", "duration_mins": 15, "intensity_factor": 0.4}]},
            {"name": "Pyramid", "repeat_count": 1, "steps": [
                {"name": "Sprint Ladder", "duration_mins": 30, "intensity_factor": 1.15}, 
                {"name": "Rest", "duration_mins": 15, "intensity_factor": 0.2}
            ]}
        ]
    },
    {
        "title": "Tempo: Diesel Mode",
        "modality": "Cycling",
        "focus": "Endurance",
        "description": "Upper Zone 3 effort. Sustainable power that requires focus but allows for long duration. The 'Sweet Spot' for building base.",
        "structure": [
            {"name": "Tempo Block", "repeat_count": 1, "steps": [{"name": "Zone 3 Steady", "duration_mins": 50, "intensity_factor": 0.80}]},
            {"name": "Cooldown", "repeat_count": 1, "steps": [{"name": "Easy Spin", "duration_mins": 10, "intensity_factor": 0.4}]}
        ]
    },
    {
        "title": "Cadence Drills: Efficiency",
        "modality": "Cycling",
        "focus": "Conditioning",
        "description": "Focusing on pedal stroke efficiency. Alternating between single-leg drills and ultra-high cadence bursts.",
        "structure": [
            {"name": "Skill Blocks", "repeat_count": 5, "steps": [
                {"name": "High RPM Spin", "duration_mins": 5, "intensity_factor": 0.7}, 
                {"name": "Single Leg Focus", "duration_mins": 5, "intensity_factor": 0.5}
            ]},
            {"name": "Cooldown", "repeat_count": 1, "steps": [{"name": "Easy Spin", "duration_mins": 10, "intensity_factor": 0.4}]}
        ]
    }
]
