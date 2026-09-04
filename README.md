# JRD Habitat · Landings Google Ads (Pays Basque + Dordogne)

8 pages d'atterrissage pour trafic payant (Google Ads), pas pour du SEO :
**4 services × 2 zones**. Statique, aucun build côté hébergeur : se dépose telle
quelle sur Cloudflare Pages, Netlify ou Vercel.

Client : **JRD Habitat**, artisan multi-services qui alterne entre le
**Pays Basque (64)** et la **Dordogne (24)** selon la période de l'année.
Les campagnes ciblent la zone où il se trouve ; il suffit de changer les URLs
finales des annonces, les deux jeux de pages restent en ligne en permanence.

```
build.py                     générateur (constantes + configs des 2 zones)
templates/                   les 4 gabarits, avec jetons {{...}}
  demoussage-toiture.html
  couverture-renovation.html
  peinture-ravalement.html
  elagage.html
pays-basque/<service>/index.html   pages générées (NE PAS éditer à la main)
dordogne/<service>/index.html      pages générées (NE PAS éditer à la main)
index.html                   hub interne de recette (liens vers les 8 pages)
assets/                      styles.css, script.js, favicon, images (partagés)
```

Modifier une page = éditer le gabarit dans `templates/` (ou une config de zone
dans `build.py`), puis :

```bash
python3 build.py
```

## Aperçu local

Config `jrd-habitat` dans `.claude/launch.json` (port 4205) :

```bash
python3 -m http.server 4205 --directory "jrd-habitat-landing"
```

Les pages sont en **`noindex, nofollow`** tant qu'elles n'ont ni mentions
légales, ni SIRET, ni domaine définitif. Ça ne bloque pas Google Ads.

---

## 1. À remplacer avant la première annonce

Tout est centralisé dans les **constantes en tête de `build.py`** (une édition,
huit pages) :

| # | Quoi | Où |
|---|------|----|
| 1 | **Téléphone** : `06 00 00 00 00` est un placeholder | `PHONE_DISPLAY` + `PHONE_TEL` dans `build.py` |
| 2 | **Domaine** (proposition : `https://jrd-habitat.fr`) | `URL_BASE` dans `build.py` |
| 3 | **Clé Web3Forms** (`REMPLACER_PAR_VOTRE_CLE_WEB3FORMS`) | dans les 4 gabarits (2 formulaires chacun) |
| 4 | **Conversions Google Ads** (gtag inactif tant que `AW-XXXXXXXXXX`) | `ADS_GTAG`, `ADS_CONV_DEVIS`, `ADS_CONV_APPEL` dans `build.py` |
| 5 | **Mentions légales + SIRET + assurance** (exigés par Google Ads) | page à créer + bloc footer |
| 6 | **Avis Google réels** (sections `#avis` en `hidden`, ne rien inventer) | les 4 gabarits |
| 7 | **Prix** (affichés « Sur devis », n'inventer aucun tarif) | sections `#prix` |
| 8 | **Ville de base par zone** : Bayonne et Périgueux sont **supposées** | `SCHEMA_ADDRESS`, `PLACENAME`, lat/lng dans `build.py` |

### À confirmer avec l'artisan (rien n'a été validé)

- Le **nom commercial exact** (« JRD Habitat ») et le numéro de téléphone.
- Les **villes de rattachement** dans chaque zone (base = Bayonne / Périgueux par défaut).
- La **garantie décennale** : la landing couverture l'affiche (obligatoire pour
  ce métier) ; vérifier l'attestation avant diffusion. Les autres pages disent
  seulement « artisan assuré ».
- Le périmètre exact de l'élagage (démontage ? abattage ? haies ?) : la page
  reste volontairement sur « élagage / taille raisonnée ».

### Sources des photos (Pexels, licence libre)

**Les 16 visuels ont été téléchargés pour ce projet uniquement** : aucune image
partagée avec un autre site, aucune photo de chantier appartenant à un tiers.
À remplacer par des photos de chantiers JRD dès qu'il en fournit.

- Démoussage : hero 38867780 · mousse 9940556 · avant 36106266 · après 31161403
  · bande CTA 36884227
- Couverture : hero 37704251 · lucarnes 37634967 · pose tuiles 31771166
  · après 31161403 (partagée démoussage) · bande CTA 37623622
- Peinture : hero volet 14613134 · échafaudage 36894047 · enduit 5493667
  · finition 5493669 · façade fissurée 9562861
- Élagage : 2310483 · 6218318

---

## 2. Structure des pages

