from fastapi import FastAPI,HTTPException

app = FastAPI()

database={
    1:{"name":"arjav","age":19,"cgpa":9},
    2:{"name":"aryan","age":22,"cgpa":2},
    3:{"name":"yug","age":20,"cgpa":8}
}

@app.get("/error/{student_id}")
def get_student(student_id:int):
    if student_id not in database:
        raise HTTPException(
            status_code=404
        )
        

    profile = database[student_id]

    return{
        "name":profile["name"],
        "cgpa":profile["cgpa"]
    }

