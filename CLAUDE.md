# Le Cœur du Bourg

**Le projet** — Site vitrine de deux appartements en location au
Bourg-d'Oisans (Isère). Marque : Le Cœur du Bourg. Un immeuble, 1 rue de
Viennois, deux appartements : un T3 et un T2. Location à la nuit de mai à
octobre, au mois de novembre à avril.

**L'architecture** — Le site est statique et généré. `data.py` contient
toutes les données (marque, bâtiments, logements, partenaires, réglages).
`build.py` les lit et écrit le HTML. `style.css` contient les styles.
`photos/` contient les images en pleine qualité.

**Deux commandes** — `python3 build.py` produit `index.html` (le vrai site,
photos en fichiers séparés). `python3 build.py --apercu` produit
`apercu-mobile.html` (fichier unique, photos intégrées et allégées, pour
consultation sur téléphone — jamais mis en ligne).

**Règles absolues, à ne jamais enfreindre :**
1. Le site ne contient AUCUN JavaScript. C'est volontaire : référencement,
   fiabilité, affichage instantané. La navigation se fait en CSS pur, avec
   `:target`. Ne propose jamais d'ajouter du JS au site généré.
2. Aucune information ne doit être écrite en dur dans le HTML. Tout vient de
   `data.py`. Ajouter un logement = ajouter un dict, rien d'autre.
3. Ne modifie jamais `index.html` ou `apercu-mobile.html` à la main : ils
   sont regénérés et tes modifications seraient écrasées.
4. `a-completer.txt` est généré automatiquement et n'est jamais publié.
5. Les photos de `photos/` sont en qualité 92 à résolution native. Ne les
   recompresse pas. Seules celles de `photos-apercu/` peuvent être allégées.

**La direction artistique** — Palette : galet de rivière, ombre de montagne,
vert de vallée. Trois polices : Instrument Serif (titres), Inter (texte),
Archivo Narrow (données en capitales). Pas de cliché chalet/bois/montagne.
Ne change pas cette direction sans qu'on te le demande explicitement.
