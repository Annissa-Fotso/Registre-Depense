import json
POSTE_VALIDES = ["loyer", "ration", "etudes", "sante", "loisir", "transport"]
def charger_utilisateurs ():
    try:
        with open ("utilisateurs.json", "r") as fichier:
            return json.load(fichier)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []

def charger_depenses ():
    try:
        with open ("depenses.json", "r") as fichier:
            return json.load(fichier)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
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
def generer_id_depense ():
    if len (depenses) == 0:
        return 1
    return max (d["id_depense"] for d in depenses ) + 1
def trouver_utilisateur(nom):
    for u in utilisateurs:
        if u["nom"] == nom :
            return u
        return None

utilisateurs = charger_utilisateurs ()
depenses = charger_depenses ()

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
    nouvel_id = generer_id_utilisateur ()   
    nouvel_utilisateur = {
        "id": nouvel_id,
        "nom": nom,
        
    }
    utilisateurs.append(nouvel_utilisateur)
    sauvegarder_utilisateurs ()
    print ("")
    print ("Nouvel utilisateur '" + nom + "' enregistré  -ID : " + str (nouvel_id))
    
    while True :
        reponse = input("Voulez-vous enregistrer une dépense maintenant ? (oui/non) : ")
        if reponse == "non":
            return
        elif reponse == "oui":
            enregistrer_depense(nouvel_utilisateur)
        else:
            print ("Reponse invalide, entrez 'oui' ou 'non'. ")
            break

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
    nouvelle_depense = {
        "id_depense" : generer_id_depense(),
        "id_utilisateur" : utilisateur["id"],
        "nom" : utilisateur ["nom"],
        "poste": poste,
        "montant": montant, 
        }
    depenses.append(nouvelle_depense)
    sauvegarder_depenses()
    print ("Depense enregistrée avec succes pour"  + utilisateur ["nom"] +  "!")

def consulter_depense():

    nom = input("Entrez votre nom : ").strip()
    utilisateur_trouve = None
    for utilisateur in utilisateurs:
        if utilisateur["nom"] == nom:
            utilisateur_trouve = utilisateur
            break
    if utilisateur_trouve is None:
        print ("Erreur, cet utilisateur n'existe pas.")
        return
    if len (utilisateur_trouve["depenses"]) == 0:
        print("Aucune depense enregistree pour" + nom + ".")
        return
    print ("")
    print (" Depenses de " + nom )
    print ("")
    for depense in utilisateur_trouve ["depenses"]:
        print ("-", depense["poste"], "-", depense["montant"], "FCFA")
def consulter_par_poste():
    nom = input("Entrez votre nom : ").strip()
    utilisateur_trouve = None
    for utilisateur in utilisateurs:
        if utilisateur["nom"] == nom:
            utilisateur_trouve = utilisateur
            break
    if utilisateur_trouve is None:
        print ("Erreur, cet utilisateur n'existe pas.")
        return
    while True:
        print ("")
        print("Postes disponibles :")
        for poste in POSTE_VALIDES:
            print ("-", poste)
        while True:
            poste_choisi = input ("Choisissez un poste : ")
            if poste_choisi in POSTE_VALIDES:
                break
            print ("Erreur : Poste invalide.")
        depense_du_poste = []
        for depense in utilisateur_trouve["depenses"]:
            if depense["poste"] == poste_choisi:
                depense_du_poste.append(depense)
        print ("")
        print("Depenses de " + nom + " - poste : " + poste_choisi)
        print ("")
        if len (depense_du_poste) == 0:
            print("Aucune depense pour ce poste.")
        else:
            for depense in depense_du_poste:
                print ("-", depense["poste"], "-", depense["montant"], "FCFA")

        while True:
            reponse = input("Voulez-vous consulter un autre poste? (oui/non) : ")
            if reponse == "non":
                return
            elif reponse == "oui":
                break
            else:
                print("Reponse invalide, entrez 'oui' ou 'non'. ")
while True:
    print("    REGISTRE DES DEPENSES       ")
    print("================================")
    print("1. Enregistrer un utilisateur   ")
    print("2. Enregistrer une depense      ")
    print("3. Consulter ses depenses       ")
    print("4. Consulter depense par poste  ")
    print("5. Quitter                      ")

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
            enregistrer_depense (utilisateur)
    elif choix == "3":
        consulter_depense ()
    elif choix == "4":
        consulter_par_poste()
    elif choix == "5":
        print ("Aurevoir !")
        break
    else:
        print("Choix invalide.")

    