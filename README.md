# Advanced Multi-Chain Sniper Bot

Automated cryptocurrency sniper bot untuk Robinhood Chain & Base dengan smart trigger system.

## ✨ Features

- ✅ Multi-chain support (Robinhood + Base + Ethereum + Arbitrum + Optimism)
- ✅ Multi-DEX auto-detection via Dexscreener
- ✅ Complex trigger system:
  - Volume filter (min $1000 24h)
  - Market cap range ($5k - $100k default)
  - Liquidity minimum ($500 default)
- ✅ TP1 Auto-sell 50% @ 200% profit (3x multiple)
- ✅ Remaining 50% for manual control
- ✅ 24/7 monitoring & real-time alerts
- ✅ SQLite position tracking
- ✅ PM2 auto-restart & auto-boot on reboot

## 📋 Requirements

- Python 3.9+
- Node.js 16+ (for PM2)
- VPS or local machine
- Contract address (CA)
- Private key (KEEP SECRET!)

## 🚀 Quick Start

### Local Setup

```bash
# Clone repo
git clone https://github.com/jdariko45/advanced-sniper-bot.git
cd advanced-sniper-bot

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Mac/Linux
# or
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Setup config
cp .env.example .env
# Edit .env dengan contract address & private key
nano .env

# Run bot
python advanced_sniper_bot.py
```

### VPS Deployment (24/7)

```bash
# SSH ke VPS
ssh ubuntu@YOUR_VPS_IP

# Setup bot
mkdir sniper-bot && cd sniper-bot
git clone https://github.com/jdariko45/advanced-sniper-bot.git .

# Virtual env
python3 -m venv venv
source venv/bin/activate

# Install deps
pip install -r requirements.txt

# Config
cp .env.example .env
nano .env  # Edit dengan CA & private key

# PM2 deployment
sudo npm install -g pm2
pm2 start advanced_sniper_bot.py --name "sniper"
pm2 save
sudo pm2 startup

# View logs
pm2 logs sniper
```

## ⚙️ Configuration

Edit `.env` file:

```env
# Target token
TARGET_CA=0x...              # Contract address
TARGET_CHAIN=base            # base, robinhood, ethereum, arbitrum, optimism
TARGET_SYMBOL=TOKEN          # Token symbol (optional)

# Wallet
PRIVATE_KEY=0x...            # ⚠️ KEEP SECRET!

# Buy settings
BUY_AMOUNT_ETH=0.001         # Amount per buy
SLIPPAGE=0.05                # 5% slippage

# Triggers (ALL must pass)
MIN_VOLUME_USD_24H=1000      # Min $1000 volume
MIN_MCAP_USD=5000            # Min market cap
MAX_MCAP_USD=100000          # Max market cap
MIN_LIQUIDITY_USD=500        # Min liquidity

# Exit strategy
TP1_PROFIT_PCT=2.0           # 200% profit = 3x
TP1_SELL_PCT=0.5             # Sell 50% at TP1
# Remaining 50% = MANUAL

# Monitoring
POLL_INTERVAL=15             # Check every 15 seconds

# Optional: Telegram
BOT_TOKEN=                   # Leave empty if not using
ADMIN_ID=                    # Leave empty if not using
```

## 🎯 How Bot Works
Monitor token on Dexscreener 24/7
↓
Token appears with liquidity pool
↓
Check all filters:
Volume >= $1000? ✓
MCap $5k-$100k? ✓
Liquidity >= $500? ✓
↓
ALL pass? → AUTO-BUY! 🎯
↓
Track position:
At 200% profit → Auto-sell 50%
Remaining 50% → Manual control
↓
Done! Ready for next token

## 📊 Monitor Bot

```bash
# Check status
pm2 status

# View logs (real-time)
pm2 logs sniper

# View logs (last 50 lines)
pm2 logs sniper --lines 50

# Check positions (bought tokens)
sqlite3 advanced_sniper.db "SELECT * FROM positions;"

# Restart bot (after .env change)
pm2 restart sniper

# Stop bot
pm2 stop sniper
```

