from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/aa")
def hello():
    return "hello"




if __name__ == "__main__":
    uvicorn.run("main:app", port=8000)