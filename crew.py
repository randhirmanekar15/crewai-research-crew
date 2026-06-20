"""A two-agent research crew (Researcher + Writer) on a local model.

CrewAI's role/goal/backstory model is the fastest path to a working multi-agent
prototype. Runs locally via Ollama.

Inspired by Aman Kharwal's tutorial:
https://amanxai.com/2026/04/28/how-to-build-ai-agents-using-crewai/
"""

from __future__ import annotations

import argparse
import os

MODEL = os.environ.get("CREWAI_MODEL", "ollama/llama3")
OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434")
DEFAULT_TOPIC = "the state of multi-agent AI in 2026"


def build_research_description(topic: str) -> str:
    """Pure helper: the Researcher task description for a topic."""
    return (
        f"Research {topic}. Surface key facts, numbers, and tradeoffs. "
        "Identify at least 5 concrete findings."
    )


def build_crew(topic: str):
    """Assemble the crew. CrewAI imports stay inside so tests can skip them."""
    from crewai import LLM, Agent, Crew, Process, Task

    local_llm = LLM(model=MODEL, base_url=OLLAMA_URL)

    researcher = Agent(
        role="Senior Research Analyst",
        goal=f"Find the most relevant, current facts on {topic}",
        backstory="You dig past the obvious and cite specifics, not vibes.",
        verbose=True,
        allow_delegation=False,
        llm=local_llm,
    )
    writer = Agent(
        role="Technical Content Strategist",
        goal="Distill research into a clear, practical summary",
        backstory="You explain things simply and avoid buzzwords.",
        verbose=True,
        allow_delegation=False,
        llm=local_llm,
    )

    research_task = Task(
        description=build_research_description(topic),
        expected_output="A bulleted brief with at least 5 concrete findings.",
        agent=researcher,
    )
    writing_task = Task(
        description="Using the research brief, write a 2-paragraph Markdown summary.",
        expected_output="A 2-paragraph Markdown summary.",
        agent=writer,
    )

    return Crew(
        agents=[researcher, writer],
        tasks=[research_task, writing_task],
        process=Process.sequential,
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="CrewAI research crew")
    parser.add_argument("topic", nargs="*", help="Topic to research")
    args = parser.parse_args()
    topic = " ".join(args.topic) or DEFAULT_TOPIC
    result = build_crew(topic).kickoff()
    print("\n=== FINAL OUTPUT ===\n")
    print(result)


if __name__ == "__main__":
    main()
