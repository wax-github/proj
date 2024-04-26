from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import random

app = Flask(__name__)

# Configure Flask-Login
app.secret_key = 'your_secret_key'
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Mock User model
class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = generate_password_hash(password)

# Mock user database
users = {
    1: User(1, 'admin', 'password'),
    2: User(2, 'testuser', 'testpassword')
}

sellers = {
    'john_doe': {'name': 'John Doe', 'email': 'john@example.com'}
}

#transactions
@app.route('/transactions')
@login_required  # Ensure this page is accessed by logged-in users only
def transactions():
    # Placeholder data to simulate transactions
    transactions = [
        {'id': 1, 'type': 'Ticket Purchase', 'status': 'In Progress', 'details': 'Concert A - Section B, Row 5'},
        {'id': 2, 'type': 'Ticket Sale', 'status': 'Completed', 'details': 'Theatre B - Section A, Row 3'},
        {'id': 3, 'type': 'Ticket Exchange', 'status': 'Pending', 'details': 'Event C - Section C, Row 10'}
    ]
    return render_template('transactions.html', transactions=transactions)


#contact seller button
@app.route('/contact_seller/<seller_id>', methods=['GET'])
def contact_seller(seller_id):
    # Assume you fetch seller details from a database or a dictionary
    seller = sellers.get(seller_id)
    if seller:
        return render_template('contact_seller.html', seller=seller)
    else:
        flash('Seller not found.')
        return redirect(url_for('homepage'))

#sending message   
@app.route('/send_message', methods=['POST'])
def send_message():
    seller_name = request.form.get('sellerName')
    message = request.form.get('message')

    # Here you would typically send an email or store the message in a database
    print(f"Message to {seller_name}: {message}")  # Just for demonstration; replace with actual logic

    flash('Your message has been sent successfully!')
    return redirect(url_for('homepage'))
    
@login_manager.user_loader
def load_user(user_id):
    return users.get(int(user_id))

# Routes for features
@app.route('/feature1')
def feature1():
    return "Feature 1 Page"

# Add other feature routes here...

@app.route('/')
def homepage():
    # Example data for upcoming events
    events = [
    {"name": "Concert A", "date": "2024-05-01", "location": "Venue X", "start_time": "2024-05-01T19:00:00"},
    {"name": "Theatre B", "date": "2024-05-10", "location": "Venue Y", "start_time": "2024-05-10T18:30:00"},
    {"name": "Event C", "date": "2024-06-15", "location": "Venue Z", "start_time": "2024-06-15T20:00:00"},
    {"name": "New Concert", "date": "2024-07-20", "location": "Venue A", "tickets_available": 80,"start_time": "2024-05-01T19:00:00"},
    {"name": "Festival D", "date": "2024-08-05", "location": "Venue B", "tickets_available": 120,"start_time": "2024-05-01T19:00:00"},
    {"name": "Theatre E", "date": "2024-09-15", "location": "Venue C", "tickets_available": 60,"start_time": "2024-05-01T19:00:00"}
    ]

    random.shuffle(events)
    user_logged_in = current_user.is_authenticated  # Properly retrieve the user's logged-in status
    return render_template('homepage.html', events=events, user_logged_in=user_logged_in)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = next((user for user in users.values() if user.username == username), None)
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('homepage'))
        else:
            return "Login Failed", 401
    return render_template('login.html')

@app.route('/logout', methods=['POST'])
@login_required
def perform_logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Here, you would handle user registration
        username = request.form['username']
        password = request.form['password']
        # You would typically save these details in a database
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/buy')
@login_required
def buy_ticket():
    return render_template('buy.html')

@app.route('/concert_a_details')
def concert_a_details():
    return render_template('concert_a_details.html')

@app.route('/sell')
@login_required
def sell_ticket():
    return render_template('sell.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/search')
def search():
    query = request.args.get('query', '')
    event_type = request.args.get('type', '')
    date = request.args.get('date', '')

    # Simulating event data retrieval and filtering
    # In real applications, replace this with actual database query logic
    all_events = [
        {'name': 'Concert A', 'type': 'concert', 'date': '2024-05-01'},
        {'name': 'Theatre B', 'type': 'theatre', 'date': '2024-05-10'},
        {'name': 'Festival C', 'type': 'festival', 'date': '2024-06-15'}
    ]

    filtered_events = [event for event in all_events if
                       (query.lower() in event['name'].lower() if query else True) and
                       (event['type'] == event_type if event_type else True) and
                       (event['date'] == date if date else True)]

    return render_template('search_results.html', events=filtered_events)

@app.route('/account')
@login_required
def account():
    # Fetch user information from the current_user object provided by Flask-Login
    user = current_user
    user = load_user(current_user.id)
    return render_template('account.html', user=user)

@app.route('/update_profile', methods=['GET', 'POST'])
@login_required
def update_profile():
    user = load_user(current_user.id)
    if request.method == 'POST':
        # Update user profile information based on form input
        user.username = request.form['username']
        user.email = request.form['email']
        # Save the updated user object (not implemented for simplicity)
        return redirect(url_for('account'))
    return render_template('update_profile.html', user=user)

@app.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    if request.method == 'POST':
        # Update user's password (not implemented for simplicity)
        return redirect(url_for('account'))
    return render_template('change_password.html')

@app.route('/delete_account', methods=['GET', 'POST'])
@login_required
def delete_account():
    if request.method == 'POST':
        # Delete user account (not implemented for simplicity)
        logout_user()  # Log out the user after deleting the account
        return redirect(url_for('homepage'))
    return render_template('delete_account.html')

if __name__ == '__main__':
    app.run(debug=True)
