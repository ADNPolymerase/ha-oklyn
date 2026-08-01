<p align="center">
  <img src="https://raw.githubusercontent.com/ADNPolymerase/ha-oklyn/main/custom_components/oklyn/brand/logo.png" alt="Oklyn" height="80">
</p>

# Oklyn pour Home Assistant

[![hacs_badge](https://img.shields.io/badge/HACS-Default-blue.svg)](https://github.com/hacs/default)
[![GitHub Release](https://badgen.net/github/release/ADNPolymerase/ha-oklyn)](https://github.com/ADNPolymerase/ha-oklyn/releases)
[![Hassfest](https://github.com/ADNPolymerase/ha-oklyn/actions/workflows/hassfest.yml/badge.svg)](https://github.com/ADNPolymerase/ha-oklyn/actions/workflows/hassfest.yml)
[![HA Version](https://img.shields.io/badge/Home%20Assistant-2024.1%2B-blue.svg)](https://www.home-assistant.io/)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/ADNPolymerase/ha-oklyn/blob/main/LICENSE)
[![Buy Me A Coffee](https://img.shields.io/badge/Buy%20Me%20A%20Coffee-support-yellow.svg?logo=buy-me-a-coffee)](https://buymeacoffee.com/adnpolymerase)

<a href="https://buymeacoffee.com/adnpolymerase" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-orange.png" alt="Buy Me A Coffee" height="60"></a>
<a href="https://adnpolymerase.github.io/HA/" target="_blank"><img src="https://raw.githubusercontent.com/ADNPolymerase/HA/main/assets/site-button.svg" alt="Link to my github.io for my other projects" height="60"></a>

Intégration custom pour le **boîtier piscine Oklyn**, https://www.oklyn.fr/ publiée via HACS.

> 🇬🇧 [Read in English](README.md)

> 🎴 **Carte dédiée disponible :** [Oklyn Card](https://github.com/ADNPolymerase/oklyn-card) — carte Lovelace avec seuils pH/RedOx, contrôle pompe, auxiliaires et correction pH. Aucune dépendance, éditeur visuel complet.
> [![Ouvrir dans HACS](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=ADNPolymerase&repository=oklyn-card&category=plugin)

---

## Fonctionnalités

- Capteurs **pH, ORP/RedOx (mV), températures eau et air, sel (g/L, modèle Sel)** — avec un attribut `status` d'alerte Oklyn (`normal` / `low` / `high`) utilisé par [Oklyn Card](https://github.com/ADNPolymerase/oklyn-card) pour la coloration.
- Sélecteur **mode pompe** (`auto` / `on` / `off`) et capteur binaire **pompe en marche** (état électrique réel, indépendant de la commande).
- Interrupteurs **Auxiliaires 1 et 2**.
- Configuration 100 % UI, scrutation cloud (`api.oklyn.fr`), flow de ré-authentification, diagnostics (token jamais exposé), traductions française/anglaise/russe.

---

## Installation (HACS)

Disponible directement dans HACS — aucun dépôt personnalisé à ajouter.

1. Ouvrez **HACS**, recherchez **Oklyn** et téléchargez-le.
2. Redémarrez Home Assistant.
3. **Paramètres → Appareils et services → Ajouter une intégration** → recherchez **Oklyn**.

En dépôt personnalisé : HACS → **⋮** → **Dépôts personnalisés** → `https://github.com/ADNPolymerase/ha-oklyn`, catégorie **Intégration**.

Alternative manuelle : copiez `custom_components/oklyn/` dans `config/custom_components/`, redémarrez, puis ajoutez l'intégration.

---

## Configuration

La configuration demande un nom d'appareil (optionnel) et votre **clef API** — dans l'application Oklyn : **Mon Compte → Clef API**. L'identifiant de l'appareil est toujours `my`.

---

## Options

Après la configuration, allez dans **Paramètres → Appareils et services → Oklyn → Configurer** pour ajuster :

| Option | Défaut | Description |
|---|---|---|
| Modèle Oklyn | Filtration + Analyse | Votre modèle de boîtier — détermine les capteurs créés (voir ci-dessous) |
| Intervalle de scrutation | 60 s | Fréquence d'interrogation de l'API (30 / 60 / 120 / 300 s) |
| Activer l'auxiliaire 1 | Oui | Créer l'entité interrupteur Aux 1 |
| Activer l'auxiliaire 2 | Oui | Créer l'entité interrupteur Aux 2 |
| Nom de l'auxiliaire 1 | Auxiliaire 1 | Nom personnalisé pour le switch Aux 1 |
| Nom de l'auxiliaire 2 | Auxiliaire 2 | Nom personnalisé pour le switch Aux 2 |

Les trois modèles correspondent à la [gamme officielle Oklyn](https://www.oklyn.fr/assistant-piscine-connecte/) : **Filtration** (températures, pompe, auxiliaires), **+ Analyse** (ajoute pH, RedOx), **+ Sel** (ajoute le sel g/L). Les modifications prennent effet immédiatement.

---

## Entités

| Entité | Type | Description |
|---|---|---|
| `sensor.oklyn_ph` | Capteur | Valeur pH (modèles Analyse) — attribut `status` : `normal` / `low` / `high` |
| `sensor.oklyn_redox` | Capteur | ORP / RedOx en mV (modèles Analyse) — attribut `status` |
| `sensor.oklyn_water_temperature` | Capteur | Température eau en °C — attribut `status` |
| `sensor.oklyn_air_temperature` | Capteur | Température air en °C |
| `sensor.oklyn_salt` | Capteur | Taux de sel en g/L (modèle Sel uniquement) — attribut `status` |
| `binary_sensor.oklyn_pump_running` | Capteur binaire | État réel de la pompe (device class `running`) |
| `select.oklyn_pump_mode` | Choix | Commande pompe : auto / on / off |
| `switch.oklyn_auxiliaire_1` | Interrupteur | Sortie auxiliaire 1 |
| `switch.oklyn_auxiliaire_2` | Interrupteur | Sortie auxiliaire 2 |

---

## Capture d'écran

![Oklyn Card](https://raw.githubusercontent.com/ADNPolymerase/ha-oklyn/main/docs/oklyn-card.fr.png)

---

## Exemple de tableau de bord

La méthode recommandée est la carte dédiée **[Oklyn Card](https://github.com/ADNPolymerase/oklyn-card)** (voir plus haut). Deux exemples YAML prêts à l'emploi sont aussi fournis : [`examples/dashboard.yaml`](examples/dashboard.yaml) (cartes natives uniquement) et [`examples/dashboard-bubble.yaml`](examples/dashboard-bubble.yaml) (nécessite Bubble Card + Pool Monitor Card depuis HACS). Collez-les via **Tableau de bord → ✏️ Modifier → ⋮ → Éditeur de configuration brute** et ajustez les identifiants d'entités si besoin.

---

## Comportement important

L'API Oklyn distingue la **commande** (`pump` = `auto`/`on`/`off`, `aux` = `on`/`off`) de l'**état réel** (`status`). En mode `auto`, le boîtier gère le planning en interne : `status` peut différer de la commande, c'est normal. Le select pompe affiche la commande et expose `status` / `running` / `in_transition` en attributs ; les interrupteurs auxiliaires reflètent l'état réel, les décalages temporaires étant exposés via `in_transition`. Après chaque commande, les données sont rafraîchies immédiatement, puis à nouveau ~6 s plus tard pour capter la transition.

---

## Dépannage

- **Authentification invalide** — token rejeté : **Paramètres → Appareils et services → Oklyn → ⋮ → Ré-authentifier**.
- **Impossible de se connecter** — l'API Oklyn est inaccessible ; vérifiez votre connexion et l'état du service Oklyn.
- **Auxiliaire 2 indisponible** — certains modèles n'ont pas de seconde sortie (404 → entité marquée indisponible) ; désactivez-la dans les options.
- **Entités bloquées sur « Indisponible »** — consultez les journaux (filtre `oklyn`), ou activez le débogage : `logger: logs: custom_components.oklyn: debug`.

---

## Confidentialité et limitations

Le token API est stocké chiffré, jamais journalisé, jamais exposé dans les attributs, et masqué dans les diagnostics. Appareil unique (`/device/my`), scrutation cloud (pas d'API locale ni de push), Aux 2 absent de certaines révisions matérielles, horodatages API sans fuseau horaire.

---

## Contribuer

Issues et pull requests bienvenues sur <https://github.com/ADNPolymerase/ha-oklyn/issues>.
