# Port Forwarding Application

A simple application for forwarding network traffic from one host:port to another. This application can be used to access services that are only available on a specific network segment or for creating simple proxies.

## Overview

This port forwarding application works by:
1. Listening on a specified local IP address and port
2. Accepting incoming connections 
3. Creating a corresponding connection to the target server
4. Forwarding all traffic between the client and target server in both directions

## Versions Available

### Python Version

Uses Python's socket and threading libraries to create a reliable port forwarding service.

**Requirements:**
- Python 3.x

**Files:**
- `port_forward.py` - Main Python script

### Node.js Version

Uses Node.js's built-in networking capabilities for efficient port forwarding with event-driven architecture.

**Requirements:**
- Node.js (v12.0 or higher recommended)

**Files:**
- `port_forward.js` - Main Node.js script

## Configuration

Both versions are configured to forward traffic from `192.168.1.11:3000` to `192.168.1.12:3000`.

To modify the configuration:

### Python Version
Edit these lines in `port_forward.py`:
```python
local_host = "192.168.1.11"  # Listen on this IP
local_port = 3000            # Listen on this port
target_host = "192.168.1.12" # Forward to this IP
target_port = 3000           # Forward to this port
```

### Node.js Version
Edit these lines in `port_forward.js`:
```javascript
const LOCAL_HOST = '192.168.1.11';
const LOCAL_PORT = 3000;
const TARGET_HOST = '192.168.1.12';
const TARGET_PORT = 3000;
```

## Usage

### Python Version

1. Copy the script to the server (192.168.1.11 in this example)
2. Run the script:
   ```
   python port_forward.py
   ```
3. The server will start listening for connections
4. To stop the server, press Ctrl+C

### Node.js Version

1. Copy the script to the server (192.168.1.11 in this example)
2. Run the script:
   ```
   node port_forward.js
   ```
3. The server will start listening for connections
4. To stop the server, press Ctrl+C

## Network Diagram

```
192.168.1.13 -----> 192.168.1.11:3000 -----> 192.168.1.12:3000
   Client        Port Forwarding Server       Target Service
```

## Troubleshooting

1. **Connection Refused**: Ensure the port forwarding server is running and listening on the correct IP and port
2. **Target Unreachable**: Verify that the target server is running and accessible from the forwarding server
3. **Permission Denied**: You may need elevated privileges to bind to certain ports (especially ports below 1024)

## Security Considerations

- This application forwards traffic without authentication or encryption
- For production environments, consider adding authentication and TLS/SSL encryption
- Be cautious about which addresses and ports you expose, especially in public networks

## License

This software is provided as-is under the MIT License.

Updated 01 May 2025
