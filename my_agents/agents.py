from agents import Agent
from my_agents.tools import query_knowledge_base, solve_math

knowledge_agent = Agent(
    name="Knowledge Agent",
    instructions="You answer general knowledge questions using the knowledge base tool.",
    tools=[query_knowledge_base],
)

math_agent = Agent(
    name="Math Agent",
    instructions="You solve math problems using the math tool.",
    tools=[solve_math],
) 