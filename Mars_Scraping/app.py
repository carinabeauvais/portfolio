# use Flask to render template, direct to url and create url. use pymongo to intereact with mongo db. 
# use scraping code, convert from jupyter to python
from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scraping
# Set up Flask
app = Flask(__name__)
# tell python how to connect to mongo using pymongo; app.config tells python connect to mongo using URI(uniform resource identifier)
# Use flask_pymongo to set up mongo connection; mongodb:localhost is the uri used to connect our app to mongo
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# define route for HTML page; tells Flask what to display. mars= uses pymongo to find mars collection in db. return render returns as HTML template
@app.route("/")
def index():
   mars = mongo.db.mars.find_one()
   return render_template("index.html", mars=mars)

# set up scraping route (button) of web application. This scrapes data when we tell it to. first line defines route. then access db, scrape data
# using scraping.py script, update db and return message when successful.
@app.route("/scrape")
def scrape():
    # assign varable that points to mongo db
   mars = mongo.db.mars
   # assign varable to hold scraped data. reference all function in the scraping.py file exported from Jupyter
   mars_data = scraping.scrape_all()
   # update the db using update one, add if new.
   mars.update_one({}, {"$set":mars_data}, upsert=True)
   # add a redirect after successful scrape. This navigates back to where we can see updated content.
   return redirect('/', code=302)
   # tell it to run
   if __name__ == "__main__":
      app.run()