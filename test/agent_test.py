import unittest
from unittest.mock import patch, MagicMock
from agents.data.types import Expertise
from agents.agent import Agent
import os
from dotenv import load_dotenv

class TestAgent(unittest.TestCase):
    @patch('clients.OpenAIClient')
    def setUp(self, mock_openai_client):
        # OpenAIClient를 mock
        self.mock_openai_instance = MagicMock()
        mock_openai_client.return_value = self.mock_openai_instance

        # Expertise 객체 생성 시 attributes에 딕셔너리 형태로 값을 전달
        self.expertise = Expertise(
            subject="의학",
        )

        # Agent 인스턴스 생성
        self.agent = Agent(expertise=self.expertise, model="gpt-4o")

    def test_init(self):
        # 에이전트가 올바르게 초기화되었는지 테스트
        self.assertEqual(self.agent.expertise.subject, "의학")
        self.assertTrue(len(self.agent.chat_data) > 0)  # 초기화된 chat_data가 비어있지 않은지 확인

    def test_repr(self):
        # __repr__ 메서드 테스트
        self.assertEqual(repr(self.agent), "Agent(model=의학)")

    def test_str(self):
        # __str__ 메서드 테스트
        self.assertEqual(str(self.agent), "Agent: 의학")

    def test_len(self):
        # __len__ 메서드 테스트
        self.assertEqual(len(self.agent), len(self.agent.chat_data))

    def test_get_item(self):
        # __getitem__ 메서드 테스트
        self.assertEqual(self.agent[0]["role"], "system")
        self.assertEqual(self.agent[1]["role"], "system")

    def test_add_message(self):
        # add_message 메서드 테스트
        self.agent.add_message("user", "사용자 메시지")
        self.assertEqual(len(self.agent.chat_data), 3)
        self.assertEqual(self.agent.chat_data[-1]["role"], "user")
        self.assertEqual(self.agent.chat_data[-1]["content"], "사용자 메시지")

    def test_get_message(self):
        # get_message 메서드 테스트
        self.assertEqual(self.agent.get_message(0)["role"], "system")
        self.assertRaises(IndexError, self.agent.get_message, 999)

    def test_clear_messages(self):
        # clear_messages 메서드 테스트
        self.agent.clear_messages()
        self.assertEqual(len(self.agent.chat_data), 2)  # 초기화된 chat_data 길이 확인

    @patch('clients.OpenAIClient.generate_response')
    def test_respond(self, mock_generate_response):
        # respond 메서드 테스트
        mock_generate_response.return_value = "Mock response"
        response = self.agent.respond()
        self.assertEqual(response, "Mock response")
        mock_generate_response.assert_called_with(self.agent.chat_data)

class TestAgentReal(unittest.TestCase):
    def setUp(self):
        load_dotenv()  # 환경변수 로드
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY 환경 변수가 설정되지 않았습니다.")

        # Expertise 객체 생성
        self.expertise = Expertise(subject="의학")

        # Agent 인스턴스 생성
        self.agent = Agent(expertise=self.expertise, model="gpt-4o")

    def test_generate_response_real(self):
        input_text = "Hello, how are you?"
        response = self.agent.respond()
        print("🧪 실제 응답:", response)
        self.assertIsInstance(response, str)
        self.assertTrue(len(response) > 0)


if __name__ == "__main__":
    unittest.main()