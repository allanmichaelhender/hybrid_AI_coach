# Custom set modality multiplies to skew training stress score (tss) appropriately depending on the modality
MODALITY_MULTIPLIERS = {
    "Running": 1.3,
    "Strength": 0.3,
    "Hypertrophy": 0.3,
    "Conditioning": 1.1,
    "Cycling": 1.0,
    "Swimming": 1.0,
    "Rest": 0
}

# Function to calculate tss scores
def calculate_complex_tss(workout_structure: list, modality: str) -> float:
    total_base_tss = 0.0

    # We loop over all the blocks in a workout and sum the tss for each to get our total
    for block in workout_structure:
        block_tss = 0.0
        for step in block['steps']:
            # Base Formula: (mins/60) * IF^2 * 100
            step_tss = (step['duration_mins'] / 60) * (step['intensity_factor'] ** 2) * 100
            block_tss += step_tss
        total_base_tss += (block_tss * block.get('repeat_count', 1))
    
    multiplier = MODALITY_MULTIPLIERS.get(modality, 1.0)

    # We round to the nearest integer for ease of use
    return round(total_base_tss * multiplier, 1)
