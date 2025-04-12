from clients import OpenAIClient
import os
from dotenv import load_dotenv
from agents.data.types import Expertise

# 에이전트는 OpenAIClient를 상속받아 생성됩니다.

PROMPT = """
당신은 {subject}분야에 전문성이 있는 의학 및 약학 전문가입니다.
해당 분야의 전문성을 바탕으로 다른 전문가들과 협업하여 문제를 해결할 예정입니다.
고객의 요청에 따라 문제를 해결하기 위해 필요한 정보를 다음 내용에서 찾아내고,
다른 전문가들의 의견 또한 참고하여 문제를 해결하세요.

이제,
다른 분야의 전문가들과 토론을 나누세요!

아래는 몇 가지 제한 사항입니다.

당신은 최대한 당신의 분야에 대한 이야기만 하세요.
그리고, 다른 전문가들의 의견에 대응하는 모습을 최대한 보여주세요.

정형화된 답변은 지양하고,
자연스러운 대화의 톤을 유지하세요.
친구 의사 동료와 대화를 함께 나눈다고 생각하세요.

200자 이내의 일반 대화 형식으로 대답하세요.
"""

class Agent(OpenAIClient):
    # 데이터 셋을 통해 에이전트 생성
    # init 함수, 에이전트의 이름, 모델, 프롬프트를 설정
    def __init__(self, expertise: Expertise, model="gpt-4o"):
        load_dotenv()
        self.expertise = expertise
        api_key = os.environ.get("OPENAI_API_KEY")
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
        return f"Agent(model={self.model}, expert={self.expertise.subject})"
    
    def __str__(self):
        return f"Agent: {self.expertise.subject}"
    
    def __len__(self):
        return len(self.chat_data)
    
    def __getitem__(self, index):
        return self.chat_data[index]
    
    def __iter__(self):
        return iter(self.chat_data)
    
    def add_message(self, role, content):
        self.chat_data.append({"role": role, "content": content})

    def get_message(self, index=None):
        if index is None:
            return self.chat_data
        else:
            try:
                return self.chat_data[index]
            except IndexError:
                raise IndexError("Index out of range")
    
    def clear_messages(self):
        self.chat_data = []
        self.chat_data.append({
            "role": "system",
            "content": PROMPT.format(subject=self.expertise.subject)
        })
        self.chat_data.append({
            "role": "system",
            "content": f"{self.expertise.description}"
        })

    def respond(self):
        response = self.generate_response(self.chat_data)
        self.add_message("assistant", response)
        return response