from flask import request, Flask, jsonify

app = Flask(__name__)


@app.route("/hello/<name>", methods = ["GET"])
def hello(name):
    greeting = "Hello {}!".format(name)
    return jsonify(greeting)

@app.route("/api/new_patient", methods = ["POST"])
def new_patient():
    # For future Michael


if __name__ == "__main__":
    app.run(host = "127.0.0.1")