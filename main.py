depenses = []
while True:
    print ("REGISTRE DES DEPENSES")
    print ("1. Ajouter une depense")
    print ("2. Consulter les depenses")
    print ("3. Afficher le total")
    print ("4. Quitter")
    choix = input("Votre choix : ")
    if choix == "1":
        montant = float (input("Montant :  "))
        poste = input("Poste de dépense : ")
        depense = {
            "montant" : montant,
            "poste" : poste,
         }
        depenses.append(depense)
        print ("Dépense enregistrée avec succès!")
    elif choix == "2":
        if len(depenses)== 0:
            print ("Aucune dépense enregistrée.")
        else:
            print ("Liste des dépenses : ")
            for depense in depenses:
                print(depense ["poste"], "-" , depense["montant"], "FCFA")
    elif choix == "3":
        total = 0
        for depense in depenses:
            total = total + depense["montant"]
        print ("Total des depenses :", total , "FCFA")
    elif choix == "4":
        print ("Aurevoir !")
        break
    else :
        print ("choix invalide.")
    
    
        
        