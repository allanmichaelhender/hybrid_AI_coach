from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from agents.state import AgentState, PlanAnalysis
from agents.prompts import SYSTEM_PROMPT
from core.config import settings



# Initialize Groq, importing our api key from .env file. Temperature is set to low for deterministic outputs, more important than creativity.
llm = ChatGroq(
    temperature=0.1, 
    model_name="llama-3.3-70b-versatile",
    api_key=settings.GROQ_API_KEY
)

async def analyzer_node(state: AgentState):
    # 1. Prepare XML to be used in our LLM prompt
    calendar_xml = "\n".join([
        f"<day index='{d['day_index']}'>{d['modality']} | {d['focus']} | Locked: {d['is_user_locked']}</day>" 
        for d in state["calendar"]
    ])

    # 2 Telling the LLM to follow our set schema for the output
    structured_llm = llm.with_structured_output(PlanAnalysis)

    # 2. Create the Prompt
    prompt = ChatPromptTemplate.from_template(SYSTEM_PROMPT)
    
    # 3. Build the Chain with the LangChain Pipe operator
    chain = prompt | structured_llm

    # 4. Invoke with a Dictionary, we are using asyncronous invoke. We parse our params needed for our promp via a dict when we invoke the chain.
    response = await chain.ainvoke({
        "cycle_length": state["cycle_length"],
        "calendar_xml": calendar_xml,
        "user_goal": state["user_goal"],
    })

    ai_reasoning = response.ai_reasoning
    print(ai_reasoning)

    # 5. Return both the text for the UI and the data for the next node
    return {
        "ai_reasoning": response.ai_reasoning,
        "planned_workouts": [w.dict() for w in response.planned_workouts]
    }
