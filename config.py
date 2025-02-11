import os
from dotenv import load_dotenv

# LLM.env 파일을 로드합니다.
load_dotenv("LLM.env")

# OpenAI API 키를 환경변수에서 불러오는 함수
def get_openai_api_key():
    return os.getenv('OPENAI_API_KEY')
