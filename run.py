from app import create_app
from waitress import serve

import subprocess


# if __name__ == "__main__":
#     app = create_app()
#     serve(app, port=9000)

subprocess.run(["waitress-serve", "--call", "--port=8030", "app:create_app"])
