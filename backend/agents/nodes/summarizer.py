from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from core.config import settings

async def summarizer_node(state):
    llm = ChatGroq(model_name="llama-3.3-70b-versatile", temperature=0.1, api_key=settings.GROQ_API_KEY)
    
    # We take the raw thoughts from the state
    raw_thoughts = state["ai_reasoning"][-1]

    prompt = ChatPromptTemplate.from_template("""
        You are a Head Coach. Summarize the following technical reasoning into a 
        concise, motivating 3-sentence briefing for an athlete. 
        Focus on the 'Why' behind the workout plan.
        
        STRICT: Do not mention 'Day 0' or 'Search Intents'. 
        Just give a professional summary.

        TECHNICAL REASONING:
        {raw_thoughts}
    """)

    chain = prompt | llm
    summary = await chain.ainvoke({"raw_thoughts": raw_thoughts})
    
    # Overwrite the reasoning with the clean version
    return {"ai_reasoning": [summary.content]}
#
