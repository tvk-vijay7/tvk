from flask import Flask, render_template, request, redirect, url_for, jsonify
import json
import os

app = Flask(__name__)
DATA_FILE = 'donors.json'

if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'w') as f:
        json.dump([], f)


def load_donors():
    with open(DATA_FILE, 'r') as f:
        return json.load(f)


def save_donors(donors):
    with open(DATA_FILE, 'w') as f:
        json.dump(donors, f, indent=4)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/add-donor', methods=['GET', 'POST'])
def add_donor():
    if request.method == 'POST':
        donor = {
            'name': request.form['name'],
            'blood_group': request.form['blood_group'],
            'mobile': request.form['mobile'],
            'location': request.form['location']
        }
        donors = load_donors()
        donors.append(donor)
        save_donors(donors)
        return "Thank you for registering as a donor!"
    return render_template('add_donor.html')


@app.route('/find-donor', methods=['GET', 'POST'])
def find_donor():
    if request.method == 'POST':
        blood_group = request.form['blood_group']
        location = request.form['location'].lower()
        donors = load_donors()
        matches = [d for d in donors if d['blood_group'] == blood_group and location in d['location'].lower()]
        return render_template('find_donor.html', donors=matches)
    return render_template('find_donor.html', donors=None)


@app.route('/admin')
def admin():
    donors = load_donors()
    return render_template('admin.html', donors=donors)


if __name__ == '__main__':
    app.run(debug=True)
