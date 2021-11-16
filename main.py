import uvicorn
import socketio
from fastapi import FastAPI

from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import Response

from core.config import config
from core.orm import create_session
from core import logg

from api import restlin
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

# Initialize Logging configuration from config yaml loader
logg.init()
log = logg.use('api')

# FastAPI application setup
app = FastAPI()

templates = Jinja2Templates(directory="storage/views")

app.include_router(
    restlin.router,
    prefix='/api',
    tags=['Restlin']
)

app.add_middleware(CORSMiddleware,
                   allow_origins=['*'],
                   allow_methods=['*'],
                   allow_headers=['*'])


@app.middleware('http')
async def db_session_handler(request: Request, call_next):
    response = Response("Internal server error.", status_code=500)
    try:
        request.state.db = create_session()
        response = await call_next(request)
    except Exception as e:
        import traceback
        traceback.print_exc(50)
    finally:
        request.state.db.close()
    return response


@app.on_event('startup')
def startup_event():
    log.info("Starting app api")


# @app.get('/')
# def get_index():
#     return dict(name='Tower Defenders API',
#                 version='1.0',
#                  )
 
@app.get('/', response_class=HTMLResponse)
def get_index(request: Request):
    return templates.TemplateResponse("our-very-cool-custom-vue-client.html", {"request": request, "id": id})
 
 

if __name__ == '__main__':
    uvicorn.run("main:app", 
    	host='0.0.0.0', 
    	port=config.app.port, 
    	reload=config.app.hot_reload, 
    	debug=config.app.debug)

