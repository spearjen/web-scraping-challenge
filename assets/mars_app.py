# import necessary libraries
from flask import Flask, render_template

# create instance of Flask app
app = Flask(__name__)


# create route that renders index.html template
@app.route("/")
def display():
    return render_template("index.html", dict=news_dict)


# # Bonus add a new route
# @app.route("/scrape")
# def bonus():

    # return render_template("bonus.html", name=name, hobby=hobby)


if __name__ == "__main__":
    app.run(debug=True)
