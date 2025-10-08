# ✨ myquery Features

## 🚀 Auto-Connect Everywhere

**NEW!** myquery sekarang auto-connect di SEMUA command jika credentials sudah ada di `.env`!

### Sebelum (Manual Connect):
```bash
# Harus connect dulu
python -m cli.main connect db --db-type postgresql --db-name mydb --db-user admin

# Baru bisa chat
python -m cli.main chat start

# Atau execute query
python -m cli.main query execute "Show data"
```

### Sekarang (Auto-Connect): 🎉
```bash
# Set .env SEKALI SAJA:
# DB_TYPE=postgresql
# DB_NAME=mydb
# DB_USER=admin
# DB_PASSWORD=secret

# Langsung chat! Auto-connect otomatis
python -m cli.main chat start

# Atau langsung query! Auto-connect juga
python -m cli.main query execute "Show data"

# Atau raw SQL! Tetap auto-connect
python -m cli.main query sql "SELECT COUNT(*) FROM users"
```

## 🎯 Kapan Auto-Connect Bekerja?

Auto-connect **ENABLED by default** di semua command berikut:

### 1. ✅ Chat Command
```bash
python -m cli.main chat start
# ↑ Auto-connects menggunakan .env atau saved session
```

### 2. ✅ Query Execute
```bash
python -m cli.main query execute "Show all customers"
# ↑ Auto-connects jika belum connected
```

### 3. ✅ Query SQL
```bash
python -m cli.main query sql "SELECT * FROM orders LIMIT 10"
# ↑ Auto-connects jika belum connected
```

## 🔧 Disable Auto-Connect

Jika ingin manual control, gunakan flag `--no-auto`:

```bash
# Chat tanpa auto-connect
python -m cli.main chat start --no-auto

# Query tanpa auto-connect
python -m cli.main query execute "Show data" --no-auto

# SQL tanpa auto-connect
python -m cli.main query sql "SELECT 1" --no-auto
```

## 📋 Prioritas Credentials

myquery mencari credentials dalam urutan ini:

1. **Command-line flags** (highest priority)
   ```bash
   python -m cli.main connect db --db-type sqlite --db-name other.db
   ```

2. **.env file** (recommended untuk default database)
   ```env
   DB_TYPE=postgresql
   DB_NAME=mydb
   DB_USER=admin
   DB_PASSWORD=secret
   ```

3. **Saved session** (.myquery_session.json)
   - Dibuat otomatis saat connect dengan flag `--save`

## 🎨 Smart Behavior

### Scenario 1: .env Lengkap ✅
```env
DB_TYPE=postgresql
DB_NAME=mydb
DB_USER=admin
DB_PASSWORD=secret
```
```bash
# Langsung jalan, gak perlu apa-apa!
python -m cli.main chat start
```

### Scenario 2: .env Tanpa Password 🔐
```env
DB_TYPE=postgresql
DB_NAME=mydb
DB_USER=admin
# DB_PASSWORD tidak diset (lebih aman!)
```
```bash
# Akan minta password saat connect
python -m cli.main chat start
🔐 Database password: ****
```

### Scenario 3: .env Partial, Override dengan Flag 🔧
```env
DB_TYPE=postgresql
DB_USER=admin
DB_PASSWORD=secret
```
```bash
# Gunakan .env untuk credentials, tapi connect ke database lain
python -m cli.main chat start --db-name analytics_db
```

### Scenario 4: Gak Ada .env ❌
```bash
python -m cli.main chat start
# Error dengan helpful message:
# ❌ Database credentials not configured.
# Please either:
# 1. Set DB_TYPE and DB_NAME in .env file
# 2. Run: python -m cli.main connect db --db-type <type> --db-name <name>
```

## 💡 Best Practices

### Untuk Development
```env
# .env (local development)
DB_TYPE=sqlite
DB_NAME=dev.db
```
```bash
# Super quick untuk testing!
python -m cli.main chat start
```

### Untuk Production
```env
# .env (production)
DB_TYPE=postgresql
DB_HOST=prod-server.com
DB_NAME=prod_db
DB_USER=app_user
# Jangan simpan password di .env untuk production!
# Akan diminta saat connect
```
```bash
# Secure: password diminta, tidak di .env
python -m cli.main chat start
🔐 Database password: ****
```

### Multiple Databases
```bash
# Database default (dari .env)
python -m cli.main chat start

# Switch ke database lain
python -m cli.main query execute "Show stats" --db-name analytics

# Atau save multiple sessions
python -m cli.main connect db --db-name sales --save
python -m cli.main connect restore  # Restore saved session
```

## 🛡️ Security Features

1. **Password tidak pernah disave** di session file
2. **Password diminta interactively** jika tidak ada di .env
3. **Environment variables** lebih aman daripada command-line (tidak muncul di history)
4. **Session file** hanya menyimpan non-sensitive info (host, user, db name)

## 🎯 Use Cases

### Quick Analysis
```bash
# Set .env sekali
# Lalu langsung query kapan saja!
python -m cli.main query execute "Show revenue trends"
python -m cli.main query execute "Top customers this month"
python -m cli.main query execute "Inventory status"
```

### Interactive Exploration
```bash
# Chat mode dengan auto-connect
python -m cli.main chat start

You: What tables exist?
You: Show me sample data from users
You: How many active customers?
You: What's the total revenue?
```

### Scripting & Automation
```bash
#!/bin/bash
# Auto-connects menggunakan .env
python -m cli.main query execute "Daily sales report" > report.txt
python -m cli.main query execute "Customer signups today" >> report.txt
```

## 📊 Connection Status

Check konfigurasi kapan saja:
```bash
python -m cli.main connect status
```

Output:
```
⚙️  .env Configuration
┌─────────────────────────┐
│ Type: postgresql        │
│ Database: mydb          │
│ Host: localhost         │
│ User: admin             │
└─────────────────────────┘

💾 Saved Session
┌─────────────────────────┐
│ Type: postgresql        │
│ Database: prod_db       │
│ Host: prod-server.com   │
│ User: app_user          │
└─────────────────────────┘
```

---

**Made easier with auto-connect! 🚀**

