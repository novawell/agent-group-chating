import streamlit as st
import asyncio
import nest_asyncio
import json
import re
from agents import multi_agent_init
from flow.chat_flow import Flow
from flow.rag_flow import RagFlow
from dotenv import load_dotenv

nest_asyncio.apply()  # 이미 실행 중인 이벤트 루프에 중첩 실행 허용
load_dotenv()

rag_flow = RagFlow()


def remove_markdown_code_block(text):
    pattern = r'^```(?:json|JSON)(.*?)```\s*$'
    match = re.search(pattern, text, re.DOTALL)
    
    if match:
        return match.group(1).strip()
    
    return text


async def run_chat_flow(user_input, agents):    
    chat_flow = Flow(agents, user_input=user_input)  # Flow 객체 생성
    turn_logs = chat_flow.run()  # Flow 실행

    chats = []
    for c in turn_logs:
        chats.append(str(c))
    response = rag_flow.run("\n".join(chats))

    return chat_flow, response


def main():
    st.title("AI 전문가 그룹 채팅")

    # 사용자 입력 받기
    user_input = st.text_area("상담 내용을 입력하세요:", height=150)

    # 에이전트 초기화
    agents = multi_agent_init()

    # 버튼 클릭 시 실행
    if st.button("대화 시작"):
        if user_input.strip():
            with st.spinner("대화를 진행 중입니다..."):
                # 이미 실행 중인 이벤트 루프를 사용
                chat_flow, recommend_response = asyncio.run(run_chat_flow(user_input, agents))
                
                # JSON 파싱 시도
                recommend_response = remove_markdown_code_block(recommend_response)

            st.write(f"Flow ID: {chat_flow.flow_id}")
            st.write(f"대화 상태: {chat_flow}")

            # 대화 내역 출력
            st.subheader("대화 내역")

            role_colors = {
                "user": "#0072C6",
                "eyes": "#2683ff",
                "liver": "#ff5722",
                "wholebody": "#9c27b0",
            }

            for turn in chat_flow.turn_log:
                if isinstance(turn, list):
                    for message in turn:
                        if isinstance(message, dict) and "role" in message and "content" in message:
                            color = role_colors.get(message["role"], "#000000")
                            st.markdown(
                                f"""
                                <div style="border: 1px solid {color}; border-radius: 8px; padding: 10px; margin-bottom: 6px;">
                                    <strong style="color: {color};">{message['role']}</strong><br/>
                                    <span>{message['content']}</span>
                                </div>
                            """,
                                unsafe_allow_html=True,
                            )
                        else:
                            st.write(str(message))
                elif isinstance(turn, dict) and "role" in turn and "content" in turn:
                    color = role_colors.get(turn["role"], "#000000")
                    st.markdown(
                        f"""
                        <div style="border: 1px solid {color}; border-radius: 8px; padding: 10px; margin-bottom: 6px;">
                            <strong style="color: {color};">{turn['role']}</strong><br/>
                            <span>{turn['content']}</span>
                        </div>
                    """,
                        unsafe_allow_html=True,
                    )
                else:
                    st.write(str(turn))

            # 최종 응답 출력
            st.subheader("최종 응답")
            
            # JSON 파싱 시도
            try:
                if isinstance(recommend_response, dict):
                    pass
                elif isinstance(recommend_response, str):
                    try:
                        recommend_response = json.loads(recommend_response)
                    except json.JSONDecodeError as e:
                        st.error(f"JSON 파싱 오류: {e}")

                elif hasattr(recommend_response, 'json'):
                    try:
                        recommend_response = recommend_response.json()
                    except Exception as e:
                        st.error(f"응답 파싱 오류: {e}")
                        
            except Exception as e:
                st.error(f"응답 처리 중 예외 발생: {e}")
            
            # 딕셔너리인지 확인 후 파싱
            if isinstance(recommend_response, dict):
                response_text = recommend_response.get("response", "")
                recommendations = recommend_response.get("recommendation", [])
                
                # 메인 응답 출력
                st.markdown(
                    f"""
                    <div style="border: 1px solid #1E88E5; border-radius: 8px; padding: 15px; margin-bottom: 20px; background-color: #E3F2FD;">
                        <strong style="color: #1E88E5; font-size: 18px;">AI 전문가 그룹의 최종 응답</strong><br/>
                        <span style="font-size: 16px;">{response_text}</span>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                
                # 추천 제품이 있는 경우만 표시
                if recommendations:
                    st.markdown("<strong style='font-size: 18px;'>💡 추천 제품</strong>", unsafe_allow_html=True)
                    
                    # 각 추천 제품을 카드 형태로 표시
                    for i, product in enumerate(recommendations):
                        product_name = product.get("product_name", "")
                        reason = product.get("reason", "")
                        
                        st.markdown(
                            f"""
                            <div style="border: 1px solid #4CAF50; border-radius: 8px; padding: 15px; margin-bottom: 15px; background-color: #F1F8E9;">
                                <strong style="color: #2E7D32; font-size: 17px;">✅ {product_name}</strong><br/>
                                <span style="font-size: 15px;">{reason}</span>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )
            else:
                # 딕셔너리가 아닌 경우 기존 방식으로 표시
                st.markdown(
                    f"""
                    <div style="border: 1px solid #000000; border-radius: 8px; padding: 10px; margin-bottom: 6px;">
                        <strong style="color: #000000;">AI 전문가 그룹의 최종 응답</strong><br/>
                        <span>{recommend_response}</span>
                    </div>
                """,
                    unsafe_allow_html=True,
                )

        else:
            st.error("입력을 제공해 주세요.")


if __name__ == "__main__":
    main()
