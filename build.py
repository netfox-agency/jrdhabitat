#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Générateur des landings JRD Habitat.

  templates/<service>.html  ×  2 zones  →  <zone>/<service>/index.html   (8 pages)

Usage :  python3 build.py
Éditer les templates ou les configs ci-dessous, puis relancer. Les pages
générées ne s'éditent jamais à la main (elles sont écrasées à chaque build).
"""

import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).parent

# ---------------------------------------------------------------- constantes
# ⚠️ PLACEHOLDERS : remplacer ici puis relancer le build (une seule fois pour les 8 pages).
PHONE_DISPLAY = "06 98 29 79 95"      # numéro réel JRD Habitat, fourni le 2026-09-03
PHONE_TEL = "+33698297995"
URL_BASE = "https://jrdhabitat.fr"        # domaine réel, en ligne
# Conversions du compte JRD Habitat 365-004-7844 (créées le 2026-08-25)
ADS_GTAG = "AW-18410008662"
ADS_CONV_DEVIS = "AW-18410008662/MyGrCPOc3OccENbgycpE"   # « Demande de devis (site) » 200 €
ADS_CONV_APPEL = "AW-18410008662/SkTQCPmc3OccENbgycpE"   # « Appel depuis le site » 100 €

# Mentions légales : tant que le SIRET n'est pas fourni, on n'affirme rien de faux.
# Dès qu'il l'envoie : SIRET = "812 345 678 00019" et le pied de page se complète seul.
SIRET = ""
ASSUREUR_DECENNALE = ""     # ex. "AXA, contrat n° 1234567"


def mentions_legales():
    bouts = ["JRD Habitat, entreprise familiale"]
    if SIRET:
        bouts.append("SIRET " + SIRET)
    if ASSUREUR_DECENNALE:
        bouts.append("Garantie décennale : " + ASSUREUR_DECENNALE)
    return " · ".join(bouts)


SERVICES = [
    "demoussage-toiture",
    "couverture-renovation",
    "peinture-ravalement",
    "elagage",
]

# ---------------------------------------------------------------- zones


def pills(cities, main):
    out = []
    for c in cities:
        cls = "zone zone-main" if c == main else "zone"
        out.append('<span class="%s">%s</span>' % (cls, c))
    return "\n      ".join(out)


def schema_area(cities):
    return "[" + ",".join('{"@type":"City","name":"%s"}' % c for c in cities[:14]) + "]"


PB_CITIES = [
    "Bayonne", "Anglet", "Biarritz", "Bidart", "Guéthary", "Saint-Jean-de-Luz",
    "Ciboure", "Urrugne", "Hendaye", "Ascain", "Saint-Pée-sur-Nivelle", "Sare",
    "Espelette", "Cambo-les-Bains", "Ustaritz", "Hasparren", "La Bastide-Clairence",
    "Saint-Palais", "Tarnos", "Ondres", "Capbreton", "Hossegor",
]

BX_CITIES = [
    "Mérignac", "Pessac", "Talence", "Gradignan", "Villenave-d'Ornon",
    "Le Haillan", "Eysines", "Le Bouscat", "Bègles", "Cestas",
    "Saint-Médard-en-Jalles", "Bruges", "Blanquefort", "Canéjan",
    "Léognan", "Martignas-sur-Jalle", "Pian-Médoc", "Saint-Aubin-de-Médoc",
]

DD_CITIES = [
    # Bergeracois d'abord : c'est là qu'il est installé (Gardonne, 24680).
    "Bergerac", "Gardonne", "Prigonrieux", "La Force", "Lamonzie-Saint-Martin",
    "Le Fleix", "Sainte-Foy-la-Grande", "Sigoulès", "Monbazillac", "Creysse",
    "Mouleydier", "Lalinde", "Eymet", "Issigeac",
    # Reste du département, couvert par la campagne.
    "Périgueux", "Trélissac", "Sarlat-la-Canéda", "Mussidan", "Montpon-Ménestérol",
    "Ribérac", "Le Bugue", "Saint-Astier",
]

ZONES = {
    "pays-basque": {
        "ZONE_KEY": "pays_basque",
        "TITLE_GEO": "au Pays Basque",
        "CITIES3": "Bayonne · Anglet · Biarritz",
        "CITIES3_COMMA": "Bayonne, Anglet, Biarritz",
        "ZONE_ALL": "dans tout le Pays Basque et le sud des Landes",
        "GEO_LINE": "Bayonne · Anglet · Biarritz · tout le Pays Basque et le sud des Landes",
        "GEO_REGION": "FR-64",
        "PLACENAME": "Bayonne",
        "LAT": "43.4933",
        "LNG": "-1.4748",
        "VILLE_PLACEHOLDER": "Bayonne, Anglet, Biarritz…",
        "VILLES_JS": '["Bayonne","Anglet","Biarritz","Saint-Jean-de-Luz","Hendaye","Bidart","Ustaritz","Cambo-les-Bains","Hasparren","Ciboure","Urrugne","Tarnos","Capbreton"]',
        # Adresse réelle (fiche Google JRD HABITAT) — identique sur les 3 zones
        "SCHEMA_ADDRESS": '{"@type":"PostalAddress","streetAddress":"Route de Sigoulès","addressLocality":"Gardonne","postalCode":"24680","addressRegion":"Nouvelle-Aquitaine","addressCountry":"FR"}',
        "SCHEMA_AREA": schema_area(PB_CITIES),
        "ZONE_PILLS": pills(PB_CITIES, "Bayonne"),
        "ZONE_H2": "Bayonne, Biarritz et <em>tout le Pays Basque.</em>",
        "ZONE_SECTION_LEAD": "Nous intervenons sur la côte comme dans l'intérieur du Pays Basque, ainsi que dans le sud des Landes, de Hendaye à Capbreton.",
        "FOOTER_GEO": "Bayonne, Anglet, Biarritz et tout le Pays Basque (64)",
        "TRUST_LOCAL_B": "Présents au Pays Basque",
        "TRUST_LOCAL_S": "Déplacement rapide, 64 et sud des Landes",
        "WHY_LEAD": {
            "demoussage-toiture": "Au Pays Basque, l'air marin, la pluie généreuse et la douceur du climat font pousser mousses et lichens toute l'année. Laissés en place, ils travaillent la toiture de l'intérieur.",
            "couverture-renovation": "Entre la pluie soutenue, l'air marin et les coups de vent d'ouest, les toitures basques sont mises à l'épreuve toute l'année. Une couverture fatiguée ne prévient pas : elle lâche pendant l'averse.",
            "peinture-ravalement": "Façades blanches, colombages rouge ou vert, boiseries exposées aux embruns : au Pays Basque, la façade fait la maison. Mais l'air marin et la pluie attaquent peintures et enduits plus vite qu'ailleurs.",
            "elagage": "Chênes, platanes, pins : au Pays Basque, la végétation pousse vite, et les coups de vent d'automne ne pardonnent ni les branches mortes ni les charpentières trop lourdes au-dessus d'un toit.",
        },
        "FAQ_CLIMATE_A": "Le climat basque, doux et très arrosé, accélère nettement la pousse des mousses et des lichens, surtout sur les pans exposés au nord ou sous les arbres. Un contrôle tous les deux à trois ans suffit, et un démoussage dès que les tuiles verdissent ou que les gouttières se chargent.",
        "FAQ_MATERIAL_Q": "Travaillez-vous la tuile canal des maisons basques ?",
        "FAQ_MATERIAL_A": "Oui. Nous travaillons la tuile canal et la tuile mécanique, majoritaires sur les maisons basques et landaises, ainsi que l'ardoise. Le remplacement se fait à l'identique pour préserver l'aspect de la maison.",
    },
    "bordeaux": {
        "ZONE_KEY": "bordeaux",
        "TITLE_GEO": "autour de Bordeaux",
        "CITIES3": "Mérignac · Pessac · Talence",
        "CITIES3_COMMA": "Mérignac, Pessac, Talence",
        "ZONE_ALL": "dans l'ouest de la métropole bordelaise",
        "GEO_LINE": "Mérignac · Pessac · Talence · tout l'ouest de la métropole",
        "GEO_REGION": "FR-33",
        "PLACENAME": "Mérignac",
        # point médian Mérignac / Pessac : le rayon de 15 km couvre toute la
        # ceinture pavillonnaire ouest sans partir dans le Médoc ni les Landes
        "LAT": "44.8220",
        "LNG": "-0.6370",
        "VILLE_PLACEHOLDER": "Mérignac, Pessac, Talence…",
        "VILLES_JS": '["Mérignac","Pessac","Talence","Gradignan","Villenave-d\'Ornon","Le Haillan","Eysines","Le Bouscat","Bègles","Cestas","Saint-Médard-en-Jalles","Bruges","Blanquefort","Canéjan","Léognan","Bordeaux"]',
        # Adresse réelle (fiche Google JRD HABITAT) — identique sur les 3 zones
        "SCHEMA_ADDRESS": '{"@type":"PostalAddress","streetAddress":"Route de Sigoulès","addressLocality":"Gardonne","postalCode":"24680","addressRegion":"Nouvelle-Aquitaine","addressCountry":"FR"}',
        "SCHEMA_AREA": schema_area(BX_CITIES),
        "ZONE_PILLS": pills(BX_CITIES, "Mérignac"),
        "ZONE_H2": "Mérignac, Pessac et <em>l'ouest de la métropole.</em>",
        "ZONE_SECTION_LEAD": "Nous intervenons sur la ceinture pavillonnaire à l'ouest de Bordeaux, de Saint-Médard-en-Jalles à Gradignan, en passant par Mérignac, Pessac, Le Haillan et Villenave-d'Ornon.",
        "FOOTER_GEO": "Mérignac, Pessac, Talence et l'ouest de la métropole bordelaise (33)",
        "TRUST_LOCAL_B": "Nous intervenons sur la métropole",
        "TRUST_LOCAL_S": "Devis et déplacement gratuits",
        "WHY_LEAD": {
            "demoussage-toiture": "Le climat bordelais, doux et très arrosé d'octobre à mars, fait proliférer mousses et lichens sur les toitures. Sous les pins de la ceinture ouest, l'ombre permanente garde le toit humide toute l'année et accélère encore la pousse.",
            "couverture-renovation": "Tuile canal des échoppes, ardoise des maisons de maître, toits plats des extensions : la métropole mélange tous les types de couverture. Entre les pluies d'automne et les coups de vent atlantiques, une toiture fatiguée lâche pendant l'averse.",
            "peinture-ravalement": "Pierre blonde des échoppes, enduits clairs, volets et boiseries : à Bordeaux la façade fait la valeur de la maison. Mais l'humidité océanique noircit les murs et attaque les peintures plus vite qu'ailleurs.",
            "elagage": "Pins maritimes, chênes et platanes : les jardins de la ceinture ouest sont arborés, et les coups de vent d'automne ne pardonnent ni les branches mortes ni les charpentières trop lourdes au-dessus d'un toit.",
        },
        "FAQ_CLIMATE_A": "Le climat océanique bordelais, doux et humide une grande partie de l'année, accélère nettement la pousse des mousses et des lichens, surtout sur les pans nord et sous les pins. Un contrôle tous les deux à trois ans suffit, et un démoussage dès que les tuiles verdissent ou que les gouttières se chargent.",
        "FAQ_MATERIAL_Q": "Travaillez-vous la tuile canal des échoppes bordelaises ?",
        "FAQ_MATERIAL_A": "Oui. Nous travaillons la tuile canal, très présente sur les échoppes et les maisons de la métropole, ainsi que la tuile mécanique et l'ardoise. Le remplacement se fait à l'identique pour préserver le caractère de la maison.",
    },
    "dordogne": {
        "ZONE_KEY": "dordogne",
        "TITLE_GEO": "en Dordogne",
        "CITIES3": "Bergerac · Sainte-Foy · Périgueux",
        "CITIES3_COMMA": "Bergerac, Sainte-Foy-la-Grande, Périgueux",
        "ZONE_ALL": "dans toute la Dordogne",
        "GEO_LINE": "Bergerac · Sainte-Foy · Lalinde · toute la Dordogne (24)",
        "GEO_REGION": "FR-24",
        "PLACENAME": "Bergerac",
        "LAT": "44.8358",
        "LNG": "0.3486",
        "VILLE_PLACEHOLDER": "Bergerac, Sainte-Foy, Lalinde…",
        "VILLES_JS": '["Bergerac","Gardonne","Prigonrieux","La Force","Lamonzie-Saint-Martin","Le Fleix","Sainte-Foy-la-Grande","Sigoulès","Creysse","Mouleydier","Lalinde","Eymet","Issigeac","Périgueux","Sarlat","Mussidan","Montpon-Ménestérol","Ribérac"]',
        # Adresse réelle (fiche Google JRD HABITAT) — identique sur les 3 zones
        "SCHEMA_ADDRESS": '{"@type":"PostalAddress","streetAddress":"Route de Sigoulès","addressLocality":"Gardonne","postalCode":"24680","addressRegion":"Nouvelle-Aquitaine","addressCountry":"FR"}',
        "SCHEMA_AREA": schema_area(DD_CITIES),
        "ZONE_PILLS": pills(DD_CITIES, "Bergerac"),
        "ZONE_H2": "Bergerac, le Bergeracois et <em>toute la Dordogne.</em>",
        "ZONE_SECTION_LEAD": "Nous intervenons dans toute la Dordogne, du Périgord blanc au Périgord noir, de Périgueux à Sarlat et de Bergerac à Brantôme.",
        "FOOTER_GEO": "Bergerac, Sainte-Foy-la-Grande, Périgueux et toute la Dordogne (24)",
        "TRUST_LOCAL_B": "Installés en Dordogne",
        "TRUST_LOCAL_S": "Basés dans le Bergeracois, on couvre le 24",
        "WHY_LEAD": {
            "demoussage-toiture": "En Dordogne, l'humidité des vallées de l'Isle, de la Vézère et de la Dordogne, les brouillards d'automne et l'ombre des chênes font prospérer mousses et lichens sur les toitures. Laissés en place, ils travaillent la couverture de l'intérieur.",
            "couverture-renovation": "Tuile plate, tuile canal, toits pentus du Périgord : les toitures de Dordogne sont belles mais exigeantes. Entre gel d'hiver, orages d'été et humidité des vallées, une couverture fatiguée ne prévient pas : elle lâche pendant l'orage.",
            "peinture-ravalement": "Pierre blonde, enduits à la chaux, colombages du Bergeracois, volets et boiseries : en Dordogne, la façade fait le charme de la maison. Mais l'humidité, le gel et le soleil d'été attaquent peintures et enduits année après année.",
            "elagage": "Chênes, noyers, tilleuls : en Dordogne, les arbres font partie de la maison. Mais un houppier trop lourd ou une branche morte au-dessus d'un toit ne pardonnent pas au premier orage.",
        },
        "FAQ_CLIMATE_A": "Le Périgord cumule vallées humides, brouillards d'automne et toitures souvent entourées d'arbres : la mousse s'y installe vite, surtout sur les pans nord. Un contrôle tous les deux à trois ans suffit, et un démoussage dès que les tuiles verdissent ou que les gouttières se chargent.",
        "FAQ_MATERIAL_Q": "Travaillez-vous la tuile plate des toits périgourdins ?",
        "FAQ_MATERIAL_A": "Oui. Nous travaillons la tuile plate et la tuile canal, typiques des toits périgourdins, ainsi que la tuile mécanique et l'ardoise. Le remplacement se fait à l'identique pour préserver le caractère de la maison.",
    },
}

# ---------------------------------------------------------------- preuves
# ⚠️ NE RIEN INVENTER ICI. Ces trois blocs restent vides tant que JRD n'a pas
# fourni le vrai matériel. Dès qu'il l'envoie, on remplit et on relance le
# build : les sections se dévoilent toutes seules sur les 8 pages.
#
# Avis : copier le texte EXACT de l'avis Google, prénom et commune réels.
#   AVIS = [{"texte": "...", "prenom": "Marc", "commune": "Bergerac", "note": 5}, ...]
AVIS = [
    # Avis Google réels de la fiche JRD HABITAT (5,0 ★ · 3 avis), recopiés mot pour mot.
    # ⚠️ Ils datent de 2021-2022 et parlent de réfection de toiture, pas de démoussage.
    # Le premier est tronqué par Google (« … Plus ») : à compléter depuis la fiche.
    {"prenom": "Jacky P.", "commune": "avril 2022", "note": 5,
     "texte": "Intervention de très bonne qualité : réfection complète d'une toiture. "
              "Travail fini et soigné. Le nettoyage des abords a été parfaitement réalisé."},
    {"prenom": "Laëtitia A.", "commune": "janvier 2021", "note": 5,
     "texte": "Entreprise professionnelle très sérieuse, de qualité, que je recommande."},
    {"prenom": "Kigan R.", "commune": "février 2021", "note": 5,
     "texte": "Professionnel, travail très soigné."},
]

# Prix : deux formules par service. Laisser vide = « Sur devis ».
#   Repères de marché 2026 pour cadrer la discussion avec lui, À VALIDER :
#   démoussage 10-30 €/m² · ravalement 30-100 €/m² · réparation toiture
#   200-3 000 € · élagage 80-1 000 €/arbre.
PRIX = {}          # {"demoussage-toiture": ("à partir de 12 €/m²", "à partir de 22 €/m²")}


def bloc_avis():
    """Cartes d'avis + attribut hidden + fragment aggregateRating."""
    if not AVIS:
        return {
            "AVIS_HIDDEN": " hidden",
            "AVIS_CARTES": (
                '<figure class="review"><div class="stars" aria-label="5 étoiles sur 5">★★★★★</div>'
                "<blockquote>[ Avis Google à coller mot pour mot ]</blockquote>"
                "<figcaption>[ Prénom ] · [ Commune ]</figcaption></figure>" * 3),
            "SCHEMA_RATING": "",
        }
    cartes = []
    for a in AVIS:
        note = int(a.get("note", 5))
        cartes.append(
            '<figure class="review"><div class="stars" aria-label="%d étoiles sur 5">%s</div>'
            "<blockquote>%s</blockquote><figcaption>%s · %s</figcaption></figure>"
            % (note, "★" * note, a["texte"], a["prenom"], a["commune"]))
    moyenne = sum(int(a.get("note", 5)) for a in AVIS) / len(AVIS)
    return {
        "AVIS_HIDDEN": "",
        "AVIS_CARTES": "\n      ".join(cartes),
        "SCHEMA_RATING": ',"aggregateRating":{"@type":"AggregateRating","ratingValue":"%.1f","reviewCount":"%d"}'
                         % (moyenne, len(AVIS)),
    }


