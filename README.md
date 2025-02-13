# Project: LLM Powered SQL DataBase Agent with Langgraph

## Overview
This project allows querying a PostgreSQL database using a language model of choice. It creates the necessary database and tables, retrieves data, and responds to user queries.

## Requirements
- Python 3.11+
- PostgreSQL
- `requirements.txt` for Python dependencies

## Installation

# LLM-Powered SQL Database Agent with LangChain and LangGraph

## Project Overview
This project is an LLM-powered SQL Database Agent that uses LangChain and LangGraph to dynamically interact with PostgreSQL databases. It allows users to generate and execute SQL queries using natural language commands, powered by the Chatollama Mistral model.

## Features
- **Natural Language to SQL Conversion:** Automatically generates SQL queries from natural language inputs.
- **Dynamic Database Exploration:** Explores database schemas to provide more accurate queries.
- **Multi-Step Reasoning:** Uses multi-step reasoning for SQL data fetching and validation.

## Prerequisites
1. **Python:** Ensure Python 3.11.10 is installed.
2. **PostgreSQL:** Set up a PostgreSQL database instance.

## Installation
1. Clone the repository:
   ```bash
   git clone git@github.com:Nithish-Chowdary/LLM-powered-SQLDataBase-Agent-with-langgraph.git
   cd LLM-powered-SQLDataBase-Agent-with-langgraph
   ```
2. Create a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install the required Python libraries:
   ```bash
   pip install -r requirements.txt
   ```

## Database Setup
1. Create a PostgreSQL database.
2. Configure the following environment variables for the database connection:
   - `DB_USER`: Your PostgreSQL username.
   - `DB_PASSWORD`: Your PostgreSQL password.
   - `DB_NAME`: The name of the PostgreSQL database.


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

