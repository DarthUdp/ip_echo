from flask import Flask, request, Response

app = Flask(__name__)


@app.route('/')
def hello_world():
    return Response(content_type="text/html", response="To get ")


if __name__ == '__main__':
    app.run()
