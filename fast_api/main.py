from fastapi import FastAPI
import uvicorn
from fastapi import Request

app = FastAPI()


@app.post('/')
async def read_root(request: Request):
    print(await request.json())
    return {'context': 'data'}


if __name__ == '__main__':
    uvicorn.run('main:app', port=8080, host='0.0.0.0', reload=True)
