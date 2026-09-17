# -*- coding: utf-8 -*-
"""Génère le site statique du Cœur du Bourg à partir de data.py.
   Aucun JavaScript n'est nécessaire pour l'afficher.
   Les photos sont intégrées au fichier : il fonctionne hors ligne."""
import html, base64, datetime, pathlib, shutil, os, re, calendar, urllib.request
from data import MARQUE, APROPOS, BATIMENTS, PARTENAIRES, LOGEMENTS, REGLAGES, FORMULAIRE

import sys
APERCU = "--apercu" in sys.argv     # fichier unique, photos allégées, pour consultation
ICI = pathlib.Path(__file__).parent
PHOTOS = ICI / ("photos-apercu" if APERCU else "photos")
E = lambda s: html.escape(str(s if s is not None else ""), quote=True)

visibles = sorted([l for l in LOGEMENTS if l["statut"] != "masque"], key=lambda l: l["ordre"])
publies = [l for l in visibles if l["statut"] == "publie"]
bientot = [l for l in visibles if l["statut"] == "bientot"]
saison = "ete" if 5 <= datetime.date.today().month <= 10 else "hiver"
bats = list(dict.fromkeys(l["batiment"] for l in visibles))
multi_bat = len(bats) > 1

_cache = {}
def data_uri(nom):
    """Aperçu : la photo est intégrée au fichier.
       Site réel : on renvoie simplement le chemin, la photo reste un fichier
       séparé — qualité intacte, mise en cache par le navigateur."""
    if nom in _cache:
        return _cache[nom]
    f = PHOTOS / nom
    if not f.exists():
        _cache[nom] = None
    elif APERCU:
        _cache[nom] = "data:image/jpeg;base64," + base64.b64encode(f.read_bytes()).decode()
    else:
        _cache[nom] = f"photos/{nom}"
    return _cache[nom]


def img(m, cls="", eager=False):
    if m and m.get("src") and data_uri(m["src"]):
        lz = "" if eager else ' loading="lazy" decoding="async"'
        alt = E(m.get("label", ""))
        # Deux recadrages : portrait sur téléphone, large sur ordinateur.
        # La photo garde sa composition au lieu d'être rognée au hasard.
        if m.get("src_large") and data_uri(m["src_large"]):
            return (f'<figure class="ph {cls}"><picture>'
                    f'<source media="(min-width:800px)" srcset="{data_uri(m["src_large"])}">'
                    f'<img src="{data_uri(m["src"])}" alt="{alt}"{lz}>'
                    f'</picture></figure>')
        return (f'<figure class="ph {cls}"><img src="{data_uri(m["src"])}" '
                f'alt="{alt}"{lz}></figure>')
    return (f'<figure class="ph ph--vide {cls}"><span class="ph-lbl">'
            f'{E(m.get("label")) if m else "Photo"}</span></figure>')


def prix_txt(l, k="ete"):
    s = l["saisons"][k]
    return (f'dès {s["tarifMin"]} {s.get("unite", "€ / nuit")}'
            if s.get("tarifMin") else "Sur demande")


def carte_logement(l, grande=False):
    if l["statut"] == "bientot":
        return (f'<article class="card card--soon"><div class="card-body">'
                f'<p class="kick">{E(l["kicker"])}</p><h3>{E(l["nom"])}</h3>'
                f'<p class="hook">{E(l["accroche"])}</p>'
                f'<p class="soon-tag">Bientôt disponible</p></div></article>')
    m0 = dict(l["medias"][0]) if l["medias"] else {"label": l["nom"]}
    if m0.get("src") and (PHOTOS / f'mini-{m0["src"]}').exists():
        m0["src"] = f'mini-{m0["src"]}'   # vignette : évite de dupliquer la photo entière
    chips = ("<ul class=\"chips\">" + "".join(f"<li>{E(c)}</li>" for c in l["chips"][:4])
             + "</ul>") if l["chips"] else ""
    lieu = BATIMENTS[l["batiment"]]["commune"] if multi_bat else "Centre du village"
    menage = next((f"+ {v}" for k, v in l["pratique"]["decision"] if k == "Ménage"), "")
    return f'''<article class="card {'card--lead' if grande else ''}">
<a class="card-media" href="#{E(l["id"])}">{img(m0, eager=grande)}
<span class="card-tag">{E(l["type"])}</span></a>
<div class="card-body">
<p class="kick">{E(l["kicker"])} · {E(lieu)}</p>
<h3><a href="#{E(l["id"])}">{E(l["nom"])}</a></h3>
<p class="hook">{E(l["accroche"])}</p>{chips}
<div class="card-foot">
<span class="card-price">{prix_txt(l)}<small>{menage}</small></span>
<a class="btn btn--sm" href="#{E(l["id"])}">Voir l'appartement</a>
</div></div></article>'''


