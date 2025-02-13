from src.graph.state import MessagesState

from langchain_core.messages import AIMessage, HumanMessage, ToolMessage
from langgraph.prebuilt import ToolNode
from langchain_core.runnables import RunnableLambda
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langgraph.graph import END

class Nodes:

    def __init__(self, llm, tools):
        self.llm = llm
        self.tools = tools

    def first_tool_message(self, state:MessagesState):
        messages = state["messages"]
        return {
            **state,
            "messages": [AIMessage(content="", tool_calls=[{"name":"list_sql_database_tool", "args":{},"id":"123"}])]}

    # def _handle_tool_errors(self, state:MessagesState):
    #     error = state.get("error")
    #     tool_calls = state["messages"][-1].tool_calls
    #     return {
    #         "messages": []
    #     }
    def create_tool_node(self, tools:list):
        return ToolNode(tools, handle_tool_errors=True)

    def gen_query(self, state:MessagesState):
        generate_query = self._generate_query()
        messages = generate_query.invoke(state)
        tool_messages = []
        if messages.tool_calls:
            for tc in messages.tool_calls:
                if tc["name"] != "SubmitFinalAnswer":
                    tool_messages.append(
                        ToolMessage(
                            content=f"The wrong tool was called: {tc['name']}. Please fix your mistakes. Remember to only call SubmitFinalAnswer to submit the final answer. Generated queries should be outputted WITHOUT a tool call.",
                            tool_call_id = tc["id"],
                        )
                    )
        else:
            tool_messages = []
        return {
            **state,
            "messages": [messages]+tool_messages}

    def check_query(self, state:MessagesState):
        messages = state["messages"]
        check_query = self._correct_query()
        return {
            **state,
            "messages": [check_query.invoke({"messages": [state["messages"][-1]]})]}

    def model_get_schema(self, state:MessagesState):
        messages = state["messages"]
        schema = self._get_schema()
        return {
            **state,
            "messages": [schema.invoke(messages)]}


    def should_continue(self, state:MessagesState):
        messages = state["messages"]
        last_message = messages[-1]
        if getattr(last_message, "tool_calls", None):
            return END
        elif last_message.content.startswith("Error"):
            return "query_gen"
        else:
            return "correct_query"



    def _generate_query(self):

        system_prompt = """
        You are a SQL expert with a strong attention to detail.Given an input question, output a syntactically correct SQLite query to run, then look at the results of the query and return the answer.
        DO NOT call any tool besides SubmitFinalAnswer to submit the final answer.
        When generating the query:

        Output the SQL query that answers the input question without a tool call.

        Unless the user specifies a specific number of examples they wish to obtain, always limit your query to at most 5 results.
        You can order the results by a relevant column to return the most interesting examples in the database.
        Never query for all the columns from a specific table, only ask for the relevant columns given the question.

        If you get an error while executing a query, rewrite the query and try again.

        If you get an empty result set, you should try to rewrite the query to get a non-empty result set.
        NEVER make stuff up if you don't have enough information to answer the query... just say you don't have enough information.

        If you have enough information to answer the input question, simply invoke the appropriate tool to submit the final answer to the user.

        DO NOT make any DML statements (INSERT, UPDATE, DELETE, DROP etc.) to the database. Do not return any sql query except answer."""

        generate_query_prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("placeholder","{messages}" )
        ])

        query_gen = generate_query_prompt | self.llm.bind_tools([self.tools.submit_final_answer])

        return query_gen


    def _correct_query(self):

        system_prompt = """
        You are a SQL expert with a strong attention to detail.
        Double check the SQLite query for common mistakes, including:
        - Using NOT IN with NULL values
        - Using UNION when UNION ALL should have been used
        - Using BETWEEN for exclusive ranges
        - Data type mismatch in predicates
        - Properly quoting identifiers
        - Using the correct number of arguments for functions
        - Casting to the correct data type
        - Using the proper columns for joins
        
        If there are any of the above mistakes, rewrite the query. If there are no mistakes, just reproduce the original query.
        
        You will call the appropriate tool to execute the query after running this check."""

        check_query_prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("placeholder", "{messages}")
        ])

        query_check = check_query_prompt | self.llm.bind_tools([self.tools.db_query_tool])

        return query_check

    def _get_schema(self):
        schema = self.llm.bind_tools([self.tools.schema_sql_database_tool])
        return schema

