# 🌸 Personal Finance Tracker 💕

A cute and interactive web application to track expenses, budgets, and savings goals with beautiful charts, user authentication, and automated categorization.

## ✨ Features

- 🔐 **User Authentication**: Secure login/register with password hashing
- 💰 **Transaction Management**: Add income and expenses with automatic categorization
- 🔄 **Recurring Transactions**: Set up monthly salary, bills, and subscriptions
- 📊 **Interactive Charts**: Beautiful visualizations of spending patterns
- 🎨 **Kawaii UI**: Adorable pastel design with animations and cute emojis
- 📱 **Responsive Design**: Works perfectly on desktop and mobile
- 🏷️ **Smart Categories**: Automatic transaction categorization (Food, Salary, Education, etc.)
- 👤 **Personal Data**: Each user sees only their own financial data
- 💾 **SQLite Database**: Lightweight local data storage

## 🛠️ Tech Stack

- **Backend**: Python 3.13, Flask 2.3.3
- **Database**: SQLite with user data isolation
- **Authentication**: Werkzeug password hashing, Flask sessions
- **Frontend**: HTML5, CSS3, Bootstrap 5
- **Charts**: Chart.js with custom pastel themes
- **Deployment**: Railway.app with automatic HTTPS
- **Security**: SQL injection protection, user data segregation

## 🔐 Security Features

### ✅ **Implemented Security Measures**

#### **Password Protection**
- **PBKDF2 Hashing**: Passwords stored using Werkzeug's secure hash functions
- **Salt Integration**: Each password gets unique salt for rainbow table protection
- **No Plain Text**: Original passwords never stored or logged

#### **Authentication System**
- **Session Management**: Encrypted session cookies for login state
- **User Isolation**: Database queries filtered by user_id
- **Login Protection**: Routes require authentication via `@login_required` decorator

#### **Database Security**
- **SQL Injection Protection**: Parameterized queries prevent malicious input
- **User Data Segregation**: Each user accesses only their own financial records
- **Structured Schema**: Foreign key relationships maintain data integrity

#### **Input Validation**
- **Date Restrictions**: Users cannot enter future dates for transactions
- **Required Fields**: Form validation prevents incomplete data submission
- **Type Safety**: Amount fields restricted to numerical input

### ⚠️ **Security Considerations for Production**

#### **Current Limitations (Suitable for Portfolio/Demo)**
- **Static Secret Key**: Hardcoded for development simplicity
- **Basic Session Security**: No automatic timeout or secure flags
- **No Rate Limiting**: Unlimited login attempts possible
- **SQLite Database**: File-based storage without enterprise access controls

#### **Production-Ready Improvements Needed**
```python
# Environment-based configuration
app.secret_key = os.environ.get('SECRET_KEY')

# Session security enhancements
app.permanent_session_lifetime = timedelta(hours=2)
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True

# Rate limiting (with Flask-Limiter)
@limiter.limit("5 per minute")
def login():
    # Login logic

# Database upgrades
# PostgreSQL with encrypted connections
# Database access logging and monitoring
```

## 🚀 Getting Started

### **Prerequisites**
- Python 3.7+ installed
- Git for version control
- Modern web browser

### **Local Development**

