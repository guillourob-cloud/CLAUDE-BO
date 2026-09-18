# -*- coding: utf-8 -*-
"""
SOURCE DE DONNÉES UNIQUE — Le Cœur du Bourg
────────────────────────────────────────────────────────────────
Ajouter un logement  = ajouter un dict dans LOGEMENTS
Ajouter un immeuble  = ajouter une entrée dans BATIMENTS
Changer un prix      = changer un nombre ici
Ajouter une photo    = poser le fichier dans photos/ et citer son nom

Puis relancer :  python3 build.py
"""

REGLAGES = {
    # Le tri du catalogue n'apparaît qu'au-delà de ce nombre de logements.
    "seuil_tri": 6,
    # Langues prévues. Seule la première est publiée pour l'instant ;
    # la structure est en place pour ajouter EN puis NL sans refonte.
    "langues": [("fr", "Français"), ("en", "English"), ("nl", "Nederlands")],
    "langue_publiee": ["fr"],
    # Panneau de préparation : jamais visible par les visiteurs.
    # Il est écrit dans un fichier séparé, a-completer.txt
    "panneau_public": False,
}

MARQUE = {
    "nom": "Le Cœur du Bourg",
    "titre": "Trois appartements en plein centre du Bourg-d'Oisans",
    "sous_titre": ("Dans un immeuble ancien de la rue de Viennois, au pied de "
                   "l'Alpe d'Huez. Tout le village à pied, la montagne au bout de la rue."),
    "email": {"v": "", "provisoire": True},
    "tel": {"v": "", "provisoire": True},
    # Signature d'exploitant, à définir au deuxième immeuble seulement.
    "signature": {"v": "", "provisoire": True},
}

# Formulaire de contact — voir MISE-EN-LIGNE.md pour la marche à suivre.
# La clé Turnstile ici est la clé PUBLIQUE (site key) : elle est faite pour
# apparaître dans le HTML, aucun risque à la coller ici. L'adresse Formspree
# et la clé SECRÈTE Turnstile ne doivent JAMAIS être écrites dans ce dépôt —
# elles se configurent uniquement comme variables d'environnement côté
# Cloudflare Pages, lues par functions/api/contact.js, jamais par build.py.
FORMULAIRE = {
    # Créée sur le tableau de bord Cloudflare, section Turnstile.
    "turnstile_site_key": {"v": "0x4AAAAAAE6Pd8qtivTpGl6j", "provisoire": False},
}

# Texte « à propos » — sans exposer personne.
APROPOS = {
    "titre": "Une affaire de famille",
    "paragraphes": [
        "Nous sommes une famille du Bourg-d'Oisans. Nous possédons un immeuble "
        "ancien rue de Viennois, en plein centre du village, et nous le remettons "
        "en état appartement par appartement.",
        "Nous faisons une grande partie des travaux nous-mêmes. C'est plus lent, "
        "mais ça veut dire que nous connaissons chaque pièce, chaque radiateur et "
        "chaque fenêtre de ces logements — et que nous sommes joignables quand "
        "quelque chose ne va pas.",
        "Nos appartements ne sont pas neufs. Ils ont des cheminées en marbre, des "
        "parquets, des murs en bois, et le charme des vieux immeubles de village. "
        "Nous les améliorons saison après saison, sans chercher à les transformer "
        "en quelque chose qu'ils ne sont pas.",
        "L'été, nous accueillons des voyageurs à la nuit. L'hiver, nous louons au "
        "mois aux gens qui viennent travailler dans la vallée et dans les stations. "
        "Nos logements vivent toute l'année.",
    ],
    "media": {"label": "Le Bourg-d'Oisans dans la vallée", "src": "mini-bourg-hauteur.jpg"},
}