def bloc_prix(service):
    a, b = PRIX.get(service, ("", ""))
    return {"PRIX_A": a or "Sur devis", "PRIX_B": b or "Sur devis"}

# ---------------------------------------------------------------- build

CONSTANTS = {
    "PHONE_DISPLAY": PHONE_DISPLAY,
    "PHONE_TEL": PHONE_TEL,
    "URL_BASE": URL_BASE,
    "ADS_GTAG": ADS_GTAG,
    "ADS_CONV_DEVIS": ADS_CONV_DEVIS,
    "ADS_CONV_APPEL": ADS_CONV_APPEL,
    "MENTIONS_LEGALES": mentions_legales(),
}


def render(template_text, zone_slug, zone, service):
    tokens = dict(CONSTANTS)
    tokens["ZONE_SLUG"] = zone_slug
    tokens.update(bloc_avis())
    tokens.update(bloc_prix(service))
    for k, v in zone.items():
        if k == "WHY_LEAD":
            tokens["WHY_LEAD"] = v[service]
        else:
            tokens[k] = v
    out = template_text
    for k, v in tokens.items():
        out = out.replace("{{%s}}" % k, v)
    leftover = sorted(set(re.findall(r"\{\{([A-Z0-9_]+)\}\}", out)))
    if leftover:
        sys.exit("Jetons non résolus dans %s/%s : %s" % (zone_slug, service, ", ".join(leftover)))
    return out


