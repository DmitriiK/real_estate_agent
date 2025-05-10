import unittest
from src.agents.agent_runner import run_agent
from src.agents.real_estate_agent.agent import root_agent

class TestAgent(unittest.TestCase):

    def test_get_agent_responce(self):
        user_message = "what is the average price to rent something in Antalya?"
        # initial_state = { "user_name": "Brandon Hancock",}
        final_responses, final_session_state = run_agent(root_agent, user_message)
        print(final_responses)
        assert True

if __name__ == "__main__":
    unittest.main()