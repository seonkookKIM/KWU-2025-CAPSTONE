ui_code = '''
import os
import streamlit as st
import json

st.set_page_config(page_title="탐색 로봇 UI", layout="wide")

st.markdown("""
<style>
    .block-container {
        padding-top: 0rem;
        padding-bottom: 0rem;
        padding-left: 4rem;
        padding-right: 5rem
    }
    .main {
        padding-top: 0rem;
    }
    header, footer {
        visibility: hidden;
        height: 0;
    }
    .container {
        display: flex;
        height: 100vh;
    }
    .left {
        width: 60%;
        padding: 20px;
        border-right: 1px solid #ccc;
        overflow: hidden; 
    }
    .right {
        width: 40%;
        padding: 20px;
        overflow-y: auto;  
        height: 100vh;
        margin-top: -13rem;
    }
    
</style>
""", unsafe_allow_html=True)
data = []
if os.path.exists("priority_data.json"):
    try:
        with open("priority_data.json", "r", encoding="utf-8") as f:
            loaded = json.load(f)
            if isinstance(loaded, list):
                data = loaded
    except Exception as e:
        st.warning(f"⚠️ JSON 파일 로딩 중 오류: {e}")
else:
    st.info("📭 데이터가 아직 없습니다. 대기 중입니다.")

# 좌우 분할 
left_col, right_col = st.columns([1.5, 1])  # 좌측 60%, 우측 40%

with left_col:
    st.markdown(
        """<div style='margin-top: 50px; border: 2px dashed gray; width: 698px; height: 393px; 
        display: flex; align-items: center; justify-content: center;
        font-size: 18px; color: #888; background-color: #f9f9f9;'>
        📷 여기에 실시간 카메라 영상이 표시됩니다</div>""",
        unsafe_allow_html=True
    )
with right_col:
    if data:
        user_command = data[0].get("명령", "명령 없음")
        st.markdown("<div style='margin-top: 0px;'>", unsafe_allow_html=True)
        st.subheader("장소 우선순위")
        st.markdown(f"<span style='font-size:17px;'><b>탐색 명령: </b> {user_command}</span>", unsafe_allow_html=True)
        st.markdown("추론된 우선순위에 대한 탐색 성공 확률과 장소별 이유 입니다.")
        
        for idx, item in enumerate(data, start=1):
            medal = "🥇" if idx == 1 else "🥈" if idx == 2 else "🥉" if idx == 3 else f"&nbsp;&nbsp;{idx}."
            st.markdown(f"""
            <div style='display: flex; align-items: center; gap: 10px;'>
                <div style='width: 30px; font-size: 18px; font-weight: bold;'>{medal}</div>
                <div style='min-width: 180px; font-weight: bold; font-size: 18px;'>{item['장소']}</div>
                <div style='min-width: 40px; text-align: right; font-weight: bold; color: black;'>{item['확률']}</div>
                <div style='flex: 1;'>
                    <progress value='{item['확률(%)']}' max='100' style='width: 100%; height: 18px;'></progress>
                </div>
            </div>
            """, unsafe_allow_html=True)

        with st.expander("📖 장소별 이유 보기 (AI 기반 분석 결과)"):
            for idx, item in enumerate(data, start=1):
                st.markdown(f"""
                <div style='margin-bottom: 5px;'>
                    <p style='font-weight: bold; font-size: 15px;'>{idx}. {item['장소']}</p>
                    <p style='margin-left: 10px; font-size: 14px; color: #333;'>• {item['이유']}</p>
                    <hr style='border: 0.5px solid #eee;' />
                </div>
                """, unsafe_allow_html=True)
    else:
        st.subheader("📡 장소 우선순위를 불러오는 중...")
        st.markdown("탐색 명령이 들어오면 자동으로 동기화됩니다.")
'''

with open("test.py", "w", encoding="utf-8") as f:
    f.write(ui_code)

print("test.py 저장 완료")
