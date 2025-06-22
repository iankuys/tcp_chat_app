import socket
import threading

clients = []

def broadcast_messages(client_socket, message, include_sender=False):
    for client in clients[:]:
        if client_socket == client and not include_sender:
            continue
        else:
            try:
                client.send(message.encode())
            except:
                clients.remove(client)

def handle_client(client_socket, addr):
    print(f"connection from address {addr}")
    try:
        client_socket.send("Enter your name: ".encode())
        
        username = ""
        while True:
            char = client_socket.recv(1).decode()
            if not char:
                break
            if char == "\r" or char == "\n":
                break
            username += char
        
        message_buffer = ""
        while True:
            char = client_socket.recv(1).decode()
            if not char:
                break
            message_buffer += char
            
            if char == "\r" or char == "\n":
                message = message_buffer.strip()
                if message:
                    chat_message = f"{username}: {message_buffer}\n"
                    print(chat_message.strip())
                    broadcast_messages(client_socket, chat_message)
                message_buffer = ""
        
    except Exception as e:
        print(f"Exception with {addr}: {e}")
    
    finally:
        if client_socket in clients:
            clients.remove(client_socket)
        client_socket.close()
        
        leave_message = f"{username} left the chat"
        broadcast_messages(client_socket, leave_message)

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    HOST = "localhost"
    PORT = 9999
    
    server.bind((HOST, PORT))
    server.listen()
    
    print(f"Chat server listening on {HOST}:{PORT}")
    print("Connect with: telnet localhost 9999")
    try:
        while True:
            conn, addr = server.accept()
            clients.append(conn)
            
            client_thread = threading.Thread(target=handle_client, args=(conn, addr))
            client_thread.daemon = True
            client_thread.start()
            
    except KeyboardInterrupt:
        print("\nShutting Down Server...")
    finally:
        server.close()
        
if __name__ == "__main__":
    start_server()
        