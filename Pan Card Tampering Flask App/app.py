from app import app
import os

if __name__ == '__main__':
    # Get the port from Render's environment, default to 5000 for local testing
    port = int(os.environ.get("PORT", 5000))
    # Bind to 0.0.0.0 so the app is accessible externally
    app.run(host='0.0.0.0', port=port)