# Prompts pour Claude Code — Le Cœur du Bourg

Sur ton ordinateur : crée un dossier `lecoeurdubourg`, mets-y `data.py`,
`build.py`, `style.css` et le dossier `photos`. Ouvre Claude Code dans ce
dossier. Puis copie-colle les prompts ci-dessous **dans l'ordre**, un à la fois.

Laisse-le en mode validation manuelle au début : tu verras ce qu'il fait.

---

## 0 · À faire une seule fois — les règles du projet

Ce prompt crée un fichier que Claude Code relira automatiquement à chaque
session. Ça t'évite de réexpliquer le projet à chaque fois. **Commence par
celui-là.**

> Crée un fichier `CLAUDE.md` à la racine du projet, contenant les règles
> suivantes, et relis-le au début de chaque session :
>
> **Le projet** — Site vitrine de deux appartements en location au
> Bourg-d'Oisans (Isère). Marque : Le Cœur du Bourg. Un immeuble, 1 rue de
> Viennois, deux appartements : un T3 et un T2. Location à la nuit de mai à
> octobre, au mois de novembre à avril.
>
> **L'architecture** — Le site est statique et généré. `data.py` contient
> toutes les données (marque, bâtiments, logements, partenaires, réglages).
> `build.py` les lit et écrit le HTML. `style.css` contient les styles.
> `photos/` contient les images en pleine qualité.
>
> **Deux commandes** — `python3 build.py` produit `index.html` (le vrai site,
> photos en fichiers séparés). `python3 build.py --apercu` produit
> `apercu-mobile.html` (fichier unique, photos intégrées et allégées, pour
> consultation sur téléphone — jamais mis en ligne).
>
> **Règles absolues, à ne jamais enfreindre :**
> 1. Le site ne contient AUCUN JavaScript. C'est volontaire : référencement,
>    fiabilité, affichage instantané. La navigation se fait en CSS pur, avec
>    `:target`. Ne propose jamais d'ajouter du JS au site généré.
> 2. Aucune information ne doit être écrite en dur dans le HTML. Tout vient de
>    `data.py`. Ajouter un logement = ajouter un dict, rien d'autre.
> 3. Ne modifie jamais `index.html` ou `apercu-mobile.html` à la main : ils
>    sont regénérés et tes modifications seraient écrasées.
> 4. `a-completer.txt` est généré automatiquement et n'est jamais publié.
> 5. Les photos de `photos/` sont en qualité 92 à résolution native. Ne les
>    recompresse pas. Seules celles de `photos-apercu/` peuvent être allégées.
>
> **La direction artistique** — Palette : galet de rivière, ombre de montagne,
> vert de vallée. Trois polices : Instrument Serif (titres), Inter (texte),
> Archivo Narrow (données en capitales). Pas de cliché chalet/bois/montagne.
> Ne change pas cette direction sans qu'on te le demande explicitement.
>
> Quand tu as créé le fichier, montre-le-moi.

---

## 1 · Vérifier que tout tourne chez toi

> Vérifie que Python 3 et Pillow sont installés sur cette machine, installe ce
> qui manque, puis lance `python3 build.py` et `python3 build.py --apercu`.
> Dis-moi si les deux fichiers se génèrent sans erreur, combien pèse chacun, et
> ouvre `index.html` dans mon navigateur pour que je vérifie l'affichage.
> Signale-moi toute erreur ou tout avertissement, même mineur.

---

## 2 · Mettre le site en ligne

C'est l'étape la plus importante. Achète le domaine avant.

> Je veux mettre ce site en ligne sur le domaine `lecoeurdubourg.fr`, que je
> viens d'acheter chez [NOM DE TON REGISTRAR].
>
> Propose-moi deux ou trois hébergeurs gratuits adaptés à un site statique,
> avec leurs avantages et inconvénients pour mon cas — je ne suis pas
> développeur et je veux quelque chose que je puisse gérer seul. Compare
> notamment : simplicité de mise à jour, certificat HTTPS, rapidité en France.
>
> Ne fais rien tant que je n'ai pas choisi. Ensuite, tu configures tout :
> dépôt, déploiement, domaine, HTTPS. Explique-moi au fur et à mesure ce que
> tu fais, et écris à la fin un fichier `MISE-EN-LIGNE.md` qui décrit la
> procédure pour publier une mise à jour, en langage simple.

---

## 3 · Brancher le formulaire de contact

> Le formulaire de la page Contact est inactif : le bouton est désactivé et
> porte le libellé « Formulaire à connecter ».
>
> Branche-le sur un service d'envoi gratuit (Formspree ou l'équivalent de mon
> hébergeur). Il faut que :
> - les messages arrivent sur l'adresse e-mail que je te donnerai ;
> - le visiteur voie une confirmation après envoi ;
> - le piège à robots déjà présent dans le HTML (`_gotcha`) reste en place ;
> - le bouton redevienne actif avec un libellé normal ;
> - tout passe par `build.py`, jamais en dur dans le HTML.
>
> Ajoute aussi une mention RGPD sous le bouton et dis-moi ce qu'il faut que
> j'écrive dans la page Confidentialité.

