from google.adk.agents.llm_agent import Agent
from .config import load_config
from .tools import build_rag_tools

_cfg = load_config('config.yaml')
rag_tools = build_rag_tools(_cfg)

root_agent = Agent(
    model='gemini-2.5-flash',
    name='root_agent',
    description='Asystent RAG (odpowiada na podstawie korpusów z config.yaml).',
    instruction=(
        'Uzywaj RAG Enginge z tools do odpowiedzi na pytanie'
    ),
    tools=rag_tools,
)
