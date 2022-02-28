from typing import List

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pymongo import MongoClient
from bson.objectid import ObjectId
import uvicorn
import base64
import json
import random
import logging, platform
import time
import io
from starlette.responses import StreamingResponse
import socket
from starlette.middleware.cors import CORSMiddleware


app = FastAPI()
#if __name__ == "__main__":
#    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="info")

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="views")


logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.DEBUG)

# Setting up connection with MongoDB
client = MongoClient("mongodb://localhost:27017/")
database = client["feedbackLoop"]
# database's table which stores the user votes.
feedback_collection = database["feedback"] 
# database's table which stores the loop settings.
loop_collection = database["loops"] 
# database's table which stores the question group settings.
questionGroup_collection = database["questionGroup"] 
# database's table which stores the question settings.
question_collection = database["question"] 

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


manager = ConnectionManager()

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    print(response)
    return response

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
     allow_methods=["DELETE", "GET", "POST", "PUT"],
    allow_headers=["*"],
)

#loads all the settings linked to one loop
@app.get("/fill/{loopId}")
async def fill(loopId: str, request: Request):
    return loopId

#receiving data through url payload
@app.get("/track")
async def returnPixel(request: Request):
    gif = 'R0lGODlhAQABAIAAAP///////yH5BAEKAAEALAAAAAABAAEAAAICTAEAOw=='
    gif_str = base64.b64decode(gif)
    logging.info("Action Tracked")
    host_name = socket.gethostname()
    host_ip = socket.gethostbyname(host_name)
    print("Hostname :  ",host_name)
    print("IP : ",host_ip)
    return StreamingResponse(io.BytesIO(gif_str), media_type="image/gif")