1. **Clone the repository**
   ```bash
   git clone https://github.com/BlissPhinehas/personal-finance-tracker.git
   cd personal-finance-tracker
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Initialize database**
   ```bash
   python app.py
   ```
   *Database tables are created automatically on first run*

4. **Access the application**
   ```
   http://127.0.0.1:5000
   ```

### **Production Deployment**

**Live Demo**: [https://web-production-892b.up.railway.app/](https://web-production-892b.up.railway.app/)

Deployed on Railway.app with:
- Automatic HTTPS encryption
- Container-based deployment
- Git-based continuous deployment
- Environment variable management

## 📸 Screenshots

### Dashboard Overview
- Monthly income/expense summaries with cute animations
- Interactive donut charts showing spending by category
- Recent transaction history with emoji categorization
- Responsive design adapting to screen sizes

### Transaction Management
- Form validation preventing future dates
- Recurring transaction setup (weekly/monthly/yearly)
- Auto-categorization based on transaction descriptions
- Real-time UI feedback with sparkle animations

### User Experience
- Secure login/registration with password confirmation
- Personalized greeting and user-specific data
- Floating animations and hover effects
- Artist signature for creative authenticity

## 🎯 Advanced Features

### **Automatic Categorization**
```python
TRANSACTION_CATEGORIES = {
    'Food': ['restaurant', 'cafe', 'grocery', 'starbucks'],
    'Salary': ['salary', 'wage', 'payroll', 'paycheck'],
    'Education': ['tuition', 'school', 'university', 'textbook'],
    # ... additional categories
}
```

### **Recurring Transaction Logic**
- Users can mark transactions as recurring
- Frequency options: weekly, monthly, quarterly, yearly
- Future enhancement: automatic recurring transaction creation

### **Data Visualization**
- Chart.js integration with custom pastel color schemes
- Real-time data updates via AJAX endpoints
- Mobile-responsive chart rendering

## 🔮 Future Enhancements

### **Short-term Roadmap**
- 📄 **CSV Import**: Bank statement upload and parsing
- 💰 **Budget Tracking**: Set monthly budgets with progress alerts
- 🎯 **Savings Goals**: Visual progress tracking toward financial targets
- 📊 **Advanced Reports**: Monthly/yearly financial summaries

### **Long-term Vision**
- 🔐 **Enhanced Security**: 2FA, session management, audit logging
- 📱 **Mobile App**: React Native companion application
- 🤖 **AI Features**: Spending pattern analysis and budget recommendations
- 💳 **Bank Integration**: API connections to financial institutions
- 📈 **Investment Tracking**: Portfolio management capabilities

## 🤝 Contributing

This project welcomes contributions! Areas for improvement:

- **Security enhancements** (rate limiting, session management)
- **Feature additions** (budget alerts, expense analytics)
- **UI/UX improvements** (accessibility, mobile optimization)
- **Testing coverage** (unit tests, integration tests)

## 📄 Technical Specifications

### **Database Schema**
```sql
-- Users table with authentication
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,  -- PBKDF2 hashed
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Transactions with user isolation
CREATE TABLE transactions (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,  -- Foreign key for data isolation
    date TEXT NOT NULL,
    description TEXT NOT NULL,
    amount REAL NOT NULL,
    category TEXT NOT NULL,
    type TEXT NOT NULL,        -- 'income' or 'expense'
    is_recurring BOOLEAN DEFAULT FALSE,
    recurring_frequency TEXT,  -- 'weekly', 'monthly', etc.
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id)
);
```

### **Security Architecture**
- **Authentication Flow**: Login → Session Creation → Route Protection
- **Data Access Pattern**: All queries filtered by authenticated user_id
- **Password Security**: PBKDF2 with automatic salting via Werkzeug
- **Session Management**: Flask's secure session handling with encrypted cookies

## 📊 Performance Metrics

- **Initial Load Time**: < 2 seconds on Railway deployment
- **Database Queries**: Optimized with user-specific filtering
- **Mobile Responsiveness**: Bootstrap 5 ensures cross-device compatibility
- **Chart Rendering**: Hardware-accelerated via Chart.js canvas implementation

## 📝 License

MIT License - feel free to use this for your own projects, learning, or portfolio demonstrations!

## 🎨 Credits

- **Design Philosophy**: Kawaii (cute) aesthetic with functional finance management
- **Color Palette**: Custom pastel gradients in pink, purple, and mint themes
- **Typography**: Google Fonts Nunito for friendly, readable interface
- **Icons**: Unicode emoji for universal compatibility and charm

---

**✨ Crafted with 💕 by [Bliss Phinehas](https://github.com/BlissPhinehas)**

*Made for learning, portfolio demonstration, and spreading financial literacy through cute design! 🌸*

---

### 📞 **Contact & Portfolio**

- **GitHub**: [BlissPhinehas](https://github.com/BlissPhinehas)
- **Live Demo**: [Kawaii Finance Tracker](https://web-production-892b.up.railway.app/)
- **Project Type**: Full-stack web application for internship portfolio

*"Combining technical skills with creative design to make finance management delightful!"* 💫
```