BATIMENTS = {
    "viennois": {
        "id": "viennois",
        "nom": "1 rue de Viennois",
        "commune": "Le Bourg-d'Oisans",
        "cp": "38520",
        "altitude": 720,
        # Localisation approximative — jamais l'adresse exacte publiquement.
        "lat": 45.0556, "lon": 6.0300, "rayon_m": 300, "carte": True,
        "accroche": "L'un des plus anciens immeubles du village, en plein centre.",
        "recit": ("Nos trois appartements sont dans le même immeuble. C'est ce qui "
                  "nous permet de mutualiser ce qu'un appartement isolé ne peut pas "
                  "avoir — et d'être sur place pour tout le monde en même temps."),
        "communs": [
            {"t": "Cave privative", "d": "Une cave fermée à clé par appartement, au sous-sol. Vélos, skis, matériel encombrant.", "soon": False},
            {"t": "Stationnement", "d": "Gratuit dans les rues du centre, sans emplacement attribué.", "soon": False},
            {"t": "Wifi fibre", "d": "Une fibre pour l'immeuble, un réseau propre à chaque appartement.", "soon": True},
            {"t": "Buanderie commune", "d": "Lave-linge et sèche-linge dans les parties communes.", "soon": True},
        ],
        # Distances réelles — remplace l'ancienne silhouette décorative.
        "reperes": [
            {"lieu": "Boulangerie, commerces, restaurants", "detail": "Rue de Viennois et alentours", "val": "à pied"},
            {"lieu": "Alpe d'Huez", "detail": "1 860 m · 21 virages", "val": "≈ 14 km"},
            {"lieu": "Les 2 Alpes", "detail": "1 650 m", "val": "à mesurer", "provisoire": True},
            {"lieu": "Col de la Croix de Fer", "detail": "2 067 m", "val": "à mesurer", "provisoire": True},
            {"lieu": "Lac de Buclet", "detail": "Baignade l'été, patinoire naturelle l'hiver", "val": "à pied"},
            {"lieu": "Grenoble", "detail": "Gare et aéroport", "val": "≈ 50 km"},
        ],
        "partenaires": ["velo", "boulangerie", "resto"],
        "medias": [
            {"slot": "vallee", "label": "Le Bourg-d'Oisans vu depuis la montée de l'Alpe d'Huez",
             "src": "vallee-tall.jpg", "src_large": "vallee-wide.jpg"},
            {"slot": "bourg",  "label": "Le Bourg-d'Oisans", "src": "bourg-hauteur.jpg"},
            {"slot": "hiver",  "label": "Le lac de Buclet en hiver", "src": "buclet-hiver.jpg"},
            {"slot": "chemin", "label": "Au bord du lac de Buclet", "src": "buclet-chemin.jpg"},
        ],
    }
}

PARTENAIRES = {
    "velo":        {"kind": "Vélo", "nom": "", "d": "Location, réparation et entretien à deux pas.", "provisoire": True},
    "boulangerie": {"kind": "Boulangerie", "nom": "", "d": "Pain et viennoiseries au coin de la rue.", "provisoire": True},
    "resto":       {"kind": "Restaurant", "nom": "", "d": "Une table du centre-bourg.", "provisoire": True},
}

