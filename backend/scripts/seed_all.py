import asyncio
import uuid
import sys
import os
import selectors
from sentence_transformers import SentenceTransformer
from sqlalchemy.ext.asyncio import AsyncSession
from database.session import AsyncSessionLocal
from models.workout import Workout
from api.services.tss_calc import calculate_complex_tss
from sqlalchemy import delete

from models.user import User
from models.plan import UserPlan  
from models.workout import Workout


from data.swim_library import SWIM_LIBRARY
from data.cycling_library import CYCLING_LIBRARY
from data.hypertrophy_library import HYPERTROPHY_LIBRARY
from data.running_library import RUNNING_LIBRARY
from data.strength_library import STRENGTH_LIBRARY
from data.conditioning_library import CONDITIONING_LIBRARY


sys.path.append(os.getcwd())

# 1. Load the Model (Runs locally on your CPU/GPU)
print("🧠 Loading Hugging Face Model (all-MiniLM-L6-v2)...")
embed_model = SentenceTransformer('all-MiniLM-L6-v2')




ALL_WORKOUTS = (
    SWIM_LIBRARY + RUNNING_LIBRARY + CYCLING_LIBRARY + 
    STRENGTH_LIBRARY + HYPERTROPHY_LIBRARY + CONDITIONING_LIBRARY
)

async def refresh_database():
    async with AsyncSessionLocal() as db:
        try:
            # --- STEP 1: CLEAR THE TABLE ---
            print("🗑️  Wiping the 'workouts' table on Neon...")
            await db.execute(delete(Workout))
            
            # --- STEP 2: GENERATE NEW DATA ---
            new_workouts = []
            print(f"🧬 Processing {len(ALL_WORKOUTS)} updated workouts...")
            
            for item in ALL_WORKOUTS:
                # Calculate new TSS based on your tweaks
                tss = calculate_complex_tss(item["structure"], item["modality"])
                
                # Create Search String for the Vector
                search_text = f"{item['modality']} {item['focus']} {item['title']} {item['description']}"
                embedding = embed_model.encode(search_text).tolist()
                
                new_workout = Workout(
                    title=item["title"],
                    description=item["description"],
                    modality=item["modality"],
                    focus=item["focus"],
                    structure=item["structure"],
                    calculated_tss=tss,
                    embedding=embedding 
                )
                new_workouts.append(new_workout)
            
            # --- STEP 3: INSERT ---
            db.add_all(new_workouts)
            await db.commit()
            print(f"✅ SUCCESS: {len(new_workouts)} workouts refreshed and re-indexed.")
            
        except Exception as e:
            await db.rollback()
            print(f"❌ ERROR during refresh: {str(e)}")

if __name__ == "__main__":
    print("🚀 Starting Atomic Refresh of 'workouts' table...")
    try:
        asyncio.run(refresh_database())
        print("🏁 Refresh Complete.")
    except Exception as e:
        print(f"⚠️  Fatal Script Error: {e}")
