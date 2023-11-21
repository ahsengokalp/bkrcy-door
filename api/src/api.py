from db import rd
from app import app
from error import Error


@app.route("/", methods=["GET"])
# how to use page
async def home():
    go_to_login_page_button = "<a href='/login'>Go to login page</a>"
    return f"<h1>usage: /user, /user/{{uid}}, /login</h1>{go_to_login_page_button}"


@app.route("/user", methods=["GET"])
# how to use page
async def user():
    return "<h1>usage: /user/{uid}</h1>"


@app.route("/user/<uid>", methods=["GET"])
# getting full user info by id
async def get_user(uid):
    id = f"user:{uid}"
    if await rd.exists(id):
        return await rd.hgetall(id)
    raise Error(f"User {uid} not found")


from asgiref.wsgi import WsgiToAsgi

asgi_app = WsgiToAsgi(app)