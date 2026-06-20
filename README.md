# CrewAI Research Crew

![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue) ![License: MIT](https://img.shields.io/badge/License-MIT-green) ![Runs 100% Local](https://img.shields.io/badge/runs-100%25%20local-orange)

**A two-agent crew — a Researcher and a Writer — that collaborate sequentially to research any topic and hand you a clean summary, running entirely on a local model.**

## Overview

Multi-agent is the defining shift of 2026. Gartner logged a **1,445% surge** in client inquiries about multi-agent systems — the single fastest-growing topic on their AI desk. The question stopped being "can one LLM do this?" and became "which agent owns which job, and how do they hand off?"

CrewAI is the fastest way to find out. Instead of writing orchestration logic, you write job descriptions — a role, a goal, a backstory — and let the framework wire the collaboration. This project is a deliberately small proof of that: a Researcher gathers the facts, a Writer turns them into a summary, and the two run in sequence. No graph definitions, no state machines, just two agents with clear mandates.

The point isn't to ship this to production. It's to show how cheap a working multi-agent prototype has become. CrewAI is the whiteboard; LangGraph is the factory floor. This repo lives firmly on the whiteboard — and runs 100% locally on Ollama, so you can iterate without burning a single API token.

## Features

- **Two collaborating agents** — a Researcher and a Writer with distinct roles, goals, and backstories.
- **Sequential handoff** — `Process.sequential` passes the Researcher's output straight into the Writer's task.
- **100% local** — runs on Ollama with `llama3`; no API keys, no per-token cost, no data leaving your machine.
- **Fails loudly** — explicit local-LLM binding errors out immediately if Ollama isn't running, instead of silently falling back.
- **Parameterized topic** — pass any research subject as a CLI argument.
- **Tiny surface area** — two files. Read the whole thing in five minutes.

## How it works

CrewAI models each agent as three plain-English fields: **role** (who the agent is), **goal** (what success looks like), and **backstory** (context that shapes tone). You describe the *people*; CrewAI handles the *coordination*. The Researcher runs first, and its findings become the input to the Writer's task.

```
   "compare CrewAI and LangGraph"
                │
                ▼
        ┌───────────────┐
        │   RESEARCHER  │   role: gather facts
        │   (llama3)    │   goal: thorough notes
        └───────┬───────┘
                │  research notes
                ▼
        ┌───────────────┐
        │    WRITER     │   role: distill
        │   (llama3)    │   goal: clean summary
        └───────┬───────┘
                ▼
          clean summary
```

## Tech stack

| Component | Choice | Why |
|-----------|--------|-----|
| Framework | CrewAI | Role/goal/backstory model = fastest multi-agent prototype |
| LLM runtime | Ollama (local) | No API keys, no cost, full privacy |
| Model | `llama3` | Solid general-purpose local model |
| Orchestration | `Process.sequential` | Simplest handoff: Researcher → Writer |
| Language | Python 3.10+ | CrewAI's baseline |

## Project structure

```
crewai-research-crew/
├── crew.py          # build_research_description, build_crew, main
├── test_crew.py     # unit tests for the task-description helper
├── ARTICLE.md
├── requirements.txt
├── LICENSE          # MIT
└── README.md
```

## Installation

```bash
git clone https://github.com/randhirmanekar15/crewai-research-crew.git
cd crewai-research-crew
pip install -r requirements.txt
ollama pull llama3
ollama serve
```

## Usage

```bash
python crew.py "compare CrewAI and LangGraph for production agents"
```

The Researcher gathers findings, hands them to the Writer, and the Writer prints a clean summary. Swap the quoted string for any topic.

## Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `CREWAI_MODEL` | `ollama/llama3` | The local model the agents run on |
| `OLLAMA_URL` | `http://localhost:11434` | Where Ollama is listening |

## Testing

```bash
pip install pytest
pytest
```

`test_crew.py` covers `build_research_description` (topic injection) without calling the live model, so the suite runs in milliseconds.

## Limitations

- **Sequential is simple but rigid.** The moment you need loops, branches, or retries, you've outgrown it — move to LangGraph.
- **Agents drift without tools.** With no search tool, the Researcher answers from training data alone. Ground it before trusting output.
- **The local model is the ceiling.** Output quality is capped by `llama3`; a bigger model raises it.

## CrewAI vs LangGraph

Use **CrewAI** when you want a working multi-agent prototype today and your flow is mostly linear — you write job descriptions, not orchestration code. Reach for **LangGraph** when you need explicit control over state, loops, branching, and recovery. CrewAI gets you to "it works"; LangGraph gets you to "it ships."

## Roadmap

- [ ] Add an **Editor agent** — a third role that polishes the Writer's draft
- [ ] Give the Researcher a **search tool** — ground findings in live results
- [ ] Support **`Process.hierarchical`** — a manager agent that delegates
- [ ] Streaming output

## Credits

📖 Full write-up: [ARTICLE.md](ARTICLE.md).

Based on Aman Kharwal's tutorial, ["How to Build AI Agents Using CrewAI"](https://amanxai.com/2026/04/28/how-to-build-ai-agents-using-crewai/).

**What I changed vs the source tutorial:**

- **Explicit local-LLM binding** that fails loudly if Ollama is down, instead of silently falling back to a remote provider.
- **Parameterized research topic** via CLI argument.

## Author

Built by **Randhir Manekar** — [randhirmanekar.com](https://randhirmanekar.com) · [github.com/randhirmanekar15](https://github.com/randhirmanekar15)

## License

MIT — see [LICENSE](LICENSE).
