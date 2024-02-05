from langchain_openai import ChatOpenAI
from langchain.tools.render import format_tool_to_openai_function
import openai
from langchain.agents.output_parsers import OpenAIFunctionsAgentOutputParser
from langchain.agents.format_scratchpad import format_to_openai_functions
from langchain.tools import tool
from pydantic import BaseModel, Field
import urlscrap
from langchain_core import utils
from langchain.prompts import ChatPromptTemplate
from langchain.schema.agent import AgentFinish
from langchain.prompts import MessagesPlaceholder
from langchain.schema.runnable import RunnablePassthrough
from langchain.agents import AgentExecutor
from langchain.memory import ConversationBufferMemory
import os
from dotenv import load_dotenv
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

class GlobalState:
    _instance = None
    _state = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(GlobalState, cls).__new__(cls)
        return cls._instance

    @classmethod
    def set_state(cls, key, value):
        cls._state[key] = value

    @classmethod
    def get_state(cls, key):
        return cls._state.get(key)

    @classmethod
    def clear_state(cls, key):
        if key in cls._state:
            del cls._state[key]

# Rest of the code remains unchanged
class RestaurantSearch(BaseModel):
    """Enter a restaurant or pasta shop in the area you're looking for and you'll see a list of restaurants and their locations."""
    Restaurnat_Search: str = Field(description="""Enter keywords that represent nearby restaurants or a specific restaurant. 
                                    If you want users to enter an address and get directions to a specific restaurant, enter the address that the user entered as the keyword. """)
    Search_flag : str = Field(description="""defalutable flag = 0.
                                If the user wants to find multiple restaurants, set flag = 1.
                                If the user wants to find a specific restaurant, set flag = 2.
                                If you want users to enter an address and get directions to a specific restaurant, then set Flag = 3.""")

Restaurant_function = utils.function_calling.convert_to_openai_function(RestaurantSearch)

@tool("search-tool",args_schema=RestaurantSearch)
def Search(Restaurnat_Search : str, Search_flag : str) -> str:
    """Search for restaurants in the area."""
    checkmarker_info = GlobalState.get_state("unique_state_key")
    if checkmarker_info:
        checkmarker = checkmarker_info.get("checkmarker")
    global pathData, flag
    restaurantData, pathData, flag = urlscrap.Search_Restaurant(Restaurnat_Search, Search_flag, checkmarker)
    return restaurantData, pathData

def run_agent(user_input):
    intermediate_steps = []
    while True:
        result = agent_chain.invoke({
            "input": user_input, 
            "intermediate_steps": intermediate_steps
        })
        if isinstance(result, AgentFinish):
            return result
        tool = {
            "search-tool": Search
        }[result.tool]
        observation = tool.run(result.tool_input)
        intermediate_steps.append((result, observation))

tools = [Search]
function = [utils.function_calling.convert_to_openai_function(Search)]
model = ChatOpenAI(temperature=0).bind(functions=function)

prompt = ChatPromptTemplate.from_messages([
    ("system", """You're the helpful but cheeky sidekick. 
        If a user wants a list of restaurants, you just show them the name and address. 
        If they want a specific restaurant, you show them the restaurant's information, links to information, and number of reviews. 
        If they want all the blog reviews, you show them all the blog reviews. If they want more information, you organize it."""),
    MessagesPlaceholder(variable_name="chat_history"),
    ("user", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad")
])

chain = prompt | model | OpenAIFunctionsAgentOutputParser() 
agent_chain = RunnablePassthrough.assign(
    agent_scratchpad= lambda x: format_to_openai_functions(x["intermediate_steps"])
) | prompt | model | OpenAIFunctionsAgentOutputParser()
memory = ConversationBufferMemory(return_messages=True,memory_key="chat_history")

agent_executor = AgentExecutor(agent=agent_chain, tools=tools, verbose=True, memory=memory)
def Output(input, checkmarker = []):
    state_key = "unique_state_key"
    GlobalState.set_state(state_key, {"checkmarker": checkmarker})
    output = agent_executor.invoke({"input" : input})
    GlobalState.clear_state(state_key)
    print(output)
    if flag == "3":
        print(pathData)
    return output['output'], pathData, flag