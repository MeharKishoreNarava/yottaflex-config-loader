# AI Prompt History & Disclosure

As part of the YottaFlex AI recruitment project, AI coding assistants were used to accelerate boilerplate creation, structure validation modules, and design idempotent upsert patterns. All generated code was personally reviewed, tested, and verified.

## Prompts Used:
1. "Help me design a configuration-driven data loader in Python where schemas, primary keys, and paths are read from a JSON configuration file rather than hardcoded."
2. "Write a robust Pydantic/dictionary validation function that catches missing primary keys, negative amounts, and unauthorized status codes, routing failures to a JSON Lines quarantine file."
3. "Implement an idempotent Pandas-to-Parquet upsert mechanism that handles duplicate keys cleanly on pipeline reruns."
4. "Create a Pytest suite covering happy paths, malformed inputs, missing keys, and duplicate record handling."