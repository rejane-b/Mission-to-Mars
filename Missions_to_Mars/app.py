from flask import Flask, render_template, request, redirect, url_for
from flask_pymongo import PyMongo
from pymongo import MongoClient
import mongoengine
import scrape_mars


app = Flask(__name__)

app.config['MONGODB_SETTINGS'] = {
    'db': 'mars_data',
    'host': 'localhost',
    'port': 27017
}

client = MongoClient()

client = MongoClient('localhost', 27017)

mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_data")


@app.route("/")
def home():

    mars_data = mongo.db.collection.find_one()


    mars_data["Mars_Table"] = mars_data["Mars_Table"].replace('<table border="1" class="dataframe">',
                                                              "<table class='table table-sm'>")

    print("--- MONGO DATA ---")
    print(mars_data)
    print("--- END MONGO DATA ---")

    return render_template("index.html", mission_mars=mars_data)



@app.route("/scrape")
def scrape():

    mars_data = scrape_mars.scrape()

    mongo.db.collection.update({}, mars_data, upsert=True)


    return redirect("/", 302)


if __name__ == "__main__":
    app.run(debug=True)
