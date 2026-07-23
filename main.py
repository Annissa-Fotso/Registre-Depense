import json
from datetime import datetime
POSTE_VALIDES = ["loyer", "ration", "etudes", "sante", "loisir", "transport"]
def charger_utilisateurs ():
    try:
        with open ("utilisateurs.json", "r") as fichier:
            return json.load(fichier)
    except (FileNotFoundError , json.JSONDecodeError):
        return []

def charger_depenses ():
    try:
        with open ("depenses.json", "r") as fichier:
            return json.load(fichier)
    except (FileNotFoundError , json.JSONDecodeError):
        return []
    
def sauvegarder_utilisateurs ():
    with open("utilisateurs.json", "w") as fichier :
        json.dump(utilisateurs, fichier, indent=2)

def sauvegarder_depenses ():
    with open("depenses.json", "w") as fichier :
        json.dump (depenses, fichier, indent=2)

def generer_id_utilisateur ():
    if len(utilisateurs) == 0:
        return 1
    return max (u["id"] for u in utilisateurs) + 1

def trouver_utilisateur(nom):
    for utilisateur in utilisateurs:
        if utilisateur["nom"] == nom :
            return utilisateur
    return None

def afficher_postes():
    print ("")
    print ("Postes disponibles : ")
    for poste in POSTE_VALIDES:
        print ("-", poste)

def depense_utilisateur(nom):
    if trouver_utilisateur(nom) is None:
        print("Erreur! cet utilisateur n'existe pas.")
        return None
    mes_depenses = []
    for d in depenses:
        if d["id_utilisateur"] == trouver_utilisateur(nom)["id"]:
            mes_depenses.append(d)
    if len(mes_depenses) == 0:
        print("Aucune depense enregistree pour " + nom + ".")
        return None
    return mes_depenses

def enregistrer_utilisateur ():
    while True:
        nom = input("Entrez votre nom : ").strip()
        if nom == "":
            print ("Erreur le nom ne peut pas être vide")
            continue
        if trouver_utilisateur(nom) is not None:
            print ("Erreur, ce nom existe dejà.")
            continue
        break 

    nouvel_utilisateur = {
        "id": generer_id_utilisateur(),
        "nom": nom,    
    }
    utilisateurs.append(nouvel_utilisateur)
    sauvegarder_utilisateurs ()
    print ("")
    print ("Utilisateur '" + nom + "' enregistré  -ID : " + str (nouvel_utilisateur["id"]) + " enregistré avec succes !")
    while True :
        reponse = input("Voulez-vous enregistrer une dépense maintenant ? (oui/non) : ")
        if reponse == "non":
            return
        elif reponse == "oui":
            enregistrer_depense(nouvel_utilisateur)
            return
        else:
            print ("Reponse invalide, entrez 'oui' ou 'non'. ")
            

def enregistrer_depense (utilisateur = None):
    if utilisateur is None:
        nom = input("Entrez votre nom: ").strip ()
        utilisateur = trouver_utilisateur(nom)
        if utilisateur is None:
            print ("Erreur! cet utilisateur n'existe pas")
            return
    afficher_postes()
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
    date = datetime.now().strftime("%d/%m/%Y  %H:%M")
    nouvelle_depense = {
        "id_utilisateur" : utilisateur["id"],
        "nom" : utilisateur ["nom"],
        "poste": poste,
        "montant": montant,
        "date" : date, 
        }
    depenses.append(nouvelle_depense)
    sauvegarder_depenses()
    print ("")
    print ("Depense enregistree avec succes !")
    print ("Poste   :", poste)
    print ("Montant :", montant, "FCFA")
    print ("Date    :", date)

def consulter_depense():
    nom = input("Entrez votre nom : ").strip()
    mes_depenses = depense_utilisateur(nom)
    if mes_depenses is None:
        return       
    print ("")
    print (" Depenses de " + nom )
    print ("")
    for d in mes_depenses:
        print ("Poste :", d["poste"])
        print ( "Montant", d["montant"], "FCFA")
        print ( "Date", d["date"])
        print ("")
def consulter_par_poste():
    nom = input("Entrez votre nom : ").strip()
    if trouver_utilisateur(nom) is None:
        print("Erreur: cet utilisateur n'existe pas.")
        return
    while True:
        afficher_postes ()
        while True:
            poste_choisi = input ("Choisissez un poste : ").lower() .strip()
            if poste_choisi in POSTE_VALIDES:
                break
            print ("Erreur : Poste invalide.")
        depense_du_poste = []
        for d in depenses :
            if d["id_utilisateur"] == trouver_utilisateur(nom)["id"] and d["poste"] == poste_choisi:
                depense_du_poste.append(d)
        print ("")
        print("Depenses de " + nom + " - " + poste_choisi)
        print ("")
        if len (depense_du_poste) == 0:
            print("Aucune depense pour ce poste.")
        else:
            for d in depense_du_poste:
                print ("Poste   :", d["poste"])
                print ("Montant : ", d["montant"], "FCFA")
                print ("Date    :",  d["date"])
                print ("")

        while True:
            reponse = input("Voulez-vous consulter un autre poste? (oui/non) : ")
            if reponse == "non":
                return
            elif reponse == "oui":
                break
            else:
                print("Reponse invalide, entrez 'oui' ou 'non'. ")
