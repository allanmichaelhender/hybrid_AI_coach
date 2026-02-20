import asyncio
from sqlalchemy import select
from langchain_huggingface import HuggingFaceEmbeddings
from models.workout import Workout
from database.session import AsyncSessionLocal

# Initialize globally
embeddings_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# --- THE ATOM (Used by Seed Script / Admin) ---
async def generate_workout_embedding(text: str) -> list[float]:
    """Pure vector generation. Use this for seeding the DB."""
    return await asyncio.to_thread(embeddings_model.embed_query, text)

# --- THE MOLECULE (Used by AI Agent / Search) ---
async def search_workouts_filtered(
    query: str, 
    modality: str = None, 
    focus: str = None, 
    limit: int = 1
):
    """The 'Hybrid Search' engine for the AI Planner."""
    # We call the 'Atom' inside the 'Molecule' to keep it DRY (Don't Repeat Yourself)
    query_vector = await generate_workout_embedding(query)
    
    async with AsyncSessionLocal() as db:
        stmt = select(Workout)
        
        if modality:
            stmt = stmt.filter(Workout.modality == modality)
        if focus:
            stmt = stmt.filter(Workout.focus == focus)
            
        stmt = stmt.order_by(Workout.embedding.cosine_distance(query_vector)).limit(limit)
        
        result = await db.execute(stmt)
        return result.scalars().first()
