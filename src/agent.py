import json
from typing import List, Dict, Any

from openai import OpenAI

from .config import OPENAI_API_KEY, MODEL_NAME
from .tools import (
    query_kpi,
    search_docs,
    QUERY_KPI_TOOL,
    SEARCH_DOCS_TOOL,
)

client = OpenAI(api_key=OPENAI_API_KEY)

TOOLS = [QUERY_KPI_TOOL, SEARCH_DOCS_TOOL]

SYSTEM_PROMPT = """
You are an analytics assistant that explains changes in business KPIs.

You have two tools:
- query_kpi: get numeric KPI details for a given YearMonth, Product, Region.
- search_docs: find explanations in notes/emails.

When the user asks about a change in performance (e.g. 'Why did Product B drop in August in North?'):
1. Use query_kpi to retrieve the data.
2. Then use search_docs with a query that mentions the product, region, and time period.
3. Combine both sources to give a short, business-friendly explanation.
4. Be explicit about whether the reasons are strongly supported or just plausible.
Keep answers concise and in plain business language.
"""


def call_tool(name: str, arguments: dict) -> Any:
    """Dispatch tool calls to the right Python function."""
    if name == "query_kpi":
        return query_kpi(**arguments)
    elif name == "search_docs":
        return search_docs(**arguments)
    else:
        raise ValueError(f"Unknown tool: {name}")


def run_agent(user_message: str, history: List[Dict[str, str]] | None = None) -> str:
    """
    Simple agent loop:
    - Takes chat history + new user message
    - Lets model decide whether to call tools
    - Executes tools and returns a final answer
    """
    if history is None:
        history = []

    messages: List[Dict[str, Any]] = [{"role": "system", "content": SYSTEM_PROMPT}]
    messages.extend(history)
    messages.append({"role": "user", "content": user_message})

    # First call: model can choose to call tools
    first = client.chat.completions.create(
        model=MODEL_NAME,
        messages=messages,
        tools=TOOLS,
        tool_choice="auto",
    )

    msg = first.choices[0].message

    # If the model decided to call tools
    if msg.tool_calls:
        # Record that the assistant requested tools
        messages.append(
            {
                "role": "assistant",
                "tool_calls": msg.tool_calls,
            }
        )

        # Execute each tool and append results as tool messages
        for tool_call in msg.tool_calls:
            tool_name = tool_call.function.name
            args = json.loads(tool_call.function.arguments or "{}")
            result = call_tool(tool_name, args)

            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": tool_name,
                    "content": json.dumps(result),
                }
            )

        # Second call: ask the model to answer using the tool results
        second = client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
        )
        final_msg = second.choices[0].message
        return final_msg.content or ""

    # If no tools were used, just return the model's answer
    return msg.content or ""
