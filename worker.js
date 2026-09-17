// Worker Cloudflare — sert le site statique (dist/, produit par build.py) et
// gère le formulaire de contact. Ce code s'exécute côté serveur, jamais dans
// le navigateur du visiteur : il ne compte pas dans la règle « aucun
// JavaScript » du site, qui ne porte que sur ce qui est envoyé au visiteur
// (voir CLAUDE.md).
//
// Variables d'environnement attendues (onglet Bindings du Worker, sur le
// tableau de bord Cloudflare — jamais dans ce dépôt, voir MISE-EN-LIGNE.md) :
//   FORMSPREE_ENDPOINT   ex. https://formspree.io/f/xxxxxxxx
//   TURNSTILE_SECRET_KEY la clé secrète (pas la clé publique du site)

const MERCI = "/#contact-merci";
const ERREUR = "/#contact-erreur";

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (request.method === "POST" && url.pathname === "/api/contact") {
      return traiterContact(request, env);
    }
    return env.ASSETS.fetch(request);
  },
};

async function traiterContact(request, env) {
  const revenirVers = (chemin) => Response.redirect(new URL(chemin, request.url), 303);

  const form = await request.formData();

  // Piège à robots : un champ invisible rempli signale un robot. On répond
  // comme un succès pour ne pas l'aider à détecter le filtrage.
  if (form.get("_gotcha")) {
    return revenirVers(MERCI);
  }

  if (env.TURNSTILE_SECRET_KEY) {
    const jeton = form.get("cf-turnstile-response");
    if (!jeton) return revenirVers(ERREUR);

    const verification = await fetch(
      "https://challenges.cloudflare.com/turnstile/v0/siteverify",
      {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: new URLSearchParams({
          secret: env.TURNSTILE_SECRET_KEY,
          response: jeton,
          remoteip: request.headers.get("CF-Connecting-IP") || "",
        }),
      }
    );
    const resultat = await verification.json();
    if (!resultat.success) return revenirVers(ERREUR);
  }

  if (!env.FORMSPREE_ENDPOINT) return revenirVers(ERREUR);

  const relais = await fetch(env.FORMSPREE_ENDPOINT, {
    method: "POST",
    headers: { Accept: "application/json" },
    body: form,
  });

  return revenirVers(relais.ok ? MERCI : ERREUR);
}
