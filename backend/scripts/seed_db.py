import asyncio
import os
import sys

# Ensure the backend root is in the Python path for imports
sys.path.insert(0, os.getcwd())

from sqlalchemy.ext.asyncio import AsyncSession
from database.session import AsyncSessionLocal
from api.services.embeddings import generate_workout_embedding
from api.services.tss_calc import calculate_complex_tss
from models.workout import Workout
from data.initial_workouts import INITIAL_WORKOUTS
import selectors

async def seed_library():
    """
    Iterates through INITIAL_WORKOUTS, calculates AI/Math fields,
    and performs a bulk insert into PostgreSQL.
    """
    print("🚀 Starting Hybrid Hour Seeding...")
    
    async with AsyncSessionLocal() as db:
        try:
            for w_data in INITIAL_WORKOUTS:
                print(f"  - Processing: {w_data['title']}")

                # 1. Calculate TSS (Applying Modality Multipliers)
                # Ensure calculate_precise_tss accepts (structure, modality)
                tss = calculate_complex_tss(w_data["structure"], w_data["modality"])

                # 2. Create the Searchable Context String for the Vector
                search_text = (
                    f"[{w_data['modality']}] {w_data['focus']}: {w_data['title']}. "
                    f"Difficulty: {w_data['rpe']}/10. Stress: {tss} TSS. "
                    f"Details: {w_data['description']}"
                )

                # 3. Generate 384-dim Embedding via HuggingFace
                vector = await generate_workout_embedding(search_text)

                # 4. Instantiate the Model
                db_workout = Workout(
                    title=w_data["title"],
                    modality=w_data["modality"].value, # Store as string
                    focus=w_data["focus"].value,       # Store as string
                    rpe=w_data["rpe"],
                    calculated_tss=tss,
                    description=w_data["description"],
                    structure=w_data["structure"],
                    embedding=vector
                )
                db.add(db_workout)

            # 5. Commit all to Neon
            await db.commit()
            print("\n✅ Success! 10 Hybrid Hour workouts are now live in Neon.")

        except Exception as e:
            print(f"\n❌ Error during seeding: {e}")
            await db.rollback()

if __name__ == "__main__":
    # THE WINDOWS FIX: 
    # Force the SelectorEventLoop which Psycopg requires to talk to Neon
    loop = asyncio.SelectorEventLoop(selectors.SelectSelector())
    asyncio.set_event_loop(loop)
    
    try:
        # Run our seed function inside the compatible loop
        loop.run_until_complete(seed_library())
    finally:
        loop.close()