def liste_logements():
    out = "".join(carte_logement(l, grande=(i == 0 and len(publies) == 1))
                  for i, l in enumerate(publies))
    if bientot:
        noms = " et ".join(E(l["nom"]) for l in bientot)
        out += (f'<p class="apres">{noms} — les deux autres appartements de '
                f"l'immeuble — rejoindront la collection après rénovation.</p>")
    return f'<div class="cards {"cards--solo" if len(publies) == 1 else ""}">{out}</div>'


def carte_osm(bat, cls=""):
    if not bat.get("carte"):
        return ""
    lat, lon, r = bat["lat"], bat["lon"], bat.get("rayon_m", 300)
    dlat = (r * 4) / 111_000
    dlon = (r * 4) / (111_000 * 0.707)
    bbox = f"{lon-dlon:.5f},{lat-dlat:.5f},{lon+dlon:.5f},{lat+dlat:.5f}"
    g = ("https://www.google.com/maps/search/?api=1&query="
         + E(f'{bat["commune"]}, {bat["cp"]}').replace(" ", "+"))
    return f'''<div class="carte {cls}">
<iframe src="https://www.openstreetmap.org/export/embed.html?bbox={bbox}&amp;layer=mapnik"
title="Situation approximative" loading="lazy" referrerpolicy="no-referrer"></iframe>
<span class="carte-zone" aria-hidden="true"></span>
<p class="carte-pied"><span>Zone approximative — adresse exacte communiquée après
réservation</span><a href="{g}" target="_blank" rel="noopener">Google Maps ↗</a></p>
</div>'''


def _deplier_ical(texte):
    """RFC 5545 : une ligne qui commence par une espace/tabulation prolonge
       la précédente. Airbnb/Booking en font peu, mais autant être robuste."""
    lignes = texte.replace("\r\n", "\n").split("\n")
    out = []
    for ligne in lignes:
        if ligne.startswith((" ", "\t")) and out:
            out[-1] += ligne[1:]
        else:
            out.append(ligne)
    return out


def _date_ical(valeur):
    m = re.match(r"(\d{8})", valeur.strip())
    return datetime.datetime.strptime(m.group(1), "%Y%m%d").date() if m else None


def _parse_vevents(texte):
    """Renvoie l'ensemble des dates occupées : [DTSTART, DTEND[, comme
       le veut la convention Airbnb/Booking (DTEND = jour de départ, donc
       déjà libre pour une nouvelle arrivée)."""
    dates, debut, fin = set(), None, None
    for ligne in _deplier_ical(texte):
        cle = ligne.split(":", 1)[0].split(";", 1)[0]
        if cle == "BEGIN" and ligne.endswith("VEVENT"):
            debut = fin = None
        elif cle == "DTSTART":
            debut = _date_ical(ligne.split(":", 1)[1])
        elif cle == "DTEND":
            fin = _date_ical(ligne.split(":", 1)[1])
        elif cle == "END" and ligne.endswith("VEVENT") and debut and fin:
            d = debut
            while d < fin:
                dates.add(d)
                d += datetime.timedelta(days=1)
    return dates


def recuperer_ical(urls):
    """Télécharge et fusionne les flux iCal d'un logement. Un flux
       injoignable ou illisible est ignoré (avertissement console) plutôt
       que de faire échouer toute la génération. Renvoie None si aucun flux
       n'a pu être lu (calendrier alors omis), sinon l'ensemble des dates
       occupées — potentiellement vide si le logement est entièrement libre."""
    occupe, au_moins_un = set(), False
    for url in urls:
        try:
            with urllib.request.urlopen(url, timeout=10) as reponse:
                texte = reponse.read().decode("utf-8", errors="replace")
        except Exception as e:
            print(f"⚠ calendrier : flux iCal injoignable ({url}) — {e}", file=sys.stderr)
            continue
        occupe |= _parse_vevents(texte)
        au_moins_un = True
    return occupe if au_moins_un else None


