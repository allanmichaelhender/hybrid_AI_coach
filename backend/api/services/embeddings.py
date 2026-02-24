import asyncio
from sqlalchemy import select
from langchain_huggingface import HuggingFaceEmbeddings
from models.workout import Workout
from database.session import AsyncSessionLocal

# We are using Hugging face for embeddingsis 
embeddings_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")


async def generate_workout_embedding(text: str) -> list[float]:
    # Assigning a new thread to the embedding task, embed_query tells the model to embed the text
    return await asyncio.to_thread(embeddings_model.embed_query, text)

# Key helper function to filter and then semantic search our workouts for the best match
async def search_workouts_filtered(
    query: str, 
    modality: str = None, 
    focus: str = None
):
    query_vector = await generate_workout_embedding(query)
    
    async with AsyncSessionLocal() as db:
        db_query = select(Workout)
        
        if modality:
            db_query = db_query.filter(Workout.modality == modality)
        if focus:
            db_query = db_query.filter(Workout.focus == focus)
            
        # Here we order by cosine distance, pgvector allows us to do this
        db_query = db_query.order_by(Workout.embedding.cosine_distance(query_vector)).limit(1)
        
        result = await db.execute(db_query)

        # Scalars converts our response object into a Workout model object, this list only contains one object and we use .first to extract it
        return result.scalars().first()
