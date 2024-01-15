import uvicorn
from fastapi import FastAPI, Request


app = FastAPI()


@app.get('/')
async def root(request: Request):
    print(await request.body())
    return {'hella': 'black'}

if __name__ == "__main__":
    uvicorn.run('main:app', port=8000, host='127.0.0.1', reload=True)
