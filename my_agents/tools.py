from agents import function_tool

@function_tool
def query_knowledge_base(query: str) -> str:
    """Query the MCP server or knowledge base."""
    return f"Stub: You asked '{query}'. (This would query the MCP/KB in production.)"

@function_tool
def solve_math(expression: str) -> str:
    """Solve a math expression."""
    try:
        result = eval(expression, {"__builtins__": {}})
        return str(result)
    except Exception as e:
        return f"Error: {e}" 