from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List

@CrewBase
class ResearchPaperCompanionCrew():
    """AI Research Paper Companion crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    @agent
    def topic_explainer(self) -> Agent:
        return Agent(
            config=self.agents_config["topic_explainer"],  # matches agents.yaml
            verbose=True,
            tools=[SerperDevTool()]  # Optional: For searching relevant info
        )

    @agent
    def literature_finder(self) -> Agent:
        return Agent(
            config=self.agents_config["literature_finder"],
            verbose=True,
            tools=[SerperDevTool()]
        )

    @agent
    def gap_analyzer(self) -> Agent:
        return Agent(
            config=self.agents_config["gap_analyzer"],
            verbose=True
        )

    @task
    def explain_topic_task(self) -> Task:
        return Task(
            config=self.tasks_config["explain_topic_task"]
        )

    @task
    def find_literature_task(self) -> Task:
        return Task(
            config=self.tasks_config["find_literature_task"]
        )

    @task
    def analyze_gaps_task(self) -> Task:
        return Task(
            config=self.tasks_config["analyze_gaps_task"],
            output_file="output/research_summary.pdf"  # ✅ Save as PDF
        )

    @crew
    def crew(self) -> Crew:
        """Creates the AI Research Paper Companion crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )


