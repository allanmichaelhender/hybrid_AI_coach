from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from core.config import settings

async def summarizer_node(state):
    llm = ChatGroq(model_name="llama-3.3-70b-versatile", temperature=0.1, api_key=settings.GROQ_API_KEY)
    
    # We take the raw thoughts from the state
    ai_reasoning = state["ai_reasoning"]

    prompt = ChatPromptTemplate.from_template("""
        You are a Head Coach. Restructure the technical reasoning into a fun and engaging paragraph. 
         
        Focus on the 'Why' behind the workout plan.
        
        This is framed as if you are talking directly to the user.

        TECHNICAL REASONING:
        {ai_reasoning}
    """)

    chain = prompt | llm
    summary = await chain.ainvoke({"ai_reasoning": ai_reasoning})
    
    # Overwrite the reasoning with the clean version
    return {"ai_reasoning": summary.content}
#
