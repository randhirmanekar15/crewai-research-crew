"""Tests for the pure task-description helper (no CrewAI required)."""

from crew import build_research_description


def test_description_includes_topic():
    desc = build_research_description("local LLMs")
    assert "local LLMs" in desc


def test_description_requests_findings():
    desc = build_research_description("anything")
    assert "5" in desc
