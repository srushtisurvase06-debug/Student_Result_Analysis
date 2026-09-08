#!/usr/bin/env python3
"""
One-Click Launcher for Student Result Analysis System

Starts the Flask application with automatic dependency checking,
server readiness detection, and browser opening.

Usage:
    python RUN_APP.py
    or double-click RUN_APP.py
"""

import os
import sys
import time
import webbrowser
import socket
from pathlib import Path
from urllib.request import urlopen
from urllib.error import URLError
import subprocess


def print_header():
    """Print application header."""
    print("=" * 60)
    print("       STUDENT RESULT ANALYSIS SYSTEM")
    print("=" * 60)
    print()


def print_status(step, total, message):
    """Print status message with progress."""
    print(f"[{step}/{total}] {message}")


def print_error(message):
    """Print error message."""
    print()
    print("=" * 60)
    print("ERROR:", message)
    print("=" * 60)


def print_success(message):
    """Print success message."""
    print()
    print("=" * 60)
    print("✓", message)
    print("=" * 60)
    print()


def get_project_root():
    """Determine project root automatically."""
    # This file is at D:\Student_Result_Analysis\RUN_APP.py
    # So the parent is the project root
    return Path(__file__).resolve().parent


def get_backend_dir(project_root):
    """Determine backend directory."""
    backend = project_root / "CODEBASE" / "BACKEND"
    if not backend.exists():
        raise FileNotFoundError(
            f"Backend directory not found at: {backend}\n"
            "Expected structure: CODEBASE/BACKEND/"
        )
    return backend


def check_python():
    """Verify Python interpreter is usable."""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 11):
        raise RuntimeError(
            f"Python 3.11+ required, but found {version.major}.{version.minor}\n"
            "Please upgrade Python to continue."
        )
    return f"Python {version.major}.{version.minor}.{version.micro}"


def check_required_files(backend_dir):
    """Verify required files exist."""
    required_files = [
        backend_dir / "app.py",
        backend_dir / "config.py",
        backend_dir.parent.parent / ".env",
    ]
    
    missing = []
    for file in required_files:
        if not file.exists():
            if file.name == ".env":
                # .env might be legitimately missing in some setups
                print(f"   Warning: {file} not found (using .env.example as reference)")
            else:
                missing.append(str(file))
    
    if missing:
        raise FileNotFoundError(
            f"Required files missing:\n" + "\n".join(f"  - {f}" for f in missing)
        )


def check_dependencies(backend_dir):
    """Check if required dependencies are installed."""
    requirements_file = backend_dir.parent.parent / "requirements.txt"
    
    if not requirements_file.exists():
        print("   Warning: requirements.txt not found, skipping dependency check")
        return
    
    # Check key dependencies
    critical_packages = {
        'flask': 'flask',
        'psycopg2': 'psycopg2',
        'bcrypt': 'bcrypt',
        'python-dotenv': 'dotenv'  # Import name is different
    }
    missing = []
    
    for package, import_name in critical_packages.items():
        try:
            __import__(import_name)
        except ImportError:
            missing.append(package)
    
    if missing:
        print()
        print("   Missing dependencies detected:")
        for pkg in missing:
            print(f"     - {pkg}")
        print()
        print("   Install with:")
        print(f"     pip install -r {requirements_file}")
        print()
        raise ImportError(f"Missing required packages: {', '.join(missing)}")


def is_port_in_use(port, host='127.0.0.1'):
    """Check if a port is already in use."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind((host, port))
            return False
        except socket.error:
            return True


def wait_for_server(url, timeout=30, check_interval=0.5):
    """Wait for server to be ready by polling the health endpoint."""
    start_time = time.time()
    health_url = url.rstrip('/') + '/health'
    
    while time.time() - start_time < timeout:
        try:
            with urlopen(health_url, timeout=2) as response:
                if response.status == 200:
                    return True
        except (URLError, ConnectionResetError, socket.timeout):
            pass
        time.sleep(check_interval)
    
    return False


def start_flask_server(backend_dir):
    """Start the Flask server as a subprocess."""
    # Change to backend directory
    os.chdir(backend_dir)
    
    # Get port from environment or use default
    port = int(os.getenv('PORT', '5000'))
    host = '127.0.0.1'
    
    # Check if port is already in use
    if is_port_in_use(port, host):
        raise RuntimeError(
            f"Port {port} is already in use.\n"
            f"Another instance might be running, or another application is using this port."
        )
    
    # Start Flask using the existing app.py
    # Use sys.executable to use the same Python interpreter
    process = subprocess.Popen(
        [sys.executable, 'app.py'],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
        universal_newlines=True
    )
    
    return process, host, port


def open_browser(url):
    """Open the default browser to the application URL."""
    try:
        webbrowser.open(url)
        return True
    except Exception as e:
        print(f"   Warning: Could not open browser automatically: {e}")
        print(f"   Please open {url} manually in your browser")
        return False


def main():
    """Main launcher function."""
    try:
        print_header()
        
        # Step 1: Check project structure
        print_status(1, 5, "Checking project structure...")
        project_root = get_project_root()
        backend_dir = get_backend_dir(project_root)
        print(f"   Project root: {project_root}")
        print(f"   Backend: {backend_dir}")
        
        # Step 2: Check Python
        print_status(2, 5, "Checking Python version...")
        python_version = check_python()
        print(f"   {python_version}")
        
        # Verify required files
        check_required_files(backend_dir)
        print("   ✓ Required files present")
        
        # Step 3: Check dependencies
        print_status(3, 5, "Checking dependencies...")
        check_dependencies(backend_dir)
        print("   ✓ All dependencies installed")
        
        # Step 4: Start Flask server
        print_status(4, 5, "Starting Flask server...")
        process, host, port = start_flask_server(backend_dir)
        url = f"http://{host}:{port}"
        
        # Wait for server to be ready
        print(f"   Waiting for server at {url}...")
        if not wait_for_server(url, timeout=30):
            print_error("Server failed to start within 30 seconds")
            process.terminate()
            print("\nServer output:")
            if process.stdout:
                print(process.stdout.read())
            return 1
        
        print("   ✓ Server is ready")
        
        # Step 5: Open browser
        print_status(5, 5, "Opening browser...")
        open_browser(url)
        
        # Success message
        print_success("Application started successfully!")
        print(f"Application running at: {url}")
        print(f"Admin login: {url}/login")
        print(f"Public result lookup: {url}/results/lookup")
        print()
        print("Press Ctrl+C to stop the application.")
        print("=" * 60)
        print()
        
        # Keep the process alive and show output
        try:
            for line in process.stdout:
                print(line, end='')
        except KeyboardInterrupt:
            print("\n\nShutting down...")
            process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
            print("Application stopped.")
            return 0
        
    except KeyboardInterrupt:
        print("\n\nStartup cancelled.")
        return 130
    
    except Exception as e:
        print_error(str(e))
        print("\nStartup failed. Please check the error message above.")
        
        # Keep console open on Windows
        if sys.platform == 'win32':
            print("\nPress Enter to close...")
            input()
        
        return 1


if __name__ == '__main__':
    sys.exit(main())
