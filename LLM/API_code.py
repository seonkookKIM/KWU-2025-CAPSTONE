import openai
import json
import os

# API 키 설정
client = openai.OpenAI(api_key="sk-xx")  # OpenAI 클라이언트 객체 생성

# 장소 정보 입력 받기
place_info = {
    "기계실": {"X": -30, "Y": 23, "Z": 0},
    "전시공간": {"X": -14, "Y": 23, "Z": 0},
    "회의실": {"X": 14, "Y": 23, "Z": 0},
    "창고": {"X": 42, "Y": 23, "Z": 0},
    "비상대피실": {"X": 69, "Y": 23, "Z": 0},
    "중앙광장": {"X": 49, "Y": 0, "Z": 0},
    "휴게실": {"X": 68, "Y": -24, "Z": 0},
    "화장실": {"X": 43, "Y": -24, "Z": 0},
    "놀이방": {"X": 13, "Y": -24, "Z": 0},
    "안내데스크": {"X": -14, "Y": -24, "Z": 0},
    "보안실": {"X": -30, "Y": -24, "Z": 0}
}

# Prompt Engineering (raw string을 사용하여 이스케이프 문제 방지)
prompt = """
사용자가 제공하는 문장에서 '대상 정보', '특징 정보', '추가 정보'를 파악하여 JSON 형식으로 정리해야 한다.
또한 대상 정보와 특징 정보 그리고 추가 정보를 고려하여 제시된 장소의 합리적인 우선순위를 매기고, 그것도 JSON으로 함께 제공한다.

대상 정보: 예) 어린이, 치매 환자, 특정 사람  
특징 정보: 예) 옷, 옷의 색상, 모자, 신발 등  
추가 정보: 예) '목이 마르다', '사람이 없는 곳을 좋아한다' 등 이때 추가 정보에 따라 강하게 반영된다.

이 3가지 정보를 기반으로 장소들의 우선순위를 추론할 때 다음과 같은 기준들을 고려하여 합리적인 우선 순위를 정한다.
목적: 이 장소가 어떤 목적에 적합한지 (예: 업무, 여행, 쇼핑, 학습 등)
중요도: 장소의 중요성이나 필요성 (예: 필수 방문, 권장 방문, 선택적 방문)
접근성: 장소로 가는 데 드는 시간, 거리 등
특징: 특정 장소의 특성 (예: 음식, 경치, 시설 등)
사용자 선호도: 장소와 관련된 특정 조건이나 선호도 (예: 조용함, 사람 많음 등)
상황: 현재 상황이나 조건에 따라 우선순위가 달라질 수 있음 (예: 날씨, 시간, 개인적 필요 등)

장소: {place_info}  
장소마다 이름과 좌표가 포함되어 있으며, 우선순위를 매길 때 아래 형식으로 반환한다.  
"priority": [["장소이름", [x, y]], ...]  
(예: [["화장실", [0, 2]], ["식당", [0, -5]]])  
확률이 적더라도 장소 전체를 다 순위를 매긴다.

장소별 우선순위 선택 이유도 "reason"에 따로 저장해둔다.
여기서 선택 이유는 최대한 길게 논리정연하게 만들어서 각 장소별로 이유까지 저장한다.
저장 시에는 장소 : 이유 와 같은 형태이다.
우선순위에 대한 근거 확률은 다음과 같은 베이지안 변형 공식을 따른다.
베이지안 변형 공식:
P(L_i | C, T) = (P(C | L_i, T) * P(L_i | T)) / Σ_j P(C | L_j, T) * P(L_j | T)
공식에 정규화를 적용하여 몇 %인지 "data"에 저장한다.
사용자 입력: "{content}"
결과는 아래 형식이다.
```json
{{
"content_input" : "",
"target_info": "",
"feature_info": "",
"extra_info": "",
"priority": [],
"reason": "",
"data": ""
}}
"""
# 사용자 입력 예시
content = input("명령 입력 : ")
#content = "흰색 모자와 노란색 운동화를 신은 어린아이를 찾아줘 목이 말라보였어"

# 프롬프트에 변수 포맷팅 적용
formatted_prompt = prompt.format(place_info=place_info, content=content)

# ChatGPT 호출
response = client.chat.completions.create(
    model="gpt-4o",  # GPT-4o 모델 사용
    messages=[{"role": "system", "content": "You are an assistant who helps with identifying and prioritizing tasks based on the given data."},
              {"role": "user", "content": formatted_prompt}]
)

# 결과 파싱
result_text = response.choices[0].message.content

# JSON 블록 추출
json_str = result_text.split("```json")[1].split("```")[0].strip()
data = json.loads(json_str)

# 변수로 저장
content_input = data["content_input"]
target_info = data["target_info"]
feature_info = data["feature_info"]
extra_info = data["extra_info"]
priority_places = data["priority"]
reason = data["reason"]
data = data["data"]

# 출력 확인
print(target_info)
print(feature_info)
print(extra_info)
print("우선순위 목록:", priority_places)
print(reason)
print(data)

streamlit_data = []
for place, coord in priority_places:
    percent_str = data.get(place, "0%")
    percent_float = float(percent_str.replace("%", ""))
    streamlit_data.append({
        "명령": content_input,
        "장소": place,
        "좌표": coord,
        "이유": reason.get(place, "이유 없음"),
        "확률": percent_str,
        "확률(%)": percent_float
    })

with open("priority_data.json", "w", encoding="utf-8") as f:
    json.dump(streamlit_data, f, ensure_ascii=False, indent=2)

print("priority_data.json 저장 완료 (Streamlit 대시보드용)")
