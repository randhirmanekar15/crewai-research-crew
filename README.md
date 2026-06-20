# CrewAI Research Crew

A two-agent crew — a **Researcher** and a **Writer** — that collaborate sequentially to research a topic and produce a clean summary. Runs on a local model via Ollama. CrewAI's role/goal/backstory model is the fastest path to a working multi-agent prototype.

## Stack

| Piece | Choice |
|-------|--------|
| Orchestration | CrewAI |
| Model serving | Ollama (local) |
| Model | `llama3` |
| Process | sequential |

## Setup

```bash
ollama pull llama3
pip install -r requirements.txt
```

## Usage

```bash
python crew.py "compare CrewAI and LangGraph for production agents"
```

Configure via env vars: `CREWAI_MODEL`, `OLLAMA_URL`.

## Test

```bash
pip install pytest
pytest        # task-description helper, no CrewAI needed
```

## Limitations

- `Process.sequential` is simple but rigid — loops/branches push you to LangGraph.
- Agents drift without tools; ground the Researcher with a real search tool.
- Local model quality is a ceiling — fine for iterating, swap up for final output.

---

Inspired by Aman Kharwal's tutorial, [How to Build AI Agents Using CrewAI](https://amanxai.com/2026/04/28/how-to-build-ai-agents-using-crewai/). Rebuilt and extended (explicit local LLM binding, parameterized topic).

MIT licensed.
