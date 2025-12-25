
import os
import sys
from llm import LLMClient, GROQ_API_URL

def test_config():
    # Test 1: Defaults
    # Clean env for the test
    if 'LLM_BASE_URL' in os.environ:
        del os.environ['LLM_BASE_URL']
    if 'LLM_API_KEY' in os.environ:
        del os.environ['LLM_API_KEY']
        
    client = LLMClient()
    print(f"Test 1 (Defaults): Base URL: {client.base_url}")
    assert client.base_url == GROQ_API_URL, "Default base URL should be Groq"

    # Test 2: Env Var Override
    test_url = "http://localhost:11434/v1/chat/completions"
    os.environ['LLM_BASE_URL'] = test_url
    client = LLMClient()
    print(f"Test 2 (Env Override): Base URL: {client.base_url}")
    assert client.base_url == test_url, "Base URL should match env var"

    # Test 3: Constructor Override
    constructor_url = "https://api.openai.com/v1/chat/completions"
    client = LLMClient(base_url=constructor_url)
    print(f"Test 3 (Constructor Override): Base URL: {client.base_url}")
    assert client.base_url == constructor_url, "Base URL should match constructor arg"

    print("\n✅ All configuration tests passed!")

if __name__ == "__main__":
    test_config()
