import subprocess
import time
import sys
import os
import requests

def wait_for_server(url, timeout=30):
    start = time.time()
    while time.time() - start < timeout:
        try:
            resp = requests.get(url, timeout=2)
            if resp.status_code == 200:
                return True
        except:
            pass
        time.sleep(1)
    return False

def main():
    # Change to the inference directory
    inference_dir = r"E:\all projects for hermes\tools-platform\apps\inference"
    os.chdir(inference_dir)
    
    # Start the server
    cmd = [sys.executable, "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
    print("Starting server:", " ".join(cmd))
    # We'll capture the output to a file to see any errors
    log_file = open("server.log", "w")
    proc = subprocess.Popen(cmd, stdout=log_file, stderr=subprocess.STDOUT, text=True)
    
    try:
        # Wait for server to be ready
        if not wait_for_server("http://localhost:8000/health", timeout=30):
            print("Server did not start in time")
            # Dump the log file
            log_file.close()
            with open("server.log", "r") as f:
                print("Server log:")
                print(f.read())
            proc.terminate()
            proc.wait(timeout=5)
            return 1
        
        print("Server is ready, running tests...")
        
        # Test health endpoint
        print("Testing /health...")
        resp = requests.get("http://localhost:8000/health", timeout=5)
        if resp.status_code == 200:
            print("  /health: OK")
            print("  Response:", resp.json())
        else:
            print(f"  /health: FAILED (status {resp.status_code})")
            print("  Response:", resp.text)
        
        # Test invalid style
        print("Testing invalid style...")
        # Create a small black image
        from PIL import Image
        import io
        img = Image.new('RGB', (1, 1), color='black')
        img_bytes = io.BytesIO()
        img.save(img_bytes, format='PNG')
        img_data = img_bytes.getvalue()
        
        # We'll use requests to post multipart/form-data
        files = {'file': ('test.png', img_data, 'image/png')}
        data = {'style': 'invalid_style'}
        resp = requests.post("http://localhost:8000/style-transfer", files=files, data=data, timeout=10)
        if resp.status_code == 400:
            print("  Invalid style: correctly rejected (status 400)")
        else:
            print(f"  Invalid style: unexpected status {resp.status_code}")
            print("  Response:", resp.text)
        
        # Test valid style (candy)
        print("Testing valid style (candy)...")
        data = {'style': 'candy'}
        resp = requests.post("http://localhost:8000/style-transfer", files=files, data=data, timeout=30)
        if resp.status_code == 200:
            print("  Valid style: OK (status 200)")
            print("  Content-Type:", resp.headers.get('Content-Type'))
        elif resp.status_code == 500:
            print("  Valid style: server error (500) - possibly style image missing or processing error")
            print("  Response:", resp.text[:200])
        else:
            print(f"  Valid style: unexpected status {resp.status_code}")
            print("  Response:", resp.text)
        
        # Test file size limit
        print("Testing file size limit...")
        # Create an image larger than 5 MiB
        large_img = Image.new('RGB', (3000, 3000), color='white')
        large_img_bytes = io.BytesIO()
        large_img.save(large_img_bytes, format='PNG')
        large_img_data = large_img_bytes.getvalue()
        files_large = {'file': ('large.png', large_img_data, 'image/png')}
        resp = requests.post("http://localhost:8000/remove-background", files=files_large, timeout=10)
        if resp.status_code == 413:
            print("  File size limit: correctly rejected (status 413)")
        else:
            print(f"  File size limit: unexpected status {resp.status_code}")
            print("  Response:", resp.text)
        
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
        log_file.close()

if __name__ == "__main__":
    sys.exit(main())