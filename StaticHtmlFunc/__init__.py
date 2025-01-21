import logging
import os
import azure.functions as func

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # Get the requested path
    path = req.params.get('path')
    if not path:
        try:
            path = req.route_params.get('path')
        except ValueError:
            path = ""

    # Serve index.html as the default
    if not path or path.endswith('/'):
        try:
            with open(os.path.join(os.path.dirname(__file__), "index.html"), "r") as f:
                html_content = f.read()
            return func.HttpResponse(html_content, mimetype="text/html")
        except FileNotFoundError:
            return func.HttpResponse("index.html not found", status_code=404)

    # Handle static files (CSS, JS, etc.)
    elif path.startswith("static/"):
        static_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), path)

        if os.path.exists(static_file_path):
            try:
                with open(static_file_path, "rb") as f:
                    content = f.read()
                    if path.endswith(".css"):
                        mimetype = "text/css"
                    elif path.endswith(".js"):
                        mimetype = "application/javascript"
                    else:
                        mimetype = "application/octet-stream"
                    return func.HttpResponse(content, mimetype=mimetype)
            except Exception as e:
                logging.error(f"Error serving static file: {e}")
                return func.HttpResponse("Internal Server Error", status_code=500)
        else:
            return func.HttpResponse("File not found", status_code=404)

    # Default response if no route matches
    return func.HttpResponse(
        "Welcome to the Azure Function serving static HTML content!",
        status_code=200
    )