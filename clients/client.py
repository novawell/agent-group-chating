# 다양한 회사들의 API를 사용하기 위한 클라이언트 코드입니다.
# 각 회사의 API에 맞는 클라이언트를 구현합니다.

from openai import OpenAI

class OpenAIClient:
    def __init__(self, api_key, model="gpt-4o"):
        self.model = model
        self.api_key = api_key
        self.client = OpenAI(api_key=api_key)

    def __repr__(self):
        return f"OpenAIClient(model={self.model})"
    
    def __str__(self):
        return f"OpenAIClient with model {self.model}"

    def generate_response(self, input_text):
        response = self.client.responses.create(
            model=self.model,
            input=input_text
        )
        return response.output_text
    
    def get_model_info(self):
        model_info = self.client.models.retrieve(model=self.model)
        return model_info
    
    def set_model(self, model):
        self.model = model
        self.client.model = model

    def get_model(self):
        return self.model

    def set_api_key(self, api_key):
        self.api_key = api_key
        self.client.api_key = api_key

    