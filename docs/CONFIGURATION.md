# Configuration Guide

Penjelasan detail setiap parameter di `.env` file.

## 📋 Environment Variables (.env)

### Target Token Configuration

#### TARGET_CA
```env
TARGET_CA=0x...
```
**Description:** Contract address token yang mau di-snipe

**Example:** `TARGET_CA=0xB095274743941e953c746F9C228DA9c18Bb6ec29`

**Required:** YES

**Note:** 
- Must valid contract address (43 characters with 0x prefix)
- Verify di Blockscout/Basescan sebelum set

---

#### TARGET_CHAIN
```env
TARGET_CHAIN=base
```

**Description:** Blockchain chain target

**Options:**
- `robinhood` - Robinhood Chain (Chain ID: 4663)
- `base` - Base Chain (Chain ID: 8453)
- `ethereum` - Ethereum Mainnet (Chain ID: 1)
- `arbitrum` - Arbitrum One (Chain ID: 42161)
- `optimism` - Optimism (Chain ID: 10)
- `ink` - Ink Chain (Chain ID: 57073)

**Default:** `base`

**Example:** `TARGET_CHAIN=ethereum`

**Note:** Change untuk monitor di chain berbeda

---

#### TARGET_SYMBOL
```env
TARGET_SYMBOL=TOKEN
```

**Description:** Token symbol (untuk display di logs)

**Example:** `TARGET_SYMBOL=LAPTOP`

**Required:** NO (optional)

**Default:** `TOKEN`

**Note:** Hanya untuk readability, tidak affect bot logic

---

### Wallet Configuration

#### PRIVATE_KEY
```env
PRIVATE_KEY=0x...
```

**Description:** Private key wallet untuk execute buy transactions

**Example:** `PRIVATE_KEY=0x9exxxxxxxxx...xxd5`

**Required:** YES

**Security:** 
- ⚠️ KEEP THIS SECRET!
- ⚠️ NEVER share atau commit ke repo
- ⚠️ Use separate wallet (not main funds)
- ⚠️ Jangan hardcode di code files

**How to get:**
1. Buka MetaMask/wallet
2. Settings > Account Details > Show Private Key
3. Copy paste di .env

---

### Buy Settings

#### BUY_AMOUNT_ETH
```env
BUY_AMOUNT_ETH=0.001
```

**Description:** Amount ETH (or chain native token) per buy transaction

**Example:** `BUY_AMOUNT_ETH=0.005` (buy 0.005 ETH per tx)

**Range:** 0.001 - 10 (depends on wallet balance)

**Default:** `0.001`

**Note:**
- 0.001 ETH ≈ $2-5 (depends on price)
- Start kecil untuk testing
- Increase setelah confident

---

#### SLIPPAGE
```env
SLIPPAGE=0.05
```

**Description:** Max slippage percentage untuk buy transaction

**Example:** `SLIPPAGE=0.05` (5% slippage)

**Range:** 0.01 - 1.0 (1% - 100%)

**Default:** `0.05` (5%)

**Note:**
- Lebih tinggi = lebih likely execute tapi lebih mahal
- Lebih rendah = lebih cheap tapi bisa fail
- 5% adalah sweet spot

**How it works:**

Token price: $100
Slippage 5%: accept price sampai $105


---

### Trigger Filters (ALL MUST PASS untuk auto-buy)

#### MIN_VOLUME_USD_24H
```env
MIN_VOLUME_USD_24H=1000
```

**Description:** Minimum 24-hour trading volume (dalam USD)

**Example:** `MIN_VOLUME_USD_24H=5000` (need minimum $5000 volume)

**Range:** 100 - 1000000

**Default:** `1000`

**Rekomendasi:**
- Conservative: 5000
- Moderate: 1000
- Aggressive: 500

**Why it matters:**
- Low volume = hard to exit (illiquid)
- High volume = safer exit
- Helps avoid pump & dump

---

#### MIN_MCAP_USD
```env
MIN_MCAP_USD=5000
```

**Description:** Minimum market cap (dalam USD)

**Example:** `MIN_MCAP_USD=10000`

**Range:** 1000 - 1000000

**Default:** `5000`

**Rekomendasi:**
- Conservative: 50000
- Moderate: 5000
- Aggressive: 1000

**Why it matters:**
- Very low mcap = rug pull risk
- Helps filter out scam tokens

---

#### MAX_MCAP_USD
```env
MAX_MCAP_USD=100000
```

**Description:** Maximum market cap (dalam USD)

**Example:** `MAX_MCAP_USD=500000` (skip jika sudah > $500k)

**Range:** 10000 - 10000000

**Default:** `100000`

**Rekomendasi:**
- Conservative: 50000 (early launch)
- Moderate: 100000 (more growth potential)
- Aggressive: 1000000 (late launch)

**Why it matters:**
- Higher mcap = less upside potential
- Early launch = more profit potential
- You can skip established tokens

---

#### MIN_LIQUIDITY_USD
```env
MIN_LIQUIDITY_USD=500
```

**Description:** Minimum liquidity pool size (dalam USD)

**Example:** `MIN_LIQUIDITY_USD=5000`

**Range:** 100 - 1000000

**Default:** `500`

**Rekomendasi:**
- Conservative: 10000
- Moderate: 500
- Aggressive: 100

**Why it matters:**
- Low liquidity = slippage ketika sell
- High liquidity = safe exit guaranteed
- Prevents liquid trap

