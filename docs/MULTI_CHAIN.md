# Multi-Chain Sniper Bot Setup

Panduan lengkap setup sniper bot untuk monitoring multiple blockchain chains.

## 📋 Supported Chains

Bot support chains berikut dengan auto-detection liquidity pools:

| Chain | Chain ID | RPC | Status |
|-------|----------|-----|--------|
| Robinhood | 4663 | https://api.matic.network | ✅ |
| Base | 8453 | https://mainnet.base.org | ✅ |
| Ethereum | 1 | https://eth.drpc.org | ✅ |
| Arbitrum | 42161 | https://arb1.arbitrum.io | ✅ |
| Optimism | 10 | https://mainnet.optimism.io | ✅ |
| Ink | 57073 | https://rpc-mainnet.inkonchain.com | ✅ |

## 🔄 Single Chain Setup

### Method 1: Edit .env & Restart

**STEP 1: Edit .env**

```bash
nano .env
```

**STEP 2: Change TARGET_CHAIN**

```env
TARGET_CHAIN=ethereum    # Change to desired chain
```

Options:
- `robinhood` (Default Robinhood Chain)
- `base` (Base Chain)
- `ethereum` (Ethereum Mainnet)
- `arbitrum` (Arbitrum One)
- `optimism` (Optimism)
- `ink` (Ink Chain)

**STEP 3: Restart Bot**

```bash
pm2 restart sniper
```

**STEP 4: Verify**

```bash
pm2 logs sniper
```

Should show: `[INFO] Chain: ethereum`

---

## 🚀 Multi-Chain Setup (Run Simultaneously)

Jalankan bot di **semua chains sekaligus** dengan PM2 instances.

### Setup 6 Chains (Full)

**STEP 1: Stop current bot**

```bash
pm2 stop sniper
```

**STEP 2: Start 6 instances (satu per chain)**

```bash
# Ethereum
pm2 start advanced_sniper_bot.py --name "sniper-eth"

# Base
pm2 start advanced_sniper_bot.py --name "sniper-base"

# Arbitrum
pm2 start advanced_sniper_bot.py --name "sniper-arb"

# Optimism
pm2 start advanced_sniper_bot.py --name "sniper-op"

# Ink
pm2 start advanced_sniper_bot.py --name "sniper-ink"

# Robinhood
pm2 start advanced_sniper_bot.py --name "sniper-hood"
```

**STEP 3: Edit .env untuk setiap instance**

```bash
# Edit default .env untuk instance pertama
nano .env
# Change: TARGET_CHAIN=ethereum
```

**STEP 4: Lihat semua instances**

```bash
pm2 status
```

Harusnya output seperti:

│ id │ name │ status │ uptime │
├────┼───────────────┼──────────┼────────┤
│ 0 │ sniper-eth │ online │ 5m │
│ 1 │ sniper-base │ online │ 4m │
│ 2 │ sniper-arb │ online │ 3m │
│ 3 │ sniper-op │ online │ 2m │
│ 4 │ sniper-ink │ online │ 1m │
│ 5 │ sniper-hood │ online │ 30s │


**STEP 5: Monitor all logs**

```bash
# All logs
pm2 logs

# Specific instance
pm2 logs sniper-eth
pm2 logs sniper-base
```

---

## ⚙️ Advanced: Multi-Config per Chain

Kalau mau **berbeda settings per chain** (bukan hanya chain):

**STEP 1: Create separate .env files**

```bash
# Copy .env untuk setiap chain
cp .env .env.ethereum
cp .env .env.base
cp .env .env.arbitrum
cp .env .env.optimism
```

**STEP 2: Edit masing-masing**

```bash
nano .env.ethereum
# TARGET_CHAIN=ethereum
# BUY_AMOUNT_ETH=0.005
# MIN_VOLUME_USD_24H=2000

nano .env.base
# TARGET_CHAIN=base
# BUY_AMOUNT_ETH=0.001
# MIN_VOLUME_USD_24H=1000
```

**STEP 3: Start instances with custom .env**

```bash
# Ethereum dengan config eth
pm2 start advanced_sniper_bot.py --name "sniper-eth" --env .env.ethereum

# Base dengan config base
pm2 start advanced_sniper_bot.py --name "sniper-base" --env .env.base
```

