from fastapi import BackgroundTasks, FastAPI, Request, Response
from bot.handlers.handlers import bot


app = FastAPI()

confirmation_code: str
secret: str


@app.on_event("startup")
async def startup():
    global confirmation_code, secret
    confirmation_code, secret = bot.setup_bot()


@app.on_event("shutdown")
async def shutdown():
    pass


@app.post("/")
async def index(request: Request, background_task: BackgroundTasks):
    global confirmation_code, secret_key

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
