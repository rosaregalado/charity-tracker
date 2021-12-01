from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId
import os


uri = os.environ.get('MONGODB_URI')
client = MongoClient(uri)
# db = client.get_default_database()
db = client.CharityTracker

# database resources
donations = db.donations
charities = db.charities

app = Flask(__name__)

# ---------------------------------------------------------------------------
# Donations routes

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
    'donation_amount': '$' + request.form.get('donation_amount'),
    'donation_date': request.form.get('donation_date'),
    'note': request.form.get('note')
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
    'donation_amount': request.form.get('donation_amount'),
    'donation_date': request.form.get('donation_date'),
    'note': request.form.get('note')

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

# ---------------------------------------------------------------------
# charities routes

# charities index route
@app.route('/charities')
def charities_index():
  return render_template('charities_index.html', charities=charities.find())

@app.route('/charities/new')
def charities_new():
  return render_template('charities_new.html')

# submit charity route - POST
@app.route('/charities', methods=['POST'])
def charity_submit():
  charity = {
    'charity_name': request.form.get('charity_name'),
    'charity_description': request.form.get('charity_description')
  }
  # add charity to db
  charities.insert_one(charity)
  return redirect(url_for('charities_index'))

# show (single) charity profile route
@app.route('/charities/<charity_name>')
def charity_profile(charity_name):
  charity = charities.find_one({'name': charity_name})
  return render_template('charities_new.html', charity=charity, donations = donations.find({'charity_name': charity_name}))

# # edit single charity route 
# @app.route('/charities/<charity_name>/edit')
# def charity_edit(charity_name):
#   charity = charities.find_one({'name': charity_name})
#   return render_template('charity_edit.html', charity=charity, title='Edit Charity')

# update charity route - POST
@app.route('/charities/<charity_name>', methods=['POST'])
def charities_update(charity_name):
  updated_charity = {
    'name': request.form.get('charity_name'),
    'description': request.form.get('charity_description')
  }
  charities.update_one(
    {'name': charity_name},
    {'$set': updated_charity}
  )
  return redirect(url_for('charity_show', charity_name=updated_charity['name']))

# delete charity
@app.route('/charities/<charity_name>/delete', methods=['POST'])
def charity_delete(charity_name):
  charities.delete_one({'name': charity_name})
  return redirect(url_for('charities_index'))

if __name__ == '__main__':
  app.run(debug=True)  