import socket
import sys
import threading
import time

def forward_socket(source, target):
    """
    Forward data between source and target sockets.
    """
    while True:
        try:
            data = source.recv(4096)
            if not data:
                break
            target.send(data)
        except:
            break
    
    try:
        source.close()
    except:
        pass
    
    try:
        target.close()
    except:
        pass

def handle_client(client_socket):
    """
    Handle each client connection by forwarding to target host.
    """
    target_host = "192.168.1.12"
    target_port = 3000
    
    try:
        # Create connection to target
        target_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        target_socket.connect((target_host, target_port))
        
        # Create threads to forward data in both directions
        client_to_target = threading.Thread(
            target=forward_socket,
            args=(client_socket, target_socket)
        )
        
        target_to_client = threading.Thread(
            target=forward_socket,
            args=(target_socket, client_socket)
        )
        
        client_to_target.daemon = True
        target_to_client.daemon = True
        
        client_to_target.start()
        target_to_client.start()
        
        # Wait for one of the threads to finish
        while client_to_target.is_alive() and target_to_client.is_alive():
            time.sleep(0.5)
            
    except Exception as e:
        print(f"Error forwarding connection: {e}")
        try:
            client_socket.close()
        except:
            pass

def main():
    local_host = "192.168.1.11"  # Listen on this IP
    local_port = 3000  # Listen on this port
    
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        # Reuse the socket if it's already in use
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((local_host, local_port))
        server.listen(5)
        
        print(f"[*] Listening on {local_host}:{local_port}")
        print(f"[*] Forwarding to 192.168.1.12:{local_port}")
        
        while True:
            client_socket, addr = server.accept()
            print(f"[*] Accepted connection from {addr[0]}:{addr[1]}")
            
            client_handler = threading.Thread(
                target=handle_client,
                args=(client_socket,)
            )
            client_handler.daemon = True
            client_handler.start()
            
    except KeyboardInterrupt:
        print("\n[*] Shutting down...")
        server.close()
        sys.exit(0)
    except Exception as e:
        print(f"[!] Error: {e}")
        server.close()
        sys.exit(1)

if __name__ == "__main__":
    main()