Chaque landing suit le modèle de conversion de l'agence : hero + formulaire au-dessus de la ligne de
flottaison, barre de réassurance, enjeu/agitation, process en 4 étapes,
avant/après, budget sans prix inventé, avis (masqués tant que vides), zone
d'intervention, FAQ, formulaire final + barre d'appel mobile.

Tracking déjà câblé dans `assets/script.js` :

- capture `gclid` / `utm_*` renvoyée dans chaque lead Web3Forms ;
- événements `dataLayer` : `form_start`, `generate_lead`, `phone_call`,
  taggés par page via `<body data-lp="service_zone">` ;
- conversions Ads (devis + appel) déclenchées dès que les IDs réels sont posés.

## 3. Campagnes Google Ads

Le compte, les actions de conversion et les campagnes sont gérés séparément par
l'agence, hors de ce dépôt. Ce qui concerne ce site :

- les identifiants de conversion sont dans les constantes de `build.py`
  (`ADS_GTAG`, `ADS_CONV_DEVIS`, `ADS_CONV_APPEL`) et se retrouvent dans le code
  des pages, comme toute balise de mesure ;
- les annonces pointent sur `<domaine>/<zone>/<service>/` : le domaine doit
  résoudre avant que Google accepte de valider une annonce ;
- le suffixe d'URL transmet le terme de recherche (`{keyword}`), indispensable au
  moteur d'alignement décrit plus bas.

## 4. Alignement requête → page (moteur de conversion)

Les campagnes portent 501 mots-clés couvrant des intentions très différentes
(urgence, prix, proximité, ville). Une page au titre figé perd ce trafic : le
visiteur ne lit pas son besoin. `assets/script.js` lit le terme de recherche
transmis par l'annonce et ajuste la page à la volée :

- **titre et sous-titre** remplacés par la variante d'intention (urgence, prix,
  hydrofuge, gouttière, rénovation, nettoyage, boiseries) ;
- **bandeau d'appel** injecté sur les intentions chaudes (fuite, branche
  dangereuse), cliquable et compté comme conversion appel ;
- **commune détectée** affichée dans l'étiquette de zone et préremplie dans le
  formulaire ;
- **besoin présélectionné** dans la liste déroulante.

Les variantes se déclarent par gabarit dans `window.LP_MATCH` (bloc en tête de
chaque template), les communes reconnues dans `window.LP_VILLES` (jeton
`VILLES_JS` de `build.py`). Sans paramètre dans l'URL, la page reste exactement
telle qu'elle est écrite.

Le terme arrive par le **suffixe d'URL finale** posé sur les campagnes :
`utm_source=google&utm_medium=cpc&utm_campaign={campaignid}&utm_content={adgroupid}&utm_term={keyword}&mt={matchtype}&res={network}`

Test rapide :
`/dordogne/couverture-renovation/?utm_term=couvreur+urgence+fuite+bergerac`

## 5. Poids des pages

Les visuels sont recadrés au ratio d'affichage et recompressés : le dossier
images est passé de 13 Mo à 4,2 Mo, la page peinture de 7,3 Mo à 1,3 Mo. Seul
le visuel du hero est chargé en priorité, le reste est en `loading="lazy"`.
Toute nouvelle image doit être recadrée au ratio de son emplacement (16/9 pour
hero et bande CTA, 4/3 pour les visuels de section) avant d'être posée.

## 6. Emplacements de preuve (avis, prix)

Les avis et les prix ne s'inventent pas, mais tout est câblé pour qu'ils se
posent en une ligne. Dans `build.py` :

```python
AVIS = [{"texte": "…", "prenom": "Marc", "commune": "Bergerac", "note": 5}]
PRIX = {"demoussage-toiture": ("à partir de 12 €/m²", "à partir de 22 €/m²")}
```

Un `python3 build.py` et, sur les 8 pages : la section avis se dévoile,
les cartes se remplissent, la note moyenne est injectée dans le schema
(`aggregateRating`), et « Sur devis » devient le tarif annoncé. Vides, les deux
blocs laissent la section masquée et les prix en « Sur devis ».
Repères de marché 2026 pour cadrer la discussion avec l'artisan, à faire
valider par lui : démoussage 10-30 €/m², ravalement 30-100 €/m², réparation de
toiture 200-3 000 €, élagage 80-1 000 € par arbre.

## 7. Déploiement

```bash
cd jrd-habitat-landing && vercel deploy --prod --yes
```

ou Cloudflare Pages (drag & drop du dossier, ou repo Git). Aucune étape de
build à configurer : `build.py` se lance en local avant commit.
