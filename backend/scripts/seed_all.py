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

from models.user import User
from models.plan import UserPlan  # 👈 This is the missing piece
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

async def seed_and_embed():
    async with AsyncSessionLocal() as db:
        to_insert = []
        
        for data in ALL_WORKOUTS:
            # A. Calculate TSS (Your Business Logic)
            tss = calculate_complex_tss(data["structure"], data["modality"])
            
            # B. CREATE SEARCH STRING: High-density metadata for the AI
            search_text = f"{data['modality']} {data['focus']} {data['title']} {data['description']}"
            
            # C. GENERATE EMBEDDING: Convert text to 384 floats
            vector = embed_model.encode(search_text).tolist()
            
            workout = Workout(
                id=uuid.uuid4(),
                title=data["title"],
                description=data["description"],
                modality=data["modality"],
                focus=data["focus"],
                structure=data["structure"],
                calculated_tss=tss,
                embedding=vector # 👈 The AI 'coordinates'
            )
            to_insert.append(workout)

        db.add_all(to_insert)
        try:
            await db.commit()
            print(f"✅ SUCCESS: {len(to_insert)} workouts embedded and seeded to Neon.")
        except Exception as e:
            await db.rollback()
            print(f"❌ SEED FAILED: {str(e)}")

if __name__ == "__main__":
    selector = selectors.SelectSelector()
    loop_factory = lambda: asyncio.SelectorEventLoop(selector)
    asyncio.run(seed_and_embed(), loop_factory=loop_factory)