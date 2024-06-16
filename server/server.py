import socket
import json
from commands import COMMANDS


def log(text: str, prefix: str = "Server") -> None:
    if text[0:7] == "Error: ":
        text = text[7:]
        prefix += " Error"

    if prefix:
        prefix = f"[{prefix}]"

    with open("history.log", "a") as f:
        f.write(f"{prefix}\n{text}\n")

    print(text)


def process_data(client_socket: socket.socket, data: str) -> str:
    if not data:
        return "Error: No data received."

    try:
        request = json.loads(data)
        cmd = request.get("cmd")
        args = request.get("args", [])

        if cmd not in COMMANDS:
            return f"Error: Command '{cmd}' not found."

        result = COMMANDS[cmd](args)
        return result
    except json.JSONDecodeError:
        return "Error: Invalid JSON format."


def start_server(host: str = "192.168.10.103", port: int = 5000) -> None:
    server_socket: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    log("", "")
    log(f"Server listening on {host}:{port}")

    client_socket, addr = server_socket.accept()
    log(f"Connection from {addr}")

    while True:
        data: str = client_socket.recv(4096).decode("utf-8")
        log(f"Request: {data}", "Client")

        result: str = process_data(client_socket, data)

        if '"cmd": "history", "args": []' in data:
            log("Sent history")
        else:
            log(f"{result}")

        if result == "STOP":
            client_socket.close()
            break

        response = json.dumps({"result": result})
        client_socket.sendall(response.encode("utf-8"))


if __name__ == "__main__":
    start_server()