def tpl_tokens_accueil():
    """Jetons propres à l'accueil (il n'appartient à aucune zone)."""
    return {}


def main():
    count = 0
    for service in SERVICES:
        tpl = (ROOT / "templates" / (service + ".html")).read_text(encoding="utf-8")
        for zone_slug, zone in ZONES.items():
            html = render(tpl, zone_slug, zone, service)
            dest = ROOT / zone_slug / service / "index.html"
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_text(html, encoding="utf-8")
            count += 1
            print("  %s" % dest.relative_to(ROOT))
    # Page d'accueil : c'est elle que voient les gens qui tapent le domaine
    # ou qui cherchent « JRD Habitat » avant d'appeler. Elle ne doit jamais
    # rester un index technique.
    tpl = (ROOT / "templates" / "accueil.html").read_text(encoding="utf-8")
    tokens = dict(CONSTANTS)
    tokens.update(bloc_avis())
    for k, v in tpl_tokens_accueil().items():
        tokens[k] = v
    out = tpl
    for k, v in tokens.items():
        out = out.replace("{{%s}}" % k, v)
    leftover = sorted(set(re.findall(r"\{\{([A-Z0-9_]+)\}\}", out)))
    if leftover:
        sys.exit("Jetons non résolus dans l'accueil : %s" % ", ".join(leftover))
    (ROOT / "index.html").write_text(out, encoding="utf-8")
    count += 1
    print("  index.html")
    print("%d pages générées." % count)


if __name__ == "__main__":
    main()
