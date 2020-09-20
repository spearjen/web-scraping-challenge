# import necessary libraries
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars
 
# create Flask app instance
app = Flask(__name__)

# setup conn to PyMongo
app.config['MONGO_URI'] = 'mongodb://localhost:27017/marsDB'
mongo = PyMongo(app)

# create route that renders template
@app.route("/")
def index():
    mars=mongo.db.mars.find_one()
    return render_template("index.html", mars=mars)
 
# create route that scrapes mars data and store as dictionary and to MongoDB
@app.route('/scrape')
def scrape():
    mars=mongo.db.mars
    mars_data = scrape_mars.scrape_all()
    mars.replace_one({},mars_data, upsert=True)
    return redirect('/')
    
if __name__ == "__main__":
    app.run(debug=True)