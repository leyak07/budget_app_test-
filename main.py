import csv
import os

FICHIER = "transactions.csv"

def charger_transactions():
    if not os.path.exists(FICHIER):
        return []
    with open(FICHIER, mode='r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return list(reader)

def sauvegarder_transactions(transactions):
    with open(FICHIER, mode='w', newline='', encoding='utf-8') as f:
        fieldnames = ['type', 'montant', 'description']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for t in transactions:
            writer.writerow(t)

transactions = charger_transactions()

def ajouter_transaction():
    type_trans = input("Type (revenu / depense) : ").strip().lower()
    if type_trans not in ['revenu', 'depense']:
        print("❌ Type invalide. Réessaie.")
        return

    try:
        montant = float(input("Montant : "))
    except ValueError:
        print("❌ Montant invalide. Réessaie.")
        return

    description = input("Description : ")

    transaction = {
        "type": type_trans,
        "montant": str(montant),  # stocké comme chaîne dans CSV
        "description": description
    }
    transactions.append(transaction)
    sauvegarder_transactions(transactions)
    print("✅ Transaction ajoutée avec succès.")

def afficher_solde():
    solde = 0
    for t in transactions:
        montant = float(t["montant"])
        if t["type"] == "revenu":
            solde += montant
        elif t["type"] == "depense":
            solde -= montant
    print(f"💰 Solde actuel : {solde:.2f} MAD")

def afficher_historique():
    if not transactions:
        print("Aucune transaction enregistrée.")
        return

    print("📜 Historique :")
    for i, t in enumerate(transactions, 1):
        print(f"{i}. {t['type']} - {t['montant']} MAD - {t['description']}")

def menu():
    while True:
        print("\n=== Application Budget ===")
        print("1. Ajouter une transaction")
        print("2. Voir le solde")
        print("3. Voir l’historique")
        print("4. Quitter")

        choix = input("Choix : ")

        if choix == '1':
            ajouter_transaction()
        elif choix == '2':
            afficher_solde()
        elif choix == '3':
            afficher_historique()
        elif choix == '4':
            print("👋 Merci d'avoir utilisé l'application.")
            break
        else:
            print("❌ Choix invalide.")

menu()
