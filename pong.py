import asyncio
import websockets

async def echo(websocket, path):
    client_ip = websocket.remote_address[0]
    # Получаем порт клиента
    client_port = websocket.remote_address[1]
    # Получаем информацию о подключении
    connection_info = websocket.remote_address
    # Получаем хост клиента
    client_host = websocket.host
    # Получаем заголовки запроса
    headers = websocket.request_headers

    print(f"New connection from {client_ip}:{client_port}")
    print(f"Connection info: {connection_info}")
    print(f"Client host: {client_host}")
    print(f"Request headers: {headers}")
    async for message in websocket:
        print(f"Received message: {message}")
        await websocket.send("ANSWER")

async def main():
    async with websockets.serve(echo, "0.0.0.0", 8081):
        await asyncio.Future() 

if __name__ == "__main__":
    asyncio.run(main())
