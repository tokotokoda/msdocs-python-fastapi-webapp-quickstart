from fastapi import FastAPI, Form, Request, status 
from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    print('Request for index page received')
    return templates.TemplateResponse('index.html', {"request": request, "result": None})

@app.post('/calculate', response_class=HTMLResponse)
async def calculate(
    request: Request,
    num1: float = Form(...),
    num2: float = Form(...),
    operation: str = Form(...)
):
    """四則演算を実行"""
    result = None
    error = None

    try:
        if operation == "add":
            result = num1 + num2
        elif operation == "subtract":
            result = num1 - num2
        elif operation == "multiply":
            result = num1 * num2
        elif operation == "divide":
            if num2 == 0:
                error = "ゼロで割ることはできません"
            else:
                result = num1 / num2
        else:
            error = "無効な操作です"
    except Exception as e:
        error = f"エラー: {str(e)}"

    return templates.TemplateResponse(
        'index.html', {"request": request, "result": result, "error": error}
    )

if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8000)
