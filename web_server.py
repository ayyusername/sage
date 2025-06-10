#!/usr/bin/env python3
"""
Web server for Sage Agent Debug UI
"""
import asyncio
import json
from datetime import datetime
from http.server import HTTPServer, SimpleHTTPRequestHandler
import urllib.parse
import threading
from sage_agent_debug import SageAgentDebug

class DebugWebHandler(SimpleHTTPRequestHandler):
    """Custom handler for debug web interface"""
    
    def __init__(self, *args, **kwargs):
        # Initialize the debug agent
        if not hasattr(DebugWebHandler, 'agent'):
            DebugWebHandler.agent = SageAgentDebug()
            # Run the async initialization in the background
            try:
                loop = asyncio.get_event_loop()
            except RuntimeError:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
            
            if not loop.is_running():
                loop.run_until_complete(DebugWebHandler.agent.initialize())
        
        super().__init__(*args, **kwargs)
    
    def do_GET(self):
        """Serve static files"""
        if self.path == '/' or self.path == '/index.html':
            self.path = '/web_ui.html'
        return super().do_GET()
    
    def do_POST(self):
        """Handle chat requests"""
        if self.path == '/chat':
            try:
                # Get request data
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                request_data = json.loads(post_data.decode('utf-8'))
                
                message = request_data.get('message', '')
                temperature = request_data.get('temperature', 0.1)
                
                print(f"🌐 Web UI Request: {message} (temp: {temperature})")
                
                # Clear previous log for this request
                DebugWebHandler.agent.conversation_log = []
                
                # Process the message
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                response = loop.run_until_complete(
                    DebugWebHandler.agent.chat(message, temperature)
                )
                loop.close()
                
                # Prepare response with debug log
                response_data = {
                    'response': response,
                    'debug_log': DebugWebHandler.agent.conversation_log,
                    'timestamp': datetime.now().isoformat()
                }
                
                # Send response
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                
                self.wfile.write(json.dumps(response_data).encode('utf-8'))
                
                print(f"✅ Response sent ({len(response)} chars)")
                print(f"📊 Debug entries: {len(DebugWebHandler.agent.conversation_log)}")
                
            except Exception as e:
                print(f"❌ Error processing request: {e}")
                
                # Send error response
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                
                error_response = {
                    'error': str(e),
                    'timestamp': datetime.now().isoformat()
                }
                
                self.wfile.write(json.dumps(error_response).encode('utf-8'))
        else:
            self.send_error(404)
    
    def do_OPTIONS(self):
        """Handle CORS preflight requests"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def log_message(self, format, *args):
        """Suppress default HTTP logging"""
        return

def start_server(port=8000):
    """Start the debug web server"""
    server_address = ('', port)
    httpd = HTTPServer(server_address, DebugWebHandler)
    
    print(f"🌐 Starting Sage Debug Web Server on http://localhost:{port}")
    print(f"🔍 Open your browser to monitor agent conversations in real-time")
    print(f"🛑 Press Ctrl+C to stop the server")
    print("=" * 60)
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
        httpd.shutdown()

if __name__ == "__main__":
    start_server()