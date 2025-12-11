import unittest
from unittest.mock import patch, MagicMock
from aicron.llm import generate_cron

class TestLLMLogic(unittest.TestCase):
    
    @patch('aicron.llm.completion')
    def test_generate_cron_success(self, mock_completion):
        # Setup mock response
        mock_response = MagicMock()
        mock_response.choices[0].message.content = "0 8 * * *|每天早上 08:00 运行"
        mock_completion.return_value = mock_response

        # Test
        result = generate_cron("Every day at 8am")
        
        # Verify
        self.assertEqual(result, "0 8 * * *|每天早上 08:00 运行")
        mock_completion.assert_called_once()

    @patch('aicron.llm.completion')
    def test_generate_cron_markdown_cleanup(self, mock_completion):
        # Setup mock response with backticks (common LLM behavior)
        mock_response = MagicMock()
        mock_response.choices[0].message.content = "`0 0 * * *|Midnight`"
        mock_completion.return_value = mock_response

        # Test
        result = generate_cron("Midnight")
        
        # Verify (backticks should be stripped)
        self.assertEqual(result, "0 0 * * *|Midnight")

    @patch('aicron.llm.completion')
    def test_generate_cron_api_error(self, mock_completion):
        # Setup mock to raise exception
        mock_completion.side_effect = Exception("Connection refused")

        # Test
        result = generate_cron("Any prompt")
        
        # Verify error handling
        self.assertTrue(result.startswith("ERROR|LLM Call failed"))
        self.assertIn("Connection refused", result)

    def test_mock_mode_default(self):
        # Test the built-in mock mode logic
        result = generate_cron("something else", model="mock")
        self.assertEqual(result, "0 8 * * *|每天 08:00 运行 (Mock)")

    def test_mock_mode_midnight(self):
        # Test specific mock trigger
        result = generate_cron("run every day", model="mock")
        self.assertEqual(result, "0 0 * * *|每天午夜运行")

if __name__ == '__main__':
    unittest.main()
