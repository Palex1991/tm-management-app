import streamlit as st
import pandas as pd

st.set_page_config(page_title="T&M Economic Management", layout="wide")

st.title("💼 Gestione Economics Time & Material")
st.markdown("Applicazione per il tracciamento di Budget, Costi, FTE e Calendari Lavorativi.")

# Inizializzazione dello Stato dei Dati (Session State)
if "roster" not in st.session_state:
    st.session_state.roster = pd.DataFrame([
        {"Risorsa": "Pasquale Nappo", "Team": "1 - PM", "Site": "Offshore", "Ruolo": "Sr Project Manager", "Sales Rate (€/h)": 111.60, "Cost Rate (€/h)": 74.30, "Valuta": "EUR"},
        {"Risorsa": "Sebastian Salazar", "Team": "1 - PM", "Site": "Onshore", "Ruolo": "Director", "Sales Rate ($/h)": 169.72, "Cost Rate ($/h)": 189.50, "Valuta": "USD"},
        {"Risorsa": "Shweta Saini", "Team": "1 - PM", "Site": "Onshore", "Ruolo": "Sr Project Manager", "Sales Rate ($/h)": 159.65, "Cost Rate ($/h)": 134.95, "Valuta": "USD"}
    ])

if "holidays" not in st.session_state:
    st.session_state.holidays = pd.DataFrame([
        {"Mese": "Gennaio", "Giorni ITA": 20, "Giorni USA": 20},
        {"Mese": "Febbraio", "Giorni ITA": 20, "Giorni USA": 19},
        {"Mese": "Marzo", "Giorni ITA": 22, "Giorni USA": 22},
        {"Mese": "Aprile", "Giorni ITA": 21, "Giorni USA": 22},
        {"Mese": "Maggio", "Giorni ITA": 20, "Giorni USA": 20},
        {"Mese": "Giugno", "Giorni ITA": 21, "Giorni USA": 21},
    ])

# Menu laterale di navigazione
menu = st.sidebar.radio("Sezione App", ["📊 Dashboard & Recap", "👥 Anagrafica Roster", "🗓️ Calendari & Festività"])

# ---------------------------------------------------------
# SEZIONE 1: DASHBOARD & RECAP
# ---------------------------------------------------------
if menu == "📊 Dashboard & Recap":
    st.header("📊 Recap Economico & Previsionale")
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Risorse Attive", len(st.session_state.roster))
    col2.metric("Ore Totali Stimate (Gen)", "440 h")
    col3.metric("Ricavo Totale Stimato", "€ 62.100")
    col4.metric("Costo Totale Stimato", "€ 45.300")
    
    st.subheader("Dettaglio Roster & Tariffe applicate")
    st.dataframe(st.session_state.roster, use_container_width=True)

# ---------------------------------------------------------
# SEZIONE 2: ANAGRAFICA ROSTER
# ---------------------------------------------------------
elif menu == "👥 Anagrafica Roster":
    st.header("👥 Gestione Team e Tariffe (Roster)")
    
    st.subheader("Aggiungi Nuova Risorsa")
    with st.form("add_resource_form"):
        col_a, col_b, col_c = st.columns(3)
        nome = col_a.text_input("Nome Risorsa")
        team = col_b.selectbox("Team", ["1 - PM", "2 - BA", "3 - TA", "4 - DEV"])
        site = col_c.selectbox("Site", ["Onshore", "Offshore"])
        
        col_d, col_e, col_f = st.columns(3)
        ruolo = col_d.text_input("Ruolo / Profilo")
        sales_rate = col_e.number_input("Sales Rate (€ o $ / h)", min_value=0.0, value=100.0)
        cost_rate = col_f.number_input("Cost Rate (€ o $ / h)", min_value=0.0, value=70.0)
        
        valuta = st.radio("Valuta", ["EUR", "USD"], horizontal=True)
        
        submitted = st.form_submit_button("Aggiungi Risorsa")
        if submitted and nome:
            new_row = {
                "Risorsa": nome, "Team": team, "Site": site, 
                "Ruolo": ruolo, "Sales Rate (€/h)": sales_rate, 
                "Cost Rate (€/h)": cost_rate, "Valuta": valuta
            }
            st.session_state.roster = pd.concat([st.session_state.roster, pd.DataFrame([new_row])], ignore_index=True)
            st.success(f"Risorsa {nome} aggiunta con successo!")
            st.rerun()

    st.subheader("Roster Attuale")
    st.dataframe(st.session_state.roster, use_container_width=True)

# ---------------------------------------------------------
# SEZIONE 3: CALENDARI & FESTIVITÀ
# ---------------------------------------------------------
elif menu == "🗓️ Calendari & Festività":
    st.header("🗓️ Giorni Lavorativi per Calendario Paese")
    st.markdown("Definizione dei giorni lavorativi netti al netto delle festività per ciascun sito.")
    
    edited_df = st.data_editor(st.session_state.holidays, use_container_width=True, num_rows="dynamic")
    st.session_state.holidays = edited_df
