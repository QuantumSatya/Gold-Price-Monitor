import os, sqlite3
from flask import Flask, jsonify, render_template, request
from gold_monitor import fetch_price, send_email
app=Flask(__name__)
DB=os.getenv("DB_PATH","gold.db")

@app.get("/")
def home(): return render_template("index.html")

@app.get("/api/price")
def price():
    p=fetch_price()
    return jsonify({"price":p})

@app.post("/api/reference")
def reference():
    data=request.json
    date=data.get("date"); ref=float(data.get("price")); threshold=float(data.get("threshold",1))
    if not date or ref<=0 or threshold<=0: return jsonify({"error":"Invalid values"}),400
    con=sqlite3.connect(DB)
    con.execute("""CREATE TABLE IF NOT EXISTS settings(
      id INTEGER PRIMARY KEY CHECK(id=1), ref_date TEXT, ref_price REAL, threshold REAL)""")
    con.execute("INSERT INTO settings(id,ref_date,ref_price,threshold) VALUES(1,?,?,?) ON CONFLICT(id) DO UPDATE SET ref_date=excluded.ref_date,ref_price=excluded.ref_price,threshold=excluded.threshold",(date,ref,threshold))
    con.commit(); con.close()
    return jsonify({"ok":True})

@app.get("/api/status")
def status():
    con=sqlite3.connect(DB); con.row_factory=sqlite3.Row
    con.execute("""CREATE TABLE IF NOT EXISTS settings(id INTEGER PRIMARY KEY CHECK(id=1),ref_date TEXT,ref_price REAL,threshold REAL)""")
    s=con.execute("SELECT * FROM settings WHERE id=1").fetchone(); con.close()
    return jsonify(dict(s) if s else {})

if __name__=="__main__": app.run(host="0.0.0.0",port=int(os.getenv("PORT","5000")))
