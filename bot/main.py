from fastapi import BackgroundTasks, FastAPI, Request, Response
from bot.handlers.handler_config import bot
from bot.handlers import commands_handler, events_handler
from bot.api.api_requests import UserAPIRequest
from bot.utils.redis_utils import add_new_users
from requests.exceptions import ConnectionError
from time import sleep


app = FastAPI()
wallets_api = UserAPIRequest()
confirmation_code: str
secret: str


@app.on_event("startup")
async def startup():
    global confirmation_code, secret
    while True:
        try:
            users, status = wallets_api.get_users()
            break
        except ConnectionError:
            print("cannot get to API server. retry...")
            sleep(2)
    if status == 200:
        for u in users:
            add_new_users(u["id"])
    confirmation_code, secret = bot.setup_bot()


@app.on_event("shutdown")
async def shutdown():
    pass


@app.post("/")
async def index(request: Request, background_task: BackgroundTasks):

    try:
        data = await request.json()
    except:
        return Response("not today", status_code=403)

    if data["type"] == "confirmation":
        return Response(confirmation_code)

    # If the secrets match, then the message definitely came from our bot
    if data["secret"] == secret:
        # Running the process in the background, because the logic can be complicated
        background_task.add_task(bot.handle_events, data)

    return Response("ok")
