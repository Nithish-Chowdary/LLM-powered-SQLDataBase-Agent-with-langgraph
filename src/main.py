from langchain_community.utilities import SQLDatabase

from src.PostgreSQL_DB.sql_Data import CreateDatabase
from src.LLM.models import chat_model
from src.tools.tools import SQLTools
from src.graph.nodes import Nodes
from src.graph.state import MessagesState
from src.graph.workflow import Workflow


def main(database_name, user, password, model_name):

    """
    TODO: need to fix model hallucination
    :param database_name:
    :param user:
    :param password:
    :param model_name:
    :return:
    """

    # Create database along with respective tables and insert data into those tables
    database = CreateDatabase(
        db_name=database_name,
        user=user,
        password=password
    )
    # create a database instance using langchain utilities
    db_connection_string = f"postgresql://{user}:{password}@localhost:5432/{database_name}"
    db = SQLDatabase.from_uri(db_connection_string)

    # get the llm model
    llm = chat_model(model_name=model_name)

    # SQLToolkit and needed tools
    tools = SQLTools(llm=llm,db=db)

    nodes = Nodes(llm=llm, tools=tools)

    graph = Workflow(nodes=nodes,tools=tools,llm=llm).app

    input_message = {"messages": [("user", "Average value of the orders?")]}
    for event in graph.stream(input_message):
        print(event)

if __name__ =="__main__":
    database_name = "mydb"
    user = "NithishChowdary1"
    model_name = "mistral"
    password=None
    main(database_name,user,password,model_name)






