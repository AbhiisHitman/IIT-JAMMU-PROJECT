#!/usr/bin/env python
# src/latest_ai_development/main.py
from latest_ai_development.crew import ResearchPaperCompanionCrew

def run():
    """
    Run the AI Research Paper Companion crew.
    """
    topic = input("Enter the research topic: ")  # ✅ Take topic from user
    inputs = {
        "topic": topic
    }
    ResearchPaperCompanionCrew().crew().kickoff(inputs=inputs)

if __name__ == "__main__":
    run()

