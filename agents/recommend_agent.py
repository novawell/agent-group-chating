from clients import OpenAIClient
import os
from dotenv import load_dotenv
from agents.data.types import Expertise
from setkeys import init_keys

# 에이전트는 OpenAIClient를 상속받아 생성됩니다.

PROMPT = """
당신은 노바웰의 건강기능식품 추천 전문가입니다.
앞서 여러 의학 전문가의 대화를 보고 건강기능식품 후보군을 참고하여
고객에게 알맞은 건강기능식품과 그 이유를 상세히 설명하세요.
고객이 보기에 최대한 전문적으로 보이도록 대답하세요.
꼭 모든 제품을 추천할 필요는 없습니다.

출력 양식은 다음과 같습니다.
{
    "response": "", # 전문가들의 대화를 보고 전반적인 피드백을 작성합니다.
    "recommendation": [{ # 추천 제품을 작성합니다.
        "product_id": "", # 추천 제품의 id
        "product_name": "", # 추천 제품의 이름
        "reason": "" # 추천 이유
    }]
}
"""


class Agent(OpenAIClient):
    # 데이터 셋을 통해 에이전트 생성
    # init 함수, 에이전트의 이름, 모델, 프롬프트를 설정
    def __init__(self, model="gpt-4o"):
        api_key = init_keys()
        super().__init__(api_key, model)

        self.chat_data = []
        self.chat_data.append({"role": "system", "content": PROMPT})

    def respond(self, group_chat=None):
        inp = {"role": "system", "content": group_chat}

        response = self.generate_response([*self.chat_data, inp])
        return response
