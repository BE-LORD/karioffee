import os
import socket
import subprocess
import time
import pytest
from playwright.sync_api import sync_playwright

def is_port_open(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

@pytest.fixture(scope="session", autouse=True)
def start_server():
    port = 8000
    process = None
    if is_port_open(port):
        print(f"Port {port} is already in use, assuming server is running.")
        yield
        return

    # conftest.py is at anti coffee/tests/conftest.py, so directory to serve is one level up
    test_dir = os.path.dirname(os.path.abspath(__file__))
    serve_dir = os.path.dirname(test_dir)
    
    print(f"Starting server in directory: {serve_dir} on port {port}")
    # On Windows, we run python -m http.server 8000 --directory <serve_dir>
    cmd = ["python", "-m", "http.server", str(port), "--directory", serve_dir]
    
    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    # Wait for the server to be up
    timeout = 10
    start_time = time.time()
    while not is_port_open(port):
        if time.time() - start_time > timeout:
            if process:
                process.terminate()
            raise RuntimeError("Failed to start http.server in time.")
        time.sleep(0.5)
        
    yield
    
    if process:
        process.terminate()
        process.wait()

@pytest.fixture(scope="session")
def playwright_instance():
    with sync_playwright() as p:
        yield p

@pytest.fixture(scope="session")
def browser(playwright_instance):
    # Always launch chromium in headless mode
    browser = playwright_instance.chromium.launch(headless=True)
    yield browser
    browser.close()

@pytest.fixture(scope="function")
def context(browser):
    context = browser.new_context()
    yield context
    context.close()

@pytest.fixture(scope="function")
def page(context):
    page = context.new_page()
    yield page
    page.close()
