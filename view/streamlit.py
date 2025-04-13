import streamlit as st
import asyncio
import nest_asyncio
from agents import multi_agent_init
from flow.chat_flow import Flow

nest_asyncio.apply()  # 이미 실행 중인 이벤트 루프에 중첩 실행 허용

async def run_chat_flow(user_input, agents):
    chat_flow = Flow(agents, user_input=user_input)
    chat_flow.run()  # Flow 실행
    return chat_flow

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
                chat_flow = asyncio.run(run_chat_flow(user_input, agents))

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
                        if isinstance(message, dict) and 'role' in message and 'content' in message:
                            color = role_colors.get(message['role'], "#000000")
                            st.markdown(f"""
                                <div style="border: 1px solid {color}; border-radius: 8px; padding: 10px; margin-bottom: 6px;">
                                    <strong style="color: {color};">{message['role']}</strong><br/>
                                    <span>{message['content']}</span>
                                </div>
                            """, unsafe_allow_html=True)
                        else:
                            st.write(str(message))
                elif isinstance(turn, dict) and 'role' in turn and 'content' in turn:
                    color = role_colors.get(turn['role'], "#000000")
                    st.markdown(f"""
                        <div style="border: 1px solid {color}; border-radius: 8px; padding: 10px; margin-bottom: 6px;">
                            <strong style="color: {color};">{turn['role']}</strong><br/>
                            <span>{turn['content']}</span>
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    st.write(str(turn))
        else:
            st.error("입력을 제공해 주세요.")

if __name__ == "__main__":
    main()