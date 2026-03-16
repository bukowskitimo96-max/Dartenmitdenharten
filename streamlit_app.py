import streamlit as st
import pandas as pd
import itertools

# Design-Anpassung für schmale Handys
st.set_page_config(page_title="Turnier", layout="centered")

st.markdown("<h1 style='text-align: center;'>🏆 Turnier Master</h1>", unsafe_allow_html=True)

if 'teams' not in st.session_state:
    st.session_state.teams = []
if 'ergebnisse' not in st.session_state:
    st.session_state.ergebnisse = {}

# Sektion 1: Teams eingeben
with st.expander("👥 Teams verwalten", expanded=len(st.session_state.teams) < 2):
    name = st.text_input("Teamname:")
    if st.button("Hinzufügen"):
        if name and name not in st.session_state.teams:
            st.session_state.teams.append(name)
            st.rerun()
    if st.button("Reset"):
        st.session_state.teams = []
        st.session_state.ergebnisse = {}
        st.rerun()

# Sektion 2: Ergebnisse
if len(st.session_state.teams) >= 2:
    st.subheader("⚽ Ergebnisse")
    paare = list(itertools.combinations(st.session_state.teams, 2))
    
    for p1, p2 in paare:
        key = f"{p1}-{p2}"
        st.write(f"**{p1}** vs **{p2}**")
        # Kleines Eingabefeld für Mobilgeräte
        res = st.text_input("Tore (z.B. 1:1)", value="0:0", key=key)
        try:
            g1, g2 = map(int, res.split(":"))
            st.session_state.ergebnisse[key] = (g1, g2)
        except: pass
        st.divider()

    # Sektion 3: Live-Tabelle
    st.subheader("📊 Tabelle")
    tabelle = {t: {"Pkt": 0, "Diff": 0} for t in st.session_state.teams}
    
    for k, (v1, v2) in st.session_state.ergebnisse.items():
        t1, t2 = k.split("-")
        tabelle[t1]["Diff"] += (v1 - v2)
        tabelle[t2]["Diff"] += (v2 - v1)
        if v1 > v2: tabelle[t1]["Pkt"] += 3
        elif v2 > v1: tabelle[t2]["Pkt"] += 3
        else:
            tabelle[t1]["Pkt"] += 1; tabelle[t2]["Pkt"] += 1

    df = pd.DataFrame(tabelle).T.sort_values(by=["Pkt", "Diff"], ascending=False)
    st.table(df)

    # Sektion 4: Finale
    top = df.index.tolist()
    if len(top) >= 2:
        st.success(f"🏁 **FINALE:** {top[0]} vs {top[1]}")
