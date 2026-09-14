import asyncio
import json
import random
from datetime import datetime
from typing import List
from pydantic import BaseModel
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from src.card_calculator import CardCalculator

app = FastAPI(title="Nedap AEOS Monitor & Calculator")

class CalcRequest(BaseModel):
    calc_type: str
    value: str
    extra_val: str = ""

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            await connection.send_text(json.dumps(message))

manager = ConnectionManager()

async def simulate_card_events():
    event_types = ["Giris Basarili", "Tanimsiz Kart", "Yetkisiz Zorlama", "Kapi Acik Kaldi"]
    doors = ["Giris Turnike 1", "Ana Bina Bariyer", "Server Odasi", "Acil Cikis"]
    while True:
        await asyncio.sleep(4)
        event = {
            "door": random.choice(doors),
            "badge_id": f"0x{random.randint(10000000, 99999999):X}",
            "status": random.choice(event_types),
            "time": datetime.now().strftime("%H:%M:%S")
        }
        await manager.broadcast(event)

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(simulate_card_events())

@app.websocket("/ws/events")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)

@app.post("/api/calculate")
async def calculate_card(req: CalcRequest):
    try:
        if req.calc_type == "hex":
            return CardCalculator.from_hex(req.value)
        elif req.calc_type == "dec":
            return CardCalculator.from_dec(int(req.value))
        elif req.calc_type == "wiegand":
            fc = int(req.value)
            cn = int(req.extra_val)
            return CardCalculator.from_wiegand(fc, cn)
        return {"error": "Gecersiz tur"}
    except Exception as e:
        return {"error": str(e)}

@app.get("/")
async def get_dashboard():
    with open("src/templates/index.html", "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())
