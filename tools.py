from __future__ import annotations

from typing import Any, List

from google.adk.tools.retrieval.vertex_ai_rag_retrieval import VertexAiRagRetrieval
from vertexai.preview import rag as vertex_rag


def build_rag_tools(config: dict[str, Any], section: str = 'ragEngines') -> List[VertexAiRagRetrieval]:
  """Create VertexAiRagRetrieval tools from configuration.

  Input:
    - config: Dict loaded from YAML.
    - section: Top-level key holding RAG engine definitions. Each entry under
      this section should be a mapping with:
        • id: Full resource name of the RAG corpus
              (projects/.../locations/.../ragCorpora/<id>).
        • ragTokK or ragTopK: integer, number of nearest neighbors to return.
        • ragDistanceThreshold: optional float; when provided it is passed to
          the tool as vector_distance_threshold.

  Output:
    - A list of VertexAiRagRetrieval instances, one per engine, named
      `retrieve_<engineName>`, ready to be attached to an Agent.
  """
  engines = config.get(section, {}) if isinstance(config, dict) else {}
  tools: List[VertexAiRagRetrieval] = []
  if not isinstance(engines, dict):
    return tools

  for engine_name, spec in engines.items():
    if not isinstance(spec, dict):
      continue
    corpus = spec.get('id')
    if not corpus:
      continue
    top_k = int(str(spec.get('ragTokK') or spec.get('ragTopK') or 5))
    kwargs: dict[str, Any] = {}
    thr = spec.get('ragDistanceThreshold')
    if thr is not None:
      try:
        kwargs['vector_distance_threshold'] = float(str(thr))
      except ValueError:
        pass
    desc = f'Retrieval z korpusu RAG: {engine_name} (PR/Issues/Commits/Pliki)'
    tools.append(
        VertexAiRagRetrieval(
            name=f'retrieve_{engine_name}',
            description=desc,
            rag_resources=[vertex_rag.RagResource(rag_corpus=corpus)],
            similarity_top_k=top_k,
            **kwargs,
        )
    )
  return tools


