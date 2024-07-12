"""
@Project :tool
@File    :socket_t.py
@IDE     :PyCharm
@Author  :xiaoj
@Date    :2024/7/3 11:54
"""
import asyncio
import detect
import glob
import json
import os
import take_photo
import conf

client_writer = None
async def handle_client(reader, writer):
    addr = writer.get_extra_info('peername')
    print(f"Connection from {addr}")

    while True:
        data = await reader.read(100)
        if not data:
            break
        message = data.decode()
        print(f"Received {message} from {addr}")
        await handle_message(message, writer)

    print("Closing the connection")
    writer.close()
    await writer.wait_closed()

async def handle_message(message, writer):
    if message == "connect":
        print("set client_writer")
        await sendMessageToClient(writer,"test", "success")
    elif message == "take_photo":
        postions = take_photo.get_current_flowers_info()
        json_string = json.dumps(postions)
        await sendMessageToClient(writer,"pollination",json_string)

async def sendMessageToClient(writer,type,message):
    m = {"type":type,"data":message}
    json_string = json.dumps(m)
    writer.write(json_string.encode())
    await writer.drain()  # Ensure the message is sent

async def process_images():
    img_dir = conf.img_dir
    save_dir = conf.save_dir
    print("Image processing started")
    while True:
       pass


async def main():
    server = await asyncio.start_server(handle_client, '192.168.1.117', 8888)
    addr = server.sockets[0].getsockname()
    print(f'Serving on {addr}')

    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())

