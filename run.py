import time
import webbrowser
import threading
import os
from app import create_app

app = create_app()

def open_browser():
    """Opens the web browser automatically after a short delay."""
    time.sleep(1.2)
    webbrowser.open("http://127.0.0.1:5000")

if __name__ == "__main__":
    threading.Thread(target=open_browser, daemon=True).start()
    print("=" * 50)
    print(" Starting SearchIt Campus Lost & Found Platform...")
    print(" Access the app at: http://127.0.0.1:5000")
    print(" Press CTRL+C to stop the server.")
    print("=" * 50)
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() in ('true', '1')
    app.run(host="127.0.0.1", port=5000, debug=debug_mode)
