# agent.py의 Agent를 통해 에이전트를 생성하는 init.py
import os
from agents.agent import Agent
from agents.data.types import Expertise
from typing import List

def multi_agent_init() -> List[Agent]:
    expertises = os.listdir("agents/data/expertise-texts")
    agents = []

    for expertise in expertises:
        with open(os.path.join("agents/data/expertise-texts", expertise), "r", encoding='utf-8') as file:
            description = file.read()
        subject = expertise.split(".")[0]
        e = Expertise(subject=subject, description=description)
        agent = Agent(expertise=e, model="gpt-4o")
        agents.append(agent)

    return agents