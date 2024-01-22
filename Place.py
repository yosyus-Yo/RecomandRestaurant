from dotenv import load_dotenv
import os
from openai import OpenAI
import time
import json
load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key = API_KEY)
function_tools = [{
    "type": "function",
    "function": {
        "name": "get_restaurant_reviwes",
        "description": "항공편 검색",
        "parameters": {
            "type": "object",
            "properties": {
                "input" : {"type": "string", "description": "사용자가 찾고자하는 음식점 키워드 for examples 불고기, 인천 맛집, 저녁 음식, 점심 음식, 아침 음식"}
            },
            "required" : ["input"]
        }
    }
}]
# #assistant 생성
# assistants_id = "asst_PKvuiE7D3rQX9qPj2uPMLEAM"
def assistant_create():
    a = open('./Searchrestaurant.txt', 'r')
    assistant = client.beta.assistants.create(
        name="Searchrestaurant",
        instructions=a.read(),
        tools=function_tools,
        model="gpt-3.5-turbo-1106"
    )
    return assistant
# assistants = client.beta.assistants.list(
#     order="desc",
#     limit="20",
# )
# if not assistants.data:
#     assistant = assistant_create()
# else:
#     assistant = assistants.data[0]

# def wait_on_run(run):
#     while run.status == "queued" or run.status == "in_progress":
#             run = client.beta.threads.runs.retrieve(
#                 thread_id=thread_id,
#                 run_id=run.id,
#             )
            
#             time.sleep(0.5)    
#     return run
# # print(assistant)
    
# #thread 생성
# # thread = client.beta.threads.create()
# # print(thread)
# thread_id = "thread_QiN4bxeyIAlh0eraL7CL3CJ8"

# def run_cancel(thread_id):
#     run = client.beta.threads.runs.list(
#         thread_id=thread_id
#     )
#     if (run.data[0].status == "queued" or run.data[0].status == "in_progress"):
#         run = run.data[0]
#         run = client.beta.threads.runs.cancel(
#         thread_id=thread_id,
#         run_id=run.id,
#         )
# def thread_message():
#     thread_messages = client.beta.threads.messages.list(thread_id)
#     return thread_messages

# #msg_f7MmkNqk7FsgSeSaDMidMZDO
# def startMessage(inputC):
#     run_cancel(thread_id)
#     InputChat = inputC
#     if InputChat:
#         message = client.beta.threads.messages.create(
#             thread_id=thread_id,
#             role="user",
#             content=InputChat
#         )

#         run = client.beta.threads.runs.create(
#         thread_id=thread_id,
#         assistant_id=assistants_id,
#         )

#         run = wait_on_run(run)

#         if run.status == "requires_action":
#             print(run.required_action.submit_tool_outputs.tool_calls)
#             tool_call = run.required_action.submit_tool_outputs.tool_calls[0]
#             arguments = json.loads(tool_call.function.arguments)
#             print(arguments)
#             task = SerpAPI.search_flights(**arguments)
            
#             run = client.beta.threads.runs.submit_tool_outputs(
#                 thread_id=thread_id,
#                 run_id=run.id,
#                 tool_outputs=[
#                     {
#                         "tool_call_id": tool_call.id,
#                         "output": str(task)
#                     }
#                 ],
#             )
#             run = wait_on_run(run)
#         messages = client.beta.threads.messages.list(
#             thread_id=thread_id
#         )
#         return messages.data[0].content[0].text.value
    
#     #git 추가