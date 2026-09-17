// Fonction serverless Cloudflare Pages — s'exécute sur les serveurs de
// Cloudflare, jamais dans le navigateur du visiteur. Elle ne fait donc pas
// exception à la règle « aucun JavaScript » du site, qui ne concerne que le
// code envoyé au navigateur (voir CLAUDE.md).
//
// Rôle : reçoit le formulaire de contact, vérifie le jeton Turnstile côté
// serveur, puis relaie vers Formspree qui gère l'envoi de l'e-mail.
//
// Variables d'environnement attendues (à définir dans le tableau de bord
// Cloudflare Pages — jamais dans ce dépôt, voir MISE-EN-LIGNE.md) :
//   FORMSPREE_ENDPOINT   ex. https://formspree.io/f/xxxxxxxx
//   TURNSTILE_SECRET_KEY la clé secrète (pas la clé publique du site)

const MERCI = "/#contact-merci";
const ERREUR = "/#contact-erreur";

export async function onRequestPost({ request, env }) {
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
