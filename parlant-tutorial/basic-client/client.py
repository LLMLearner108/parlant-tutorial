from parlant.client import ParlantClient

SERVER_ADDRESS="http://localhost:8800"
client = ParlantClient(base_url=SERVER_ADDRESS)

AGENT_ID = "ko8buqXQXE"
agent = client.agents.retrieve(AGENT_ID)

session = client.sessions.create(agent_id=AGENT_ID, allow_greeting=False)

while True:
     customer_message = input("Customer: ")

     if customer_message in ("quit", "bye", "exit", "cya l8r m8"):
         break

     customer_event = client.sessions.create_event(
         session_id=session.id,
         source="customer",
         kind="message",
         message=customer_message,
     )

     agent_event, *_ = client.sessions.list_events(
         session_id=session.id,
         source="ai_agent",
         kinds="message",
         min_offset=customer_event.offset,
     )

     # Let type-checker know we do have data here
     assert agent_event.data
     agent_message = agent_event.data["message"]

     print(f"Agent: {agent_message}")
