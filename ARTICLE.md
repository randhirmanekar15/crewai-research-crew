# I Built a Two-Agent Research Crew in One Evening — Here's What CrewAI Got Right

*A Researcher and a Writer, talking to each other, running entirely on a local llama3. No API bill, no cloud, just role-goal-backstory and a sequential handoff.*

## Why this, why now

Multi-agent systems are the defining shift of 2026, and the numbers aren't subtle. Gartner logged a **1,445% surge** in client inquiries about multi-agent systems between early 2024 and mid-2025. By the end of this year, roughly **40% of enterprise apps** are expected to ship with task-specific agents baked in. We've gone from "can an LLM answer a question" to "can a team of LLMs get a job done."

The problem is most people freeze at the framework-selection step and never build anything. So let me make the call for you.

If you want a working multi-agent prototype *tonight*, use CrewAI. If you're building a stateful production system with branching, loops, and human-in-the-loop checkpoints, that's LangGraph territory. CrewAI optimizes for getting a crew running in hours. LangGraph optimizes for the graph you'll still trust in production a year from now. I started with CrewAI on purpose — fastest path from zero to "oh, it actually works."

## What it does

Two agents, one job. A **Researcher** agent investigates a topic and produces structured findings. A **Writer** agent takes those findings and turns them into a clean summary. They run sequentially: research first, then writing, with the research output flowing straight into the writing task.

The whole thing runs on a local Ollama model. No keys, no rate limits, no per-token anxiety while I iterate.

## The stack

| Layer | Choice | Why |
|---|---|---|
| Orchestration | CrewAI | Role/goal/backstory model, fastest prototype |
| Language | Python 3.11 | CrewAI's native runtime |
| Model serving | Ollama (local) | Free, private, no rate limits |
| Model | llama3 | Already on my machine, good enough to test the wiring |
| Process | `Process.sequential` | Research → write, clean handoff |

## How it works

The mental model is the whole reason CrewAI clicks so fast. You don't write orchestration logic. You write **job descriptions**.

Every agent gets three things: a **role** (who they are), a **goal** (what success looks like), and a **backstory** (the context that shapes how they behave). It's the same brief you'd hand a new hire. The framework turns that into the system prompt and manages the conversation for you.

First, point CrewAI at the local model and define the two agents:

```python
from crewai import Agent, Task, Crew, Process
from crewai import LLM

local_llm = LLM(model="ollama/llama3", base_url="http://localhost:11434")

researcher = Agent(
    role="Senior Research Analyst",
    goal="Find the most relevant, current facts on {topic}",
    backstory="You dig past the obvious. You cite specifics, not vibes.",
    verbose=True,
    allow_delegation=False,
    llm=local_llm,
)

writer = Agent(
    role="Technical Writer",
    goal="Turn raw research into a tight, readable summary",
    backstory="You write the way smart people actually talk. No fluff.",
    verbose=True,
    allow_delegation=False,
    llm=local_llm,
)
```

Then define the tasks and assemble the crew:

```python
research_task = Task(
    description="Research {topic}. Surface key facts, numbers, and tradeoffs.",
    expected_output="A bulleted brief with at least 5 concrete findings.",
    agent=researcher,
)

writing_task = Task(
    description="Using the research brief, write a 200-word summary.",
    expected_output="A clean, structured summary a busy reader can skim.",
    agent=writer,
)

crew = Crew(
    agents=[researcher, writer],
    tasks=[research_task, writing_task],
    process=Process.sequential,
)

result = crew.kickoff(inputs={"topic": "the state of multi-agent AI in 2026"})
print(result)
```

That's it. `kickoff()` runs the research task, feeds its output into the writing task, and hands you the finished summary.

## What I changed

The base tutorial is a clean skeleton. I made four edits to make it mine.

1. **Swapped to a model I already had.** The original leans on llama3 too, but I pinned `base_url` explicitly so it never silently falls back to a cloud provider. If Ollama isn't running, I *want* it to fail loudly.

2. **Added a third agent — an Editor.** A critic that reads the Writer's draft and flags anything vague or unsupported. This is where multi-agent earns its keep: one agent's blind spot is another agent's job. Quality jumped noticeably on the second pass.

3. **Gave the Researcher a tool.** Out of the box, llama3 "researches" from training memory — which means it confidently makes things up. I wired in a simple web-search tool so the findings are grounded in something real, not the model's imagination.

4. **Pointed it at a topic I actually care about.** I swapped the toy prompt for "compare CrewAI and LangGraph for production agents" and used the output as research scaffolding for *this very post*.

## Where it breaks

I'm not going to pretend this is production-ready.

**Sequential is simple but rigid.** `Process.sequential` is a straight line. The moment you need a loop ("re-research if the draft is weak") or a branch, you're fighting the abstraction. That's the wall where people graduate to LangGraph.

**Agents drift without tools.** Give an LLM a "research" role with no actual search tool and it will hallucinate a beautifully formatted lie. Grounding isn't optional — it's the difference between a demo and a tool.

**Local model quality is a real ceiling.** llama3 on my machine is great for testing the *wiring*. For output I'd publish, I felt the gap against a frontier model immediately. Local is for iteration; swap up for the final run.

**Long runs cost time even when they're free.** Three agents, multiple passes, local inference — a single kickoff can take minutes. Free of dollars, not free of patience.

## Takeaway

Reach for CrewAI when you want to *learn how multi-agent systems think* and ship a working crew the same day. The role/goal/backstory model is the fastest on-ramp in the ecosystem, full stop.

Reach for LangGraph when "it works on my machine" becomes "it has to work for 10,000 users" — when you need state, retries, branching, and human checkpoints you can actually trust.

Start with CrewAI. You'll understand agents far better by the time you outgrow it.

*Built on and adapted from Aman Kharwal's walkthrough, ["How to Build AI Agents Using CrewAI."](https://amanxai.com/2026/04/28/how-to-build-ai-agents-using-crewai/)*

### Sources
- [Aman Kharwal — How to Build AI Agents Using CrewAI](https://amanxai.com/2026/04/28/how-to-build-ai-agents-using-crewai/)
- [LangChain — AI Agent Frameworks (2026)](https://www.langchain.com/resources/ai-agent-frameworks)
- [nxcode — CrewAI vs LangChain: AI Agent Framework Comparison 2026](https://www.nxcode.io/resources/news/crewai-vs-langchain-ai-agent-framework-comparison-2026)
- [Gartner — Hype Cycle for Agentic AI](https://www.gartner.com/en/articles/hype-cycle-for-agentic-ai)
