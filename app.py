from flask import Flask, render_template, redirect
import pymongo
import scrape_mars

# Create an instance of Flask
app = Flask(__name__)

# setup mongo connection
conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)

# connect to mongo db and collection
db = client.mars_db
mars = db.mars_collection
mars.insert_one(scrape_mars.scrape())

@app.route("/")
def home():      
    mars_data = mars.find_one()
    return render_template("index.html", mars_data = mars_data)

@app.route("/scrape")
def scrape():
   
    # Run the scrape function
    data = scrape_mars.scrape()
    
    # Update the Mongo database using update and upsert=True
    mars.update(
        {},
        data,
        upsert=True
    )
    
    # Redirect back to home page
    return redirect("/")


if __name__ == "__main__":
    app.run(debug = False)
