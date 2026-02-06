

# 🌸 Personal Finance Tracker 💕

**Live Demo:** [Kawaii Finance Tracker](https://web-production-892b.up.railway.app/)

A cute and interactive web app for tracking expenses, budgets, and savings goals. It features user authentication, automated categorization, and beautiful visualizations — all wrapped in a fun pastel design.

---

## ✨ Features

* 🔐 **User Authentication**: Secure login/register with password hashing
* 💰 **Transaction Management**: Add income and expenses with smart categorization
* 🔄 **Recurring Transactions**: Handle salaries, bills, and subscriptions automatically
* 📊 **Interactive Charts**: Visualize spending and income patterns
* 🎨 **Kawaii UI**: Soft pastel theme with animations and emojis
* 📱 **Responsive Design**: Optimized for desktop and mobile
* 👤 **Private Data**: Each user sees only their own records
* 💾 **SQLite Database**: Lightweight, easy to deploy

---

## 🛠️ Tech Stack

* **Backend:** Python (Flask)
* **Frontend:** HTML5, CSS3, Bootstrap 5
* **Database:** SQLite (with user isolation)
* **Authentication:** Werkzeug password hashing, Flask sessions
* **Charts:** Chart.js with custom pastel themes
* **Deployment:** Railway.app (HTTPS + Git CI/CD)

---

## 🔐 Security Overview

* **Hashed Passwords (PBKDF2)** with unique salts
* **Encrypted Sessions** for login state
* **Parameterized Queries** to prevent SQL injection
* **User Data Isolation** through foreign key relationships
* **Input Validation** for date, type, and completeness

**For production:**
Add environment-based config, secure cookies, rate limiting, and switch to PostgreSQL with encryption.

---

## 🚀 Getting Started

### Prerequisites

* Python 3.7+
* Git installed

### Setup

```bash
git clone https://github.com/BlissPhinehas/personal-finance-tracker.git
cd personal-finance-tracker
pip install -r requirements.txt
python app.py
```

Visit [http://127.0.0.1:5000]([APP LINK](https://web-production-892b.up.railway.app/login))

---

## 📸 Screenshots

<img width="1901" height="516" alt="image" src="https://github.com/user-attachments/assets/69bbf05d-64ee-4bea-b535-e8e8d02ec991" /> 
<img width="1919" height="994" alt="image" src="https://github.com/user-attachments/assets/309fbe50-9db8-452c-92a6-2b1941f41463" /> 
<img width="1919" height="994" alt="image" src="https://github.com/user-attachments/assets/f19fcfae-689e-44f7-8a0d-1bf1f1e83b10" /> 
<img width="1917" height="998" alt="image" src="https://github.com/user-attachments/assets/30d8c342-3ae3-45a8-8219-3535f68b8064" />


---

## 🎯 Advanced Features

* 🏷️ **Automatic Categorization** based on keywords
* 🔁 **Recurring Transaction Logic** with frequency options
* 📊 **Real-Time Charts** via AJAX updates

---

## 🔮 Future Enhancements

* 📄 CSV import for bank statements
* 💰 Budget tracking and savings goals
* 📈 Advanced financial reports
* 🔐 2FA and session management
* 🤖 AI-based spending insights
* 📱 Mobile app (React Native)

---

## 🤝 Contributing

Open to suggestions and pull requests for:

* Security improvements
* New financial features
* UI/UX optimization
* Testing coverage

---

## 📄 License

**MIT License** – Free to use and modify for learning or personal projects.

---

## 🎨 Credits

* **Design:** Kawaii-inspired pastel theme
* **Typography:** Nunito (Google Fonts)
* **Icons:** Unicode emojis

---

### 📞 Contact & Portfolio

* **GitHub:** [BlissPhinehas](https://github.com/BlissPhinehas)
* **Live Demo:** [Kawaii Finance Tracker](https://web-production-892b.up.railway.app/)

> *“Combining technical skills with creative design to make finance management delightful!”* 💫

---
