import os, sqlite3
from flask import Flask, jsonify, render_template, request
from gold_monitor import fetch_price
app=Flask(__name__)
DB=os.getenv("DB_PATH","gold.db")

def init():
    c=sqlite3.connect(DB)
    c.execute("""CREATE TABLE IF NOT EXISTS settings(
      id INTEGER PRIMARY KEY CHECK(id=1), ref_date TEXT, ref_price REAL, threshold REAL)""")
    c.commit(); c.close()

@app.get("/")
def home(): init(); return render_template("index.html")

@app.get("/api/price")
def price(): return jsonify({"price":fetch_price()})

@app.get("/api/status")
def status():
    init(); c=sqlite3.connect(DB); c.row_factory=sqlite3.Row
    s=c.execute("SELECT * FROM settings WHERE id=1").fetchone(); c.close()
    return jsonify(dict(s) if s else {})

@app.post("/api/reference")
def reference():
    d=request.json
    date=d.get("date"); price=float(d.get("price",0)); threshold=float(d.get("threshold",1))
    if not date or price<=0 or threshold<=0: return jsonify({"error":"Invalid reference"}),400
    init(); c=sqlite3.connect(DB)
    c.execute("""INSERT INTO settings(id,ref_date,ref_price,threshold) VALUES(1,?,?,?)
      ON CONFLICT(id) DO UPDATE SET ref_date=excluded.ref_date,
      ref_price=excluded.ref_price,threshold=excluded.threshold""",(date,price,threshold))
    c.commit(); c.close(); return jsonify({"ok":True})

if __name__=="__main__":
    init(); app.run(host="0.0.0.0",port=int(os.getenv("PORT","5000")))
