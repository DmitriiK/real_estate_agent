import unittest
import re

import sqlglot

from src.agents.agent_runner import run_agent
from src.agents.text2SQL.agent import root_agent as ag_t2s

class TestAgent(unittest.TestCase):

    def test_text2sql_agent(self):
        user_message = "what is the average price to rent something in Antalya?"
        final_responses, _ = run_agent(ag_t2s, user_message)
        sql_query = final_responses[0]
        # Strip out formatting like ```sql and ```, - I could not make llm model produce it without this formatting
        sql_query = re.sub(r"```.*?\n|```", "", sql_query) 
        print(sql_query)
        sqlglot.parse_one(sql_query, read="postgres")
        assert True

if __name__ == "__main__":
    unittest.main()