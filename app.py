from flask import Flask, render_template, request, redirect, url_for, jsonify, session, flash
import json
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "default_secret_key_for_dev")

DATA_FILE = 'donors.json'
NOTIFICATIONS_FILE = 'notifications.json'

# Admin credentials
ADMIN_USERNAME = 'tvkkishore7'
ADMIN_PASSWORD = 'BRBhacker'

# Initialize files if they don't exist
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'w') as f:
        json.dump([], f)

if not os.path.exists(NOTIFICATIONS_FILE):
    with open(NOTIFICATIONS_FILE, 'w') as f:
        json.dump([], f)


def load_donors():
    """Load donors from JSON file"""
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_donors(donors):
    """Save donors to JSON file"""
    with open(DATA_FILE, 'w') as f:
        json.dump(donors, f, indent=4)


def load_notifications():
    """Load notifications from JSON file"""
    try:
        with open(NOTIFICATIONS_FILE, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_notifications(notifications):
    """Save notifications to JSON file"""
    with open(NOTIFICATIONS_FILE, 'w') as f:
        json.dump(notifications, f, indent=4)


def add_notification(message, search_details=None):
    """Add a new notification"""
    notifications = load_notifications()
    notification = {
        'id': len(notifications) + 1,
        'message': message,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'details': search_details,
        'read': False
    }
    notifications.append(notification)
    save_notifications(notifications)


@app.route('/')
def index():
    """Home page with navigation to add donor and find donor"""
    return render_template('index.html')


@app.route('/add-donor', methods=['GET', 'POST'])
def add_donor():
    """Add new blood donor to the system"""
    if request.method == 'POST':
        # Validate and sanitize input data
        name = request.form.get('name', '').strip()
        blood_group = request.form.get('blood_group', '').strip()
        mobile = request.form.get('mobile', '').strip()
        location = request.form.get('location', '').strip()
        
        # Basic validation
        if not all([name, blood_group, mobile, location]):
            return render_template('add_donor.html', error="All fields are required")
        
        # Validate mobile number (should be numeric and reasonable length)
        if not mobile.isdigit() or len(mobile) < 10:
            return render_template('add_donor.html', error="Invalid mobile number")
        
        # Create donor record
        donor = {
            'name': name,
            'blood_group': blood_group,
            'mobile': mobile,
            'location': location
        }
        
        # Load existing donors and add new one
        donors = load_donors()
        donors.append(donor)
        save_donors(donors)
        
        return render_template('thank_you.html')
    
    return render_template('add_donor.html')


@app.route('/find-donor', methods=['GET', 'POST'])
def find_donor():
    """Find blood donors by blood group and location"""
    donors = None
    
    if request.method == 'POST':
        blood_group = request.form.get('blood_group', '').strip()
        location = request.form.get('location', '').strip().lower()
        
        if blood_group and location:
            all_donors = load_donors()
            # Filter donors by blood group and location (case insensitive partial match)
            donors = [
                d for d in all_donors 
                if d['blood_group'] == blood_group and location in d['location'].lower()
            ]
            
            # Add notification for admin
            search_details = {
                'blood_group': blood_group,
                'location': location,
                'results_found': len(donors) if donors else 0
            }
            add_notification(f"Someone searched for {blood_group} blood donors in {location}", search_details)
    
    return render_template('find_donor.html', donors=donors)


@app.route('/admin-kishore', methods=['GET', 'POST'])
def admin_login():
    """Admin login page"""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['admin_logged_in'] = True
            return redirect(url_for('admin_panel'))
        else:
            flash('Invalid username or password!', 'error')
    
    return render_template('admin_login.html')


@app.route('/admin-panel')
def admin_panel():
    """Admin panel to view all registered donors and notifications"""
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    
    donors = load_donors()
    notifications = load_notifications()
    
    # Count unread notifications
    unread_count = len([n for n in notifications if not n.get('read', True)])
    
    return render_template('admin.html', donors=donors, notifications=notifications, unread_count=unread_count)


@app.route('/mark-notification-read/<int:notification_id>')
def mark_notification_read(notification_id):
    """Mark a notification as read"""
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    
    notifications = load_notifications()
    for notification in notifications:
        if notification['id'] == notification_id:
            notification['read'] = True
            break
    
    save_notifications(notifications)
    return redirect(url_for('admin_panel'))


@app.route('/delete-donor/<int:donor_index>')
def delete_donor(donor_index):
    """Delete a donor from the system"""
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    
    donors = load_donors()
    if 0 <= donor_index < len(donors):
        deleted_donor = donors.pop(donor_index)
        save_donors(donors)
        flash(f'Donor {deleted_donor["name"]} has been deleted successfully.', 'success')
    else:
        flash('Invalid donor selection.', 'error')
    
    return redirect(url_for('admin_panel'))


@app.route('/delete-notification/<int:notification_id>')
def delete_notification(notification_id):
    """Delete a notification"""
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    
    notifications = load_notifications()
    notifications = [n for n in notifications if n['id'] != notification_id]
    save_notifications(notifications)
    flash('Notification deleted successfully.', 'success')
    
    return redirect(url_for('admin_panel'))


@app.route('/clear-all-notifications')
def clear_all_notifications():
    """Clear all notifications"""
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    
    save_notifications([])
    flash('All notifications cleared successfully.', 'success')
    
    return redirect(url_for('admin_panel'))


@app.route('/admin-logout')
def admin_logout():
    """Admin logout"""
    session.pop('admin_logged_in', None)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
