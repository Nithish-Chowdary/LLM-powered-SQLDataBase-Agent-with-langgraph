from langchain_core.pydantic_v1 import BaseModel, Field

def run_no_throw(query, connection):
    """
    performs the search and returns a None if nothing to show
    :param query: query to be executed
    :param connection: connection to the SQL Database
    :return: Result from database if present else None
    """
    try:
        cursor = connection
        cursor.execute(query)
        return cursor.fetchall()
    except Exception as e:
        print(f"Error executing query:{e}")
        return None

class SubmitFinalAnswer(BaseModel):
    """Submit the final answer to the user based on the query results."""
    final_answer: str = Field(..., description="The final answer to the user")
