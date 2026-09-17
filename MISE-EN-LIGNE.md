# Mettre le site en ligne — Le Cœur du Bourg

Ce document explique, en langage simple, comment publier le site sur
Cloudflare Pages, brancher le formulaire de contact, et comment publier une
mise à jour au quotidien. À suivre une seule fois pour la mise en place ;
la section « Publier une mise à jour » sert ensuite en permanence.

## 1 · Mettre le site en ligne sur Cloudflare Pages

1. Créez un compte gratuit sur [dash.cloudflare.com](https://dash.cloudflare.com)
   si vous n'en avez pas.
2. Dans le tableau de bord, allez dans **Workers & Pages** → **Créer une
   application** → **Pages** → **Connecter à Git**.
3. Autorisez Cloudflare à accéder au dépôt GitHub `guillourob-cloud/CLAUDE-BO`,
   et sélectionnez-le.
4. Choisissez la branche à publier (celle que vous utilisez comme version
   « officielle » du site — demandez-moi si vous voulez que je vous aide à
   en mettre une en place proprement).
5. Dans les réglages de build, indiquez :
   - **Commande de build** : `python3 build.py`
   - **Dossier de sortie (build output directory)** : `dist`
6. Lancez le déploiement. Au bout de quelques minutes, le site est en ligne
   sur une adresse du type `https://claude-bo.pages.dev` (Cloudflare choisit
   le nom, vous pouvez le voir et le changer dans les réglages du projet).

À partir de là, **chaque mise à jour du dépôt republie automatiquement le
site** — voir la section 5.

### Brancher lecoeurdubourg.fr, une fois acheté

1. Dans le projet Cloudflare Pages, onglet **Domaines personnalisés** →
   **Configurer un domaine personnalisé**.
2. Entrez `lecoeurdubourg.fr`, puis suivez les instructions affichées : si
   le domaine est chez un registrar externe (OVH, Gandi…), Cloudflare vous
   donnera un enregistrement DNS à ajouter chez ce registrar. Le certificat
   HTTPS se met en place tout seul, sans rien à faire de plus.

## 2 · Brancher le formulaire de contact

Le formulaire s'appuie sur trois éléments à mettre en place dans cet ordre.

### a) Formspree — reçoit et vous transmet les messages par e-mail

1. Créez un compte gratuit sur [formspree.io](https://formspree.io).
2. Créez un formulaire, entrez l'adresse e-mail qui doit recevoir les
   messages.
3. Formspree affiche une adresse du type `https://formspree.io/f/xxxxxxxx` —
   copiez-la.
4. Dans Cloudflare Pages : **Paramètres du projet** → **Variables
   d'environnement** → **Ajouter une variable**, pour l'environnement de
   **Production** :
   - Nom : `FORMSPREE_ENDPOINT`
   - Valeur : l'adresse copiée à l'étape précédente
   - Cochez « Chiffrer » si l'option est proposée.

### b) Cloudflare Turnstile — protège le formulaire contre les robots

1. Dans le tableau de bord Cloudflare : **Turnstile** → **Ajouter un site**.
2. Domaine : `lecoeurdubourg.fr` (ou l'adresse `*.pages.dev` en attendant).
3. Cloudflare affiche deux clés :
   - la **clé de site** (publique, sans danger à publier) ;
   - la **clé secrète** (à ne jamais partager ni publier).
4. La **clé de site** va dans `data.py`, dans `FORMULAIRE["turnstile_site_key"]["v"]`
   — remplacez la valeur vide par cette clé, puis relancez `python3 build.py`,
   committez et poussez. Tant que cette clé est vide, le formulaire
   fonctionne sans Turnstile (moins protégé, mais jamais cassé).
5. La **clé secrète** va dans Cloudflare Pages, en variable d'environnement
   (comme pour Formspree ci-dessus) :
   - Nom : `TURNSTILE_SECRET_KEY`
   - Valeur : la clé secrète
   - Cochez « Chiffrer ».
   **Ne me donnez jamais cette clé secrète** — entrez-la vous-même
   directement dans Cloudflare.

### c) Rien d'autre à faire

Le fichier `functions/api/contact.js` (déjà dans le dépôt) reçoit le
formulaire, vérifie Turnstile, puis transmet à Formspree. Il se déploie
automatiquement avec le reste du site, sans configuration supplémentaire.

## 3 · Calendrier des disponibilités (préparation)

Un flux GitHub Actions (`.github/workflows/rebuild-quotidien.yml`) est déjà
en place pour republier le site chaque nuit, une fois que le calendrier
iCal existera (ce n'est pas encore fait à ce jour). Pour l'activer dès
maintenant :

1. Dans le projet Cloudflare Pages : **Paramètres** → **Deploy Hooks** →
   créez-en un (donnez-lui un nom, ex. « rebuild quotidien »), et copiez
   l'URL affichée.
2. Sur GitHub, dans le dépôt : **Settings** → **Secrets and variables** →
   **Actions** → **New repository secret** :
   - Nom : `CF_DEPLOY_HOOK_URL`
   - Valeur : l'URL copiée à l'étape précédente

Sans effet visible tant que le calendrier iCal n'est pas branché, mais rien
à refaire le jour où il le sera.

## 4 · Ce que ça coûte

Tout ce qui précède est gratuit : Cloudflare Pages (bande passante
illimitée), Formspree (jusqu'à 50 messages/mois), Cloudflare Turnstile,
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