---

## 🛠️ Managing Multiple Instances

### View Status

```bash
# All instances
pm2 status

# Specific instance
pm2 info sniper-eth
```

### View Logs

```bash
# All logs
pm2 logs

# Specific instance (last 50 lines)
pm2 logs sniper-eth --lines 50

# Real-time logs
pm2 logs sniper-eth --follow
```

### Control Instances

```bash
# Restart specific
pm2 restart sniper-eth

# Restart all
pm2 restart all

# Stop specific
pm2 stop sniper-eth

# Stop all
pm2 stop all

# Delete specific
pm2 delete sniper-eth

# Delete all
pm2 delete all
```

### Monitor Performance

```bash
# CPU & Memory usage
pm2 monit

# Show dashboard
pm2 web
# Then open: http://localhost:9615
```

---

## 🔍 Checking Trades Per Chain

### Check positions per chain

```bash
# All positions
sqlite3 advanced_sniper.db "SELECT * FROM positions;"

# Specific chain
sqlite3 advanced_sniper.db "SELECT * FROM positions WHERE chain='ethereum';"

# Specific symbol
sqlite3 advanced_sniper.db "SELECT * FROM positions WHERE symbol='TOKEN';"
```

### Get summary

```bash
sqlite3 advanced_sniper.db "SELECT chain, COUNT(*) as count FROM positions GROUP BY chain;"
```

Example output:

arbitrum|2
base|5
ethereum|3


---

## 📊 Multi-Chain Monitoring

### Real-time Dashboard

Monitor semua chains sekaligus:

**Terminal 1: PM2 Status**
```bash
pm2 status
# Lihat status semua instances
```

**Terminal 2: All Logs**
```bash
pm2 logs
# Lihat logs realtime dari semua instances
```

**Terminal 3: Database Monitor**
```bash
watch -n 5 'sqlite3 advanced_sniper.db "SELECT chain, COUNT(*) as trades FROM positions GROUP BY chain;"'
# Auto-refresh setiap 5 detik
```

---

## 🚨 Troubleshooting

### Instance tidak jalan

```bash
# Check logs
pm2 logs sniper-eth

# Restart
pm2 restart sniper-eth

# Check config
pm2 show sniper-eth
```

### Semua instances stop

```bash
# Restart semua
pm2 restart all

# Save state
pm2 save

# Setup auto-restart on boot
pm2 startup
sudo pm2 startup
```

### Memory leak di instance tertentu

```bash
# Setup auto-restart setiap jam
pm2 restart sniper-eth --cron "0 * * * *"
```

### Delete & restart fresh

```bash
# Delete all
pm2 delete all

# Save (clear saved apps)
pm2 save

# Start fresh
pm2 start advanced_sniper_bot.py --name "sniper-base"
pm2 save
```

---

## 💡 Best Practices

### Do's ✅

- ✓ Use separate wallet untuk testing
- ✓ Fund minimal ($10-50 per chain)
- ✓ Start dengan small trades ($1-5)
- ✓ Monitor logs regularly
- ✓ Save PM2 config setelah changes
- ✓ Backup database files

### Don'ts ❌

- ✗ Don't use main wallet
- ✗ Don't run too many instances (resource)
- ✗ Don't leave unmonitored for long
- ✗ Don't commit .env ke repo
- ✗ Don't share private key

---

## ⚠️ Important Notes

1. **Each instance uses same code** - hanya TARGET_CHAIN yang berubah
2. **Database sharing** - semua instances write ke sama `advanced_sniper.db`
3. **Resource usage** - 6 instances ≈ 200MB RAM (depends on system)
4. **PM2 logs** - combined logs dari semua instances

---

## 📞 Quick Reference

```bash
# Setup
pm2 start advanced_sniper_bot.py --name "sniper-eth"
pm2 save
pm2 startup

# Monitoring
pm2 status
pm2 logs sniper-eth

# Management
pm2 restart all
pm2 stop sniper-eth
pm2 delete sniper-eth

# Database
sqlite3 advanced_sniper.db "SELECT * FROM positions;"
```

---

Made with ❤️ for multi-chain snipers!
