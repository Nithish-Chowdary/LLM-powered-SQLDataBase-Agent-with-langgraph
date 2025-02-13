from IPython.display import Image, display
from langchain_core.runnables.graph import MermaidDrawMethod

from langgraph.graph import StateGraph
from langgraph.graph.graph import START, END

from src.graph.state import  MessagesState



class Workflow:

    def __init__(self, nodes, tools, llm):
        self.nodes = nodes
        self.tools = tools
        self.llm = llm
        workflow = StateGraph(MessagesState)

        workflow.add_node("first_tool_call", self.nodes.first_tool_message)
        workflow.add_node("list_tables_tool", self.nodes.create_tool_node([self.tools.list_sql_database_tool]))
        workflow.add_node("get_schema_tool", self.nodes.create_tool_node([self.tools.schema_sql_database_tool]))
        workflow.add_node("model_get_schema", self.nodes.model_get_schema)
        workflow.add_node("query_gen", self.nodes.gen_query)
        workflow.add_node("correct_query", self.nodes.check_query)
        workflow.add_node("execute_query", self.nodes.create_tool_node([self.tools.db_query_tool]))

        workflow.add_edge(START, "first_tool_call")
        workflow.add_edge("first_tool_call", "list_tables_tool")
        workflow.add_edge("list_tables_tool", "model_get_schema")
        workflow.add_edge("model_get_schema", "get_schema_tool")
        workflow.add_edge("get_schema_tool", "query_gen")
        workflow.add_conditional_edges("query_gen", self.nodes.should_continue,
                                       {
                                           END:END,
                                           "query_gen":"query_gen",
                                           "correct_query":"correct_query"
                                       })
        workflow.add_edge("correct_query", "execute_query")
        workflow.add_edge("execute_query", "query_gen")

        self.app = workflow.compile()
