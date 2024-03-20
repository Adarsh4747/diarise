import os
from langchain.schema import HumanMessage
from langchain.chat_models import ChatOpenAI
import ast
import firebase_admin
from firebase_admin import credentials,firestore


cred = credentials.Certificate("serviceAccount.json")
firebase_admin.initialize_app(cred) 
db=firestore.client()

def chat(diri):
    data2={"message":diri}
    list=db.collection("163675").document("diarization").get()
    if list.exists:  
        db.collection("163675").document("diarization").update(data2)
    else:
        db.collection("163675").document("diarization").set(data2)
    print("done")

def importing(id):
    list=db.collection("163675").document("history").get()
    if list.exists:  
        list=db.collection("163675").document("history").get()
        data=list.to_dict()
        return (data.get('2024-02-03', '').strip())
    else:
        return ("there was no period today")


def promptmaker(statement,date,time):
    instructions = f"""Your duty is to diarise a conversation between doctor and patient .
    you should accurately guess which statement is said by doctor and which one is said by the patient.
    you should return a diarised text which include details like date,time of visit ,reason of visit and then diarised summary.
    all this should be in a formal format.properly aligned.
    only include what is told by patient and doctor don't add anything extra or beautify the things told.
    todays date is {date}
    Time is {time}
    """
    question=f"diarise the {statement} in the order mentioned above."

    prompt = instructions+question

    return askgpt(prompt)

def askgpt(prompt):
    # print("etti")
    openai_api_key =os.environ.get('OPENAI_API_KEY')
    chat_model = ChatOpenAI(temperature=0, model='gpt-4', openai_api_key=openai_api_key,max_tokens=350)
    
    output = chat_model([HumanMessage(content=prompt)])
    response = output.content
    diarised_list = response.splitlines()
    return diarised_list


def start(date,time):
    statement=importing("163675")
    diri=promptmaker(statement,date,time)
    chat(diri)
