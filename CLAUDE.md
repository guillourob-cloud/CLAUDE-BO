# Le Cœur du Bourg

**Le projet** — Site vitrine de deux appartements en location au
Bourg-d'Oisans (Isère). Marque : Le Cœur du Bourg. Un immeuble, 1 rue de
Viennois, deux appartements : un T3 et un T2. Location à la nuit de mai à
octobre, au mois de novembre à avril.

**L'architecture** — Le site est statique et généré. `data.py` contient
toutes les données (marque, bâtiments, logements, partenaires, réglages).
`build.py` les lit et écrit le HTML. `style.css` contient les styles.
`photos/` contient les images en pleine qualité. Hébergement : un Cloudflare
Worker nommé `claude-bo` (pas Cloudflare Pages) — voir `wrangler.jsonc` et
`worker.js`, qui sert les fichiers générés et gère le formulaire de contact.

**Deux commandes** — `python3 build.py` produit `index.html` (le vrai site,
photos en fichiers séparés). `python3 build.py --apercu` produit
`apercu-mobile.html` (fichier unique, photos intégrées et allégées, pour
consultation sur téléphone — jamais mis en ligne).

**Règles absolues, à ne jamais enfreindre :**
1. Le site ne contient AUCUN JavaScript, sauf l'unique exception ci-dessous.
   C'est volontaire : référencement, fiabilité, affichage instantané. La
   navigation se fait en CSS pur, avec `:target`. Ne propose jamais d'ajouter
   du JS au site généré en dehors de cette exception.
   - **Exception documentée** : le widget anti-robot Cloudflare Turnstile du
     formulaire de contact (`page_contact()` dans `build.py`). Comme toutes
     les pages du site vivent dans un seul document HTML (navigation par
     `:target`), ce script est présent sur toutes les pages, pas seulement
     sur Contact — mais il ne se charge que si `FORMULAIRE["turnstile_site_key"]`
     est renseigné dans `data.py`, et reste `async defer` (non bloquant).
     Tant que cette clé est vide, le site reste 100 % sans JS.
   - Le code de `worker.js` (le Cloudflare Worker qui héberge le site)
     s'exécute côté serveur, jamais dans le navigateur : il ne compte pas
     dans cette règle, qui ne porte que sur ce qui est envoyé au visiteur.
2. Aucune information ne doit être écrite en dur dans le HTML. Tout vient de
   `data.py`. Ajouter un logement = ajouter un dict, rien d'autre.
3. Ne modifie jamais `index.html` ou `apercu-mobile.html` à la main : ils
   sont regénérés et tes modifications seraient écrasées.
4. `a-completer.txt` est généré automatiquement et n'est jamais publié.
5. Les photos de `photos/` sont en qualité 92 à résolution native. Ne les
   recompresse pas. Seules celles de `photos-apercu/` peuvent être allégées.
6. Aucun secret (clé Turnstile secrète, endpoint Formspree) ne doit jamais
   être écrit dans `data.py` ni ailleurs dans ce dépôt : ils vivent
   uniquement dans les Bindings du Worker, sur le tableau de bord
   Cloudflare. Seule la clé Turnstile *publique* (site key) est faite pour
   être dans `data.py`.
7. Le dossier de sortie du site (`dist/`, publié par le Worker via
   `wrangler.jsonc`) est produit en passant `SORTIE=dist` à `build.py` —
   c'est ce qu'utilisent la commande de build Cloudflare et le workflow
   GitHub Actions. Sans cette variable, `build.py` écrit à la racine du
   projet (usage local normal).

**La direction artistique** — Palette : galet de rivière, ombre de montagne,
vert de vallée. Trois polices : Instrument Serif (titres), Inter (texte),
Archivo Narrow (données en capitales). Pas de cliché chalet/bois/montagne.
Ne change pas cette direction sans qu'on te le demande explicitement.
