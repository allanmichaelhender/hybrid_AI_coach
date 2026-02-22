CONDITIONING_LIBRARY = [
    {
        "title": "The HYROX Simulation: Sled & Run",
        "modality": "Conditioning",
        "focus": "Anaerobic",
        "description": "Simulating the metabolic shift of HYROX. Alternating 1km treadmill efforts with heavy sled pushes. Building the ability to run on 'heavy legs'.",
        "structure": [
            {
                "name": "Warmup",
                "repeat_count": 1,
                "steps": [
                    {
                        "name": "Dynamic Prep",
                        "duration_mins": 10,
                        "intensity_factor": 0.4,
                    }
                ],
            },
            {
                "name": "Hybrid Blocks",
                "repeat_count": 4,
                "steps": [
                    {
                        "name": "1km Run (Race Pace)",
                        "duration_mins": 5,
                        "intensity_factor": 0.95,
                    },
                    {
                        "name": "Heavy Sled Push (50m)",
                        "duration_mins": 5,
                        "intensity_factor": 1.1,
                    },
                    {
                        "name": "Active Rest",
                        "duration_mins": 2,
                        "intensity_factor": 0.2,
                    },
                ],
            },
        ],
    },
    {
        "title": "EMOM 40: Work Capacity",
        "modality": "Conditioning",
        "focus": "Metcon",
        "description": "Every Minute On the Minute. Minute 1: Burpees, Minute 2: KB Swings, Minute 3: Wall Balls, Minute 4: Rest. Pure aerobic-power development.",
        "structure": [
            {
                "name": "Movement Flow",
                "repeat_count": 1,
                "steps": [
                    {"name": "Joint Prep", "duration_mins": 10, "intensity_factor": 0.3}
                ],
            },
            {
                "name": "EMOM Work",
                "repeat_count": 10,
                "steps": [
                    {
                        "name": "High Volume Reps",
                        "duration_mins": 4,
                        "intensity_factor": 0.85,
                    },
                    {
                        "name": "Static Recovery",
                        "duration_mins": 1,
                        "intensity_factor": 0.1,
                    },
                ],
            },
        ],
    },
    {
        "title": "The Chipper: Engine Room",
        "modality": "Conditioning",
        "focus": "Endurance",
        "description": "One long list of movements to 'chip' away at. Rowing, Lunges, Box Step-ups, and Farmers Carries. No rest until the list is done.",
        "structure": [
            {
                "name": "Main Set",
                "repeat_count": 1,
                "steps": [
                    {
                        "name": "Continuous Functional Work",
                        "duration_mins": 60,
                        "intensity_factor": 0.75,
                    }
                ],
            }
        ],
    },
    {
        "title": "Interval Shuttles: Pro Agility",
        "modality": "Conditioning",
        "focus": "Anaerobic",
        "description": "Short, sharp directional changes. 10m shuttle sprints. Building the fast-twitch reactivity needed for obstacle racing and sports.",
        "structure": [
            {
                "name": "Warmup",
                "repeat_count": 1,
                "steps": [
                    {
                        "name": "Drills & Strides",
                        "duration_mins": 15,
                        "intensity_factor": 0.5,
                    }
                ],
            },
            {
                "name": "Agility Blocks",
                "repeat_count": 10,
                "steps": [
                    {
                        "name": "Shuttle Sprints",
                        "duration_mins": 1,
                        "intensity_factor": 1.3,
                    },
                    {"name": "Full Rest", "duration_mins": 3, "intensity_factor": 0.1},
                ],
            },
            {
                "name": "Cool Down",
                "repeat_count": 1,
                "steps": [
                    {"name": "Walk Out", "duration_mins": 5, "intensity_factor": 0.2}
                ],
            },
        ],
    },
    {
        "title": "The Devil's Press: Lactate Threshold",
        "modality": "Conditioning",
        "focus": "Threshold",
        "description": "Sustained high-rep DB work. Ground-to-overheads with dumbbells. Building the mental grit to stay moving under a high heart rate.",
        "structure": [
            {
                "name": "Activation",
                "repeat_count": 1,
                "steps": [
                    {
                        "name": "Shoulder/Hip Flow",
                        "duration_mins": 10,
                        "intensity_factor": 0.3,
                    }
                ],
            },
            {
                "name": "Threshold Engine",
                "repeat_count": 5,
                "steps": [
                    {
                        "name": "Continuous DB Reps",
                        "duration_mins": 8,
                        "intensity_factor": 0.9,
                    },
                    {
                        "name": "Deep Breathing Rest",
                        "duration_mins": 2,
                        "intensity_factor": 0.2,
                    },
                ],
            },
        ],
    },
    {
        "title": "Farmer & Skier: Grip/Pull Duo",
        "modality": "Conditioning",
        "focus": "Conditioning",
        "description": "Focusing on the back half of a HYROX race. Alternating heavy farmer's carries with 500m Ski-Erg intervals.",
        "structure": [
            {
                "name": "Grip Prep",
                "repeat_count": 1,
                "steps": [
                    {
                        "name": "Hanging/Sculling",
                        "duration_mins": 10,
                        "intensity_factor": 0.4,
                    }
                ],
            },
            {
                "name": "Grip Fatigue Sets",
                "repeat_count": 6,
                "steps": [
                    {
                        "name": "Carry + Ski Pull",
                        "duration_mins": 6,
                        "intensity_factor": 1.05,
                    },
                    {"name": "Rest", "duration_mins": 2, "intensity_factor": 0.1},
                ],
            },
        ],
    },
    {
        "title": "The Sandbag Mile",
        "modality": "Conditioning",
        "focus": "Power",
        "description": "Shouldered sandbag walking lunges. Building the absolute leg and core durability required for the end of a long race.",
        "structure": [
            {
                "name": "Joint Prep",
                "repeat_count": 1,
                "steps": [
                    {
                        "name": "Walking Flow",
                        "duration_mins": 15,
                        "intensity_factor": 0.3,
                    }
                ],
            },
            {
                "name": "The Grind",
                "repeat_count": 5,
                "steps": [
                    {
                        "name": "Sandbag Lunges",
                        "duration_mins": 7,
                        "intensity_factor": 0.95,
                    },
                    {
                        "name": "Shake Out Rest",
                        "duration_mins": 2,
                        "intensity_factor": 0.2,
                    },
                ],
            },
        ],
    },
    {
        "title": "Burpee Broad Jump Overload",
        "modality": "Conditioning",
        "focus": "Power",
        "description": "Explosive plyometrics under fatigue. 20m of broad jumps followed by a 200m row recovery.",
        "structure": [
            {
                "name": "Warmup",
                "repeat_count": 1,
                "steps": [
                    {
                        "name": "Plyo Drills",
                        "duration_mins": 15,
                        "intensity_factor": 0.4,
                    }
                ],
            },
            {
                "name": "Explosive Sets",
                "repeat_count": 8,
                "steps": [
                    {
                        "name": "Jumps + Row",
                        "duration_mins": 4,
                        "intensity_factor": 1.15,
                    },
                    {
                        "name": "Mandatory Rest",
                        "duration_mins": 1,
                        "intensity_factor": 0.1,
                    },
                ],
            },
        ],
    },
    {
        "title": "Wall Ball & Row: Aerobic Power",
        "modality": "Conditioning",
        "focus": "Endurance",
        "description": "High volume upper/lower coordination. 100 Wall Balls for time, followed by 2000m Row. Building rhythmic endurance.",
        "structure": [
            {
                "name": "Flow",
                "repeat_count": 1,
                "steps": [
                    {"name": "Mixed Bag", "duration_mins": 10, "intensity_factor": 0.4}
                ],
            },
            {
                "name": "Work Block",
                "repeat_count": 2,
                "steps": [
                    {
                        "name": "High Rep Coordination",
                        "duration_mins": 20,
                        "intensity_factor": 0.85,
                    },
                    {"name": "Rest", "duration_mins": 5, "intensity_factor": 0.1},
                ],
            },
        ],
    },
    {
        "title": "The Engine Room: Sandbag & Burpee",
        "modality": "Conditioning",
        "focus": "Work Capacity",
        "description": "Functional grinding. 400m Sandbag Lunges immediately into 100 Target Burpees. Building the grit to stay moving under extreme metabolic fatigue.",
        "structure": [
            {
                "name": "Dynamic Prep",
                "repeat_count": 1,
                "steps": [
                    {
                        "name": "Movement Flow",
                        "duration_mins": 10,
                        "intensity_factor": 0.4,
                    }
                ],
            },
            {
                "name": "Main Grind",
                "repeat_count": 4,
                "steps": [
                    {
                        "name": "Weighted Lunges",
                        "duration_mins": 8,
                        "intensity_factor": 0.95,
                    },
                    {
                        "name": "Target Burpees",
                        "duration_mins": 2,
                        "intensity_factor": 1.15,
                    },
                    {"name": "Rest", "duration_mins": 2.5, "intensity_factor": 0.1},
                ],
            },
        ],
    },
]