MOIS_FR = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet",
           "août", "septembre", "octobre", "novembre", "décembre"]
JOURS_FR = ["L", "M", "M", "J", "V", "S", "D"]


def _mois_suivant(d):
    return d.replace(year=d.year + 1, month=1) if d.month == 12 else d.replace(month=d.month + 1)


def _calendrier_mois(mois, occupe, aujourdhui):
    nb_jours = calendar.monthrange(mois.year, mois.month)[1]
    cases = '<span class="dispo-j dispo-j--vide"></span>' * mois.weekday()
    for j in range(1, nb_jours + 1):
        d = mois.replace(day=j)
        if d < aujourdhui:
            cls = "dispo-j--passe"
        elif d in occupe:
            cls = "dispo-j--occupe"
        else:
            cls = "dispo-j--libre"
        cases += f'<span class="dispo-j {cls}">{j}</span>'
    entete = "".join(f'<span class="dispo-ent">{j}</span>' for j in JOURS_FR)
    return (f'<div class="dispo-bloc"><h4>{MOIS_FR[mois.month - 1]} {mois.year}</h4>'
            f'<div class="dispo-grille">{entete}{cases}</div></div>')


def calendrier_html(occupe, n_mois=4):
    aujourdhui = datetime.date.today()
    mois = aujourdhui.replace(day=1)
    blocs = ""
    for _ in range(n_mois):
        blocs += _calendrier_mois(mois, occupe, aujourdhui)
        mois = _mois_suivant(mois)
    return f'<div class="dispo-mois">{blocs}</div>'


def page_accueil():
    bat = BATIMENTS["viennois"]
    reperes = "".join(
        f'<li><span class="rep-l">{E(r["lieu"])}<em>{E(r["detail"])}</em></span>'
        f'<b class="{"tbd" if r.get("provisoire") else ""}">{E(r["val"])}</b></li>'
        for r in bat["reperes"])
    communs = "".join(
        f'<li><h4>{E(c["t"])}</h4><p>{E(c["d"])}'
        + ('<span class="soon"> — prochainement</span>' if c["soon"] else "")
        + "</p></li>" for c in bat["communs"])

    return f'''<section class="page" id="accueil">
<header class="hero">
{img(bat["medias"][0], "hero-img", eager=True)}
<div class="hero-txt"><div class="wrap">
<p class="alt">Le Bourg-d'Oisans · 720 m</p>
<h1>{E(MARQUE["titre"])}</h1>
<p class="lede-h">{E(MARQUE["sous_titre"])}</p>
<div class="hero-btns">
<a class="btn btn--light" href="#appartements">Voir les appartements</a>
<a class="btn btn--ghost-light" href="#contact">Nous écrire</a>
</div></div></div></header>

<section class="sec"><div class="wrap">
<p class="eyebrow">Nos appartements</p>
<h2>Ce que nous louons</h2>
{liste_logements()}
</div></section>

<section class="sec sec--paper"><div class="wrap">
<p class="eyebrow">Où c'est</p>
<div class="deux">
<div>
<h2>Au centre du village,<br>au pied des cols</h2>
<p class="lede">Le Bourg-d'Oisans est dans la vallée, à 720 m. C'est d'ici que
partent l'Alpe d'Huez et les grands cols, et c'est ici qu'on trouve les commerces,
le marché et les restaurants — au pied de l'immeuble.</p>
<ul class="reperes">{reperes}</ul>
</div>
<div class="deux-media">{img(bat["medias"][1])}{carte_osm(bat)}</div>
</div></div></section>

<section class="sec"><div class="wrap">
<p class="eyebrow">L'immeuble</p>
<div class="deux deux--inv">
<div class="deux-media">{img(bat["medias"][3])}</div>
<div>
<h2>{E(bat["nom"])}</h2>
<p class="lede">{E(bat["accroche"])} {E(bat["recit"])}</p>
<ul class="communs">{communs}</ul>
</div></div></div></section>

<section class="sec sec--dark"><div class="wrap">
<p class="eyebrow eyebrow--d">Deux saisons</p>
<div class="deux">
<div>
<h2>Des logements habités toute l'année</h2>
<p class="lede-d">L'été, nous louons à la nuit aux voyageurs. L'hiver, au mois,
aux gens qui viennent travailler dans la vallée et dans les stations. Nos
appartements ne restent pas fermés neuf mois par an : ils sont entretenus,
chauffés et utilisés en continu.</p>
<a class="btn btn--ghost-light" href="#a-propos">Qui nous sommes</a>
</div>
<div class="deux-media">{img(bat["medias"][2])}</div>
</div></div></section>
</section>'''


