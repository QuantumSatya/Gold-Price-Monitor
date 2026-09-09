import os,re,sqlite3,requests,smtplib
from bs4 import BeautifulSoup
from email.message import EmailMessage
from datetime import datetime,timezone

URL="https://www.goodreturns.in/gold-rates/"
DB=os.getenv("DB_PATH","gold.db")

def init():
 c=sqlite3.connect(DB); c.execute("""CREATE TABLE IF NOT EXISTS settings(id INTEGER PRIMARY KEY CHECK(id=1),ref_date TEXT,ref_price REAL,threshold REAL)"""); c.commit(); return c

def fetch_price():
 r=requests.get(URL,headers={"User-Agent":"Mozilla/5.0 GoldMonitor"},timeout=20); r.raise_for_status()
 text=BeautifulSoup(r.text,"html.parser").get_text(" ",strip=True)
 m=re.search(r"24K\s*Gold\s*/g\s*₹\s*([\d,]+)",text)
 if not m: raise RuntimeError("24K price not found")
 return float(m.group(1).replace(",",""))

def settings():
 c=init(); row=c.execute("SELECT ref_date,ref_price,threshold FROM settings WHERE id=1").fetchone(); c.close(); return row

def send_email(subject,body):
 user=os.getenv("SMTP_USERNAME"); pwd=os.getenv("SMTP_APP_PASSWORD")
 to=[x.strip() for x in os.getenv("ALERT_EMAIL_TO","").split(",") if x.strip()]
 if not(user and pwd and to): print("Email not configured"); return False
 m=EmailMessage(); m["From"]=user; m["To"]=", ".join(to); m["Subject"]=subject; m.set_content(body)
 with smtplib.SMTP(os.getenv("SMTP_HOST","smtp.gmail.com"),587,timeout=20) as s:
  s.starttls(); s.login(user,pwd); s.send_message(m)
 return True

def check():
 s=settings()
 if not s: print("No manual reference configured."); return
 ref_date,ref,threshold=s; cur=fetch_price(); pct=(cur-ref)/ref*100
 if abs(pct)>=threshold:
  direction="DROP" if pct<0 else "RISE"
  emoji="📉" if pct<0 else "📈"
  body=f"""24K GOLD {emoji} {direction} ALERT

Current price: ₹{cur:,.0f}/g
Reference date: {ref_date}
Reference price: ₹{ref:,.0f}/g
Change: {pct:+.2f}%
Your threshold: {threshold:.2f}%

Source: Goodreturns India 24K
Checked: {datetime.now(timezone.utc).isoformat()}
"""
  send_email(f"🚨 24K Gold {direction} Alert",body)
 else: print(f"No alert: {pct:+.2f}%")
if __name__=="__main__": check()
