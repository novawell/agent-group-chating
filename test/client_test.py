import unittest
from unittest.mock import MagicMock, patch
from clients.client import OpenAIClient
from dotenv import load_dotenv
import os

class TestOpenAIClient(unittest.TestCase):
    @patch('clients.client.OpenAI')
    def setUp(self, mock_openai_class):
        # OpenAI의 인스턴스 모킹
        self.mock_openai_instance = MagicMock()
        mock_openai_class.return_value = self.mock_openai_instance

        # response 구조 모킹
        self.mock_openai_instance.responses.create.return_value.output_text = "Mock response"
        self.mock_openai_instance.models.retrieve.return_value = {"id": "gpt-4o", "status": "available"}

        self.client = OpenAIClient(api_key="TEST_API_KEY", model="gpt-4o")

    def test_repr(self):
        self.assertEqual(repr(self.client), "OpenAIClient(model=gpt-4o)")

    def test_str(self):
        self.assertEqual(str(self.client), "OpenAIClient with model gpt-4o")

    def test_generate_response(self):
        response = self.client.generate_response("Hello")
        print(response)
        self.assertEqual(response, "Mock response")
        self.mock_openai_instance.responses.create.assert_called_with(
            model="gpt-4o",
            input="Hello"
        )

    def test_get_model_info(self):
        info = self.client.get_model_info()
        self.assertEqual(info, {"id": "gpt-4o", "status": "available"})
        self.mock_openai_instance.models.retrieve.assert_called_with(model="gpt-4o")

    def test_set_model(self):
        self.client.set_model("gpt-4")
        self.assertEqual(self.client.get_model(), "gpt-4")
        self.assertEqual(self.client.model, "gpt-4")
        self.assertEqual(self.client.client.model, "gpt-4")

    def test_set_api_key(self):
        self.client.set_api_key("new_key")
        self.assertEqual(self.client.api_key, "new_key")
        self.assertEqual(self.client.client.api_key, "new_key")

class TestOpenAIClientReal(unittest.TestCase):
    def setUp(self):
        load_dotenv()
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY 환경 변수가 설정되지 않았습니다.")
        self.client = OpenAIClient(api_key=api_key, model="gpt-3.5-turbo")

    def test_generate_response_real(self):
        input_text = "Hello, how are you?"
        response = self.client.generate_response(input_text)
        print("🧪 실제 응답:", response)
        self.assertIsInstance(response, str)
        self.assertTrue(len(response) > 0)

if __name__ == "__main__":
    unittest.main()
