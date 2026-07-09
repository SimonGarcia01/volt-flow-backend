from fastapi import APIRouter, WebSocket, WebSocketDisconnect

router = APIRouter(prefix="/ocpp", tags=["ocpp"])

#Defines the websocket endpoint for OCPP communication with charge points
#Each charge point will connect using it's id
@router.websocket("/{charge_point_id}")
async def ocpp_endpoint(websocket: WebSocket, charge_point_id: str):
    #Accept the WebSocket connection
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            # Here you can handle the received OCPP message
            print(f"Received from {charge_point_id}: {data}")
            # You can also send a response back to the charge point if needed
            await websocket.send_text(f"Message received: {data}")
    except WebSocketDisconnect:
        print(f"Charge point {charge_point_id} disconnected")