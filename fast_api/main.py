from fastapi import FastAPI
import uvicorn
from fastapi import Request

app = FastAPI()


@app.get('/')
def read_root(request: Request):
    print(request)
    return {'context': 'data'}


if __name__ == '__main__':
    uvicorn.run('main:app', port=8000, host='0.0.0.0', reload=True)
