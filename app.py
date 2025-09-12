from flask import Flask, render_template, request, redirect, url_for, jsonify, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import os
from datetime import datetime, timedelta
from functools import wraps

# Constants
UPLOAD_FOLDER = 'uploads'
MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB

# Use environment variable for secret key
SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-key-change-in-production')

# Categories for transaction classification
TRANSACTION_CATEGORIES = {
    'Food': ['restaurant', 'cafe', 'grocery', 'food', 'pizza', 'starbucks', 'mcdonald'],
    'Transportation': ['gas', 'fuel', 'uber', 'lyft', 'taxi', 'metro', 'bus', 'parking'],
    'Shopping': ['amazon', 'walmart', 'target', 'mall', 'store', 'shopping', 'clothes'],
    'Bills': ['electric', 'water', 'internet', 'phone', 'rent', 'mortgage', 'insurance'],
    'Entertainment': ['movie', 'netflix', 'spotify', 'game', 'concert', 'theater'],
    'Healthcare': ['hospital', 'doctor', 'pharmacy', 'medical', 'dental', 'health'],
    'Education': ['tuition', 'school', 'university', 'course', 'textbook', 'education'],
    'Salary': ['salary', 'wage', 'payroll', 'paycheck', 'income', 'bonus'],
    'Investment': ['stock', 'crypto', 'dividend', 'investment', 'trading'],
    'Savings': ['savings', 'emergency fund', 'deposit'],
    'Other': []
}

app = Flask(__name__)
app.secret_key = SECRET_KEY
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

# Set session lifetime for security
app.permanent_session_lifetime = timedelta(hours=2)

