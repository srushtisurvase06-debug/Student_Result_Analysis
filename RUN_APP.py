#!/usr/bin/env python
"""
One-Click Launcher for Student Result Analysis System

This script automatically starts the Flask application with a single command
or double-click. It performs pre-flight checks, starts the server, and opens
the browser when ready.

Usage:
    python RUN_APP.py
    OR double-click RUN_APP.py in Windows Explorer
"""

import sys
import os
import time
import socket
import subprocess
import webbrowser
from pathlib import Path
from urllib.request import urlopen
from urllib.error import URLError


def print_banner():
    """Display startup banner."""
    print("\n" + "=" * 50)
    print("    STUDENT RESULT ANALYSIS SYSTEM")
    print("=" * 50 + "\n")


def print_step(step, total, message):
    """Display step progress."""
    print(f"[{step}/{total}] {message}")


def get_project_root():
    """Get the absolute path to the project root directory."""
    # RUN_APP.py is at project root
    return Path(__file__).resolve().parent


def get_backend_dir(project_root):
    """Get the backend directory path."""
    return project_root / "CODEBASE" / "BACKEND"


def check_project_structure(backend_dir):
    """Verify that required project files exist."""
    required_files = [
        backend_dir / "app.py",
        backend_dir / "config.py",
    ]
    
    missing = [f for f in required_files if not f.exists()]
    
    if missing:
        print("\n❌ ERROR: Missing required files:")
        for f in missing:
            print(f"   - {f}")
        return False
    
    return True


def check_python():
    """Verify Python interpreter is working."""
    try:
        version = sys.version_info
        if version.major < 3 or (version.major == 3 and version.minor < 8):
            print(f"\n❌ ERROR: Python 3.8+ required, found {version.major}.{version.minor}")
            return False
        return True
    except Exception as e:
        print(f"\n❌ ERROR: Could not verify Python version: {e}")
        return False


def check_dependencies(backend_dir):
    """Check if required dependencies are installed."""
    # Import from the backend directory
    sys.path.insert(0, str(backend_dir))
    
    missing_deps = []
    
    try:
        import flask
    except ImportError:
        missing_deps.append("flask")
    
    try:
        import psycopg2
    except ImportError:
        missing_deps.append("psycopg2-binary")
    
    try:
        import dotenv
    except ImportError:
        missing_deps.append("python-dotenv")
    
    try:
        import bcrypt
    except ImportError:
        missing_deps.append("bcrypt")
    
    if missing_deps:
        print("\n❌ ERROR: Missing required dependencies:")
        for dep in missing_deps:
            print(f"   - {dep}")
        print("\nTo install missing dependencies, run:")
        print(f"   pip install {' '.join(missing_deps)}")
        print("\nOr install all dependencies:")
        print("   pip install -r requirements.txt")
        return False
    
    return True


def load_environment(project_root):
    """Load environment configuration."""
    env_file = project_root / ".env"
    env_example = project_root / ".env.example"
    
    if not env_file.exists():
        if env_example.exists():
            print("\n⚠️  WARNING: .env file not found")
            print(f"   A template exists at: {env_example}")
            print("   Copy .env.example to .env and configure it before running.")
            return False
        else:
            print("\n⚠️  WARNING: No .env configuration found")
            print("   The application may not work correctly without environment variables.")
    
    return True


def get_app_config(backend_dir):
    """Get host and port from environment or use defaults."""
    # Load environment from project root
    project_root = backend_dir.parent.parent
    env_file = project_root / ".env"
    
    if env_file.exists():
        try:
            from dotenv import load_dotenv
            load_dotenv(env_file)
        except ImportError:
            pass
    
    host = os.getenv('FLASK_HOST', '127.0.0.1')
    port = int(os.getenv('PORT', '5000'))
    
    return host, port


