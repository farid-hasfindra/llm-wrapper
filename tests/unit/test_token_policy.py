from app.llm.token_manager import TokenManager

def test_token_estimation():
    tm = TokenManager()
    text = "Hello world"
    # 11 chars / 4 ~ 2 tokens
    assert tm.estimate_tokens(text) == 2
