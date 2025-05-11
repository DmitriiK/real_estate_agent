import unittest
from src.agents.agent_runner import run_agent
from src.agents.text2SQL.agent import root_agent as ag_t2s

class TestAgent(unittest.TestCase):

    def test_text2sql_agent(self):
        user_message = "what is the average price to rent something in Antalya?"
        # initial_state = { "user_name": "Brandon Hancock",}
        final_responses, final_session_state = run_agent(ag_t2s, user_message)
        print(final_responses)
        assert True

if __name__ == "__main__":
    unittest.main()