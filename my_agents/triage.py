from agents import Agent
from agent_definitions import knowledge_agent, math_agent

triage_agent = Agent(
    name="Triage Agent",
    instructions="You determine whether a question is about general knowledge or math, and hand off to the appropriate agent.",
    handoffs=[knowledge_agent, math_agent],
) 