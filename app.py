from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId
import os

app = Flask(__name__)
app.config["MONGO_URI"] = os.getenv('MONGO_URI', 'mongodb://localhost:27017/internships')

# Connect to MongoDB
client = MongoClient(app.config["MONGO_URI"])
db = client.internship_db
applications = db.applications

# Route to serve the main page
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/home')
def home1():
    return render_template('index.html')


# Route to handle position-specific application forms
@app.route('/apply/<position>', methods=['GET', 'POST'])
def apply_position(position):
    if request.method == 'POST':
        application_data = {
            'position': position,
            'name': request.form.get('name'),
            'email': request.form.get('email'),
            'phone': request.form.get('phone'),
            'education': request.form.get('education'),
            'status': 'Pending'
        }
        applications.insert_one(application_data)
        return redirect(url_for('thank_you'))
    
    # GET request - show form
    return render_template('apply.html', position=position)

# Thank you page
@app.route('/thank-you')
def thank_you():
    return render_template('thank_you.html')

if __name__ == '__main__':
    app.run(debug=True)