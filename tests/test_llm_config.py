
import os
import sys
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent))

from _github.scripts.llm import LLMClient, GROQ_API_URL

def test_config():
    # Test 1: Defaults (assuming no env vars set for LLM_*)
    # Note: We need to be careful if the environment already has them, but for now we assume they don't or we unset them.
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