---

### Exit Strategy

#### TP1_PROFIT_PCT
```env
TP1_PROFIT_PCT=2.0
```

**Description:** Profit percentage untuk TP1 (Take Profit 1)

**Format:** Decimal (2.0 = 200%)

**Example:** `TP1_PROFIT_PCT=5.0` (TP1 at 500% = 6x)

**Range:** 0.5 - 20.0 (50% - 2000%)

**Default:** `2.0` (200%)

**How it works:**

Entry: $100
TP1 (200%): $300 (3x multiple)
TP1 (500%): $600 (6x multiple)


**Rekomendasi:**
- Conservative: 2.0 (200%, 3x)
- Moderate: 3.0 (300%, 4x)
- Aggressive: 5.0 (500%, 6x)

---

#### TP1_SELL_PCT
```env
TP1_SELL_PCT=0.5
```

**Description:** Percentage untuk sell at TP1

**Format:** Decimal (0.5 = 50%)

**Example:** `TP1_SELL_PCT=0.3` (sell hanya 30% at TP1)

**Range:** 0.1 - 1.0 (10% - 100%)

**Default:** `0.5` (50%)

**How it works:**

Buy: 1000 tokens
TP1 triggered (200% profit)
Sell 50%: 500 tokens di-jual
Remaining: 500 tokens tetap held (manual)


**Rekomendasi:**
- Conservative: 0.5 (50% sell)
- Moderate: 0.3 (30% sell)
- Aggressive: 0.1 (10% sell)

**Note:**
- Sisa tokens (50%) = manual control
- Bisa hold untuk lebih besar profit
- Atau manual exit kapan saja

---

### Monitoring

#### POLL_INTERVAL
```env
POLL_INTERVAL=15
```

**Description:** Interval (dalam detik) untuk check market data

**Example:** `POLL_INTERVAL=5` (check setiap 5 detik)

**Range:** 5 - 300

**Default:** `15`

**Effect:**
- Lebih kecil = lebih frequent check, lebih cepat trigger tapi lebih CPU
- Lebih besar = lebih jarang check, lebih slow trigger

**Rekomendasi:**
- Fast trigger: 5-10 detik
- Balanced: 15 detik
- Low resource: 30+ detik

---

#### DB_PATH
```env
DB_PATH=advanced_sniper.db
```

**Description:** Path file database SQLite

**Example:** `DB_PATH=/home/user/sniper-bot/db/trades.db`

**Default:** `advanced_sniper.db` (di folder bot)

**Note:**
- Stores all position history
- Don't delete kecali intentional
- Backup regularly

---

### Optional: Telegram Notifications

#### BOT_TOKEN
```env
BOT_TOKEN=
```

**Description:** Telegram bot token untuk notifications

**Required:** NO (leave kosong jika tidak pakai)

**How to setup:**
1. Talk to @BotFather di Telegram
2. Create new bot
3. Copy token
4. Paste di .env

---

#### ADMIN_ID
```env
ADMIN_ID=
```

**Description:** Your Telegram user ID untuk receive notifications

**Required:** NO (leave kosong jika tidak pakai)

**How to get:**
1. Talk to @userinfobot di Telegram
2. Copy ID
3. Paste di .env

---

## 🎯 Recommended Configurations

### Conservative (Safe)
```env
TARGET_CA=0x...
TARGET_CHAIN=base
PRIVATE_KEY=0x...
BUY_AMOUNT_ETH=0.001
MIN_VOLUME_USD_24H=5000
MIN_MCAP_USD=50000
MAX_MCAP_USD=50000
MIN_LIQUIDITY_USD=10000
TP1_PROFIT_PCT=2.0
TP1_SELL_PCT=0.5
POLL_INTERVAL=15
```

### Moderate (Balanced)
```env
TARGET_CA=0x...
TARGET_CHAIN=base
PRIVATE_KEY=0x...
BUY_AMOUNT_ETH=0.002
MIN_VOLUME_USD_24H=1000
MIN_MCAP_USD=5000
MAX_MCAP_USD=100000
MIN_LIQUIDITY_USD=500
TP1_PROFIT_PCT=3.0
TP1_SELL_PCT=0.5
POLL_INTERVAL=15
```

### Aggressive (High Risk/High Reward)
```env
TARGET_CA=0x...
TARGET_CHAIN=base
PRIVATE_KEY=0x...
BUY_AMOUNT_ETH=0.005
MIN_VOLUME_USD_24H=500
MIN_MCAP_USD=1000
MAX_MCAP_USD=500000
MIN_LIQUIDITY_USD=100
TP1_PROFIT_PCT=5.0
TP1_SELL_PCT=0.2
POLL_INTERVAL=5
```

---

## ⚠️ Common Mistakes

❌ Set MAX_MCAP terlalu kecil → Skip semua tokens
❌ Set MIN_LIQUIDITY terlalu tinggi → Bot tidak trigger
❌ BUY_AMOUNT_ETH terlalu besar → Risk terlalu tinggi
❌ Forget to change TARGET_CHAIN → Snipe di wrong chain
❌ SLIPPAGE terlalu kecil → Transactions keep failing

---

## ✅ Tips

✓ Start with conservative settings
✓ Test dengan small amounts dulu
✓ Increase aggressiveness after confident
✓ Monitor logs sebelum set more aggressive
✓ Backup .env kalau sudah tuned

---

Made with ❤️ for sniper traders!
