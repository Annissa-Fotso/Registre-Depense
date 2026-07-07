import json
try:
    with open ("utilisateurs.json", "r") as fichier:
        utilisateurs = json.load(fichier)
except FileNotFoundError:
    utilisateurs = []

POSTE_VALIDES = ["loyer", "ration", "etudes", "sante", "loisir", "transport"]

def sauvegarder ():
    with open("utilisateurs.json", "w") as fichier :
        json.dump(utilisateurs, fichier, indent=2)

def enregistrer_utilisateur ():
    while True:
        nom = input("Entrez votre nom : ").strip()
        if nom == " ":
            print ("Erreur le nom ne peut pas être vide")
            continue
        existe = False
        for utilisateur in utilisateurs:
            if utilisateur["nom"] == nom:
                existe = True
                break
        if existe:
            print ("Ce nom existe déjà, veuillez saisir un autre nom.")
            continue
        break
        
    nouvel_utilisateur = {
        "nom": nom,
        "depenses": []
    }
    utilisateurs.append(nouvel_utilisateur)
    sauvegarder ()
    print ("Nouvel utilisateur '" + nom + "' enregistré avec succès! ")
    
    while True :
        reponse = input("Voulez-vous enregistrer une dépense maintenant ? (oui/non) : ")
        if reponse == "non":
            return
        elif reponse == "oui":
            enregistrer_depense(nouvel_utilisateur)
        else:
            print ("Reponse invalide, entrez 'oui' ou 'non'. ")

def enregistrer_depense (utilisateur):
    print ("Postes disponibles : ")
    for poste in POSTE_VALIDES:
        print ("-", poste)
    while True:
        poste = input ("Choisissez un poste : ").lower() .strip()
        if poste in POSTE_VALIDES:
            break
        print ("Erreur : poste de depense invalide .")
    while True :
        try :
            montant = float (input("Entrez le montant : "))
            if montant <= 0 :
                print ("Erreur ! Le montant doit être superieur à 0.")
                continue
            break
        except ValueError:
            print ("Veuillez saisir un nombre valide.") 
    depense = {"montant": montant, "poste": poste}
    utilisateur["depenses"].append(depense)
    sauvegarder()
    print ("Depense enregistrée avec succes pour"  + utilisateur ["nom"] +  "!")

while True:
    print("    REGISTRE DES DEPENSES       ")
    print("================================")
    print("1. Enregistrer un utilisateur   ")
    print("2. Enregistrer une depense      ")
    print("3. Quitter                      ")

    choix = input ("Votre choix : ") .strip()
    if choix == "1":
        enregistrer_utilisateur()
    elif choix == "2":
        nom = input ("Entrez votre nom :").strip()
        utilisateur_trouve = None
        for utilisateur in utilisateurs:
            if utilisateur["nom"] == nom :
                utilisateur_trouve = utilisateur
                break 
        if utilisateur_trouve is None:
            print ("Erreur! Cet utilisateur introuvable.")
        else : 
            enregistrer_depense (utilisateur_trouve)
    elif choix == "3":
        print ("Aurevoir !")
        break
    else:
        print("Choix invalide.")

    