utilisateurs = charger_utilisateurs ()
depenses = charger_depenses ()

def modifier_depense():
    nom = input("Entrez votre nom : ").strip()
    mes_depenses = depense_utilisateur(nom)
    if mes_depenses is None:
        return
    print ("")
    print (" Depenses de " + nom )
    print ("") 
    for i, d in enumerate(mes_depenses, 1):
        print(str(i) + ". Poste :", d["poste"], "| Montant :", d["montant"], "FCFA | Date :", d["date"])
    print ("")
    while True:
        try:
            choix = int (input("Entrez le numéro de la dépense a modifier : "))
            if choix < 1 or choix > len(mes_depenses):
                print("Erreur! numero invalide.")
                continue
            break
        except ValueError:
            print ("Erreur! veuillez saisir un nombre.")
    depense_a_modifier = mes_depenses[ choix -1]
    afficher_postes()
    while True:
        nouveau_poste = input("Nouveau poste : ").lower().strip()
        if nouveau_poste in POSTE_VALIDES:
            break
        print("Erreur! poste invalide.")

    while True:
        try:
            nouveau_montant = float (input("Nouveau montant : "))
            if nouveau_montant <= 0:
                print("Erreur! le montant doit être superieur a 0.")
                continue
            break
        except ValueError:
            print ("Erreur! veuillez saisir un nombre valide.")
    nouvelle_date = datetime.now().strftime("%d/%m/%Y %H/:%M")
    depense_a_modifier["poste"] = nouveau_poste
    depense_a_modifier["montant"] = nouveau_montant
    depense_a_modifier["date"] = nouvelle_date
    sauvegarder_depenses()
    print("")
    print("Depenses modifiee avec succes !")
    print("Nouveau poste : ", nouveau_poste)
    print("Nouveau montant :", nouveau_montant, "FCFA")
    print ("Date modifiee :", nouvelle_date)
def supprimer_depense ():
    nom = input ("Entrez votre nom : ").strip()
    mes_depenses = depense_utilisateur(nom)
    if mes_depenses is None:
        return
    print("")
    print("Depenses de " + nom)
    print("")
    for i, d in enumerate(mes_depenses, 1):
        print(str(i) + ". Poste :", d["poste"], "| Montant :", d["montant"], "FCFA | Date :", d["date"])
        print("")
        while True:
            try:
                choix = int(input("Numero de la depense à supprimer : "))
                if choix < 1 or choix > len(mes_depenses):
                    print ("Erreur! numero invalide.")
                    continue
                break
            except ValueError:
                print("Erreur! veuillez saisir un nombre.")

        depense_a_supprimer = mes_depenses[choix - 1]
        print("")
        print("Depense choisie :", depense_a_supprimer["poste"], "-", depense_a_supprimer["montant"], "FCFA -", depense_a_supprimer["date"])
        while True:
            confirmation = input ("Etes-vous sur de vouloir supprimer? (oui/non) : ").lower().strip()
            if confirmation == "oui":
                depenses.remove(depense_a_supprimer)
                sauvegarder_depenses()
                print("Depense supprimee avec succes !")
                return
            elif confirmation == "non":
                print("Suppression annulee.")
                return
            else:
                print("Reponse invalide, entrez 'oui' ou 'non'.")

while True:
    print("    REGISTRE DES DEPENSES       ")
    print("================================")
    print("1. Enregistrer un utilisateur   ")
    print("2. Enregistrer une depense      ")
    print("3. Consulter ses depenses       ")
    print("4. Consulter depense par poste  ")
    print("5. Modifier une depense         ")
    print("6. Supprimer une depense        ")
    print("7. Quitter                      ")

    choix = input ("Votre choix : ") .strip()
    if choix == "1":
        enregistrer_utilisateur()
    elif choix == "2":
        enregistrer_depense ()
    elif choix == "3":
        consulter_depense ()
    elif choix == "4":
        consulter_par_poste()
    elif choix == "5":
        modifier_depense()
    elif choix == "6":
        supprimer_depense()
    elif choix == "7":
        print("Aurevoir !")
        break
    else:
        print("Choix invalide.")

    