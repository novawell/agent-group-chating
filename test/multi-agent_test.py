import os
from agents import Agent, multi_agent_init, Expertise

def test_multi_agent_init():
    try:
        # multi_agent_init 함수 호출하여 agents 생성
        agents = multi_agent_init()

        # 결과가 리스트 형태인지 확인
        if not isinstance(agents, list):
            raise TypeError("multi_agent_init 함수는 리스트를 반환해야 합니다.")

        # 각 agent가 Agent 인스턴스인지 확인
        for agent in agents:
            if not isinstance(agent, Agent):
                raise TypeError(f"Expected an instance of Agent, but got {type(agent)}.")

        # 텍스트 파일에서 읽은 내용이 정확히 설정되었는지 확인
        for agent in agents:
            if not agent.expertise.subject or not agent.expertise.description:
                raise ValueError("Agent의 subject 또는 description이 잘못 설정되었습니다.")

        # 각 Agent 객체에 대해 respond 메서드 호출하여 응답 확인
        for agent in agents:
            agent.add_message("user", "요즘 너무 피곤하고 힘들어요. 가끔 한기도 들어요.")
            response = agent.respond()
            if not isinstance(response, str) or len(response) == 0:
                raise ValueError(f"Agent의 응답이 비어있거나 문자열이 아닙니다. {agent.expertise.subject}에서 발생한 문제입니다.")
            print(f"{agent.expertise.subject} 에이전트의 응답: {response}")

        print("모든 에이전트가 올바르게 초기화되고 응답을 생성했습니다.")

    except FileNotFoundError as e:
        print(f"Error: 파일을 찾을 수 없습니다. {e}")
    except TypeError as e:
        print(f"Error: 타입 오류 발생. {e}")
    except ValueError as e:
        print(f"Error: 값 오류 발생. {e}")
    except Exception as e:
        print(f"Unexpected Error: {e}")

# 테스트 실행
test_multi_agent_init()