# Redirect root to login if not authenticated
@app.before_request
def require_login():
    allowed_routes = ['login', 'register', 'static']
    if request.endpoint not in allowed_routes and 'user_id' not in session:
        return redirect(url_for('login'))

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT id, password FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()
        conn.close()
        
        if user and check_password_hash(user[1], password):
            session['user_id'] = user[0]
            session['username'] = username
            flash(f'Welcome back, {username}! 💕', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password! 😿', 'error')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Check if username exists
        cursor.execute('SELECT id FROM users WHERE username = ?', (username,))
        if cursor.fetchone():
            flash('Username already exists! Try another one! 🌸', 'error')
            conn.close()
            return render_template('register.html')
        
        # Create new user
        hashed_password = generate_password_hash(password)
        cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', 
                      (username, hashed_password))
        conn.commit()
        
        # Auto-login new user
        cursor.execute('SELECT id FROM users WHERE username = ?', (username,))
        user_id = cursor.fetchone()[0]
        session['user_id'] = user_id
        session['username'] = username
        
        conn.close()
        flash(f'Welcome to Kawaii Finance, {username}! ✨', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('register.html')

@app.route('/logout')
def logout():
    username = session.get('username', 'Friend')
    session.clear()
    flash(f'Goodbye, {username}! See you soon! 👋💕', 'success')
    return redirect(url_for('login'))

def init_db():
    """Initialize the SQLite database with required tables."""
    conn = sqlite3.connect('finance.db')
    cursor = conn.cursor()
    
    # Users table
    cursor.execute('''CREATE TABLE IF NOT EXISTS users
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      username TEXT UNIQUE NOT NULL,
                      password TEXT NOT NULL,
                      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    
    # Transactions table with proper structure
    cursor.execute('''CREATE TABLE IF NOT EXISTS transactions
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      user_id INTEGER NOT NULL,
                      date TEXT NOT NULL,
                      description TEXT NOT NULL,
                      amount REAL NOT NULL,
                      category TEXT NOT NULL,
                      type TEXT NOT NULL,
                      is_recurring BOOLEAN DEFAULT FALSE,
                      recurring_frequency TEXT,
                      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                      FOREIGN KEY (user_id) REFERENCES users (id))''')
    
    # Budgets table
    cursor.execute('''CREATE TABLE IF NOT EXISTS budgets
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      user_id INTEGER NOT NULL,
                      category TEXT NOT NULL,
                      amount REAL NOT NULL,
                      month TEXT NOT NULL,
                      FOREIGN KEY (user_id) REFERENCES users (id))''')
    
    # Savings goals table
    cursor.execute('''CREATE TABLE IF NOT EXISTS savings_goals
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      user_id INTEGER NOT NULL,
                      name TEXT NOT NULL,
                      target_amount REAL NOT NULL,
                      current_amount REAL DEFAULT 0,
                      target_date TEXT,
                      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                      FOREIGN KEY (user_id) REFERENCES users (id))''')
    
    conn.commit()
    conn.close()

def classify_transaction(description):
    """
    Classify a transaction based on its description.
    :param description: Transaction description string
    :return: Category name
    """
    description = description.lower()
    
    for category, keywords in TRANSACTION_CATEGORIES.items():
        if any(keyword in description for keyword in keywords):
            return category
    
    return 'Other'

def get_db_connection():
    """Get database connection."""
    return sqlite3.connect('finance.db')

def get_current_month():
    """Get current month in YYYY-MM format."""
    return datetime.now().strftime('%Y-%m')

@app.route('/')
@login_required
def dashboard():
    """Main dashboard route."""
    conn = get_db_connection()
    cursor = conn.cursor()
    user_id = session['user_id']
    
    # Get recent transactions with explicit column selection
    cursor.execute('''SELECT id, user_id, date, description, amount, category, type, 
                             is_recurring, recurring_frequency, created_at 
                      FROM transactions 
                      WHERE user_id = ? 
                      ORDER BY date DESC, created_at DESC 
                      LIMIT 10''', (user_id,))
    recent_transactions = cursor.fetchall()
    
    # Get monthly spending by category for current user
    current_month = get_current_month()
    cursor.execute('''SELECT category, SUM(amount) FROM transactions 
                     WHERE user_id = ? AND date LIKE ? AND type = 'expense' 
                     GROUP BY category''', (user_id, current_month + '%'))
    spending_by_category = cursor.fetchall()
    
    # Get savings goals for current user
    cursor.execute('SELECT * FROM savings_goals WHERE user_id = ?', (user_id,))
    savings_goals = cursor.fetchall()
    
    # Get total income vs expenses this month for current user
    cursor.execute('''SELECT type, SUM(amount) FROM transactions 
                     WHERE user_id = ? AND date LIKE ? GROUP BY type''', (user_id, current_month + '%'))
    monthly_totals = dict(cursor.fetchall())
    
    # Debug print
    print(f"Monthly totals: {monthly_totals}")
    print(f"Recent transactions: {recent_transactions[:2]}")  # First 2 transactions
    
    conn.close()
    
    return render_template('dashboard.html', 
                         recent_transactions=recent_transactions,
                         spending_by_category=spending_by_category,
                         savings_goals=savings_goals,
                         monthly_income=monthly_totals.get('income', 0),
                         monthly_expenses=monthly_totals.get('expense', 0))

@app.route('/api/chart_data')
@login_required
def chart_data():
    """API endpoint for chart data."""
    conn = get_db_connection()
    cursor = conn.cursor()
    user_id = session['user_id']
    
    # Spending by category for current user
    current_month = get_current_month()
    cursor.execute('''SELECT category, SUM(amount) FROM transactions 
                     WHERE user_id = ? AND date LIKE ? AND type = 'expense' 
                     GROUP BY category''', (user_id, current_month + '%'))
    category_data = dict(cursor.fetchall())
    
    # Monthly trends for current user
    cursor.execute('''SELECT strftime('%Y-%m', date) as month, 
                            SUM(CASE WHEN type = 'income' THEN amount ELSE 0 END) as income,
                            SUM(CASE WHEN type = 'expense' THEN amount ELSE 0 END) as expenses
                     FROM transactions 
                     WHERE user_id = ? AND date >= date('now', '-6 months')
                     GROUP BY month 
                     ORDER BY month''', (user_id,))
    monthly_trends = cursor.fetchall()
    
    conn.close()
    
    return jsonify({
        'category_data': category_data,
        'monthly_trends': monthly_trends
    })

@app.route('/add_transaction', methods=['GET', 'POST'])
@login_required
def add_transaction():
    """Add new transaction route."""
    if request.method == 'POST':
        try:
            date = request.form['date']
            description = request.form['description']
            amount = float(request.form['amount'])  # Ensure it's a float
            category = request.form['category']
            transaction_type = request.form['type']
            is_recurring = 'is_recurring' in request.form
            recurring_frequency = request.form.get('recurring_frequency', '') if is_recurring else ''
            
            # Debug print
            print(f"Adding transaction: {description}, {amount}, {category}, {transaction_type}")
            
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('''INSERT INTO transactions 
                             (user_id, date, description, amount, category, type, is_recurring, recurring_frequency) 
                             VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                          (session['user_id'], date, description, amount, category, transaction_type, 
                           is_recurring, recurring_frequency))
            conn.commit()
            conn.close()
            
            if is_recurring:
                flash(f'Recurring transaction added! It will repeat {recurring_frequency}! 🔄✨', 'success')
            else:
                flash('Transaction added successfully! 💫', 'success')
            return redirect(url_for('dashboard'))
            
        except ValueError as e:
            flash(f'Please enter a valid amount! Error: {str(e)} 💸', 'error')
        except Exception as e:
            flash(f'Error adding transaction: {str(e)} 😿', 'error')
    
    return render_template('add_transaction.html')

@app.route('/delete_transaction/<int:transaction_id>', methods=['POST'])
@login_required
def delete_transaction(transaction_id):
    """Delete a transaction."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Verify transaction belongs to current user
    cursor.execute('SELECT id FROM transactions WHERE id = ? AND user_id = ?', 
                   (transaction_id, session['user_id']))
    
    if cursor.fetchone():
        cursor.execute('DELETE FROM transactions WHERE id = ? AND user_id = ?', 
                       (transaction_id, session['user_id']))
        conn.commit()
        flash('Transaction deleted! 🗑️✨', 'success')
    else:
        flash('Transaction not found! 😿', 'error')
    
    conn.close()
    return redirect(url_for('dashboard'))

@app.route('/users_debug')
def users_debug():
    """Debug route to check users."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, created_at FROM users")
    users = cursor.fetchall()
    conn.close()
    return jsonify({'users': users})

# Debug route to check database
@app.route('/debug')
@login_required
def debug():
    """Debug route to check database structure."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Get table structure
    cursor.execute("PRAGMA table_info(transactions)")
    columns = cursor.fetchall()
    
    # Get sample data
    cursor.execute("SELECT * FROM transactions LIMIT 5")
    transactions = cursor.fetchall()
    
    conn.close()
    
    return jsonify({
        'columns': columns,
        'sample_transactions': transactions
    })

if __name__ == '__main__':
    init_db()
    app.run(debug=True)