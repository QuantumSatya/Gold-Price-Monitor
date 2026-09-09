import os,re,sqlite3,requests
from bs4 import BeautifulSoup

URL="https://www.goodreturns.in/gold-rates/"
DB=os.getenv("DB_PATH","gold.db")

def fetch_price():
    r=requests.get(URL,headers={"User-Agent":"Mozilla/5.0 GoldMonitor"},timeout=20)
    r.raise_for_status()
    text=BeautifulSoup(r.text,"html.parser").get_text(" ",strip=True)
    m=re.search(r"24K\s*Gold\s*/g\s*₹\s*([\d,]+)",text)
    if not m: raise RuntimeError("24K price not found on Goodreturns")
    return float(m.group(1).replace(",",""))

def get_settings():
    c=sqlite3.connect(DB); c.execute("""CREATE TABLE IF NOT EXISTS settings(
      id INTEGER PRIMARY KEY CHECK(id=1),ref_date TEXT,ref_price REAL,threshold REAL)""")
    row=c.execute("SELECT ref_date,ref_price,threshold FROM settings WHERE id=1").fetchone()
    c.close(); return row

def telegram(message):
    token=os.getenv("TELEGRAM_BOT_TOKEN")
    chats=[x.strip() for x in os.getenv("TELEGRAM_CHAT_IDS","").split(",") if x.strip()]
    if not token or not chats:
        print("Telegram not configured. Alert:",message); return
    url=f"https://api.telegram.org/bot{token}/sendMessage"
    for chat in chats:
        r=requests.post(url,json={"chat_id":chat,"text":message},timeout=20)
        print("Telegram:",r.status_code,r.text)

def check():
    s=get_settings()
    if not s:
        print("No manual reference configured."); return
    ref_date,ref,threshold=s
    current=fetch_price()
    change=(current-ref)/ref*100
    if change<=-threshold or change>=threshold:
        direction="📉 DROP" if change<0 else "📈 RISE"
        msg=f"""🪙 24K GOLD ALERT

{direction}

Current: ₹{current:,.0f}/g
Reference date: {ref_date}
Reference: ₹{ref:,.0f}/g
Change: {change:+.2f}%
Threshold: {threshold:.2f}%

Source: Goodreturns India 24K"""
        telegram(msg)
    else:
        print(f"No alert: {change:+.2f}%")
if __name__=="__main__": check()