def is_port_available(host, port):
    """Check if the port is available."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    try:
        sock.connect((host, port))
        sock.close()
        return False  # Port is in use
    except (socket.timeout, ConnectionRefusedError, OSError):
        return True  # Port is available


def wait_for_server(url, timeout=30):
    """Wait for the server to start accepting connections."""
    start_time = time.time()
    
    while time.time() - start_time < timeout:
        try:
            response = urlopen(url, timeout=2)
            response.close()
            return True
        except (URLError, OSError):
            time.sleep(0.5)
    
    return False


def start_flask_server(backend_dir, host, port):
    """Start the Flask application server."""
    app_file = backend_dir / "app.py"
    
    # Set working directory to backend
    env = os.environ.copy()
    env['PYTHONUNBUFFERED'] = '1'  # Force unbuffered output
    
    # Start Flask using the existing app.py
    process = subprocess.Popen(
        [sys.executable, str(app_file)],
        cwd=str(backend_dir),
        env=env,
        stdout=sys.stdout,
        stderr=sys.stderr
    )
    
    return process


def open_browser(url):
    """Open the default browser to the application URL."""
    try:
        webbrowser.open(url)
        return True
    except Exception as e:
        print(f"\n⚠️  Could not open browser automatically: {e}")
        print(f"   Please open your browser manually and visit: {url}")
        return False


def main():
    """Main launcher function."""
    print_banner()
    
    # Step 1: Check project structure
    print_step(1, 5, "Checking project structure...")
    project_root = get_project_root()
    backend_dir = get_backend_dir(project_root)
    
    if not check_project_structure(backend_dir):
        print("\n❌ STARTUP FAILED: Project structure check failed")
        input("\nPress Enter to exit...")
        return 1
    
    print("   ✓ Project structure OK")
    
    # Step 2: Check Python
    print_step(2, 5, "Checking Python interpreter...")
    if not check_python():
        print("\n❌ STARTUP FAILED: Python check failed")
        input("\nPress Enter to exit...")
        return 1
    
    print(f"   ✓ Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
    
    # Step 3: Check dependencies
    print_step(3, 5, "Checking dependencies...")
    if not check_dependencies(backend_dir):
        print("\n❌ STARTUP FAILED: Dependency check failed")
        input("\nPress Enter to exit...")
        return 1
    
    print("   ✓ All required dependencies installed")
    
    # Step 3.5: Load environment
    if not load_environment(project_root):
        print("\n⚠️  Continuing without .env file (application may not work correctly)")
    else:
        print("   ✓ Environment configuration loaded")
    
    # Get configuration
    host, port = get_app_config(backend_dir)
    url = f"http://{host}:{port}"
    
    # Check if port is available
    if not is_port_available(host, port):
        print(f"\n❌ ERROR: Port {port} is already in use")
        print(f"   Another application may be running on port {port}")
        print(f"   Stop that application or change the PORT in .env")
        input("\nPress Enter to exit...")
        return 1
    
    # Step 4: Start Flask server
    print_step(4, 5, "Starting Flask server...")
    print(f"   Host: {host}")
    print(f"   Port: {port}")
    
    try:
        process = start_flask_server(backend_dir, host, port)
    except Exception as e:
        print(f"\n❌ ERROR: Failed to start Flask server: {e}")
        input("\nPress Enter to exit...")
        return 1
    
    # Wait for server to be ready
    print("   Waiting for server to start...")
    if not wait_for_server(url, timeout=30):
        print("\n❌ ERROR: Server did not start within 30 seconds")
        print("   Check the error messages above for details")
        process.terminate()
        input("\nPress Enter to exit...")
        return 1
    
    print("   ✓ Flask server started successfully")
    
    # Step 5: Open browser
    print_step(5, 5, "Opening browser...")
    open_browser(url)
    print("   ✓ Browser opened")
    
    # Show running status
    print("\n" + "=" * 50)
    print(f"   Application running at: {url}")
    print("=" * 50)
    print("\nPress Ctrl+C to stop the application\n")
    
    # Keep running until interrupted
    try:
        process.wait()
    except KeyboardInterrupt:
        print("\n\nShutting down...")
        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
        print("Application stopped.")
    
    return 0


if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except Exception as e:
        print(f"\n❌ UNEXPECTED ERROR: {e}")
        import traceback
        traceback.print_exc()
        input("\nPress Enter to exit...")
        sys.exit(1)
