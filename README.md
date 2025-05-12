# Real Estate Agent AI Assistant

## Overview
This project is an AI-powered assistant designed for a real estate agency. The assistant helps potential buyers and renters find their ideal property by engaging them in a conversation. It gathers user preferences such as location, budget, property type, and other criteria, and provides relevant property options from the agency's database.

## Features
- **Interactive Conversations**: The assistant engages users in a natural language conversation to understand their preferences.
- **Property Search**: Supports filtering properties based on location, budget, property type, and other attributes.
- **SQL Query Generation**: Converts user queries into SQL statements to fetch data from the database.
- **Agent System**: Includes specialized agents for renting and sales processes.
- **Session Management**: Maintains session state to track user interactions and preferences.

## Project Structure
The project is organized as follows:

```
real_estate_agent/
├── pyproject.toml          # Project dependencies and metadata
├── README.md               # Project documentation
├── sql/                    # SQL scripts and views
│   ├── v_emlak_by_disticts.sql
│   └── v_emlak_data_mart.sql
├── src/                    # Source code
│   ├── settings.py         # Configuration settings
│   ├── utils/              # Utility functions
│   │   ├── utils.py
│   │   └── sql_communicator.py
│   ├── agents/             # AI agents
│   │   ├── receptionist/   # Receptionist agent
│   │   ├── text2SQL/       # Text-to-SQL agent
│   │   └── shared_agent_tools.py
│   ├── tests/              # Unit tests
│   │   ├── test_utils.py
│   │   ├── test_sql.py
│   │   └── test_agents.py
└── .vscode/                # VS Code settings
```

## Key Components

### Agents
- **Receptionist Agent**: Acts as the first point of contact for clients. Delegates tasks to specialized agents.
- **Rent Agent**: Assists clients in finding rental properties based on their preferences.
- **Sales Agent**: Handles payment calculations and provides detailed information about selected properties.
- **Text-to-SQL Agent**: Converts natural language queries into SQL statements for database interaction.

### Utilities
- **`utils.py`**: Contains helper functions like `make_json_serializable` and `safe_format`.
- **`sql_communicator.py`**: Handles database interactions using SQLAlchemy.

### SQL Views
- **`v_emlak_data_mart.sql`**: Defines a view for detailed property data.
- **`v_emlak_by_disticts.sql`**: Aggregates property data by districts.

### Tests
- Comprehensive unit tests are provided for utilities, SQL interactions, and agents.

## Setup

### Prerequisites
- Python 3.12 or higher
- PostgreSQL database

### Installation
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd real_estate_agent
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Configure the database connection in `src/settings.py`.

### Running the Application
1. Launch the web UI for agents:
 (this should be launched when you have src/agents as current folder)
   ```bash
   adk web
   ```
2. Interact with the agents through the web interface.

### Running Tests
Run unit tests using the following command:
```bash
python -m unittest discover -s ./src/tests -p "*test*.py"
```

## Usage
1. Start the receptionist agent to greet clients and determine their needs.
2. Use the rent agent to search for rental properties or the sales agent for payment calculations.
3. The agents interact with the database to fetch and present relevant property data.

## Contributing
1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Submit a pull request with a detailed description of your changes.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgments
- **Google ADK**: Used for building AI agents.
- **SQLAlchemy**: For database interactions.
- **SQLGlot**: For SQL parsing and validation.
- [**DEZC-FinalProject**](https://github.com/DmitriiK/DEZC-FinalProject): my DE project, where I have ETL for the population of DB.
## Known issues
 - search does not work for the words with specific Turkish symbols, like 'ş, ı'
 - payment agent for some reason provide data as json, not tabular, at least under Gemini
 ## Thought about further development
 - Add RAG semanitic search using vector fields in Postgres
 - Leverage geo data to search by distnanse to sea or whatever
 - Integrate to Telegram agent