from langchain_huggingface import HuggingFaceEmbeddings
import asyncio

# Initialize the model globally so it only loads into memory once
# This model is ~80MB, so it's very light on your CPU/RAM
embeddings_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

async def generate_workout_embedding(text: str) -> list[float]:
    """
    Converts workout text into a 384-dimension vector.
    We use asyncio.to_thread because the embedding math is CPU-intensive
    and would otherwise block the FastAPI event loop.
    """
    return await asyncio.to_thread(embeddings_model.embed_query, text)
