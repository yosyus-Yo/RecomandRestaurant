from dotenv import load_dotenv
import os
from openai import OpenAI
import time
import json
import urlscrap
load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key = API_KEY)
function_tools = [{
    "type": "function",
    "function": {
        "name": "Search_Restaurant",
        "description": "음식점 리스트를 가져오는 함수",
        "parameters": {
            "type": "object",
            "properties": {
                "input" : {"type": "string", "description": "사용자가 찾고자하는 음식점 키워드 for examples 불고기, 인천 근처 맛집, 저녁 음식, 점심 음식, 아침 음식, 맛집"}
            },
            "required" : ["input"]
        }
    }
},
{
    "type": "function",
    "function": {
        "name": "get_restaurant_url_selenium",
        "description": "음식점 리뷰를 가져오는 함수",
        "parameters": {
            "type": "object",
            "properties": {
                "input" : {"type": "string", "description": "사용자가 찾고자하는 음식점 키워드 for examples 전주가마솥곰탕 운정점, 성심당, 꾸아 파주운정점"}
            },
            "required" : ["input"]
        }
    }
}]
# #assistant 생성
assistants_id = "asst_XlzRhT9dRIrYMINYBIJw4NKT"
def assistant_create():
    a = open('./Searchrestaurant.txt', 'r')
    assistant = client.beta.assistants.create(
        name="Searchrestaurant",
        instructions=a.read(),
        tools=function_tools,
        model="gpt-3.5-turbo-1106"
    )
    return assistant
assistants = client.beta.assistants.list(
    order="desc",
    limit="20",
)
if assistants.data[0].id != assistants_id:
    assistant = assistant_create()
else:
    assistant = assistants.data[0]

def wait_on_run(run):
    while run.status == "queued" or run.status == "in_progress":
            run = client.beta.threads.runs.retrieve(
                thread_id=thread_id,
                run_id=run.id,
            )
            
            time.sleep(0.5)    
    return run
    
#thread 생성
# thread = client.beta.threads.create()
thread_id = "thread_bDQEv6EN3yPxSVbpwilgKqXU"
print(thread_id)
# response = client.beta.threads.delete(thread_id)

def run_cancel(thread_id):
    run = client.beta.threads.runs.list(
        thread_id=thread_id
    )
    for data in run.data:
        if (data.status == "requires_action" or data.status == "queued" or data.status == "in_progress"):
            run = data
            run = client.beta.threads.runs.cancel(
            thread_id=thread_id,
            run_id=run.id,
            )
        print(data.status)
def thread_message():
    thread_messages = client.beta.threads.messages.list(thread_id)
    return thread_messages
    
#msg_f7MmkNqk7FsgSeSaDMidMZDO
def startMessage(inputC):
    run_cancel(thread_id)
    InputChat = inputC
    if InputChat:
        message = client.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=InputChat
        )
        print(InputChat)
        run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistants_id,
        )
        data = []
        run = wait_on_run(run)
        print("런 상태 : ", run.status)
        if run.status == "requires_action":
            print("requires_action들어옴")
            tool_call = run.required_action.submit_tool_outputs.tool_calls[0]
            arguments = json.loads(tool_call.function.arguments)
            print(arguments)
            
            try :
                task, data = urlscrap.Search_Restaurant(**arguments)
                print(data)
                print(task)
            except TypeError: 
                print("해당사항 없음")
                task = "해당사항 없음"
            
            run = client.beta.threads.runs.submit_tool_outputs(
                thread_id=thread_id,
                run_id=run.id,
                tool_outputs=[
                    {
                        "tool_call_id": tool_call.id,
                        "output": str(task)
                    }
                ],)
            run = wait_on_run(run)
        print("requires_action에서 나옴")
        messages = client.beta.threads.messages.list(
            thread_id=thread_id
        )
        print("다 끝나감")
        print("런 상태 : " , run.status)
        return messages.data[0].content[0].text.value, data

        
    
    #git 추가

# inputC = input("입력 : ")
# print(startMessage(inputC))