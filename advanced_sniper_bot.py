#!/usr/bin/env python3
import asyncio, logging, time, os, sqlite3
import requests
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s — %(message)s")
logger = logging.getLogger("AdvancedSniper")

class BotConfig:
    TARGET_CA = os.getenv("TARGET_CA", "")
    TARGET_CHAIN = os.getenv("TARGET_CHAIN", "robinhood")
    TARGET_SYMBOL = os.getenv("TARGET_SYMBOL", "TOKEN")
    PRIVATE_KEY = os.getenv("PRIVATE_KEY", "")
    BUY_AMOUNT_ETH = float(os.getenv("BUY_AMOUNT_ETH", "0.001"))
    MIN_VOLUME_USD_24H = float(os.getenv("MIN_VOLUME_USD_24H", "1000"))
    MIN_MCAP_USD = float(os.getenv("MIN_MCAP_USD", "5000"))
    MAX_MCAP_USD = float(os.getenv("MAX_MCAP_USD", "100000"))
    MIN_LIQUIDITY_USD = float(os.getenv("MIN_LIQUIDITY_USD", "500"))
    TP1_PROFIT_PCT = float(os.getenv("TP1_PROFIT_PCT", "2.0"))
    TP1_SELL_PCT = float(os.getenv("TP1_SELL_PCT", "0.5"))
    POLL_INTERVAL = int(os.getenv("POLL_INTERVAL", "15"))
    DB_PATH = os.getenv("DB_PATH", "advanced_sniper.db")

class Database:
    def __init__(self, db_path):
        self.db_path = db_path
        self.init()
    def init(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS positions (id INTEGER PRIMARY KEY, ca TEXT, chain TEXT, symbol TEXT, eth_in REAL, tokens_out REAL, entry_price_usd REAL, entry_ts INTEGER, buy_tx TEXT, status TEXT DEFAULT 'open')")
        conn.commit()
        conn.close()
    def open_position(self, ca, chain, symbol, eth_in, tokens_out, entry_price, buy_tx):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("INSERT INTO positions (ca, chain, symbol, eth_in, tokens_out, entry_price_usd, entry_ts, buy_tx) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (ca, chain, symbol, eth_in, tokens_out, entry_price, int(time.time()), buy_tx))
        conn.commit()
        pos_id = c.lastrowid
        conn.close()
        return pos_id

db = Database(BotConfig.DB_PATH)

class MarketDataFetcher:
    @classmethod
    def get_best_pair(cls, ca, chain):
        try:
            r = requests.get(f"https://api.dexscreener.com/latest/dex/tokens/{ca}", timeout=10)
            data = r.json()
            pairs = [p for p in data.get("pairs", []) if (p.get("chainId") or "").lower() == chain]
            if pairs:
                p = pairs[0]
                return {"symbol": p.get("baseToken", {}).get("symbol", "?"), "price_usd": float(p.get("priceUsd") or 0), "volume_24h": float((p.get("volume") or {}).get("h24") or 0), "mcap_usd": float(p.get("marketCap") or 0), "liquidity_usd": float((p.get("liquidity") or {}).get("usd") or 0)}
        except:
            pass
        return None

async def main():
    logger.info("="*60)
    logger.info("ADVANCED SNIPER BOT")
    logger.info("="*60)
    if not BotConfig.TARGET_CA:
        logger.error("ERROR: TARGET_CA not set in .env!")
        return
    if not BotConfig.PRIVATE_KEY:
        logger.error("ERROR: PRIVATE_KEY not set in .env!")
        return
    logger.info(f"Target: {BotConfig.TARGET_CA}")
    logger.info(f"Chain: {BotConfig.TARGET_CHAIN}")
    logger.info(f"Buy: {BotConfig.BUY_AMOUNT_ETH} ETH")
    logger.info(f"TP1: {BotConfig.TP1_PROFIT_PCT*100:.0f}% profit ({BotConfig.TP1_SELL_PCT*100:.0f}% sell)")
    logger.info("")
    try:
        while True:
            pair = MarketDataFetcher.get_best_pair(BotConfig.TARGET_CA, BotConfig.TARGET_CHAIN)
            if pair:
                vol = pair.get("volume_24h", 0)
                mc = pair.get("mcap_usd", 0)
                liq = pair.get("liquidity_usd", 0)
                vol_ok = vol >= BotConfig.MIN_VOLUME_USD_24H
                mc_ok = BotConfig.MIN_MCAP_USD <= mc <= BotConfig.MAX_MCAP_USD
                liq_ok = liq >= BotConfig.MIN_LIQUIDITY_USD
                logger.info(f"[MONITOR] {pair['symbol']}: ${pair['price_usd']:.10f} | Vol ${vol:,.0f} {'✓' if vol_ok else '✗'} | MCap ${mc:,.0f} {'✓' if mc_ok else '✗'} | Liq ${liq:,.0f} {'✓' if liq_ok else '✗'}")
                if vol_ok and mc_ok and liq_ok:
                    logger.info("✓✓✓ TRIGGER ACTIVATED! AUTO-BUY! ✓✓✓")
                    pos_id = db.open_position(BotConfig.TARGET_CA, BotConfig.TARGET_CHAIN, pair['symbol'], BotConfig.BUY_AMOUNT_ETH, 1000, pair['price_usd'], "0xdemo" + "a"*60)
                    logger.info(f"Position #{pos_id} recorded (DEMO MODE)")
            else:
                logger.warning("Cannot fetch pair data")
            await asyncio.sleep(BotConfig.POLL_INTERVAL)
    except KeyboardInterrupt:
        logger.info("Bot stopped.")

if __name__ == "__main__":
    asyncio.run(main())