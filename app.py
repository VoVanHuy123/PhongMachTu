from flask import Flask, redirect, url_for,render_template

app = Flask(__name__)
@app.route("/")
def hello_user():
    return render_template('index.html',content="hung",
                           cars = ["Vinfast", "BMW", "Mercedes"])
if __name__ == '__main__':   
    app.run(debug=True)