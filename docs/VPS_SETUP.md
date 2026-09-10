# VPS Deployment Guide

Panduan step-by-step deploy sniper bot ke VPS untuk 24/7 running.

## 📋 Requirements

- VPS dengan Ubuntu 20.04+ atau Debian
- Python 3.9+
- Node.js 16+
- SSH access ke VPS
- Minimal 1GB RAM

## 🔑 VPS Providers (Recommended)

Beberapa pilihan VPS murah:
- **DigitalOcean** - $5/bulan (1GB RAM, 25GB SSD)
- **Vultr** - $3.50/bulan (1GB RAM)
- **Linode** - $5/bulan (1GB RAM)
- **Tencent Cloud** - ~$3/bulan
- **AWS Lightsail** - $3.50/bulan

## 🚀 Step-by-Step Setup

### STEP 1: SSH ke VPS

```bash
ssh ubuntu@YOUR_VPS_IP
```

Ganti `YOUR_VPS_IP` dengan IP VPS Anda

Jika diminta password, enter password Anda

---

### STEP 2: Update System

```bash
sudo apt-get update
sudo apt-get upgrade -y
```

Tunggu selesai (bisa 5-10 menit)

---

### STEP 3: Install Python & Dependencies

```bash
sudo apt-get install -y python3 python3-pip python3-venv
```

Tunggu selesai

---

### STEP 4: Install Node.js (untuk PM2)

```bash
sudo apt-get install -y nodejs npm
```

Tunggu selesai

---

### STEP 5: Verify Installations

```bash
python3 --version
node --version
npm --version
```

Harusnya muncul versi setiap tool

---

### STEP 6: Create Bot Folder

```bash
mkdir -p ~/sniper-bot
cd ~/sniper-bot
```

---

### STEP 7: Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/advanced-sniper-bot.git .
```

Ganti `YOUR_USERNAME` dengan GitHub username Anda

Tunggu clone selesai

---

### STEP 8: Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

Seharusnya prompt berubah jadi `(venv) ubuntu@...`

---

### STEP 9: Install Python Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

Tunggu 2-5 menit

---

### STEP 10: Setup Configuration

```bash
cp .env.example .env
nano .env
```

Edit `.env` dengan:
- TARGET_CA: contract address
- PRIVATE_KEY: private key wallet
- TARGET_CHAIN: chain (base, ethereum, dll)

Save: `Ctrl+X`, `y`, `Enter`

---

### STEP 11: Test Bot Locally

```bash
python advanced_sniper_bot.py
```

Tunggu sampai muncul:

[INFO] ADVANCED SNIPER BOT
[INFO] Target: 0x...
[INFO] Chain: base
[MONITOR] ...


Stop bot: `Ctrl+C`

---

### STEP 12: Install PM2

```bash
sudo npm install -g pm2
```

Tunggu selesai

---

### STEP 13: Start Bot dengan PM2

```bash
pm2 start advanced_sniper_bot.py --name "sniper"
```

Tunggu instant

---

### STEP 14: Setup Auto-Startup

```bash
pm2 save
pm2 startup
```

Tunggu selesai

Copy output command dari `pm2 startup`, terus jalankan:

```bash
sudo env PATH=$PATH:/usr/bin /usr/lib/node_modules/pm2/bin/pm2 startup systemd -u ubuntu --hp /home/ubuntu
```

(Copy dari output, jangan hardcode!)

---

### STEP 15: Verify Bot Running

```bash
pm2 status
```

Harusnya show:

│ id │ name │ status │
│ 0 │ sniper │ online │


---

### STEP 16: View Logs

```bash
pm2 logs sniper
```

Tekan `Ctrl+C` untuk exit logs

---

### STEP 17: (Optional) Setup Firewall

```bash
sudo ufw enable
sudo ufw allow ssh
sudo ufw allow 22
```

---

## 📊 Monitor Bot

### Check Status

```bash
pm2 status
```

### View Logs

```bash
pm2 logs sniper          # Real-time
pm2 logs sniper --lines 50   # Last 50 lines
```

### Restart Bot

```bash
pm2 restart sniper
```

### Stop Bot

```bash
pm2 stop sniper
```

### View Positions (Trades)

```bash
sqlite3 advanced_sniper.db "SELECT * FROM positions;"
```

---

## 🔧 Common Tasks

### Update Bot Code

```bash
cd ~/sniper-bot
git pull origin main
pm2 restart sniper
```

### Change Configuration

```bash
nano .env
# Edit settings
pm2 restart sniper
```

### Backup Database

```bash
cp advanced_sniper.db advanced_sniper.db.backup
```

### View Bot Folder

```bash
ls -la ~/sniper-bot
```

### SSH into Folder

```bash
cd ~/sniper-bot
ls
```

---

## 🚨 Troubleshooting

### Bot tidak jalan

```bash
pm2 logs sniper
# Check logs untuk error message
```

### Python modules not found

```bash
source venv/bin/activate
pip install -r requirements.txt
```

### PM2 not found

```bash
sudo npm install -g pm2
```

### Cannot connect to VPS

```bash
# Check SSH key
ssh -v ubuntu@YOUR_VPS_IP

# Or use password
ssh ubuntu@YOUR_VPS_IP
```

### Bot using too much memory

```bash
# Setup auto-restart every hour
pm2 restart sniper --cron "0 * * * *"
```

---

## 💡 Tips & Best Practices

### Security
- ✓ Use strong VPS password
- ✓ Setup SSH key auth (more secure)
- ✓ Enable firewall
- ✓ Never share .env file
- ✓ Backup database regularly

### Performance
- ✓ Monitor logs regularly
- ✓ Check CPU/Memory usage: `pm2 monit`
- ✓ Setup log rotation (avoid disk full)
- ✓ Backup database weekly

### Maintenance
- ✓ Update OS monthly: `sudo apt-get update && upgrade`
- ✓ Update Python packages: `pip install --upgrade pip`
- ✓ Check disk space: `df -h`
- ✓ Monitor processes: `ps aux | grep python`

---

## 📞 Quick Commands

```bash
# Connect to VPS
ssh ubuntu@YOUR_VPS_IP

# Go to bot folder
cd ~/sniper-bot

# Activate venv
source venv/bin/activate

# Check bot status
pm2 status

# View logs
pm2 logs sniper

# Restart bot
pm2 restart sniper

# View database
sqlite3 advanced_sniper.db "SELECT * FROM positions;"

# Backup database
cp advanced_sniper.db advanced_sniper.db.backup
```

---

## ⚠️ Important Notes

1. **Bot runs 24/7** - Even if laptop is off
2. **Auto-restart** - PM2 automatically restart jika crash
3. **Auto-boot** - Bot auto-start setelah VPS reboot
4. **Database persists** - Semua trades saved di database
5. **Secure wallet** - Use separate wallet (not main funds)

---

Made with ❤️ for 24/7 snipers!