def page_appartements():
    return f'''<section class="page" id="appartements">
<section class="sec"><div class="wrap">
<p class="eyebrow">1 rue de Viennois · Le Bourg-d'Oisans</p>
<h2>Nos appartements</h2>
<p class="lede">Trois appartements dans le même immeuble, au centre du village.
Un seul interlocuteur, une seule adresse.</p>
{liste_logements()}
</div></section>
<section class="sec sec--paper"><div class="wrap">
<p class="eyebrow">Situation</p><h2>Où se trouve l'immeuble</h2>
{carte_osm(BATIMENTS["viennois"], "carte--large")}
</div></section></section>'''


def page_logement(l):
    bat = BATIMENTS[l["batiment"]]
    meds, autres = l["medias"], [x for x in visibles if x["id"] != l["id"]]

    galerie = ""
    if meds:
        galerie = ('<div class="gal">' + "".join(
            f'<div class="g{" g--lead" if i == 0 else ""}">{img(m, eager=(i == 0))}</div>'
            for i, m in enumerate(meds[:8])) + "</div>")

    faits = []
    if l["surface"]: faits.append((f'{l["surface"]} m²', "Surface"))
    else: faits.append((l["type"], "Type"))
    if l["capacite"]: faits.append((l["capacite"], "Voyageurs"))
    if l["chambres"] is not None: faits.append((l["chambres"], "Chambres"))
    if l["sdb"]: faits.append((l["sdb"], "Salle de bain"))
    if l["etage"] is not None: faits.append((f'{l["etage"]}ᵉ', "Étage"))
    faits.append((f'{bat["altitude"]} m', "Altitude"))

    blocs = ""
    for k in ("ete", "hiver"):
        s, rv = l["saisons"][k], l["reservation"].get(k, {})
        now = saison == k
        btn = ""
        if rv.get("url"):
            tgt = ' target="_blank" rel="noopener"' if rv["mode"] == "airbnb" else ""
            btn = (f'<a class="btn {"btn--light" if now else "btn--ghost"} btn--full" '
                   f'href="{E(rv["url"])}"{tgt}>{E(rv["libelle"])}</a>')
        note = f'<p class="book-n">{E(s["note"])}</p>' if s.get("note") else ""
        blocs += (f'<div class="book-r{" book-r--now" if now else ""}">'
                  f'<p class="book-w">{E(s["du"])} → {E(s["au"])}'
                  + ("<em>saison en cours</em>" if now else "")
                  + f'</p><p class="book-p">{prix_txt(l, k)}</p>{note}{btn}</div>')

    dec = ("<ul class=\"prat\">" + "".join(
        f"<li><span>{E(a)}</span><b>{E(b)}</b></li>" for a, b in l["pratique"]["decision"])
        + "</ul>") if l["pratique"]["decision"] else ""

    det = ('<details class="plus"><summary>Informations pratiques</summary><ul class="prat">'
           + "".join(f"<li><span>{E(a)}</span><b>{E(b)}</b></li>" for a, b in l["pratique"]["detail"])
           + "</ul></details>") if l["pratique"]["detail"] else ""

    lits = ("<ul class=\"lits\">" + "".join(
        f'<li><span>{E(c["ou"])}</span><b>{E(c["quoi"])}</b></li>' for c in l["couchages"])
        + "</ul>") if l["couchages"] else ""

    moments = ('<section class="sec sec--paper"><div class="wrap">'
               "<p class=\"eyebrow\">Ce qu'il faut savoir</p><ul class=\"moments\">"
               + "".join(f'<li><h4>{E(m["t"])}</h4><p>{E(m["d"])}</p></li>' for m in l["moments"])
               + "</ul></div></section>") if l["moments"] else ""

    equip = ""
    if l["equipements"]:
        g = "".join(f'<div class="eq"><h4>{E(k)}</h4><ul>'
                    + "".join(f"<li>{E(i)}</li>" for i in v) + "</ul></div>"
                    for k, v in l["equipements"].items())
        if l["bientot"]:
            g += ('<div class="eq"><h4>Prochainement</h4><ul>'
                  + "".join(f'<li class="soon">{E(i)}</li>' for i in l["bientot"]) + "</ul></div>")
        equip = (f'<section class="sec"><div class="wrap"><p class="eyebrow">Équipements</p>'
                 f'<h2>Ce que vous trouverez</h2><div class="eqs">{g}</div>{det}</div></section>')

    v = l["visite360"]
    v360 = ""
    if v.get("url"):
        v360 = (f'<section class="sec sec--dark"><div class="wrap">'
                f'<p class="eyebrow eyebrow--d">Visite immersive</p><h2>{E(v["titre"])}</h2>'
                f'<div class="v360"><iframe src="{E(v["url"])}" title="{E(v["titre"])}" '
                f'loading="lazy" allowfullscreen '
                f'allow="accelerometer; gyroscope; xr-spatial-tracking"></iframe></div>'
                f'</div></section>')

    faits_html = "".join(f'<div><b>{E(a)}</b><span>{E(b)}</span></div>' for a, b in faits)
    autres_html = "".join(carte_logement(x) for x in autres)
    desc = "".join(f"<p>{E(p)}</p>" for p in l["description"])
    pull = f'<p class="pull">{E(l["citation"])}</p>' if l["citation"] else ""

    dispo = ""
    if l["ical"]:
        occupe = recuperer_ical(l["ical"])
        if occupe is not None:
            precision = (" La réservation se confirme sur Airbnb."
                         if l["reservation"].get("ete", {}).get("mode") == "airbnb" else "")
            dispo = (f'<section class="sec sec--paper"><div class="wrap">'
                     f'<p class="eyebrow">Disponibilités</p><h2>Calendrier indicatif</h2>'
                     f'<p class="lede">Mis à jour automatiquement, à titre indicatif.'
                     f'{precision}</p>'
                     f'{calendrier_html(occupe)}'
                     f'<ul class="dispo-legende">'
                     f'<li><span class="dispo-j dispo-j--libre"></span>Libre</li>'
                     f'<li><span class="dispo-j dispo-j--occupe"></span>Occupé</li>'
                     f'</ul></div></section>')

    return f'''<section class="page" id="{E(l["id"])}">
<div class="lg-top"><div class="wrap">
<a class="back" href="#appartements">← Nos appartements</a>
<p class="kick">{E(l["kicker"])} · {E(bat["nom"])}, {E(bat["commune"])}</p>
<h1>{E(l["nom"])}</h1>
</div></div>
{galerie}
<div class="faits">{faits_html}</div>
<section class="sec"><div class="wrap lg-grid">
<div class="lg-txt"><div class="prose">{desc}</div>{pull}{lits}</div>
<aside class="lg-book"><div class="book">{blocs}</div>{dec}</aside>
</div></section>
{dispo}{moments}{equip}{v360}
<section class="sec sec--paper"><div class="wrap">
<p class="eyebrow">Où c'est</p><h2>{E(bat["nom"])}</h2>
<p class="lede">{E(bat["cp"])} {E(bat["commune"])} — {bat["altitude"]} m</p>
{carte_osm(bat, "carte--large")}
</div></section>
<section class="sec"><div class="wrap">
<p class="eyebrow">Dans le même immeuble</p><h2>Les autres appartements</h2>
<div class="cards">{autres_html}</div>
</div></section>
</section>'''


