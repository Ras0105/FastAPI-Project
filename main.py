#----------IMPORTS---------------------------------------------
#--------------------------------------------------------------
from fastapi import FastAPI,Request,Form
from database import students_collection,client
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from typing import List,Optional

#--------------------------------------------------------------
#----------VARIABLES-------------------------------------------
#--------------------------------------------------------------
app=FastAPI()
templates = Jinja2Templates(directory="templates")





#--------------------------------------------------------------
#----------LOGIC-----------------------------------------------
#--------------------------------------------------------------



#--------------------------------------------------------------
#----------127.0.0.1:8000/-------------------------------------
#--------------------------------------------------------------
@app.get("/")
def home(req: Request):
    return templates.TemplateResponse(
        request=req,
        name="login.html",
    )


#--------------------------------------------------------------
#----------Login Page------------------------------------------
#--------------------------------------------------------------
@app.get("/login")
def login(request: Request, error: int = 0):

    message = ""
    if error == 1:
        message = "Wrong email or password"

    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={
            "request": request,
            "message": message
        }
    )

@app.post("/student-login")
def student_login(
    req: Request,
    email: str = Form(...),
    password: str = Form(...),
    role: str = Form(...)
):
    # User pressed login without entering anything
    if email.strip() == "" or password.strip() == "":
        return RedirectResponse(
    url="/login",
    status_code=303
)

    result = students_collection.find_one({
        "email": email,
        "password": password,
        "role":role
    })

    # Correct Login
    if result:
        if role=="Student":
            return RedirectResponse(
                url="/student-page",
                status_code=303
            )
        elif role=="Admin":
            return RedirectResponse(
                url="/admin-page",
                status_code=303
            )

    # Wrong Login
    return RedirectResponse(
        url="/login?error=1",
        status_code=303
    )


#--------------------------------------------------------------
#----------STUDENT PAGE-------------------------------------------
#--------------------------------------------------------------
@app.get("/student-page")
def home(req: Request):
    return templates.TemplateResponse(
        request=req,
        name="student.html"
    )

#--------------------------------------------------------------
#----------Admin Page-------------------------------------------
#--------------------------------------------------------------
@app.get("/admin-page")
def admin_page(req: Request):
    students = list(students_collection.find().sort("_id", -1))
    return templates.TemplateResponse(
        request=req,
        name="admin.html",
        context={
            "request": req,
            "students": students
        }
    )

#--------------------------------------------------------------
#----------127.0.0.1:8000/signup-student-----------------------
#--------------------------------------------------------------
@app.get("/signup-student")
def home(req: Request):
    return templates.TemplateResponse(
        request=req,
        name="signup.html"
    )
# signup.html will open

#--------------------------------------------------------------
#----------127.0.0.1:8000/create-student-----------------------
#--------------------------------------------------------------
@app.post("/create-student")
def create_student(
    name: str = Form(...),
    age: int = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    role: str = Form(...)
):
    student = {
        "name": name,
        "age": age,
        "email": email,
        "password":password,
        "role":role
    }

    students_collection.insert_one(student)

    return RedirectResponse(
        url="/",
        status_code=303
    )
# from signup.html's form create_student function will be called and the student will be created
# after creation it will be redirected to the login page, user can now login or change password, if forgotten
# http://127.0.0.1:8000/create-student

#--------------------------------------------------------------
#----------127.0.0.1:8000/update-password----------------------
#--------------------------------------------------------------
@app.get("/reset-password")
def reset_password(req:Request):
    return templates.TemplateResponse(
        request=req,
        name="forget.html"
    )

#--------------------------------------------------------------
#----------127.0.0.1:8000/update-password----------------------
#--------------------------------------------------------------
@app.post("/update-password")
def update_password(
    req: Request,
    email: str = Form(...),
    newpass: str = Form(...)
):
    filter_query={"email":email}
    update_query={"$set":{"password":newpass}}
    result=students_collection.update_one(filter_query,update_query)

    if result.matched_count == 0:
        message="Student not found"

    elif result.modified_count == 0:
        message="You Already Have Same Password"

    else:
        message="Password updated successfully"

    return templates.TemplateResponse(
    request=req,
    name="login.html",
    context={
        "request": req,
        "message": message
    }
)

#--------------------------------------------------------------
#----------127.0.0.1:8000/read-student-------------------------
#--------------------------------------------------------------
@app.get("/read-student")
def read_student(req: Request):
    users = list(students_collection.find().sort("_id",-1))

    return templates.TemplateResponse(
        request=req,
        name="read.html",
        context={
            "request": req,
            "students": users
        }
    )
# from admin.html page read-student will be shown-> read.html
# http://127.0.0.1:8000/read-student



#--------------------------------------------------------------
#----------127.0.0.1:8000/delete-all-------------------------
#--------------------------------------------------------------
@app.post("/delete-all")
def delete_all(req: Request,confirm: str = Form(...)):
    confirm=confirm.upper()
    if confirm=="DELETE":
        students_collection.delete_many({"role": "Student"})
        return RedirectResponse(
            url="/admin-page",
            status_code=303
        )

    students = list(students_collection.find().sort("_id", -1))

    return templates.TemplateResponse(
        request=req,
        name="admin.html",
        context={
            "request": req,
            "students": students,
            "message": "Type DELETE to confirm."
        }
    )
#------------------------------------------------------------
#----------127.0.0.1:8000/delete-some------------------------
#------------------------------------------------------------
from typing import List, Optional

@app.post("/delete-some")
def delete_some(
    req: Request,
    emails: Optional[List[str]] = Form(None)
):
    if not emails:

        students = list(students_collection.find().sort("_id", -1))

        return templates.TemplateResponse(
            request=req,
            name="admin.html",
            context={
                "request": req,
                "students": students,
                "message": "Please select at least one student."
            }
        )

    students_collection.delete_many({
        "role": "Student",
        "email": {
            "$in": emails
        }
    })

    return RedirectResponse(
        url="/admin-page",
        status_code=303
    )



@app.get("/delete-page")
def delete_page(req: Request):

    students = list(
        students_collection.find(
            {"role": "Student"},
            {"_id": 0, "email": 1}
        )
    )

    return templates.TemplateResponse(
        request=req,
        name="delete.html",
        context={
            "request": req,
            "students": students
        }
    )












# @app.post("/update-student")
# def update_student():
#     # filter_query = {
#     #     "email": "rasshi@gmail.com"
#     # }
#     # new_values = {
#     #     "$set": {
#     #         "name": "Rasshi Srivastav",
#     #         "age": 21
#     #     }
#     # }
#     # result = students_collection.update_one(filter_query, new_values)
#     result = students_collection.update_one(
#     {"email": "rasshi@gmail.com"},
#     {"$set": {"age": 21}}
#     )
#     if result.matched_count == 0:
#         return {"message": "Student not found"}

#     if result.modified_count == 0:
#         return {"message": "Student already has these values"}

#     return {"message": "Student updated successfully"}


# @app.post("/delete-student")
# def delete_user():
#     filter_query = {
#         "email": "khushi2@gmail.co"
#     }

#     result = students_collection.delete_one(filter_query)

#     if result.deleted_count == 1:
#         return {"message": "User Deleted Successfully"}

#     return {"message": "User Not Found"}






















# #workbench.browser.openLocalhostLinks