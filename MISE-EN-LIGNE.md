# Mettre le site en ligne — Le Cœur du Bourg

Ce document explique, en langage simple, comment finir de publier le site
sur Cloudflare (Worker `claude-bo`, déjà connecté au dépôt GitHub), brancher
le formulaire de contact, et comment publier une mise à jour au quotidien.
À suivre une seule fois pour la mise en place ; la section « Publier une
mise à jour » sert ensuite en permanence.

**Note technique** : ce projet est un *Cloudflare Worker* (pas un projet
« Pages » classique) — c'est ce que montre le champ « Deploy command : npx
wrangler deploy » dans l'interface Cloudflare. Concrètement, ça veut dire
que le dossier à publier et le script qui gère le formulaire sont définis
dans deux fichiers du dépôt (`wrangler.jsonc` et `worker.js`), pas dans des
réglages du tableau de bord.

## 1 · Finir la mise en ligne

Le dépôt est déjà connecté (projet `claude-bo`). Deux choses restent à
faire dans le tableau de bord Cloudflare, sous **Workers & Pages → claude-bo** :

1. **Corriger la commande de build** — onglet **Settings** → section build :
   remplacez la commande de build par :
   ```
   SORTIE=dist python3 build.py
   ```
   (Sans cette variable, le site se génère à la racine du projet au lieu du
   dossier `dist/` que `wrangler.jsonc` publie — ce qui expliquerait pourquoi
   le premier déploiement n'a servi qu'un site vide.)
2. **Activer une adresse publique** — sur la page d'aperçu du projet, la
   bannière du haut indique « No URLs enabled ». Dans **Settings → Domains
   & Routes**, activez le sous-domaine `workers.dev`. Le site devient alors
   accessible sur `https://claude-bo.<votre-compte>.workers.dev`.
3. Déclenchez un nouveau déploiement (bouton **New deployment**, ou un
   simple `git push`) pour que ces changements prennent effet.

À partir de là, **chaque mise à jour du dépôt republie automatiquement le
site** — voir la section 5.

### Brancher lecoeurdubourg.fr, une fois acheté

1. Dans le projet, onglet **Settings → Domains & Routes** → **Add** →
   **Custom domain**.
2. Entrez `lecoeurdubourg.fr`, puis suivez les instructions affichées : si
   le domaine est chez un registrar externe (OVH, Gandi…), Cloudflare vous
   donnera un enregistrement DNS à ajouter chez ce registrar. Le certificat
   HTTPS se met en place tout seul, sans rien à faire de plus.

## 2 · Brancher le formulaire de contact

Le formulaire s'appuie sur trois éléments à mettre en place dans cet ordre.

### a) Formspree — reçoit et vous transmet les messages par e-mail

Déjà fait : `https://formspree.io/f/xljdelrg`. Il reste à le rentrer dans
Cloudflare (étape c ci-dessous).

### b) Cloudflare Turnstile — protège le formulaire contre les robots

Déjà fait : la clé publique (site key) est intégrée dans `data.py`. Il
reste seulement la clé secrète à rentrer dans Cloudflare (étape c).

### c) Entrer les deux valeurs dans le Worker

1. Dans le projet **claude-bo**, onglet **Bindings** (ou **Settings →
   Variables and Secrets** selon la version de l'interface) → **Add
   binding** → type **Environment Variable** ou **Secret**.
2. Ajoutez :
   - Nom `FORMSPREE_ENDPOINT`, valeur `https://formspree.io/f/xljdelrg` —
     type Secret si l'option existe, sinon variable normale.
   - Nom `TURNSTILE_SECRET_KEY`, valeur : la clé **secrète** Turnstile
     (visible dans **Turnstile** sur le tableau de bord Cloudflare, à côté
     de la clé publique déjà utilisée). **Ne me la donnez jamais** —
     entrez-la vous-même directement ici, en type Secret.
3. Redéployez (un nouveau déploiement applique les nouvelles variables).

### d) Rien d'autre à faire

`worker.js` (déjà dans le dépôt) reçoit le formulaire, vérifie Turnstile,
puis transmet à Formspree. Il se déploie avec le reste du site, sans
configuration supplémentaire une fois les deux valeurs ci-dessus entrées.

## 3 · Calendrier des disponibilités

Le calendrier est déjà codé : chaque fiche logement affiche automatiquement
les 4 prochains mois avec les dates occupées, dès que `data.py` contient au
moins un lien iCal pour ce logement.

### a) Coller les liens iCal

1. Sur Airbnb : espace hôte → Calendrier → l'appartement concerné →
   **Disponibilité** → **Synchroniser les calendriers** → **Exporter le
   calendrier**. Copiez le lien affiché (il ressemble à
   `https://www.airbnb.fr/calendar/ical/12345.ics?s=xxxxxxxx`).
2. Sur Booking (si utilisé) : Extranet → Tarifs et disponibilités →
   Synchronisation des calendriers → Exporter le calendrier iCal.
3. Dans `data.py`, pour le logement concerné, remplissez :
   ```python
   "ical": [
       "https://www.airbnb.fr/calendar/ical/12345.ics?s=xxxxxxxx",
       "https://admin.booking.com/.../calendar.ics",  # si applicable
   ],
   ```
4. Relancez `python3 build.py` : la fiche affiche désormais le calendrier.
   Si un lien est incorrect ou injoignable, la génération continue quand
   même — un avertissement s'affiche juste dans le terminal, et seul ce
   lien-là est ignoré.

### b) Le tenir à jour automatiquement

Un flux GitHub Actions (`.github/workflows/rebuild-quotidien.yml`) republie
le site chaque nuit pour que le calendrier reflète les réservations
récentes, même sans nouveau commit. Comme c'est un Worker (pas Pages), il
n'y a pas de « Deploy Hook » à appeler : ce flux construit et publie
lui-même via `wrangler`. Pour l'activer, ajoutez deux secrets sur GitHub
(dépôt → **Settings** → **Secrets and variables** → **Actions** → **New
repository secret**) :

1. `CLOUDFLARE_API_TOKEN` — dans le tableau de bord Cloudflare : **My
   Profile** (icône en haut à droite) → **API Tokens** → **Create Token**
   → modèle **Edit Cloudflare Workers**. Copiez le jeton affiché (il ne
   sera plus jamais visible ensuite).
2. `CLOUDFLARE_ACCOUNT_ID` — visible dans le tableau de bord Cloudflare,
   sur la page **Workers & Pages** (colonne de droite), ou dans l'URL du
   tableau de bord.

## 4 · Ce que ça coûte

Tout ce qui précède est gratuit : Cloudflare Workers (généreux plan
gratuit), Formspree (jusqu'à 50 messages/mois), Cloudflare Turnstile,
GitHub Actions. Le seul coût est celui du nom de domaine, déjà prévu à
part.

## 5 · Publier une mise à jour

Une fois tout ce qui précède en place, mettre le site à jour se résume à :

1. Modifiez `data.py` (prix, textes, nouveau logement…) ou ajoutez des
   photos dans `photos/`.
2. Lancez `python3 build.py` pour vérifier que tout se génère sans erreur,
   et ouvrez `index.html` dans votre navigateur pour vérifier l'affichage.
3. Envoyez les changements sur le dépôt GitHub (`git add`, `git commit`,
   `git push` — ou demandez-moi de le faire).

Cloudflare reconstruit et republie alors le site automatiquement, en
général en une ou deux minutes. Il n'y a rien d'autre à faire.
