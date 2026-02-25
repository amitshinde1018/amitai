# DataStructure067 — Login System Setup

## 📁 Project Structure
```
ds067/
├── app.py
├── requirements.txt
├── setup.sql
└── templates/
    ├── login.html
    ├── signup.html
    └── dashboard.html
```

---

## ⚙️ Step 1 — Python Packages Install करा

Terminal मध्ये हे run करा:

```bash
pip install Flask Flask-MySQLdb bcrypt
```

---

## 🗄️ Step 2 — MySQL Database बनवा

MySQL मध्ये login करा आणि `setup.sql` run करा:

```bash
mysql -u root -p < setup.sql
```

किंवा phpMyAdmin मध्ये `setup.sql` चा content paste करा आणि run करा.

---

## 🔧 Step 3 — app.py मध्ये MySQL details बदला

```python
app.config['MYSQL_HOST']     = 'localhost'
app.config['MYSQL_USER']     = 'root'       # ← तुमचा username
app.config['MYSQL_PASSWORD'] = ''           # ← तुमचा password
app.config['MYSQL_DB']       = 'ds067_db'
```

---

## 🚀 Step 4 — Server Start करा

```bash
python app.py
```

Browser मध्ये उघडा: **http://localhost:5000**

---

## ✅ Features
- `/login`    — Login page
- `/signup`   — New user registration  
- `/dashboard`— Login झाल्यावर दिसते
- `/logout`   — Session clear होते
- Password bcrypt ने hash होतो (secure!)
