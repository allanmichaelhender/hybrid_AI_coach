import os
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from agents.state import AgentState
from agents.prompts import SYSTEM_PROMPT
from core.config import settings


# Initialize Groq
llm = ChatGroq(
    temperature=0.1, 
    model_name="llama-3.1-70b-versatile",
    api_key=settings.GROQ_API_KEY
)

async def analyzer_node(state: AgentState):
    # 1. Prepare XML (The "Data Prep")
    calendar_xml = "\n".join([
        f"<day index='{d['day_index']}'>{d['modality']} | {d['focus']} | Locked: {d['is_user_locked']}</day>" 
        for d in state["calendar"]
    ])

    # 2. Create the Template (The "Contract")
    # This is the 'Option B' way: separates instructions from data
    prompt = ChatPromptTemplate.from_template(SYSTEM_PROMPT)
    
    # 3. Build the Chain (The "Pipe")
    chain = prompt | llm

    # 4. Invoke with a Dictionary (The "Injection")
    response = await chain.ainvoke({
        "cycle_length": state["cycle_length"],
        "calendar_xml": calendar_xml,
        "user_goal": state["user_goal"],
        "request_scope": state["request_scope"],
        "target_day": state.get("target_day", "N/A")
    })

    return {"ai_reasoning": [response.content]}