def page_apropos():
    txt = "".join(f"<p>{E(p)}</p>" for p in APROPOS["paragraphes"])
    return f'''<section class="page" id="a-propos">
<section class="sec"><div class="wrap deux">
<div><p class="eyebrow">À propos</p><h2>{E(APROPOS["titre"])}</h2>
<div class="prose">{txt}</div>
<a class="btn" href="#appartements">Voir les appartements</a></div>
<div class="deux-media">{img(APROPOS["media"])}</div>
</div></section></section>'''


def page_contact_etat(id_, titre, texte):
    return f'''<section class="page" id="{id_}">
<section class="sec"><div class="wrap wrap--etroit">
<p class="eyebrow">Contact</p><h2>{E(titre)}</h2>
<p class="lede">{E(texte)}</p>
<a class="btn" href="#accueil">Retour à l'accueil</a>
</div></section></section>'''


def page_contact():
    opts = "".join(f'<option>{E(l["nom"])}</option>' for l in visibles)
    tsk = FORMULAIRE["turnstile_site_key"]["v"]
    # Le site reste sans JavaScript tant que cette clé n'est pas renseignée :
    # le script Turnstile n'est écrit dans le document que si on l'utilise
    # vraiment (voir CLAUDE.md, exception documentée).
    turnstile = f'<div class="cf-turnstile" data-sitekey="{E(tsk)}"></div>' if tsk else ""
    turnstile_script = ('<script src="https://challenges.cloudflare.com/turnstile/v0/api.js" '
                         'async defer></script>') if tsk else ""
    email = MARQUE["email"]["v"]
    secours = (f' Vous pouvez aussi nous écrire directement à {E(email)}.' if email else "")
    return f'''<section class="page" id="contact">
<section class="sec"><div class="wrap wrap--etroit">
<p class="eyebrow">Contact</p><h2>Écrivez-nous</h2>
<p class="lede">Pour une réservation, une question, ou une demande de location
à la saison d'hiver. Nous répondons sous 24 heures.</p>
<form action="/api/contact" method="post">
<div class="r2">
<p class="f"><label for="n">Nom</label><input id="n" name="nom" autocomplete="name" required></p>
<p class="f"><label for="e">E-mail</label><input id="e" name="email" type="email"
autocomplete="email" inputmode="email" required></p></div>
<p class="f"><label for="t">Téléphone <span>(facultatif)</span></label>
<input id="t" name="tel" type="tel" autocomplete="tel" inputmode="tel"></p>
<p class="f"><label for="a">Appartement</label>
<select id="a" name="logement"><option>Peu importe</option>{opts}</select></p>
<p class="f"><label for="s">Type de séjour</label><select id="s" name="saison">
<option>À la nuit — mai à octobre</option>
<option>À la saison — novembre à avril</option></select></p>
<div class="r2">
<p class="f"><label for="d1">Du</label><input id="d1" name="du" type="date"></p>
<p class="f"><label for="d2">Au</label><input id="d2" name="au" type="date"></p></div>
<p class="f"><label for="m">Message</label><textarea id="m" name="message" required></textarea></p>
<input type="text" name="_gotcha" tabindex="-1" autocomplete="off" class="pot" aria-hidden="true">
{turnstile}
<button class="btn btn--full" type="submit">Envoyer le message</button>
<p class="rgpd">Vos coordonnées servent uniquement à répondre à votre demande.</p>
</form></div></section></section>
{page_contact_etat("contact-merci", "Message envoyé", "Merci, nous vous répondons sous 24 heures.")}
{page_contact_etat("contact-erreur", "Message non envoyé",
                    "Une erreur est survenue en envoyant votre message. Réessayez dans un instant." + secours)}
{turnstile_script}'''


