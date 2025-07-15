from agents import Runner

async def run_agent(agent, user_input):
    return await Runner.run(agent, user_input) 