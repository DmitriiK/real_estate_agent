import uuid

from dotenv import load_dotenv

from google.adk.agents import BaseAgent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from src.agents.text2SQL.agent import root_agent


load_dotenv()

def run_agent(agent: BaseAgent, user_message: str,  initial_state: dict = None, app_name: str = 'test_app', user_id = 'test_user') -> None:
    # Create a new session service to store state
    session_service_stateful = InMemorySessionService()

    SESSION_ID = str(uuid.uuid4())
    stateful_session = session_service_stateful.create_session(
        app_name=app_name,
        user_id=user_id,
        session_id=SESSION_ID,
        state=initial_state,
    )
    print(f"CREATED NEW SESSION:{SESSION_ID=}")

    runner = Runner(
        agent=agent,
        app_name=app_name,
        session_service=session_service_stateful,
    )

    new_message = types.Content(
        role="user", parts=[types.Part(text=user_message)]
    )
    final_responses = []
    for event in runner.run(user_id=user_id, session_id=SESSION_ID, new_message=new_message, ):
        if event.is_final_response():
            if event.content and event.content.parts:
                final_responses.append(event.content.parts[0].text)

    session = session_service_stateful.get_session(app_name=app_name, user_id=user_id, session_id=SESSION_ID)
    return final_responses, session.state.items()

if __name__ == "__main__":
    agent = root_agent
    user_message = "what is the average price to rent something in Antalya?"
    initial_state = {
        "user_name": "Brandon Hancock",
    }
    final_responses, final_session_state = run_agent(agent, user_message, initial_state)
    print("Final Responses:")
    for response in final_responses:
        print(response)
