import asyncio
import json
import websockets


async def handler(websocket, path):
    async for client in websocket:
        data = json.loads(str(client))
        msg = """
            <ul id="message-list"
                class="list-group w-100 mt-3 d-flex flex-column"
                style="height: 300px; overflow-y: auto"
                hx-swap-oob="beforeend">
                <li class="card mb-2">
                    <div class="card-body">{message}</div>
                </li>
            </ul>
        """.format(message=data['message'])
        await websocket.send(msg)

start_server = websockets.serve(handler, "localhost", 8765)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()