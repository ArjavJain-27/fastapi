from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

#pydantic model
class student(BaseModel):
    name: str
    age: int

#database
students = []

#post method to create a student
@app.post("/students")
def create_student(student: student):
    students.append(student)
    return {
        "data": student
    }


#get method to get all students
@app.get("/students")
def get_students(): 
    return {
        "data": students
    }

#get method to get a student by id
@app.get("/students/{student_id}")
def get_student(student_id: int):
    for student in students:
        if student["id"] == student_id:
            return {
                "data": students
            }

#put method to update a student
@app.put("/students/{student_id}")        
def update_student(student_id: int, updated_student: student):
    for student in students:
        if student["id"] == student_id:
            student["name"] = updated_student.name
            student["age"] = updated_student.age
            return {
                "data": student
            }

#delete method to delete a student    
@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    for student in students:
        if student["id"]== student_id:
            students.remove(student)
            return {
                "message": "Student deleted successfully"
            }