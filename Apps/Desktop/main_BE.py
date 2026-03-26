import asyncio
import uvicorn
import threading

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from scripts.webrtc import _webrtc_init

fapi_app = FastAPI(info=True)
fapi_app.add_middleware( # allows any connections - very indev
    CORSMiddleware,
    allow_origins=["*"],         
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@fapi_app.get("/ping")
async def fapi_ping(request:Request):
    return JSONResponse({"Message":"Success"}, status_code=200)

def _run_webrtc():
    asyncio.run(_webrtc_init())

if __name__ == "__main__":
    threading.Thread(target=_run_webrtc).start()
    uvicorn.run(fapi_app, host="0.0.0.0",)