from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import HTMLResponse
from csp import generate
from model import Constraint, Course, CreateConstraint, CreateCourse
from fastapi import FastAPI
import uvicorn
import pyrebase
import collections
if not hasattr(collections, 'MutableMapping'):
    import collections.abc
    collections.MutableMapping = collections.abc.MutableMapping

# Firebase configuration (replace with your actual project settings)
firebaseConfig = {
 "apiKey": "AIzaSyDu8nKmsNz6v0ckh2yy1ypwemwfo7v2Z4I",

  "authDomain": "timetable-4db8f.firebaseapp.com",

  "projectId": "timetable-4db8f",

  "storageBucket": "timetable-4db8f.appspot.com",

  "messagingSenderId": "183909393981",

  "appId": "1:183909393981:web:3dcfca1f8a7c7efe90ac54",

  "measurementId": "G-07SD6KPX49",
  "databaseURL":"https://timetable-4db8f-default-rtdb.asia-southeast1.firebasedatabase.app/"

}

# Initialize Pyrebase
firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()

app = FastAPI()

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == '__main__':
    uvicorn.run("app:app", host="localhost", port=8080, reload=True)


@app.get("/get-courses")
async def get_courses():
    courses = db.child("courses").get()
    course_list = [Course(**course.val()) for course in courses.each()]
    return course_list


@app.get("/get-constraints")
async def get_constraints():
    constraints = db.child("constraints").get()
    constraint_list = [Constraint(**constraint.val()) for constraint in constraints.each()]
    return constraint_list


@app.post("/add-course", response_model=Course)
async def post_course(course: CreateCourse):
    document = course.dict()
    db.child("courses").push(document)  # Push data into Firebase
    return document


@app.post("/add-constraints", response_model=Constraint)
async def post_constraints(constraint: CreateConstraint):
    document = constraint.dict()
    db.child("constraints").push(document)
    return document


@app.get("/generate-timetable")
async def generate_timetable():
    constraints = db.child("constraints").get()
    constraint_list = [Constraint(**constraint.val()) for constraint in constraints.each()]
    
    courses = db.child("courses").get()
    course_list = [Course(**course.val()) for course in courses.each()]
    print("CourseS list",course_list)
    if not constraint_list or not course_list:
        return HTMLResponse(status_code=400)

    courses_dict = [item.dict() for item in course_list]
    print("course dic",constraint_list[-1].dict())
    data = generate(constraint_list[-1].dict(), courses_dict)
    print(data)
    print("above is data")
    return data
