# Troubleshooting Guide

Common issues & solutions untuk sniper bot.

## 🔴 Bot Errors

### Error: "Cannot fetch pair data"

**Cause:** Token belum listed di Dexscreener atau contract address salah

**Solution:**
```bash
# Check contract address
# Buka: https://basescan.org/address/YOUR_CA
# Verify token sudah ada di Dexscreener
# https://dexscreener.com/base/YOUR_CA

# Jika belum ada, tunggu sampai token launch
# Bot akan auto-detect begitu ada liquidity pool
```

---

### Error: "AttributeError: type object has no attribute..."

**Cause:** Bot code incomplete atau corrupt

**Solution:**
```bash
# Re-download bot file
cd ~/sniper-bot
git pull origin main

# Restart
pm2 restart sniper
```

---

### Error: "ModuleNotFoundError: No module named 'web3'"

**Cause:** Python dependencies tidak terinstall

**Solution:**
```bash
# Activate venv
source venv/bin/activate

# Install requirements
pip install -r requirements.txt

# Verify
pip list | grep web3
```

---

### Error: "Invalid private key"

**Cause:** PRIVATE_KEY di .env salah format

**Solution:**
```bash
# Check format harus: 0x + 64 hex characters

# Wrong: 0x123 (terlalu pendek)
# Wrong: 123abc (tanpa 0x)
# Correct: 0x9exxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxd5

# Fix di .env
nano .env
# Verify private key format
```

---

### Error: "Insufficient balance"

**Cause:** Wallet tidak punya cukup ETH untuk buy

**Solution:**
```bash
# Check wallet balance
# MetaMask / Wallet app

# Fund wallet dengan ETH
# Send ETH ke wallet address

# Reduce BUY_AMOUNT_ETH di .env
nano .env
# Change: BUY_AMOUNT_ETH=0.001 → 0.0005
pm2 restart sniper
```

---

### Error: "Cannot connect to RPC"

**Cause:** RPC endpoint error atau network issue

**Solution:**
```bash
# Check internet connection
ping google.com

# Restart bot
pm2 restart sniper

# Check logs
pm2 logs sniper
```

---

## 🟡 Bot Not Triggering

### Bot Running but Never Buys

**Symptoms:** Logs show MONITOR tapi never trigger

**Common Causes:**

1. **Token doesn't meet filters**
   - Volume < $1000 ❌
   - MCap < $5000 atau > $100000 ❌
   - Liquidity < $500 ❌

**Solution:**
```bash
# Check logs untuk filter breakdown
pm2 logs sniper

# Adjust filters di .env kalau terlalu strict
nano .env
# Reduce MIN_VOLUME, increase MAX_MCAP
pm2 restart sniper
```

2. **Wrong chain setting**
   - Bot monitoring Base tapi token di Ethereum

**Solution:**
```bash
# Verify TARGET_CHAIN di .env
cat .env | grep TARGET_CHAIN

# Ganti ke correct chain
nano .env
# Change TARGET_CHAIN=base → ethereum
pm2 restart sniper
```

3. **Contract address wrong**
   - CA tidak valid atau salah chain

**Solution:**
```bash
# Verify CA di block explorer
# Base: https://basescan.org
# Ethereum: https://etherscan.io

# Jika salah, update di .env
nano .env
# Update TARGET_CA
pm2 restart sniper
```

---

### Bot Bought but Didn't Sell at TP

**Symptoms:** Position open tapi tidak auto-sell

**Cause:** Bot crashed atau stopped

**Solution:**
```bash
# Check if bot running
pm2 status

# If not running, restart
pm2 restart sniper

# Check position status
sqlite3 advanced_sniper.db "SELECT * FROM positions;"

# Manual sell (jika TP tercapai)
# Use your wallet to manually sell via DEX
```

---

## 🔵 PM2 Issues

### PM2: "command not found"

**Cause:** PM2 tidak terinstall

**Solution:**
```bash
sudo npm install -g pm2
pm2 --version
```

---

### PM2: Bot not auto-starting after reboot

**Cause:** pm2 startup tidak setup dengan benar

**Solution:**
```bash
# Re-setup startup
pm2 startup
# Copy output command & run it

pm2 save
pm2 startup
```

---

### PM2: Too many logs (disk full)

**Cause:** Log files growing too big

**Solution:**
```bash
# Clear PM2 logs
pm2 flush

# Or rotate logs
pm2 install pm2-logrotate

# Or delete old logs
rm ~/.pm2/logs/*
```

---

### PM2: High memory usage

**Cause:** Memory leak dalam bot

**Solution:**
```bash
# Check memory usage
pm2 monit

# Setup auto-restart every hour
pm2 restart sniper --cron "0 * * * *"

# Or set memory limit
pm2 delete sniper
pm2 start advanced_sniper_bot.py --name "sniper" --max-memory-restart 500M
```

---

## 🟠 Database Issues

### Error: "database is locked"

**Cause:** Multiple processes accessing database

**Solution:**
```bash
# Stop bot
pm2 stop sniper

# Check database
sqlite3 advanced_sniper.db ".status"

# Restart bot
pm2 restart sniper
```

---

### Cannot query database

