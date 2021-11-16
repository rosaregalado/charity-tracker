from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId
import os

client = MongoClient()
db = client.CharityTracker
# uri = os.environ.get('MONGODB_URI')
# client = MongoClient(uri)
# db = client.get_default_database()

# resources
donations = db.donations

app = Flask(__name__)

# root route - GET
@app.route('/')
def donations_index():
  return render_template('donations_index.html', donations=donations.find())

# show single donation route - GET
@app.route('/donations/<donation_id>')
def donations_show(donation_id):
  # show one donation
  donation = donations.find_one({'_id': ObjectId(donation_id)})
  return render_template('donations_show.html', donation=donation)

# add new donation route - GET
@app.route('/donations/new')
def donations_new():
  return render_template('donations_new.html', donation = {}, title = 'New Donation')

# submit donation route - POST
@app.route('/donations', methods=['POST'])
def donation_submit():
  donation = {
    'charity_name': request.form.get('charity_name'),
    'charity_description': request.form.get('charity_description'),
    'donation_amount': request.form.get('donation_amount'),
    'donation_date': request.form.get('donation_date')
  }
  # add donation to db
  donation_id = donations.insert_one(donation).inserted_id
  return redirect(url_for('donations_show', donation_id=donation_id))

# edit single donation route - GET
@app.route('/donations/<donation_id>/edit')
def donations_edit(donation_id):
  donation = donations.find_one({'_id': ObjectId(donation_id)})
  return render_template('donations_edit.html', donation=donation, title='Edit Donation')

# update single donation - POST
@app.route('/donations/<donation_id>', methods=['POST'])
def donations_update(donation_id):
  updated_donation = {
    'charity_name': request.form.get('charity_name'),
    'charity_description': request.form.get('charity_description'),
    'donation_amount': '$' + request.form.get('donation_amount'),
    'donation_date': request.form.get('donation_date')
  }
  # set the former donation to the updated donation
  donations.update_one(
    {'_id': ObjectId(donation_id)},
    {'$set': updated_donation}
  )
  # return to donation's show page
  return redirect(url_for('donations_show', donation_id=donation_id))

# delete single donation - POST
@app.route('/donations/<donation_id>/delete', methods=['POST'])
def donations_delete(donation_id):
  donations.delete_one({'_id': ObjectId(donation_id)})
  return redirect(url_for('donations_index'))

if __name__ == '__main__':
  app.run(debug=True)  