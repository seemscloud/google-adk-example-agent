from __future__ import annotations

from typing import Any
import os


def load_config(path: str = 'config.yaml') -> dict[str, Any]:
  """Load configuration from a YAML file into a Python dict.

  Behavior:
  - Resolves a relative 'path' against this module's directory, so callers can
    run the app from anywhere and still load test/config.yaml.
  - Attempts to parse using PyYAML when available; returns an empty dict if the
    parsed content is not a mapping.
  - If PyYAML is unavailable or parsing fails, falls back to a minimal,
    line-based parser that understands simple `key: value` pairs.
  - On any I/O or parsing error the function returns an empty dict rather than
    raising, so callers can safely proceed with defaults.
  """
  if not os.path.isabs(path):
    path = os.path.join(os.path.dirname(__file__), path)

  try:
    import yaml
    with open(path, 'r', encoding='utf-8') as f:
      data = yaml.safe_load(f) or {}
    return data if isinstance(data, dict) else {}
  except Exception:
    pass

  config: dict[str, Any] = {}
  try:
    with open(path, 'r', encoding='utf-8') as f:
      for raw_line in f:
        line = raw_line.strip()
        if not line or ':' not in line:
          continue
        key, value = line.split(':', 1)
        key = key.strip()
        value = value.strip().strip('"\'')
        config[key] = value
  except Exception:
    return {}
  return config


