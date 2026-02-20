import asyncio
import os
import sys
import selectors
import uuid

# Ensure the root project dir is in path
sys.path.insert(0, os.getcwd())

from sqlalchemy import select
from database.session import AsyncSessionLocal
from api.services.embeddings import generate_workout_embedding
from models.workout import Workout

async def search_workouts_filtered(
    query: str, 
    modality: str = None, 
    focus: str = None, 
    limit: int = 3
):
    """
    Performs a Hybrid Search:
    1. Deterministic SQL filtering (Modality/Focus)
    2. Semantic Vector Ranking (Cosine Distance)
    """
    print(f"\n🔍 Searching for: '{query}'")
    if modality or focus:
        print(f"   Filters: [Modality: {modality}, Focus: {focus}]")
    
    # 1. Generate embedding for the user's natural language query
    query_vector = await generate_workout_embedding(query)
    
    async with AsyncSessionLocal() as db:
        # 2. Build the query dynamically
        stmt = select(Workout)
        
        # Apply strict SQL filters if provided
        if modality:
            stmt = stmt.filter(Workout.modality == modality)
        if focus:
            stmt = stmt.filter(Workout.focus == focus)
            
        # 3. Apply Semantic Ranking using Cosine Distance (<=>)
        # Smaller distance = Higher similarity
        stmt = stmt.order_by(Workout.embedding.cosine_distance(query_vector)).limit(limit)
        
        result = await db.execute(stmt)
        workouts = result.scalars().all()
        
        if not workouts:
            print("❌ No workouts matched these filters.")
            return

        print(f"✅ Top {len(workouts)} Matches Found:\n")
        for i, w in enumerate(workouts, 1):
            # Calculate a pseudo-similarity score (1 - distance)
            # Since we don't have the raw distance in scalars(), we just list them by rank
            print(f"{i}. {w.title} [{w.modality} - {w.focus}]")
            print(f"   TSS: {w.calculated_tss} | RPE: {w.rpe}/10")
            print(f"   Description: {w.description[:80]}...")
            print("-" * 60)

async def main():
    # TEST SCENARIO 1: Strict Filtering (The 'Slow Swim' test)
    # This should now correctly find 'Technical Drill Flush'
    await search_workouts_filtered(
        "Something easy in the pool", 
        modality="Swimming", 
        focus="Aerobic Low"
    )

    # TEST SCENARIO 2: Partial Filtering (The 'Legs' test)
    # Matches 'Strength' modality but searches vector for 'legs'
    await search_workouts_filtered(
        "I want to smash my legs", 
        modality="Strength"
    )

    # TEST SCENARIO 3: Pure Semantic (No filters)
    # Defaults to searching the entire library
    await search_workouts_filtered("High intensity lung burner")

if __name__ == "__main__":
    # THE WINDOWS FIX
    loop = asyncio.SelectorEventLoop(selectors.SelectSelector())
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(main())
    finally:
        loop.close()
