
import streamlit as st
import pandas as pd
import os

CLASSIFICA_FILE = "classifica.csv"
STORICO_FILE = "storico.csv"

if not os.path.exists(CLASSIFICA_FILE):
    classifica = pd.DataFrame(columns=["Giocatore", "Partite", "Vittorie", "Set Vinti", "Set Persi"])
    classifica.to_csv(CLASSIFICA_FILE, index=False)
else:
    classifica = pd.read_csv(CLASSIFICA_FILE)

if not os.path.exists(STORICO_FILE):
    storico = pd.DataFrame(columns=["Giocatore 1", "Giocatore 2", "Risultato"])
    storico.to_csv(STORICO_FILE, index=False)
else:
    storico = pd.read_csv(STORICO_FILE)

st.title("Torneo Tennis - Inserimento Risultati e Classifica")

with st.form("Inserisci Risultato"):
    giocatore1 = st.text_input("Giocatore 1")
    giocatore2 = st.text_input("Giocatore 2")
    risultato = st.text_input("Risultato (es. 6-0 6-0 o 1-6 7-5 6-3)")
    submitted = st.form_submit_button("Salva Risultato")

    if submitted and giocatore1 and giocatore2 and risultato:
        set_g1 = 0
        set_g2 = 0
        try:
            for set_score in risultato.strip().split():
                g1, g2 = map(int, set_score.split("-"))
                if g1 > g2:
                    set_g1 += 1
                else:
                    set_g2 += 1
        except:
            st.error("Formato punteggio non valido. Usa es. 6-0 6-0")
            st.stop()

        vincitore = giocatore1 if set_g1 > set_g2 else giocatore2

        for g, sets_vinti, sets_persi, vittoria in [
            (giocatore1, set_g1, set_g2, vincitore == giocatore1),
            (giocatore2, set_g2, set_g1, vincitore == giocatore2)
        ]:
            if g in classifica["Giocatore"].values:
                idx = classifica[classifica["Giocatore"] == g].index[0]
                classifica.at[idx, "Partite"] += 1
                classifica.at[idx, "Vittorie"] += int(vittoria)
                classifica.at[idx, "Set Vinti"] += sets_vinti
                classifica.at[idx, "Set Persi"] += sets_persi
            else:
                classifica.loc[len(classifica)] = [g, 1, int(vittoria), sets_vinti, sets_persi]

        storico.loc[len(storico)] = [giocatore1, giocatore2, risultato]

        classifica.to_csv(CLASSIFICA_FILE, index=False)
        storico.to_csv(STORICO_FILE, index=False)

        st.success("Risultato salvato e classifica aggiornata!")

st.subheader("Classifica Aggiornata")
st.dataframe(classifica.sort_values(by=["Vittorie", "Set Vinti"], ascending=False))

st.subheader("Storico Partite")
st.dataframe(storico)
