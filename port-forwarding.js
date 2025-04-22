const net = require('net');

// Configuration
const LOCAL_HOST = '192.168.1.11';
const LOCAL_PORT = 3000;
const TARGET_HOST = '192.168.1.12';
const TARGET_PORT = 3000;

// Create the forwarding server
const server = net.createServer((clientSocket) => {
  // Connect to target server
  const targetSocket = net.connect({
    host: TARGET_HOST,
    port: TARGET_PORT
  }, () => {
    console.log(`Connected to target ${TARGET_HOST}:${TARGET_PORT}`);
    
    // Set up two-way data transfer
    clientSocket.pipe(targetSocket);
    targetSocket.pipe(clientSocket);
    
    // Handle client socket events
    clientSocket.on('error', (err) => {
      console.error('Client socket error:', err);
      targetSocket.end();
    });
    
    clientSocket.on('end', () => {
      console.log('Client disconnected');
      targetSocket.end();
    });
    
    // Handle target socket events
    targetSocket.on('error', (err) => {
      console.error('Target socket error:', err);
      clientSocket.end();
    });
    
    targetSocket.on('end', () => {
      console.log('Target disconnected');
      clientSocket.end();
    });
  });
  
  targetSocket.on('error', (err) => {
    console.error(`Error connecting to target ${TARGET_HOST}:${TARGET_PORT}:`, err);
    clientSocket.end();
  });
});

// Handle server errors
server.on('error', (err) => {
  console.error('Server error:', err);
});

// Start the server
server.listen(LOCAL_PORT, LOCAL_HOST, () => {
  console.log(`Port forwarding server running at ${LOCAL_HOST}:${LOCAL_PORT}`);
  console.log(`Forwarding connections to ${TARGET_HOST}:${TARGET_PORT}`);
});

// Handle script termination
process.on('SIGINT', () => {
  console.log('\nShutting down port forwarding server...');
  server.close();
  process.exit(0);
});