import subprocess
import time
import socket
import sys
import os

def wait_for_port(port, host='localhost', timeout=10.0):
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            with socket.create_connection((host, port), timeout=1.0):
                return True
        except (ConnectionRefusedError, socket.timeout):
            time.sleep(0.5)
    return False

def main():
    # Change to the inference directory
    inference_dir = r"E:\all projects for hermes\tools-platform\apps\inference"
    os.chdir(inference_dir)
    
    # Start the server
    cmd = [sys.executable, "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
    print("Starting server:", " ".join(cmd))
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    try:
        # Wait for server to be ready
        if not wait_for_port(8000, timeout=30.0):
            print("Server did not start in time")
            proc.terminate()
            proc.wait(timeout=5)
            stdout, stderr = proc.communicate()
            print("STDOUT:", stdout)
            print("STDERR:", stderr)
            return 1
        
        print("Server is ready, running tests...")
        
        # Import urllib to make requests
        import urllib.request
        import urllib.error
        import json
        
        def fetch(url, data=None, headers=None, method=None):
            req = urllib.request.Request(url, data=data, headers=headers or {}, method=method)
            try:
                with urllib.request.urlopen(req, timeout=10.0) as resp:
                    return resp.read(), resp.status, dict(resp.getheaders())
            except urllib.error.HTTPError as e:
                return e.read(), e.code, dict(e.headers)
            except urllib.error.URLError as e:
                return None, None, str(e)
        
        # Test health endpoint
        print("Testing /health...")
        body, status, headers = fetch("http://localhost:8000/health")
        if status == 200:
            print("  /health: OK")
            print("  Response:", body.decode()[:200])
        else:
            print(f"  /health: FAILED (status {status})")
            print("  Response:", body)
        
        # Test invalid style
        print("Testing invalid style...")
        # We need to do a POST request with file and form data.
        # Creating a multipart request is complex with urllib. We'll use a small image.
        # Let's create a 1x1 black PNG in memory.
        import io
        from PIL import Image
        img = Image.new('RGB', (1, 1), color='black')
        img_bytes = io.BytesIO()
        img.save(img_bytes, format='PNG')
        img_data = img_bytes.getvalue()
        
        # Build multipart/form-data manually (simplified for small file)
        boundary = "----WebKitFormBoundary7MA4YWxkTrZu0gW"
        body_lines = []
        # File part
        body_lines.append(f"--{boundary}")
        body_lines.append('Content-Disposition: form-data; name="file"; filename="test.png"')
        body_lines.append('Content-Type: image/png')
        body_lines.append('')
        body_lines.append(img_data.decode('latin-1'))  # Assuming latin-1 can represent the bytes
        # Style part
        body_lines.append(f"--{boundary}")
        body_lines.append('Content-Disposition: form-data; name="style"')
        body_lines.append('')
        body_lines.append("invalid_style")
        body_lines.append(f"--{boundary}--")
        body_lines.append('')
        
        body = '\r\n'.join(body_lines).encode('latin-1')
        headers = {
            'Content-Type': f'multipart/form-data; boundary={boundary}',
        }
        
        body, status, headers = fetch("http://localhost:8000/style-transfer", data=body, headers=headers, method="POST")
        if status == 400:
            print("  Invalid style: correctly rejected (status 400)")
        else:
            print(f"  Invalid style: unexpected status {status}")
            print("  Response:", body)
        
        # Test valid style (candy)
        print("Testing valid style (candy)...")
        body_lines = []
        body_lines.append(f"--{boundary}")
        body_lines.append('Content-Disposition: form-data; name="file"; filename="test.png"')
        body_lines.append('Content-Type: image/png')
        body_lines.append('')
        body_lines.append(img_data.decode('latin-1'))
        body_lines.append(f"--{boundary}")
        body_lines.append('Content-Disposition: form-data; name="style"')
        body_lines.append('')
        body_lines.append("candy")
        body_lines.append(f"--{boundary}--")
        body_lines.append('')
        
        body = '\r\n'.join(body_lines).encode('latin-1')
        headers = {
            'Content-Type': f'multipart/form-data; boundary={boundary}',
        }
        
        body, status, headers = fetch("http://localhost:8000/style-transfer", data=body, headers=headers, method="POST")
        if status == 200:
            print("  Valid style: OK (status 200)")
            print("  Content-Type:", headers.get('Content-Type'))
        elif status == 500:
            print("  Valid style: server error (500) - possibly style image missing or processing error")
            print("  Response:", body[:200])
        else:
            print(f"  Valid style: unexpected status {status}")
            print("  Response:", body)
        
        print("Tests completed.")
        return 0
        
    finally:
        # Terminate the server
        print("Stopping server...")
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()
            proc.wait()
        print("Server stopped.")

if __name__ == "__main__":
    sys.exit(main())