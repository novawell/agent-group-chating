from typing import List
from agents import Agent
import random # 지금은 그냥 random으로 에이전트를 선택하지만, 나중에 더 정교한 방법으로 바꿀 예정

# 매 턴이 끝날 때마다 어떤 에이전트를 다음 턴에 활성화할지 결정하는 함수
# 이 함수는 각 에이전트의 응답을 기반으로 다음 에이전트를 선택

def activator(agents: List[Agent], user_input: str) -> List[Agent]:
    active_agent = None
    
    random_agents = random.sample(agents, random.randint(1, len(agents) - 1))

    for agent in random_agents:
       print(f"다음 턴에 활성화할 에이전트: {agent.expertise.subject}")
    
    return random_agents