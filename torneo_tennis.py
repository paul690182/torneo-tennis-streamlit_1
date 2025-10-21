
import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime

conn = sqlite3.connect("torneo_tennis.db", check_same_thread=False)
c = conn.cursor()

c.execute("CREATE TABLE IF NOT EXISTS classifica (giocatore TEXT PRIMARY KEY, punti INTEGER DEFAULT 0)")
c.execute("""
    CREATE TABLE IF NOT EXISTS risultati (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        giocatore1 TEXT,
        giocatore2 TEXT,
        punteggio TEXT,
        data TEXT
    )
""")
conn.commit()

lista_giocatori = [
    "Paolo R.", "Paola C.", "Francesco M.", "Massimo B.",
    "Daniele T.", "Simone V.", "Gianni F.", "Leo S.",
    "Maura F.", "Giovanni D.", "Andrea P.", "Maurizio P."
]

for g in lista_giocatori:
    c.execute("INSERT OR IGNORE INTO classifica (giocatore, punti) VALUES (?, 0)", (g,))
conn.commit()

st.title("🎾 Torneo Tennis - Tutti contro Tutti")
st.markdown("---")

st.header("📥 Inserisci Risultato")
col1, col2 = st.columns(2)
with col1:
    g1 = st.selectbox("Giocatore 1", lista_giocatori)
with col2:
    g2 = st.selectbox("Giocatore 2", [g for g in lista_giocatori if g != g1])

punteggio = st.selectbox("Punteggio", ["2-0", "2-1", "1-2", "0-2"])

if st.button("✅ Registra Risultato"):
    c.execute("SELECT * FROM risultati WHERE (giocatore1=? AND giocatore2=?) OR (giocatore1=? AND giocatore2=?)", (g1, g2, g2, g1))
    if c.fetchone():
        st.warning("⚠️ Questo incontro è già stato registrato.")
    else:
        data = datetime.now().strftime("%Y-%m-%d %H:%M")
        c.execute("INSERT INTO risultati (giocatore1, giocatore2, punteggio, data) VALUES (?, ?, ?, ?)", (g1, g2, punteggio, data))
        if punteggio == "2-0":
            c.execute("UPDATE classifica SET punti = punti + 3 WHERE giocatore = ?", (g1,))
        elif punteggio == "2-1":
            c.execute("UPDATE classifica SET punti = punti + 2 WHERE giocatore = ?", (g1,))
            c.execute("UPDATE classifica SET punti = punti + 1 WHERE giocatore = ?", (g2,))
        elif punteggio == "1-2":
            c.execute("UPDATE classifica SET punti = punti + 1 WHERE giocatore = ?", (g1,))
            c.execute("UPDATE classifica SET punti = punti + 2 WHERE giocatore = ?", (g2,))
        elif punteggio == "0-2":
            c.execute("UPDATE classifica SET punti = punti + 3 WHERE giocatore = ?", (g2,))
        conn.commit()
        st.success("✅ Risultato registrato con successo!")

st.markdown("---")

st.header("📊 Classifica Attuale")
df = pd.read_sql_query("SELECT * FROM classifica ORDER BY punti DESC", conn)
st.dataframe(df, use_container_width=True)

st.markdown("---")

st.header("📄 Storico Incontri")
storico = pd.read_sql_query("SELECT * FROM risultati ORDER BY data DESC", conn)
st.dataframe(storico, use_container_width=True)