---

## 4 · Le calendrier des disponibilités

> Chaque logement dans `data.py` a un champ `ical` (liste vide pour l'instant).
> Je vais y coller les liens d'export iCal d'Airbnb et de Booking.
>
> Modifie `build.py` pour qu'au moment de la génération il télécharge ces flux,
> en extraie les dates occupées, et affiche sur chaque fiche un calendrier des
> trois ou quatre prochains mois avec les dates libres et occupées.
>
> Contraintes :
> - en CSS pur, aucun JavaScript sur le site ;
> - si un flux est injoignable, la génération ne doit pas échouer : le
>   calendrier est simplement omis et un avertissement s'affiche dans la
>   console ;
> - le style doit reprendre la palette existante ;
> - le calendrier indique clairement qu'il est indicatif et que la réservation
>   se fait sur Airbnb.
>
> Explique-moi ensuite à quelle fréquence il faut relancer la génération pour
> que les disponibilités restent à jour, et propose-moi une façon simple de
> l'automatiser.

---

## 5 · Modifier ou ajouter un logement — à réutiliser

Celui-ci te servira en permanence. Adapte les valeurs.

> Dans `data.py`, mets à jour le logement `le-petit-coeur-du-bourg` :
> - `surface` : [LE CHIFFRE]
> - ajoute les photos suivantes que je viens de déposer dans `photos/` : [NOMS]
>
> Régénère les deux versions du site et vérifie que la fiche s'affiche
> correctement, que le bandeau de chiffres montre bien la surface, et que le
> fichier `a-completer.txt` ne mentionne plus la surface manquante.

Et pour un futur appartement :

> Je veux ajouter un troisième appartement. Duplique la structure d'un
> logement existant dans `data.py`, avec l'identifiant `[IDENTIFIANT]`, le nom
> `[NOM]`, et mets-le en `"statut": "bientot"` pour l'instant.
> Vérifie qu'il apparaît bien dans le catalogue, le pied de page et le menu
> déroulant du formulaire, sans que j'aie eu à toucher autre chose.

---

## 6 · Les pages légales

> Il manque trois pages obligatoires : mentions légales, conditions de
> location, et politique de confidentialité. Les liens existent dans le pied de
> page mais ne mènent nulle part.
>
> Crée-les dans `data.py` sous forme de textes, et ajoute leur génération dans
> `build.py` en suivant exactement la structure des pages existantes.
>
> Pour le contenu, pose-moi d'abord les questions nécessaires : statut
> juridique, identité de l'hébergeur du site, numéro d'enregistrement du
> meublé, conditions d'annulation que je veux appliquer. Ne remplis rien au
> hasard, et signale-moi ce qui doit être validé par un professionnel.

---

## 7 · Vérification performance et référencement

À lancer une fois le site en ligne.

> Le site est maintenant en ligne. Fais un audit complet et donne-moi la liste
> des corrections par ordre d'impact :
> - vitesse de chargement, en particulier sur mobile en 4G ;
> - poids et format des images (propose WebP en gardant le JPEG en secours) ;
> - balises title et meta description de chaque page ;
> - données structurées schema.org pour un hébergement touristique ;
> - fichiers `sitemap.xml` et `robots.txt` ;
> - accessibilité : contrastes, textes alternatifs, navigation au clavier.
>
> Applique ensuite les corrections une par une en me montrant ce que tu
> changes. Ne casse rien de l'architecture existante.

---

## 8 · Le multilingue — plus tard

> `REGLAGES` dans `data.py` prévoit trois langues : fr, en, nl. Seul le
> français est publié et le sélecteur affiche EN et NL en grisé.
>
> Fais-moi une proposition technique pour activer l'anglais, sans casser
> l'architecture : où stocker les traductions, comment générer les pages, quelle
> structure d'URL, et comment indiquer les versions linguistiques à Google.
>
> Ne code rien pour l'instant — je veux d'abord comprendre et valider
> l'approche, parce que c'est une décision qu'on ne pourra pas défaire
> facilement.

---

## Quelques réflexes utiles

**Une tâche à la fois.** Ne colle pas deux prompts d'un coup. Tu perdrais la
possibilité de vérifier ce qui a changé.

**Avant toute grosse modification**, demande-lui :
> Avant de commencer, explique-moi ce que tu comptes faire et quels fichiers tu
> vas modifier. Ne touche à rien tant que je n'ai pas validé.

**S'il casse quelque chose** :
> Annule les dernières modifications et reviens à l'état précédent. Ensuite
> explique-moi ce qui n'a pas marché.

**Un réflexe qui sauve** : demande-lui dès la première session de mettre le
projet sous Git. Ça enregistre chaque version et permet de revenir en arrière
à tout moment :
> Mets ce projet sous Git, avec un `.gitignore` adapté qui exclut
> `apercu-mobile.html`, `__pycache__` et les fichiers générés. Fais un premier
> commit de l'état actuel. Et à partir de maintenant, fais un commit après
> chaque modification importante, avec un message clair en français.
