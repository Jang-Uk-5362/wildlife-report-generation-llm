import openai
from fastapi import FastAPI, HTTPException
from config import get_openai_api_key

# OpenAI API 키 설정
openai.api_key = get_openai_api_key()

# FastAPI 인스턴스 생성
app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Welcome to FastAPI!"}

@app.get("/generate-report")
async def generate_report(
    latitude: float,
    longitude: float,
    animal_name: str,
    incident_time: str,
    responder: str,
    department: str,
    incident_details: str
):
    # 수정된 프롬프트 생성
    prompt = f"""
    다음 정보를 바탕으로 로드킬 보고서를 작성해 주세요:

    **도로교통공사 출동 보고서**

    **사건 발생 일시**: {incident_time}

    **위도, 경도**: {latitude}, {longitude}

    **출동 일시**: {incident_time}

    **소속 부서**: {department}

    **사건 내용**: {incident_details}

    **동물명**: {animal_name}

    **보고서 작성자**: {responder}
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150
        )
        return {"report": response["choices"][0]["message"]["content"]}
    
    except openai.error.OpenAIError as e:
        raise HTTPException(status_code=500, detail=f"OpenAI API Error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
