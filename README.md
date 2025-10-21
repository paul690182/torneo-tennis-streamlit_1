# Torneo Tennis - Streamlit App

Questa applicazione Streamlit consente a 12 giocatori di inserire i risultati delle partite di tennis tutti contro tutti, visualizzare la classifica aggiornata e consultare lo storico degli incontri.

## Come usare

1. Clona o scarica questo repository
2. Installa le dipendenze:
   ```bash
   pip install -r requirements.txt
   ```
3. Avvia l'app:
   ```bash
   streamlit run torneo_tennis.py
   ```

## Funzionalità
- Inserimento risultati con punteggio (2-0, 2-1, 1-2, 0-2)
- Classifica aggiornata dinamicamente
- Storico visibile a tutti
- Salvataggio persistente su database SQLite
