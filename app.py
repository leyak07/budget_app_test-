import streamlit as st
import csv
import os
from datetime import datetime
import matplotlib.pyplot as plt

FICHIER = "transactions.csv"

def charger_transactions():
    if not os.path.exists(FICHIER):
        return []
    with open(FICHIER, mode='r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return list(reader)

def sauvegarder_transactions(transactions):
    with open(FICHIER, mode='w', newline='', encoding='utf-8') as f:
        fieldnames = ['type', 'montant', 'categorie', 'date']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for t in transactions:
            writer.writerow(t)

transactions = charger_transactions()

st.title("Gestionnaire de Budget avec Catégories")

categories = ["Alimentation", "Transport", "Logement", "Divertissement", "Salaire", "Autres"]

with st.form("ajouter_transaction"):
    type_trans = st.selectbox("Type", ["revenu", "depense"])
    montant = st.number_input("Montant", min_value=0.0, format="%.2f")
    categorie = st.selectbox("Catégorie", categories)
    submit = st.form_submit_button("Ajouter")

    if submit:
        if montant > 0:
            nouvelle_transaction = {
                "type": type_trans,
                "montant": str(montant),
                "categorie": categorie,
                "date": datetime.now().strftime("%Y-%m-%d")
            }
            transactions.append(nouvelle_transaction)
            sauvegarder_transactions(transactions)
            st.success("✅ Transaction ajoutée.")
        else:
            st.error("❌ Le montant doit être supérieur à 0.")

# Calcul du solde
solde = 0
for t in transactions:
    montant = float(t["montant"])
    if t["type"] == "revenu":
        solde += montant
    else:
        solde -= montant

st.write(f"### Solde actuel : {solde:.2f} MAD")

# Affichage historique
if transactions:
    st.write("### Historique")
    for t in transactions:
        st.write(f"{t['date']} | {t['type']} | {t['montant']} MAD | {t['categorie']}")
else:
    st.write("Aucune transaction pour l’instant.")

# --- Graphique de répartition par catégorie ---

# Préparer les données
depenses = {}
revenus = {}

for t in transactions:
    cat = t["categorie"]
    montant = float(t["montant"])
    if t["type"] == "depense":
        depenses[cat] = depenses.get(cat, 0) + montant
    else:
        revenus[cat] = revenus.get(cat, 0) + montant

# Afficher les graphiques seulement s'il y a des données
if depenses:
    fig1, ax1 = plt.subplots()
    ax1.pie(depenses.values(), labels=depenses.keys(), autopct='%1.1f%%', startangle=90)
    ax1.set_title("Répartition des dépenses par catégorie")
    st.pyplot(fig1)

if revenus:
    fig2, ax2 = plt.subplots()
    ax2.pie(revenus.values(), labels=revenus.keys(), autopct='%1.1f%%', startangle=90)
    ax2.set_title("Répartition des revenus par catégorie")
    st.pyplot(fig2)
