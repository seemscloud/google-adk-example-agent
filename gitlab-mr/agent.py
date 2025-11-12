from google.adk.agents.llm_agent import Agent
from .config import load_config
from .tools import build_rag_tools

_cfg = load_config('config.yaml')
rag_tools = build_rag_tools(_cfg)

root_agent = Agent(
    model='gemini-2.5-flash',
    name='gitlab_mr',
    description='RAG assistant that answers using corpora defined in config.yaml.',
    instruction=(
        'Use retrieve_* RAG tools to fetch context for GitLab merge requests, commits, '
        'and files. If no relevant context is found, politely say so. Keep answers '
        'concise and readable, include brief quotes/citations when helpful.'
    ),
    tools=rag_tools,
)
