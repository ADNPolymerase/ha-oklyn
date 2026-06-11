# Oklyn pour Home Assistant

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/ADNPolymerase/ha-oklyn)
[![HA Version](https://img.shields.io/badge/Home%20Assistant-2024.1%2B-blue.svg)](https://www.home-assistant.io/)
[![Buy Me A Coffee](https://img.shields.io/badge/Buy%20Me%20A%20Coffee-support-yellow.svg?logo=buy-me-a-coffee)](https://buymeacoffee.com/adnpolymerase)

<a href="https://buymeacoffee.com/adnpolymerase" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-orange.png" alt="Buy Me A Coffee" height="60"></a>

Intégration custom pour le **boîtier piscine Oklyn**, https://www.oklyn.fr/ publiée via HACS.

> 🎴 **Carte dédiée disponible :** [Oklyn Card](https://github.com/ADNPolymerase/oklyn-card) — carte Lovelace avec seuils pH/RedOx, contrôle pompe, auxiliaires et correction pH. Aucune dépendance, éditeur visuel complet.
> [![Ouvrir dans HACS](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=ADNPolymerase&repository=oklyn-card&category=plugin)

---

## Fonctionnalités

- Capteur **pH**
- Capteur **ORP / RedOx** (mV)
- Capteur **température eau** (°C)
- Capteur **température air** (°C)
- Sélecteur **mode pompe** : `auto` / `on` / `off`
- Interrupteur **Auxiliaire 1**
- Interrupteur **Auxiliaire 2**
- Configuration 100 % via l'interface — aucun YAML requis
- Scrutation cloud via `https://api.oklyn.fr/public/v1/`
- Flow de ré-authentification si le token expire
- Support des diagnostics (token jamais exposé)
- Traductions française et anglaise

---

## Installation via HACS

1. Dans Home Assistant, ouvrez **HACS → Intégrations**.
2. Cliquez sur le menu **⋮ → Dépôts personnalisés**.
3. Ajoutez `https://github.com/ADNPolymerase/ha-oklyn` avec la catégorie **Intégration**.
4. Recherchez **Oklyn** et cliquez sur **Télécharger**.
5. Redémarrez Home Assistant.
6. Allez dans **Paramètres → Appareils et services → Ajouter une intégration** et recherchez **Oklyn**.

---

## Installation manuelle

1. Téléchargez ou clonez ce dépôt.
2. Copiez le dossier `custom_components/oklyn/` dans le répertoire
   `config/custom_components/` de votre Home Assistant.
3. Redémarrez Home Assistant.
4. Allez dans **Paramètres → Appareils et services → Ajouter une intégration** et recherchez **Oklyn**.

---

## Configuration

Lors de la configuration, les champs suivants sont demandés :

| Champ | Obligatoire | Défaut | Description |
|---|---|---|---|
| Nom de l'appareil | Non | Oklyn | Nom affiché dans HA |
| Token API | Oui | — | Votre `X-Api-Token` depuis l'application Oklyn |

L'identifiant de l'appareil est toujours `my` — vous n'avez pas à le saisir.

### Comment obtenir votre clef API

L'accès à l'API est sécurisé par une clef privée gérée dans l'application Oklyn :
**Oklyn → Mon Compte → Clef API**

---

## Options

Après la configuration, allez dans **Paramètres → Appareils et services → Oklyn → Configurer** pour ajuster :

| Option | Défaut | Description |
|---|---|---|
| Intervalle de scrutation | 60 s | Fréquence d'interrogation de l'API (30 / 60 / 120 / 300 s) |
| Activer l'auxiliaire 1 | Oui | Créer l'entité interrupteur Aux 1 |
| Activer l'auxiliaire 2 | Oui | Créer l'entité interrupteur Aux 2 |
| Nom de l'auxiliaire 1 | Auxiliaire 1 | Nom personnalisé pour le switch Aux 1 |
| Nom de l'auxiliaire 2 | Auxiliaire 2 | Nom personnalisé pour le switch Aux 2 |

Les modifications prennent effet immédiatement (l'intégration se recharge automatiquement).

---

## Entités

| Entité | Type | Description |
|---|---|---|
| `sensor.oklyn_ph` | Capteur | Valeur pH |
| `sensor.oklyn_redox` | Capteur | ORP / RedOx en mV |
| `sensor.oklyn_water_temperature` | Capteur | Température eau en °C |
| `sensor.oklyn_air_temperature` | Capteur | Température air en °C |
| `select.oklyn_pump_mode` | Choix | Commande pompe : auto / on / off |
| `switch.oklyn_auxiliaire_1` | Interrupteur | Sortie auxiliaire 1 |
| `switch.oklyn_auxiliaire_2` | Interrupteur | Sortie auxiliaire 2 |

---

## Capture d'écran

![Oklyn Card](docs/oklyn-card.png)

---

## Exemple de tableau de bord

### Oklyn Card (recommandé)

Une carte Lovelace dédiée est disponible — pH/RedOx avec seuils, températures,
contrôle pompe, auxiliaires (interrupteur ou régulateur), correction pH.
Aucune dépendance, éditeur visuel complet.

[![Ouvrir dans HACS](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=ADNPolymerase&repository=oklyn-card&category=plugin)
→ [ADNPolymerase/oklyn-card](https://github.com/ADNPolymerase/oklyn-card)

### Exemples YAML

Deux exemples prêts à l'emploi sont fournis :

- [`examples/dashboard.yaml`](examples/dashboard.yaml) — **cartes natives uniquement**
  (aucune dépendance HACS) : jauges de qualité de l'eau (pH / RedOx), tuiles de
  température avec historique 24h, sélecteur de mode pompe et interrupteurs auxiliaires.
- [`examples/dashboard-bubble.yaml`](examples/dashboard-bubble.yaml) — rendu plus soigné,
  mais **nécessite deux plugins frontend HACS** (installation en 1 clic) :
  - Bubble Card : [![Ouvrir dans HACS](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=Clooos&repository=Bubble-Card&category=plugin)
  - Pool Monitor Card : [![Ouvrir dans HACS](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=wilsto&repository=pool-monitor-card&category=plugin)

  Boutons de mode pompe, contrôles auxiliaires 1/2 (chacun dans son bloc optionnel),
  et un panneau complet de qualité de l'eau.

Pour les utiliser : **Tableau de bord → ✏️ Modifier → ⋮ → Éditeur de configuration brute**,
puis collez les cartes. Ajustez les identifiants d'entités si vous les avez renommés
(note : les identifiants par défaut dépendent de la langue de votre Home Assistant).

---

## Comportement important

### Pompe

L'entité pompe reflète la **commande** envoyée à l'API Oklyn, pas nécessairement l'état réel.

- `pump` (champ API) = commande : `auto`, `on` ou `off`
- `status` (champ API) = état réel actuel : `on` ou `off`

En mode **auto**, le boîtier Oklyn gère le planning de la pompe en interne.
`status` peut être `on` ou `off` alors que la commande est `auto` — c'est **normal**.

L'entité `select.oklyn_pump_mode` :
- Affiche `current_option` = `pump` (la commande)
- Expose `status`, `running` et `in_transition` en attributs
- `in_transition` est `true` uniquement quand la commande est `on` ou `off` et diffère de `status`
  (jamais quand la commande est `auto`)

### Auxiliaires

- `aux` (champ API) = commande envoyée : `on` ou `off`
- `status` (champ API) = état réel actuel : `on` ou `off`

L'état `is_on` de l'interrupteur reflète **status** (état réel), pas la commande.
Un décalage temporaire entre commande et status est normal et exposé via `in_transition`.

### Après une commande

Après l'envoi d'une commande (pompe ou auxiliaire), l'intégration rafraîchit immédiatement les données,
puis programme un second rafraîchissement ~6 secondes plus tard pour capter la transition d'état réelle.

---

## Dépannage

### Authentification invalide

Votre token API a été rejeté. Allez dans **Paramètres → Appareils et services → Oklyn → ⋮ →
Ré-authentifier** pour saisir un nouveau token.

### Impossible de se connecter

L'API Oklyn est inaccessible. Vérifiez votre connexion internet et l'état du service Oklyn.

### Auxiliaire 2 indisponible

Certains modèles Oklyn ne disposent pas d'une seconde sortie auxiliaire. Si `aux2` renvoie une erreur 404,
l'entité est automatiquement marquée comme indisponible. Vous pouvez la désactiver dans les options.

### Entités bloquées sur "Indisponible"

Consultez **Paramètres → Système → Journaux** et filtrez sur `oklyn` pour les détails.
Activez les logs de débogage en ajoutant à votre `configuration.yaml` :

```yaml
logger:
  logs:
    custom_components.oklyn: debug
```

---

## Confidentialité

Le token API est stocké de manière chiffrée dans le stockage des entrées de configuration de Home Assistant.
Il n'est **jamais** journalisé, jamais exposé dans les attributs d'entité, et jamais inclus
dans les exports de diagnostics (il apparaît comme `**REDACTED**`).

---

## Limitations connues

- Appareil unique uniquement — l'API Oklyn utilise `/device/my` sans support multi-appareils.
- Scrutation cloud — pas d'API locale ni de notifications push.
- L'auxiliaire 2 peut ne pas être disponible sur certaines révisions matérielles Oklyn.
- Les horodatages de l'API ne contiennent pas d'information de fuseau horaire ; ils sont stockés tels quels.

---

## Contribuer

Issues et pull requests bienvenues sur <https://github.com/ADNPolymerase/ha-oklyn/issues>.
