# Project: LLM Powered SQL DataBase Agent with Langgraph

## Overview
This project allows querying a PostgreSQL database using a language model of choice. It creates the necessary database and tables, retrieves data, and responds to user queries.

## Requirements
- Python 3.11+
- PostgreSQL
- `requirements.txt` for Python dependencies

## Installation

1. **Set Up Virtual Environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up PostgreSQL Database:**
   Create a PostgreSQL database with the appropriate credentials.

## Environment Variables
Create a `.env` file with the following variables:

```env
DB_NAME=
DB_USER=
DB_PASSWORD=
CHAT_MODEL_NAME="mistral"
```

## Running the Project
1. **Load Environment Variables:** Ensure the `.env` file is in the project directory.
2. **Run the Main Script:**
   ```bash
   python main.py
   ```

## Code Explanation
- **Environment Variables:** Loaded using `dotenv`.
- **Database Connection:** A PostgreSQL connection string is created based on the environment variables.
- **Model Usage:** ChatLlama Mistral is used for generating responses to database queries.

## Functions
### `main(database_name, user, password, model_name)`
- Creates a PostgreSQL database if it doesn’t exist.
- Establishes a connection using `SQLDatabase`.
- Loads the chat model using the specified model name.
- Sets up the necessary tools and nodes.
- Streams user queries to the workflow graph for responses.

=

