from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import google.auth
import google.oauth2.id_token
from google.auth.transport import requests
from google.cloud import firestore
import constants


app = FastAPI()

app.mount("/public", StaticFiles(directory="public"), name="public")
templets = Jinja2Templates(directory="templates")

firestore_db = firestore.Client()
firebase_request_adapter = requests.Request()


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    id_token = request.cookies.get("token")
    user_token = None
    user_token = validateFirebaseToken(id_token)

    if not user_token:
        return templets.TemplateResponse(
            "index.html",
            {
                "request": request,
                "user_token": None,
            },
        )
    
    createUser(user_token)

    if user_token['email'] == constants.admin:
        users = firestore_db.collection("users").get()
        return templets.TemplateResponse(
            "admin.html",
            {   "request": request,
                "user_token": user_token,
                "users" : users
            }
    )

    return templets.TemplateResponse(
        "index.html",
        {   "request": request,
            "user_token": user_token,
        }
    )


def validateFirebaseToken(id_token):
    if not id_token:
        return None
    user_token = None
    try:
        user_token = google.oauth2.id_token.verify_firebase_token(
            id_token, firebase_request_adapter
        )
    except ValueError as err:
        print(str(err))
    return user_token


def createUser(user_token):
    print("Fetching user")
    user = firestore_db.collection("users").document(user_token["user_id"]).get()
    print("User", user)
    if not user.exists:
        firestore_db.collection("users").document(user_token["user_id"]).create(
            {
                "id": user_token["user_id"],
                "email": user_token["email"],
            }
        )
        print("Writing user")


@app.get("/login", response_class=HTMLResponse)
def login( req:Request ):

    id_token = req.cookies.get("token")
    user_token = None
    user_token = validateFirebaseToken(id_token)

    if not user_token:
        return templets.TemplateResponse(
            "login.html",
            {
                "request": req,
                "user_token": None,
            },
        )
    
    return RedirectResponse("/")


@app.get("/signup", response_class=HTMLResponse)
def signup( req:Request ):

    id_token = req.cookies.get("token")
    user_token = None
    user_token = validateFirebaseToken(id_token)

    if not user_token:
        return templets.TemplateResponse(
            "signup.html",
            {
                "request": req,
                "user_token": None,
            },
        )
    
    return RedirectResponse("/")





# $Env:GOOGLE_APPLICATION_CREDENTIALS="key.json"
