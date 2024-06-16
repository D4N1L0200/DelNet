import socket
import json


def send_command(client_socket, command, arguments=[]) -> str:
    request = {"cmd": command, "args": arguments}
    client_socket.sendall(json.dumps(request).encode("utf-8"))
    response = client_socket.recv(4096).decode("utf-8")

    try:
        result = json.loads(response)
        return result.get("result", "Error: No result found.")
    except json.JSONDecodeError:
        return "Error: Invalid response format."


if __name__ == "__main__":
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(("192.168.10.103", 5000))

    while True:
        try:
            command = input("> ")
        except EOFError:
            break

        if not command:
            continue

        if command == "stop":
            break

        parts = command.split()
        cmd = parts[0]
        args = parts[1:]
        result = send_command(client_socket, cmd, args)
        print(result)

    send_command(client_socket, "stop")
    client_socket.close()
