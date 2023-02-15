from flask import Flask

app = Flask(__name__)


@app.route("/", methods=["GET"])
def get_data():
    pass
    return

@app.route("/", methods=["GET"])
def get_epochs():
    pass
    return

@app.route("/", methods=["GET"])
def get_state_vectors():
    pass
    return

@app.route("/", methods=["GET"])
def get_speed():
    pass
    return

# the next statement should usually appear at the bottom of a flask app
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
