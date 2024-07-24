from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import google.auth
import google.oauth2.id_token
from google.auth.transport import requests
from google.cloud import firestore
import constants
import starlette.status as status
from datetime import datetime


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
    testimonials = firestore_db.collection("testimonials").get()
    subscriptions = firestore_db.collection("subscriptions").get()

    if not user_token:
        return templets.TemplateResponse(
            "index.html",
            {
                "request": request,
                "user_token": None,
                "testimonials" : testimonials,
                "subscriptions" : subscriptions
            },
        )
    
    createUser(user_token)


    if user_token['email'] == constants.admin:
        users = firestore_db.collection("users").get()
        return templets.TemplateResponse(
            "admin.html",
            {   "request": request,
                "user_token": user_token,
                "users" : users,
                "testimonials" : testimonials,
                "subscriptions" : subscriptions
            }
    )

    return templets.TemplateResponse(
        "index.html",
        {   "request": request,
            "user_token": user_token,
            "testimonials" : testimonials,
            "subscriptions" : subscriptions
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
    user = firestore_db.collection("users").document(user_token["user_id"]).get()
    if not user.exists:
        firestore_db.collection("users").document(user_token["user_id"]).create(
            {
                "id": user_token["user_id"],
                "email": user_token["email"],
            }
        )


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


@app.post("/add-testimonial", response_class=RedirectResponse)
async def addTestimonial( req: Request ):
    id_token = req.cookies.get("token")
    user_token = None
    user_token = validateFirebaseToken(id_token)

    if not user_token:
        return RedirectResponse("/", status_code=status.HTTP_302_FOUND)
    
    form = await req.form()
    firestore_db.collection("testimonials").document().set({
        "name" : form["name"],
        "testimonial" : form["testimonial"],
        "created" : datetime.now()
    })

    return RedirectResponse("/", status_code=status.HTTP_302_FOUND)

@app.get("/remove-testimonial/{id}", response_class=RedirectResponse)
async def addTestimonial( req: Request, id:str ):
    id_token = req.cookies.get("token")
    user_token = None
    user_token = validateFirebaseToken(id_token)

    if not user_token:
        return RedirectResponse("/", status_code=status.HTTP_302_FOUND)
    
    testimonial = firestore_db.collection("testimonials").document(id)
    if testimonial.get().exists:
        testimonial.delete()

    return RedirectResponse("/", status_code=status.HTTP_302_FOUND)

# $Env:GOOGLE_APPLICATION_CREDENTIALS="key.json"