**Cause:** Syntax error atau database corrupt

**Solution:**
```bash
# Verify database
sqlite3 advanced_sniper.db "SELECT COUNT(*) FROM positions;"

# Backup database
cp advanced_sniper.db advanced_sniper.db.backup

# Restart bot (akan auto-repair)
pm2 restart sniper
```

---

### Lost positions data

**Cause:** Database deleted atau corrupted

**Solution:**
```bash
# If you have backup
cp advanced_sniper.db.backup advanced_sniper.db

# If no backup, database will recreate
# But historical data will be lost
# Start fresh next time with backup
```

---

## 🟢 Network Issues

### Connection timeout to DEX

**Cause:** Network latency atau DEX down

**Solution:**
```bash
# Check internet
ping 1.1.1.1

# Check DEX status (Dexscreener)
# Visit https://dexscreener.com

# Wait dan retry
# Bot auto-retry setiap POLL_INTERVAL
```

---

### Bot can't connect to RPC

**Cause:** Chain RPC endpoint down

**Solution:**
```bash
# Check current RPC
# Bot uses default RPC untuk setiap chain

# Try another RPC provider
# Edit bot code untuk add alternative RPC (advanced)

# Or wait untuk RPC provider recover
```

---

## 🟣 Configuration Issues

### Wrong parameters causing issues

**Symptoms:** Bot buying wrong tokens atau not buying

**Solution:**

| Issue | Solution |
|-------|----------|
| Too many false signals | Increase MIN_VOLUME, MAX_MCAP |
| Never triggers | Decrease MIN_VOLUME, MIN_MCAP |
| Slippage too high | Increase SLIPPAGE dari 0.05 → 0.1 |
| TP never hit | Reduce TP1_PROFIT_PCT dari 2.0 → 1.0 |

```bash
# Edit config
nano .env

# Adjust parameters
# Save & restart
pm2 restart sniper
```

---

## ⚙️ Performance Issues

### Bot slow / high CPU

**Cause:** POLL_INTERVAL too small

**Solution:**
```bash
# Increase polling interval
nano .env
# Change: POLL_INTERVAL=15 → 30
pm2 restart sniper
```

---

### Trades not executing fast enough

**Cause:** POLL_INTERVAL too large

**Solution:**
```bash
# Decrease polling interval
nano .env
# Change: POLL_INTERVAL=30 → 10
pm2 restart sniper
```

---

## 📊 Monitoring Issues

### Can't view logs

**Cause:** Log buffer overflow

**Solution:**
```bash
# Flush logs
pm2 flush

# View specific lines
pm2 logs sniper --lines 100
```

---

### Database query slow

**Cause:** Too many positions in database

**Solution:**
```bash
# Archive old positions
# Backup first
cp advanced_sniper.db advanced_sniper.db.full

# Query untuk count
sqlite3 advanced_sniper.db "SELECT COUNT(*) FROM positions;"

# If too many (>10000), consider archive
# Delete old records:
sqlite3 advanced_sniper.db "DELETE FROM positions WHERE entry_ts < $(date -d '30 days ago' +%s);"
```

---

## 🆘 Emergency Recovery

### Bot completely broken

```bash
# 1. Stop bot
pm2 stop sniper

# 2. Re-clone repo
cd ~
rm -rf sniper-bot
git clone https://github.com/YOUR_USERNAME/advanced-sniper-bot.git sniper-bot
cd sniper-bot

# 3. Setup fresh
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 4. Restore config
cp .env.example .env
nano .env  # Re-edit

# 5. Start again
pm2 start advanced_sniper_bot.py --name "sniper"
pm2 save
```

---

### Lost wallet access

**⚠️ CRITICAL!**

If private key compromised:

Move all funds to new wallet IMMEDIATELY
Generate new private key
Update .env dengan new key
DO NOT use old wallet

---

## ✅ Verification Checklist

If something wrong, go through this:

```bash
# 1. Bot status
pm2 status
# Should show: online

# 2. Check logs
pm2 logs sniper --lines 50
# Should show: [MONITOR] logs

# 3. Config
cat .env | head -20
# Verify TARGET_CA, PRIVATE_KEY, CHAIN set

# 4. Database
sqlite3 advanced_sniper.db "SELECT COUNT(*) FROM positions;"
# Should show: number

# 5. Connectivity
ping google.com
# Should show: packets received

# 6. Python
source venv/bin/activate
python -c "import web3; print(web3.__version__)"
# Should show: version number

# If all pass = bot should be working!
```

---

## 📞 Getting More Help

If issue not solved:

1. **Check logs carefully**
```bash
   pm2 logs sniper --lines 200
```

2. **Google the error message**
   - Usually common issue sudah ada solution

3. **Check GitHub Issues**
   - https://github.com/jdariko45/advanced-sniper-bot/issues

4. **Open new issue**
   - Include: error message, .env (without secrets), logs

---

## 💡 Prevention Tips

- ✅ Backup .env regularly
- ✅ Backup database weekly
- ✅ Monitor logs daily
- ✅ Update bot monthly
- ✅ Use separate wallet (not main)
- ✅ Start with small amounts
- ✅ Test before large trades

---

Made with ❤️ for happy snipers!