#receiving data through url payload
@app.get("/⚡/{dataStr}")
#@app.websocket("/receive/{dataStream}")
async def receiveDataStream(dataStr: str, request: Request):

    logging.info('receiving data stream: '+str(dataStr))

    template = {'isLightning':0, 'isError':0,'isAlert':0,'isUpdate':0,'model':[],'errors':[], 'info':[]}
    dataStr_base64_decode = ""
    dataStr_to_json = ""
    user_account = {
        "name":"roman.medioni",
        "GGI": 1#random.randint(0, 9999)
    }

    try:
        dataStr_base64_decode = base64.b64decode(dataStr)
        dataStr_to_json = json.loads(dataStr_base64_decode)
        
        #loop on all the elements posted via the base64 object, should be 1 or 2 
        #since it does not make sense to be able to simultaneously send an input for more than 2 dimensions
        #unless we want to leverage this call when filling answers via the web browser, in its form shape
        for dataStrObject in dataStr_to_json:

            questionModel = {}
            #Extract the datamodel id and the value that it should be linked to
            questionId = dataStrObject['feedbackLoop_question_id']
            value = dataStrObject['feedbackLoop_question_value']

            #get the data model based on the id retrieved above
            questionModel = question_collection.find_one({"_id": ObjectId(questionId)})
            #if data model is found, we are ready for the insertion if value is in line with model
            if bool(questionModel):
                #check if value sent is an authorized value
                if value in questionModel['data_values'][0]['values']:
                    #if value authorized, last check is to look at potentially existing values for a known user
                    print("value authorized")
                    #checking if feedback existing for this datamodel and user
                    feedback = feedback_collection.find_one({"questionId":ObjectId(questionId),"user":user_account})
                    #a feedback element was found matching those criterias and ok to update
                    if bool(feedback):
                        #Feedback already exists
                        print(feedback)
                        if (questionModel['allow_change']):
                            #if allowed to update the value
                            #store a view of the object populated with the data model linked
                            feedback_populated = {}
                            pipeline = [
                                {'$lookup': {'from' : 'question','localField' : 'questionId', 'foreignField' : '_id', 'as' : 'question'}},
                                {'$unwind': '$question'},
                                {'$match':{'questionId' : ObjectId(questionId),"user":user_account, "_id":ObjectId(feedback['_id'])}}
                            ]
                            
                            #check if value submitted is the same
                            if feedback['value'] != value:
                                #value re-submitted is different
                                feedback_collection.find_one_and_update({"_id":ObjectId(feedback['_id'])},{"$set":{"value":value}})
                                for item in (feedback_collection.aggregate(pipeline)): feedback_populated = item
                                template['isUpdate'] = 1
                                feedback_populated['notification'] = {'label':'success','text':'Your feedback was updated from '+str(feedback['value'] )+' to '+str(value)}
                                template['model'].append(feedback_populated)
                                template['info'].append({'label':'success','text':'Your feedback was updated from '+str(feedback['value'] )+' to '+str(value)})
                            else:
                                #value re-submitted is the same
                                for item in (feedback_collection.aggregate(pipeline)): feedback_populated = item
                                #generate the template for the html
                                template['isAlert'] = 1
                                feedback_populated['notification'] = {'label':'info','text':'You already gave the same feedback: '+str(feedback['value'])}
                                template['model'].append(feedback_populated)
                                template['info'].append({'label':'info','text':'You already gave the same feedback: '+str(feedback['value'])})
                        else:
                            #change not allowed but potentially, multiple inserts are possible.
                            if (questionModel['allow_multiple']):
                                #feedback exists already but allow multiple is set to true >> what use case??
                                feedback_collection.insert_one(
                                    {
                                        'questionId':ObjectId(questionId),
                                        'value':value,
                                        'user':user_account
                                    }
                                )
                                template['isLightning'] = 1
                                template['info'].append({'label':'success','text':'Thank you for your vote (you can vote again if you want!)'})

                            else:
                                #store a view of the object populated with the data model linked
                                feedback_populated = {}
                                pipeline = [
                                    {'$lookup': {'from' : 'question','localField' : 'questionId', 'foreignField' : '_id', 'as' : 'question'}},
                                    {'$unwind': '$question'},
                                    {'$match':{'questionId' : ObjectId(questionId),"user":user_account, "_id":ObjectId(feedback['_id'])}}
                                ]
                                feedback_collection.find_one({"_id": ObjectId(questionId)})
                                for item in (feedback_collection.aggregate(pipeline)): feedback_populated = item
                                template['model'].append(feedback_populated)
                                template['isError'] = 1
                                template['errors'].append({'label':'warning','text':'You cannot vote more than once and updating your answer is not allowed'})
                    else:
                        #Feedback does not exist and data matches the model
                        feedback_collection.insert_one(
                            {
                                'questionId':ObjectId(questionId),
                                'value':value,
                                'user':user_account
                            }
                        )
                        template['isLightning'] = 1
                        template['info'].append({'label':'success','text':'Thank you for your vote!'})
                else: 
                    #value not allowed
                    template['isError'] = 1
                    template['errors'].append({'label':'warning','text':'Value '+ str(value) +' not allowed'})
            else:
                #data model cannot be found
                template['isError'] = 1
                template['errors'].append({'label':'warning','text':'Could not find dataset id '+questionId})
    except Exception as e:
        #error during the processing of the data stream
        template['isError'] = 1
        template['errors'].append({'label':'warning','text':'Seems like the data you are sending us is not in the right format'})

    return templates.TemplateResponse("receive.html", {"request": request, "template":template})

#user can get a live feed of the data_stream_id
@app.websocket("/feed/{data_stream_id}")
async def websocket_endpoint(websocket: WebSocket, data_stream_id: str):
    print(feedback_collection.count_documents({}))

    await manager.connect(websocket)
    await manager.broadcast(f"user like #"+str(feedback_collection.count_documents({})))
    try:
        while True:
            #DS:b43fSxO
            data = await websocket.receive_text()
            #collection.insert_one({'message':data})
            count = feedback_collection.count_documents({})
            print(count)
            #await manager.broadcast(f"Client #"+feedback_collection.count_documents({}))
            #await manager.send_personal_message(f"You wrote: {data}", websocket)
            #await manager.broadcast(f"Client #{data_stream_id} says: {count}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        #await manager.broadcast(f"Current count #{count}")


@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(f"You wrote: {data}", websocket)
            await manager.broadcast(f"Client #{client_id} says: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{client_id} left the chat")