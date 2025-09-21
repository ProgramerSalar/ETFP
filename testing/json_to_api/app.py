from flask import Flask
import datetime


app = Flask(__name__)

@app.route('/')
def home():

    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return f"Nodemon is working {current_time} ...."


if __name__ == "__main__":
    app.run(port=5000, debug=True)