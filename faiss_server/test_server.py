from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route("/test", methods=["GET"])
def test():
    return "Hell"


app.run(host='0.0.0.0', port='5000', debug=True)