LOGEMENTS = [
{
    "id": "le-coeur-du-bourg",      # ne change JAMAIS, même si le nom change
    "batiment": "viennois",
    "nom": "Le Cœur du Bourg",
    "statut": "publie",
    "ordre": 1,
    "kicker": "T3 · 2ᵉ étage",
    "accroche": "48 m² dans un immeuble ancien, deux chambres avec balcon, "
                "au-dessus de la rue du marché.",

    "type": "T3", "surface": 48, "capacite": 4, "chambres": 2,
    "sdb": 1, "wc": 1, "etage": 2, "ascenseur": False,

    "couchages": [
        {"ou": "Chambre 1", "quoi": "1 lit double 140 × 190"},
        {"ou": "Chambre 2", "quoi": "2 lits simples 90 × 190"},
    ],
    "exterieur": "Deux balcons, un par chambre — exposition sud/sud-est",
    "vue": "Les toits du village, les Grandes Rousses et les massifs de l'Oisans",
    "chips": ["48 m²", "4 voyageurs", "2 chambres", "2 balcons", "Baignoire", "Cave à vélos"],

    "description": [
        "L'appartement occupe le deuxième étage d'un des plus anciens immeubles "
        "du village. Parquet, moulures, cheminées en marbre, murs de bois : il n'a "
        "pas été refait à neuf, et c'est ce qui lui donne son caractère.",
        "Les deux chambres ont chacune leur balcon, exposé sud/sud-est. On y prend "
        "le café le matin au-dessus de la rue, et le jour de marché on a la meilleure "
        "place du village.",
        "La grande pièce de vie réunit la cuisine et une longue table de bois. "
        "Salle de bain avec baignoire. Draps et serviettes fournis.",
    ],
    "citation": "Un appartement de village, avec ce que ça veut dire de bois, "
                "de parquet et de cheminées.",

    "moments": [
        {"t": "Les balcons", "d": "Un par chambre, plein sud-est. Le soleil entre le matin et reste jusqu'en début d'après-midi."},
        {"t": "Le marché", "d": "Il passe sous les fenêtres. Depuis le balcon, on voit toute la rue et la montagne au fond."},
        {"t": "La cave", "d": "Privative, fermée à clé, au sous-sol. Vélos, skis, matériel encombrant."},
        {"t": "L'immeuble", "d": "Pierre, hauteur sous plafond, escalier ancien. Nous le rénovons pièce après pièce."},
    ],

    "equipements": {
        "Cuisine": ["Plaques et four", "Micro-ondes", "Réfrigérateur-congélateur",
                    "Cafetière filtre", "Bouilloire", "Grille-pain", "Vaisselle pour 6"],
        "Confort": ["Chauffage", "Baignoire", "Lit bébé sur demande", "Rehausseur enfant sur demande"],
        "Linge":   ["Draps fournis", "Serviettes fournies"],
        "Matériel":["Cave privative fermée à clé"],
    },
    "bientot": ["Wifi fibre", "Télévision", "Canapé dans la pièce de vie"],

    # Infos pratiques — réparties selon le moment, pas empilées.
    "pratique": {
        "decision": [        # près du bouton : ce qui change une décision d'achat
            ("Ménage", "60 € par séjour"),
            ("Séjour minimum", "2 nuits"),
            ("Taxe de séjour", "en supplément"),
            ("Draps et serviettes", "inclus"),
        ],
        "detail": [          # replié en bas de fiche
            ("Arrivée", "à partir de 16 h"),
            ("Départ", "avant 10 h"),
            ("Étage", "2ᵉ, sans ascenseur"),
            ("Stationnement", "gratuit dans les rues du centre"),
            ("Animaux", "non acceptés"),
            ("Tabac", "appartement non-fumeur"),
        ],
    },

    "saisons": {
        "ete":   {"label": "À la nuit", "du": "Mai", "au": "Octobre",
                  "tarifMin": 110, "unite": "€ / nuit", "nuitsMin": 2, "public": True,
                  "note": "Dates disponibles et réservation sur Airbnb."},
        "hiver": {"label": "À la saison", "du": "Novembre", "au": "Avril",
                  "tarifMin": 650, "unite": "€ / mois", "public": False,
                  "note": "Électricité en sus, relevé de compteur à l'entrée et à la sortie."},
    },

    "reservation": {
        "ete":   {"mode": "airbnb", "url": "https://www.airbnb.fr/rooms/1732423185427703033",
                  "libelle": "Voir les dates et réserver"},
        "hiver": {"mode": "formulaire", "url": "#contact",
                  "libelle": "Demander la saison d'hiver"},
    },

    # Calendrier : liens iCal exportés depuis Airbnb / Booking. build.py les
    # lit et génère un calendrier statique des dates occupées.
    "ical": [
        "https://www.airbnb.fr/calendar/ical/1732423185427703033.ics?t=6b72b1c2fd9a4ee6878bcfb89116c2e1",
        "https://ical.booking.com/v1/export?t=46b75029-e158-40db-8535-ca0b86afa551",
    ],

    "visite360": {"url": "", "plateforme": "",
                  "titre": "Visiter l'appartement en 360°",
                  "pieces": ["Entrée", "Pièce de vie", "Cuisine", "Chambre 1",
                             "Chambre 2", "Salle de bain", "Balcon"],
                  "provisoire": True},

    "medias": [
        {"slot": "balcon",  "label": "Vue depuis le balcon, jour de marché", "src": "balcon-marche.jpg"},
        {"slot": "vie",     "label": "La pièce de vie",  "src": "piece-de-vie.jpg"},
        {"slot": "ch1",     "label": "Chambre 1",        "src": "chambre-1.jpg"},
        {"slot": "ch2",     "label": "Chambre 2",        "src": "chambre-2.jpg"},
        {"slot": "cuisine", "label": "La cuisine",       "src": "cuisine.jpg"},
        {"slot": "repas",   "label": "Le coin repas",    "src": "coin-repas.jpg"},
        {"slot": "sdb",     "label": "Salle de bain",    "src": "salle-de-bain.jpg"},
        {"slot": "entree",  "label": "L'entrée",         "src": "entree.jpg"},
    ],
    # Photos qui manquent encore — sert de brief au photographe.
    "medias_manquants": ["Façade depuis la rue", "Second balcon",
                         "Chambre 2 en plan large", "Cave à vélos",
                         "Vue sur les Grandes Rousses"],

    "admin": {
        "numeroEnregistrement": {"v": "", "provisoire": True},
        "dpe": {"v": "", "provisoire": True},
        "classement": {"v": "", "provisoire": True},
    },
},
{
    "id": "le-petit-coeur-du-bourg",   # ne change JAMAIS
    "batiment": "viennois",
    "nom": "Le Petit Cœur du Bourg",
    "statut": "publie",
    "ordre": 2,
    "kicker": "T2 · 3ᵉ étage, sous les toits",
    "accroche": "Sous la charpente, une chambre et un séjour ouvert sur la "
                "kitchenette. Baignoire et lave-linge.",

    "type": "T2", "surface": None, "capacite": 4, "chambres": 1,
    "sdb": 1, "wc": 1, "etage": 3, "ascenseur": False,

    "couchages": [
        {"ou": "Chambre", "quoi": "1 lit double"},
        {"ou": "Séjour",  "quoi": "1 canapé-lit"},
    ],
    "exterieur": "",
    "vue": "Les toits du Bourg-d'Oisans et les massifs alentour",
    "chips": ["4 voyageurs", "1 chambre", "Baignoire", "Lave-linge", "Sous les toits"],

    "description": [
        "Au dernier étage de l'immeuble, cet appartement occupe les combles : "
        "charpente apparente, rampants, velux qui ouvrent sur les toits du village "
        "et les montagnes derrière.",
        "Une chambre avec un lit double ancien en noyer, et un séjour ouvert sur la "
        "kitchenette, avec un canapé-lit et une grande table de bois. Quatre personnes "
        "y dorment confortablement.",
        "Salle de bain avec baignoire, lave-linge et WC. C'est l'appartement le mieux "
        "équipé pour les séjours longs.",
    ],
    "citation": "Un escalier monte vers un réduit sous le toit — trop bas pour être "
                "une pièce, juste ce qu'il faut pour un coin lecture.",

    "moments": [
        {"t": "Sous la charpente", "d": "Poutres apparentes et rampants dans toutes les pièces. Les velux cadrent les toits et la montagne."},
        {"t": "Le coin lecture", "d": "Un escalier droit mène à un espace sous le toit, sans hauteur sous plafond. On ne s'y tient pas debout — on s'y installe."},
        {"t": "Lave-linge et baignoire", "d": "Rares dans un appartement de cette taille. C'est ce qui le rend vivable sur plusieurs mois."},
        {"t": "Le silence", "d": "Dernier étage, personne au-dessus."},
    ],

    "equipements": {
        "Cuisine": ["Plaques", "Four", "Micro-ondes", "Réfrigérateur",
                    "Cafetière filtre", "Bouilloire", "Vaisselle"],
        "Confort": ["Chauffage", "Baignoire", "Rangements"],
        "Linge":   ["Lave-linge", "Draps fournis", "Serviettes fournies"],
        "Matériel":["Cave privative fermée à clé"],
    },
    "bientot": ["Wifi fibre", "Télévision"],

    "pratique": {
        "decision": [
            ("Ménage", "60 € par séjour"),
            ("Séjour minimum", "2 nuits"),
            ("Taxe de séjour", "en supplément"),
            ("Draps et serviettes", "inclus"),
        ],
        "detail": [
            ("Arrivée", "à partir de 16 h"),
            ("Départ", "avant 10 h"),
            ("Étage", "3ᵉ, sous les toits, sans ascenseur"),
            ("Stationnement", "gratuit dans les rues du centre"),
            ("Animaux", "non acceptés"),
            ("Tabac", "appartement non-fumeur"),
        ],
    },

    "saisons": {
        "ete":   {"label": "À la nuit", "du": "Mai", "au": "Octobre",
                  "tarifMin": 90, "unite": "€ / nuit", "nuitsMin": 2, "public": True,
                  "note": "Dates disponibles et réservation sur demande."},
        "hiver": {"label": "À la saison", "du": "Novembre", "au": "Avril",
                  "tarifMin": 550, "unite": "€ / mois", "public": False,
                  "note": "Électricité en sus. Lave-linge dans l'appartement."},
    },
    "reservation": {
        "ete":   {"mode": "formulaire", "url": "#contact", "libelle": "Demander ces dates"},
        "hiver": {"mode": "formulaire", "url": "#contact", "libelle": "Demander la saison d'hiver"},
    },
    "ical": [],
    "visite360": {"url": "", "plateforme": "", "titre": "Visiter l'appartement en 360°",
                  "pieces": ["Séjour", "Kitchenette", "Chambre", "Salle de bain", "Coin lecture"],
                  "provisoire": True},

    "medias": [
        {"slot": "sejour",   "label": "Le séjour", "src": "t2-sejour.jpg"},
        {"slot": "sejour2",  "label": "Le séjour sous les combles", "src": "t2-sejour-2.jpg"},
        {"slot": "chambre",  "label": "La chambre", "src": "t2-chambre.jpg"},
        {"slot": "chambre2", "label": "La chambre, rangements", "src": "t2-chambre-2.jpg"},
        {"slot": "cuisine",  "label": "La kitchenette", "src": "t2-cuisine.jpg"},
        {"slot": "escalier", "label": "L'escalier vers le coin lecture", "src": "t2-escalier.jpg"},
        {"slot": "sdb",      "label": "La salle de bain", "src": "t2-salle-de-bain.jpg"},
        {"slot": "bain",     "label": "Baignoire", "src": "t2-sdb-bain.jpg"},
    ],
    "medias_manquants": ["Surface à confirmer", "Vue depuis les velux",
                         "Coin lecture sous le toit", "Salle de bain en lumière du jour",
                         "Cave à vélos"],

    "admin": {
        "numeroEnregistrement": {"v": "", "provisoire": True},
        "dpe": {"v": "", "provisoire": True},
        "classement": {"v": "", "provisoire": True},
    },
},
]
