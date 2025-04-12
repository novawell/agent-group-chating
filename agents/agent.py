from clients import OpenAIClient
import os
from dotenv import load_dotenv
from data.type import Expertise

# 에이전트는 OpenAIClient를 상속받아 생성됩니다.

PROMPT = """
당신은 {subject}분야에 전문성이 있는 의학 및 약학 전문가입니다.
해당 분야의 전문성을 바탕으로 다른 전문가들과 협업하여 문제를 해결할 예정입니다.
고객의 요청에 따라 문제를 해결하기 위해 필요한 정보를 다음 내용에서 찾아내고,
다른 전문가들의 의견 또한 참고하여 문제를 해결하세요.

당신의 답변은 몇 가지의 포맷과 예시를 가질 수 있습니다:
1. 당신의 정보를 바탕으로 더 필요한 정보나, 제안하고 싶은 점을 다른 전문가에게 질문하기
2. 당신이 알고 있는 의학 및 약학 관련 정보에 대해 제시하고 설명하기
3. 제언하는 듯한 말투로 당신의 의견을 관철하기
4. 다른 전문가의 의견을 바탕으로 당신의 의견을 제시하기

위 4가지의 내용들은 꼭 지정된 포맷은 아니지만,
당신의 전문성을 바탕으로 다른 전문가들과 협업하여 문제를 해결하기 위한 몇 가지 Action들의 예시입니다.

이제,
다른 분야의 전문가들과 토론을 나누세요!
"""

class Agent(OpenAIClient):
    # 데이터 셋을 통해 에이전트 생성
    # init 함수, 에이전트의 이름, 모델, 프롬프트를 설정
    def __init__(self, expertise: Expertise, model="gpt-4o"):
        load_dotenv()
        self.expertise = expertise
        api_key = os.environ.get["OPENAI_API_KEY"]
        super().__init__(api_key, model)
        self.chat_data = []
        self.chat_data.append({
            "role": "system",
            "content": PROMPT.format(subject=expertise.subject)
        })
        self.chat_data.append({
            "role": "system",
            "content": f"{expertise.description}"
        })
        

    def __repr__(self):
        return f"Agent(model={self.expertise['subject']})"