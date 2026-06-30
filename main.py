#----------IMPORTS---------------------------------------------
#--------------------------------------------------------------
from fastapi import FastAPI,Request,Form
from database import students_collection,client
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from typing import List,Optional
from fastapi.staticfiles import StaticFiles

#--------------------------------------------------------------
#----------VARIABLES-------------------------------------------
#--------------------------------------------------------------
app=FastAPI()
templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")
# browser sends to GET /static/style.css but FastAPI doesn't know static so, to let it understand it, we mount the css file in main.py
# This is like telling FastAPI:
# Whenever someone asks for something starting with /static, don't look in my routes. Instead, go inside my static folder.


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
    password: str = Form(...), #required
    course: Optional[str] = Form(None), #not required
    branch: Optional[str] = Form(None),
    city: Optional[str] = Form(None),
    semester: Optional[int] = Form(None),
    status: Optional[str] = Form(None),
    role: str = Form(...)
):
    student = {
        "name": name,
        "age": age,
        "email": email,
        "password":password,
        "course":course,
        "branch":branch,
        "city":city,
        "semester":semester,
        "status":status,
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
def delete_all(req: Request,confirm: Optional[str] = Form(None)):
    # confirm=confirm.upper()
    if confirm=="DeLeTe":
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
            "message_delete_all": "Type DeLeTe to confirm."
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
                "message_delete_some": "Please select at least one student."
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

#------------------------------------------------------------
#----------127.0.0.1:8000/delete-page------------------------
#------------------------------------------------------------
# @app.get("/delete-page")
# def delete_page(req: Request):
#     students = list(
#         students_collection.find(
#             {"role": "Student"},
#             {"_id": 0, "email": 1}
#         )
#     )
#     return templates.TemplateResponse(
#         request=req,
#         name="delete.html",
#         context={
#             "request": req,
#             "students": students
#         }
#     )







#------------------------------------------------------------
#----------127.0.0.1:8000/update-all------------------------
#------------------------------------------------------------
@app.post("/update-all")
def update_all(
    req: Request,
    field: str = Form(...),
    value: str = Form(...)
):
    allowed_fields = [
        "name",
        "age",
        "course",
        "branch",
        "semester",
        "city",
        "status"
    ]

    if field not in allowed_fields:
        return {"message_field": "Invalid field selected."}
    
    if field in ["age", "semester"]:
        value = int(value)
    
    filter_query = {}
    new_values = {
        "$set": {field:value}
    }
    # {{$set:{"semester":3}}
    result = students_collection.update_many(filter_query, new_values)
    students = list(students_collection.find().sort("_id", -1))

    return templates.TemplateResponse(
        request=req,
        name="admin.html",
        context={
            "request": req,
            "students": students,
            "message_update_all": "Students updated successfully.",
            "matched_all": result.matched_count,
            "modified_all": result.modified_count
        }
    )




#------------------------------------------------------------
#----------127.0.0.1:8000/update-some------------------------
#------------------------------------------------------------
@app.post("/update-some")
def update_some(
    req: Request,
    emails: Optional[List[str]] = Form(None),
    field: str = Form(...),
    value: str = Form(...)
):
    allowed_fields = [
        "name",
        "age",
        "course",
        "branch",
        "semester",
        "city",
        "status"
    ]
    if field not in allowed_fields:
        return {"message": "Invalid field selected."}
    if field in ["age", "semester"]:
        value = int(value)
    if not emails:
        students = list(students_collection.find().sort("_id", -1))
        return templates.TemplateResponse(
            request=req,
            name="admin.html",
            context={
                "request": req,
                "students": students,
                "message_update_some": "Please select at least one student."
            }
        )
    result = students_collection.update_many(
        {"email": {"$in": emails}},{
            "$set": {
                field: value}})
    students = list(students_collection.find().sort("_id", -1))
    return templates.TemplateResponse(
        request=req,
        name="admin.html",
        context={
            "request": req,
            "students": students,
            "message_update_some": "Students updated successfully.",
            "matched_some": result.matched_count,
            "modified_some": result.modified_count
        }
    )

#------------------------------------------------------------
#----------127.0.0.1:8000/update-one------------------------
#------------------------------------------------------------
@app.post("/update-one")
def update_one(
    req: Request,
    emails: Optional[List[str]] = Form(None),
    field: str = Form(...),
    value: str = Form(...)
):
    allowed_fields = [
        "name",
        "age",
        "course",
        "branch",
        "semester",
        "city",
        "status"
    ]
    if field not in allowed_fields:
        return {"message": "Invalid field selected."}
    if field in ["age", "semester"]:
        value = int(value)
    if not emails:
        students = list(students_collection.find().sort("_id", -1))
        return templates.TemplateResponse(
            request=req,
            name="admin.html",
            context={
                "request": req,
                "students": students,
                "message_update_one": "Please select at least one student."
            }
        )
    result = students_collection.update_many(
        {"email": {"$in": emails}},{
            "$set": {
                field: value}})
    students = list(students_collection.find().sort("_id", -1))
    return templates.TemplateResponse(
        request=req,
        name="admin.html",
        context={
            "request": req,
            "students": students,
            "message_update_one": "Students updated successfully.",
            "matched_one": result.matched_count,
            "modified_one": result.modified_count
        }
    )



# #------------------------------------------------------------
# #----------127.0.0.1:8000/update-one------------------------
# #------------------------------------------------------------
# @app.post("/update-one")
# def update_one_student(
#     req: Request,
#     field: str = Form(...),
#     value: str = Form(...)
# ):
#     allowed_fields = [
#         "name",
#         "age",
#         "course",
#         "branch",
#         "semester",
#         "city",
#         "status"
#     ]

#     if field not in allowed_fields:
#         return {"message_field": "Invalid field selected."}
    
#     if field in ["age", "semester"]:
#         value = int(value)
    
#     filter_query = {}
#     new_values = {
#         "$set": {field:value}
#     }
#     result = students_collection.update_one(filter_query, new_values)
#     students = list(students_collection.find().sort("_id", -1))

#     return templates.TemplateResponse(
#         request=req,
#         name="admin.html",
#         context={
#             "request": req,
#             "students": students,
#             "message_update": "Students updated successfully.",
#             "matched": result.matched_count,
#             "modified": result.modified_count
#         }
#     )

#------------------------------------------------------------
#----------127.0.0.1:8000/update-one------------------------
#------------------------------------------------------------



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