import http.server
import os
import socketserver
import sys

PORT = 8888
DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "public")


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIR, **kwargs)


def serve():
    if not os.path.exists(DIR):
        print(f"Error: Output directory '{DIR}' does not exist.")
        print("Please run `python src/main.py` first to generate the website.")
        sys.exit(1)

    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"Serving Tolkien Fan Club website at http://localhost:{PORT}")
        print("Press Ctrl+C to stop the server.")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server.")


if __name__ == "__main__":
    serve()
