from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
import uvicorn

# OpenAI API 키 설정 (당신의 키로 교체하세요!)
openai_api_key = ""

app = FastAPI()

client = OpenAI(api_key = openai_api_key)

# CORS 설정
origins = ["http://localhost:3000"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TextRequest(BaseModel):
    text: str

@app.post("/spellcheck")
def spellcheck(req: TextRequest):
    prompt = f"다음 문장의 맞춤법과 문장을 자연스럽게 교정해줘:\n\n{req.text}"

    try:
        response = client.chat.completions.create(
            model="gpt-4",  # 필요하면 gpt-4로 변경 가능
            messages=[
                {"role": "system", "content": "당신은 한국어 문장을 교정해주는 전문가입니다."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2
        )
        corrected_text = response.choices[0].message.content.strip()
        return {"corrected_text": corrected_text}
    except Exception as e:
        return {"corrected_text": f"오류 발생: {str(e)}"}

if __name__ == "__main__":
    uvicorn.run("backend2:app", host="localhost", port=7000, reload=True)


