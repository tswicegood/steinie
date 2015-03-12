import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from steinie import app

app = app.Steinie()


@app.get("/")
def handle(request):
    return "Hello, World!  This is Steinie.\n"

if __name__ == "__main__":
    app.run()
