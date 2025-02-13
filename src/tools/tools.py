from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_core.tools import tool

from src.tools.utils import run_no_throw, SubmitFinalAnswer



class SQLTools:

    def __init__(self, llm, db ):
        self.toolkit = SQLDatabaseToolkit(db=db,llm=llm)
        # Get all available tools from the toolkit
        self.tools = {tool.name: tool for tool in self.toolkit.get_tools()}

    def query_sql_database_tool(self):
        """
        Retrieve the tool to execute SQL queries.

        Returns:
            Tool: The tool for querying the SQL database.
        """
        return self.tools.get("sql_db_query", None)

    def schema_sql_database_tool(self):
        """
        Retrieve the tool to get information about the SQL database.

        Returns:
            Tool: The tool for retrieving info about the SQL database.
        """
        return self.tools.get("sql_db_schema", None)

    def list_sql_database_tool(self):
        """
        Retrieve the tool to list the available tables in the database.

        Returns:
            Tool: The tool for listing tables in the SQL database.
        """
        return self.tools.get("sql_db_list_tables", None)

    def query_sql_checker_tool(self):
        """
        Retrieve the tool to check SQL query validity.

        Returns:
            Tool: The tool for validating SQL queries.
        """
        return self.tools.get("sql_db_query_checker", None)


    @tool()
    def db_query_tool(self,db,  query:str):
        """
        Executes a SQL query against the database and returns the result,

        :param query: query to perform the SQL search
        :return:  if the query is invalid or returns no result, an error message will be returned.
        in case of error, the user is advised to rewrite the query
        """
        result = db.run_no_throw(query)
        if not result:
            return "Error: Query failed. Please rewrtie the query and try again."
        return result

    def submit_final_answer(self):
        SubmitFinalAnswer()


