from flow.chat_flow import Flow
from flow.rag_flow import RagFlow
from agents import multi_agent_init

agents = multi_agent_init()
rag_flow = RagFlow()


chat_flow = Flow(
    agents,
    user_input="""
아, 제가 너무 피곤해서 병원에 갔는데, 한쪽에서는 장 문제라고 하고
한쪽에서는 전신적인 문제라고 하네요.
눈의 피로도 상당할 거라고 하구요.
                 
이런 경우에는 어떻게 해야 하나요?
""",
)

turn_logs = chat_flow.run()
chats = [turn_logs[0][0]["content"]]

for c in turn_logs[1:]:
    chats.append(c[0])

response = rag_flow.run("\n".join(chats))


print("최종")
print("=" * 20, "최종 응답", "=" * 20)
print(response)
