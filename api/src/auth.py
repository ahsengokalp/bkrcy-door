from app import (
    app,
    LoginManager,
    UserMixin,
    redirect,
    url_for,
    request,
    login_user,
    logout_user,
    login_required,
    check_password_hash,
    generate_password_hash,
    render_template_string,
    current_user,
)
from db import rd
from secrets import token_hex
import asyncio

app.secret_key = token_hex(16)

login_menager = LoginManager()
login_menager.init_app(app)


class User(UserMixin):
    def __init__(self, id, password):
        self.id = id
        self.password = password

    async def get(id):
        passw = await rd.hget(f"account:{id}", "password")
        return User(id, passw)


@login_menager.user_loader
def user_loader(id):
    return User(id, asyncio.run(User.get(id)))


@app.route("/login", methods=["GET"])
async def login():
    # create simple login page with button and form
    page = """
    <form action="/login" method="POST">
        <input type="text" name="id">
        <input type="password" name="password">
        <input type="submit" value="login">
    </form>
    """
    return page


@app.post("/login")
async def login_post():
    id = request.form["id"]
    user = await User.get(id=id)

    if user is None or not check_password_hash(user.password, request.form["password"]):
        return redirect(url_for("login"))

    login_user(user)
    return redirect(url_for("protected"))


@app.route("/protected")
@login_required
def protected():
    return render_template_string("Logged in as: {{ user.id }}", user=current_user)


@app.route("/logout")
def logout():
    logout_user()
    return "Logged out"