def fichier_chantier():
    bat = BATIMENTS["viennois"]
    t = ["À COMPLÉTER — Le Cœur du Bourg",
         "Généré par build.py. Ce fichier n'est pas publié sur le site.", ""]
    for l in publies:
        if l["medias_manquants"]:
            t.append(f'PHOTOS · {l["nom"]} : ' + ", ".join(l["medias_manquants"]))
        if not l["visite360"].get("url"):
            t.append(f'VISITE 360 · {l["nom"]} : à réaliser, puis coller l\'URL dans visite360.url')
        if not l["ical"]:
            t.append(f'CALENDRIER · {l["nom"]} : coller les liens iCal Airbnb/Booking dans "ical"')
        m = [k for k, v in (l.get("admin") or {}).items()
             if isinstance(v, dict) and not v.get("v")]
        if m:
            t.append(f'ADMINISTRATIF · {l["nom"]} : ' + ", ".join(m))
    p = [k for k, v in PARTENAIRES.items() if v.get("provisoire")]
    if p: t.append("PARTENAIRES : accords à conclure — " + ", ".join(p))
    s = [c["t"] for c in bat["communs"] if c["soon"]]
    if s: t.append("IMMEUBLE : annoncés prochainement — " + ", ".join(s))
    r = [x["lieu"] for x in bat["reperes"] if x.get("provisoire")]
    if r: t.append("DISTANCES à mesurer : " + ", ".join(r))
    if not MARQUE["email"]["v"]:
        t.append("CONTACT : créer une adresse sur le domaine")
    t.append("FORMULAIRE : brancher Formspree ou Netlify Forms (attribut action)")
    t.append("LANGUES : publiée(s) " + ", ".join(REGLAGES["langue_publiee"])
             + " | prévues " + ", ".join(c for c, _ in REGLAGES["langues"]))
    t.append("LÉGAL : mentions légales, conditions de location, confidentialité")
    t.append("PHOTO : refaire soi-même la vue de la rue (celle du Café des 2 Mondes "
             "appartient à un tiers et n'est pas utilisée)")
    return "\n".join(t) + "\n"