## 🔄 Update Bot

```bash
# Pull latest changes
git pull origin main

# Restart with new code
pm2 restart sniper
```

## ⚠️ Security & Risks

**IMPORTANT:**
- ✓ Use **separate wallet** (not main funds)
- ✓ Fund with **minimal amount** ($10-50)
- ✓ Start with **small trades** ($1-5)
- ✓ **NEVER share** private key
- ✓ **NEVER commit** .env file (use .env.example)
- ✓ Crypto trading is **HIGH RISK**
- ✓ Bot is for **EDUCATIONAL purposes**

## 🛠️ Supported Chains

| Chain | Chain ID | Status |
|-------|----------|--------|
| Robinhood | 4663 | ✅ Supported |
| Base | 8453 | ✅ Supported |
| Ethereum | 1 | ✅ Supported |
| Arbitrum | 42161 | ✅ Supported |
| Optimism | 10 | ✅ Supported |
| Ink | 57073 | ✅ Supported |

## 🔄 Multi-Chain Setup

### Change Target Chain

Edit `.env` file dan ubah `TARGET_CHAIN` sesuai chain yang diinginkan:

```env
TARGET_CHAIN=base              # Default (Base Chain)
# Atau ganti dengan:
TARGET_CHAIN=ethereum          # Ethereum Mainnet
TARGET_CHAIN=arbitrum          # Arbitrum One
TARGET_CHAIN=optimism          # Optimism
TARGET_CHAIN=ink               # Ink Chain
TARGET_CHAIN=robinhood         # Robinhood Chain
```

Terus restart bot:

```bash
pm2 restart sniper
```

### Run Multiple Chains Simultaneously

Jalankan 5+ bot instance sekaligus untuk monitor semua chain:

**Contoh: Setup 5 chains**

```bash
# Instance 1: Ethereum
pm2 start advanced_sniper_bot.py --name "sniper-eth"

# Instance 2: Base  
pm2 start advanced_sniper_bot.py --name "sniper-base"

# Instance 3: Arbitrum
pm2 start advanced_sniper_bot.py --name "sniper-arb"

# Instance 4: Optimism
pm2 start advanced_sniper_bot.py --name "sniper-op"

# Instance 5: Ink
pm2 start advanced_sniper_bot.py --name "sniper-ink"
```

Setiap instance akan membaca `.env` yang sama dengan `TARGET_CHAIN` masing-masing.

**Lihat semua instances:**

```bash
pm2 status
```

**Monitor logs semua:**

```bash
pm2 logs        # All instances
pm2 logs sniper-eth   # Specific instance
```

**Detailed guide:** Lihat [docs/MULTI_CHAIN.md](docs/MULTI_CHAIN.md)

## 📚 Documentation

- [Configuration Guide](docs/CONFIGURATION.md) - Detailed config explanation
- [VPS Setup](docs/VPS_SETUP.md) - Step-by-step VPS deployment
- [Multi-Chain Setup](docs/MULTI_CHAIN.md) - Detailed multi-chain guide
- [Troubleshooting](docs/TROUBLESHOOTING.md) - Common issues & fixes

## 📝 License

MIT License - See [LICENSE](LICENSE) file

## 🤝 Contributing

Contributions welcome!

1. Fork repo
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## ⭐ Support

If you find this useful:
- ⭐ Star the repo
- 🍴 Fork it
- 📢 Share it
- 💬 Report issues

## 📧 Questions?

Open an issue on GitHub!

## ⚖️ Disclaimer

This bot is for **EDUCATIONAL purposes only**. Cryptocurrency trading involves significant risk of loss. Use at your own risk. Author is not responsible for any losses or damages.

---

**Made with ❤️ for crypto traders**
