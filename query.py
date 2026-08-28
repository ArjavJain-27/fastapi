from fastapi import FastAPI

app = FastAPI()

database = [
    
    {"id":1,"city":"indore","risk":"low"},
    {"id":2,"city":"delhi","risk":"high"},
    {"id":3,"city":"goa","risk":"low"},
    {"id":4,"city":"mumbai","risk":"high"},
    {"id":5,"city":"chennai","risk":"low"},
]

@app.get("/data")
def get_data(city:str,risk:str):
    data = [
        d for d in database # d for d is list comprehension
        if d["city"]==city and d["risk"]==risk 
    ]

    return{
        "city":city,
        "risk":risk,
        "count":len(data)
    }