CSS = (ICI / "style.css").read_text(encoding="utf-8")

langues = "".join(
    (f'<span class="on">{c.upper()}</span>' if c in REGLAGES["langue_publiee"]
     else f'<span class="off" title="bientôt">{c.upper()}</span>')
    for c, _ in REGLAGES["langues"])

pages = "".join([page_appartements(), page_apropos(), page_contact()]
                + [page_logement(l) for l in visibles]
                + [page_accueil()])          # accueil en dernier = vue par défaut

foot_l = "<br>".join(f'<a href="#{E(l["id"])}">{E(l["nom"])}</a>' for l in visibles)

DOC = f'''<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{E(MARQUE["nom"])} — Appartements au Bourg-d'Oisans</title>
<meta name="description" content="{E(MARQUE["sous_titre"])}">
<meta name="theme-color" content="#141C1F">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Inter:wght@400;500;600&family=Archivo+Narrow:wght@400;500;600&display=swap" rel="stylesheet">
<style>{CSS}</style>
</head>
<body>
<header class="bar"><div class="bar-in">
<a class="marque" href="#accueil"><span>{E(MARQUE["nom"])}</span><i>720 m</i></a>
<nav class="nav">
<a href="#appartements">Appartements</a>
<a href="#a-propos">À propos</a>
<a href="#contact">Contact</a></nav>
<p class="lang">{langues}</p>
</div></header>
<main>{pages}</main>
<footer><div class="wrap">
<div class="foot">
<div><p class="foot-n">{E(MARQUE["nom"])}</p>
<p>1 rue de Viennois<br>38520 Le Bourg-d'Oisans</p></div>
<div><h4>Appartements</h4><p>{foot_l}</p></div>
<div><h4>Contact</h4><p><a href="#contact">Formulaire de contact</a></p></div>
</div>
<p class="foot-bas">
<span>© {datetime.date.today().year} {E(MARQUE["nom"])} — photographies protégées</span>
<span>Mentions légales</span><span>Conditions de location</span><span>Confidentialité</span>
</p></div></footer>
</body></html>'''

# Sur Cloudflare (variable SORTIE=dist passée explicitement dans la commande
# de build), le site publié doit vivre dans un dossier séparé de la racine
# du dépôt — sinon data.py et build.py deviendraient téléchargeables
# publiquement à côté du site. Voir wrangler.jsonc (assets.directory) et
# MISE-EN-LIGNE.md.
out = pathlib.Path(os.environ["SORTIE"]) if os.environ.get("SORTIE") else ICI
out.mkdir(parents=True, exist_ok=True)

nom = "apercu-mobile.html" if APERCU else "index.html"
(out / nom).write_text(DOC, encoding="utf-8")
(ICI / "a-completer.txt").write_text(fichier_chantier(), encoding="utf-8")

if out != ICI and not APERCU:
    # Le HTML référence "photos/xxx.jpg" en chemin relatif : il faut que le
    # dossier photos/ existe à côté du site publié, pas seulement à la racine.
    dest_photos = out / "photos"
    if dest_photos.exists():
        shutil.rmtree(dest_photos)
    if PHOTOS.exists():
        shutil.copytree(PHOTOS, dest_photos)

mode = "aperçu (photos intégrées, allégées)" if APERCU else "site réel (photos en fichiers séparés, pleine qualité)"
print(f"{nom} — {len(DOC)//1024} Ko | {len(visibles)} logements | "
      f"{sum(1 for v in _cache.values() if v)} photos | {mode}")
