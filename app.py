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
        fieldnames = ['type', 'montant', 'description', 'categorie', 'date']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for t in transactions:
            writer.writerow(t)

transactions = charger_transactions()

st.title("Gestionnaire de Budget 💸")

# Formulaire d'ajout de transaction
with st.form("ajouter_transaction"):
    type_trans = st.selectbox("Type", ["revenu", "depense"])
    montant = st.number_input("Montant", min_value=0.0, format="%.2f")
    description = st.text_input("Description")
    categorie = st.selectbox("Catégorie", ["Nourriture", "Transport", "Santé", "Loisirs", "Autres"])
    submit = st.form_submit_button("Ajouter")

    if submit:
        if montant > 0:
            nouvelle_transaction = {
                "type": type_trans,
                "montant": str(montant),
                "description": description,
                "categorie": categorie,
                "date": datetime.now().strftime("%Y-%m-%d")
            }
            transactions.append(nouvelle_transaction)
            sauvegarder_transactions(transactions)
            st.success("✅ Transaction ajoutée avec succès.")
        else:
            st.error("❌ Le montant doit être supérieur à 0.")

# Bouton de réinitialisation
if st.button("🗑️ Réinitialiser l'historique"):
    if os.path.exists(FICHIER):
        os.remove(FICHIER)
    transactions.clear()
    st.success("🧹 Historique supprimé. Vous pouvez recommencer à zéro.")

# Calcul du solde
solde = 0
for t in transactions:
    montant = float(t["montant"])
    if t["type"] == "revenu":
        solde += montant
    else:
        solde -= montant

st.write(f"### 💰 Solde actuel : {solde:.2f} MAD")

# Affichage historique sécurisé (sans erreur même si le CSV est incomplet)
if transactions:
    st.write("### 📜 Historique des transactions")
    for t in transactions:
        st.write(
            f"{t.get('date', '❓')} | {t['type']} | {t['montant']} MAD | {t.get('categorie', 'Non précisé')} | {t['description']}"
        )
else:
    st.write("ℹ️ Aucune transaction pour l’instant.")

# Graphique camembert des dépenses par catégorie
st.write("### 📊 Répartition des dépenses par catégorie")

depenses = [t for t in transactions if t["type"] == "depense"]

if depenses:
    categories = {}
    for d in depenses:
        cat = d.get("categorie", "Autres")
        montant = float(d["montant"])
        categories[cat] = categories.get(cat, 0) + montant

    labels = list(categories.keys())
    values = list(categories.values())

    fig, ax = plt.subplots()
    ax.pie(values, labels=labels, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')  # cercle parfait
    st.pyplot(fig)
else:
    st.info("ℹ️ Aucune dépense enregistrée pour le graphique.")
