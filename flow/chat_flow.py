import asyncio
from typing import List, Dict, Any
from agents import Agent
from flow.activator import activator
import uuid


class Flow:
    def __init__(self, agents: List[Agent], user_input: str) -> None:
        self.messages = [{"role": "user", "content": user_input}]
        self.turn_log = [self.messages.copy()]

        self.agents = agents
        self.turn_count = 1
        self.flow_id = str(uuid.uuid4())

        for agent in agents:
            agent.add_message("user", user_input)

        print(f"사용자 입력: {user_input}")

    def __len__(self) -> int:
        return len(self.turn_count)

    def __getitem__(self, index: int):
        try:
            return self.turn_log[index]
        except IndexError:
            raise IndexError("Index out of range")

    def __repr__(self) -> str:
        return f"Flow({self.flow_id}"

    def __str__(self) -> str:
        return f"Flow({self.flow_id}, {self.turn_count} turns, {len(self.messages)} messages)"

    async def get_agent_response(self, agents: List[Agent]):
        tasks = [asyncio.to_thread(agent.respond) for agent in agents]
        return await asyncio.gather(*tasks)

    def turn(self, agents: List[Agent]):
        if self.turn_count > 5:
            print("플로우를 종료합니다.")
            return

        print(self)
        print("=" * 20, f"Turn {self.turn_count}", "=" * 20)
        loop = asyncio.get_event_loop()
        responses = loop.run_until_complete(self.get_agent_response(agents))

        for agent, response in zip(agents, responses):
            print(f"{agent.expertise.subject} 에이전트의 응답: {response} \n")
            self.messages.append({"role": agent.expertise.subject, "content": response})
            for tot_agent in self.agents:
                if tot_agent != agent:
                    tot_agent.add_message("user", f"{agent.expertise.subject} 전문가의 응답: {response}")

        self.turn_log.append(responses.copy())
        self.turn_count += 1

        # 다음 턴에 활성화할 에이전트를 결정
        next_agent = activator(self.agents, "")
        return self.turn(next_agent)

    def run(self):
        # 첫 번째 턴을 시작
        print(self.flow_id, "플로우 시작")
        self.turn(self.agents)

        return self.turn_log
