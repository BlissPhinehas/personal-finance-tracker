from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
import sqlite3
import os
from datetime import datetime

# Constants
UPLOAD_FOLDER = 'uploads'
MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB
SECRET_KEY = 'your-secret-key-change-in-production'

# Categories for transaction classification
TRANSACTION_CATEGORIES = {
    'Food': ['restaurant', 'cafe', 'grocery', 'food', 'pizza', 'starbucks', 'mcdonald'],
    'Transportation': ['gas', 'fuel', 'uber', 'lyft', 'taxi', 'metro', 'bus', 'parking'],
    'Shopping': ['amazon', 'walmart', 'target', 'mall', 'store', 'shopping', 'clothes'],
    'Bills': ['electric', 'water', 'internet', 'phone', 'rent', 'mortgage', 'insurance'],
    'Entertainment': ['movie', 'netflix', 'spotify', 'game', 'concert', 'theater'],
    'Healthcare': ['hospital', 'doctor', 'pharmacy', 'medical', 'dental', 'health'],
    'Income': ['salary', 'wage', 'payroll', 'deposit', 'income', 'refund']
}

app = Flask(__name__)
app.secret_key = SECRET_KEY
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

def init_db():
    """Initialize the SQLite database with required tables."""
    conn = sqlite3.connect('finance.db')
    cursor = conn.cursor()
    
    # Transactions table
    cursor.execute('''CREATE TABLE IF NOT EXISTS transactions
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      date TEXT NOT NULL,
                      description TEXT NOT NULL,
                      amount REAL NOT NULL,
                      category TEXT NOT NULL,
                      type TEXT NOT NULL,
                      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    
    # Budgets table
    cursor.execute('''CREATE TABLE IF NOT EXISTS budgets
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      category TEXT NOT NULL UNIQUE,
                      amount REAL NOT NULL,
                      month TEXT NOT NULL)''')
    
    # Savings goals table
    cursor.execute('''CREATE TABLE IF NOT EXISTS savings_goals
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      name TEXT NOT NULL,
                      target_amount REAL NOT NULL,
                      current_amount REAL DEFAULT 0,
                      target_date TEXT,
                      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    
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
def dashboard():
    """Main dashboard route."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Get recent transactions
    cursor.execute('SELECT * FROM transactions ORDER BY date DESC LIMIT 10')
    recent_transactions = cursor.fetchall()
    
    # Get monthly spending by category
    current_month = get_current_month()
    cursor.execute('''SELECT category, SUM(amount) FROM transactions 
                     WHERE date LIKE ? AND type = 'expense' 
                     GROUP BY category''', (current_month + '%',))
    spending_by_category = cursor.fetchall()
    
    # Get savings goals
    cursor.execute('SELECT * FROM savings_goals')
    savings_goals = cursor.fetchall()
    
    # Get total income vs expenses this month
    cursor.execute('''SELECT type, SUM(amount) FROM transactions 
                     WHERE date LIKE ? GROUP BY type''', (current_month + '%',))
    monthly_totals = dict(cursor.fetchall())
    
    conn.close()
    
    return render_template('dashboard.html', 
                         recent_transactions=recent_transactions,
                         spending_by_category=spending_by_category,
                         savings_goals=savings_goals,
                         monthly_income=monthly_totals.get('income', 0),
                         monthly_expenses=monthly_totals.get('expense', 0))

@app.route('/add_transaction', methods=['GET', 'POST'])
def add_transaction():
    """Add new transaction route."""
    if request.method == 'POST':
        date = request.form['date']
        description = request.form['description']
        amount = float(request.form['amount'])
        category = request.form['category']
        transaction_type = request.form['type']
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO transactions (date, description, amount, category, type) VALUES (?, ?, ?, ?, ?)',
                      (date, description, amount, category, transaction_type))
        conn.commit()
        conn.close()
        
        flash('Transaction added successfully!', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('add_transaction.html')

@app.route('/api/chart_data')
def chart_data():
    """API endpoint for chart data."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Spending by category
    current_month = get_current_month()
    cursor.execute('''SELECT category, SUM(amount) FROM transactions 
                     WHERE date LIKE ? AND type = 'expense' 
                     GROUP BY category''', (current_month + '%',))
    category_data = dict(cursor.fetchall())
    
    # Monthly trends
    cursor.execute('''SELECT strftime('%Y-%m', date) as month, 
                            SUM(CASE WHEN type = 'income' THEN amount ELSE 0 END) as income,
                            SUM(CASE WHEN type = 'expense' THEN amount ELSE 0 END) as expenses
                     FROM transactions 
                     WHERE date >= date('now', '-6 months')
                     GROUP BY month 
                     ORDER BY month''')
    monthly_trends = cursor.fetchall()
    
    conn.close()
    
    return jsonify({
        'category_data': category_data,
        'monthly_trends': monthly_trends
    })

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
    