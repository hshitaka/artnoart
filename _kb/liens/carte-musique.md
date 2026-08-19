# Carte musique — test kb-liens

Première carte. Pas les autres domaines (cuisine, herbe, pedago), sauf si un geste musical y a **déjà** touché.

Règle : [_kb/liens/REGLE.md](REGLE.md).
Perf : [_kb/perf/FONCTION.md](../perf/FONCTION.md).

## Nœuds (matière musicale)

| Nœud | Rôle | Pas ça |
| --- | --- | --- |
| DJ | Pratique, canon, sets | Pas l’état de flow |
| djay | Outil de mix DJ | Pas Ableton |
| Ableton | Session, clips, Push, pièce | Pas djay |
| Voix | Prise, présence, traitement | Pas « la perf » |
| Prod | Pièces, sessions, extraits | Pas le mix d’écoute |
| Mix | Bus, balance, extraits de set | Pas la prod |

kb-perf n’est **pas** un nœud musical. Il s’attache à un geste, quel que soit le domaine.

## Liens tenus

Uniquement ce qui a déjà servi (site ARTNOART, dossier presse, pratique nommée ici).

### Prod → Mix

- **Geste :** même atelier ARTNOART : extraits prod et extraits mix publiés ensemble.
- **Statut :** tenu

### Mix → DJ

- **Geste :** un extrait du site s’appelle *Live Set Excerpt* — le mix pointe déjà vers le set.
- **Statut :** tenu

### DJ → djay

- **Geste :** pratique courante nommée pour cette carte : le geste DJ passe par djay.
- **Statut :** tenu

### Ableton → Prod

- **Geste :** ARTNOART déclare Ableton comme outil de l’atelier (pièces et outils live).
- **Statut :** tenu

### Ableton → pédagogie

- **Geste :** ateliers déjà animés autour d’Ableton Live, Push et MaxMSP.
- **Statut :** tenu
- **Note :** la pedago n’a pas encore sa carte. Le lien existe quand même : le geste a eu lieu.

### Outils live → scène

- **Geste :** Bionic Looper (Bionic Orchestra 2.0, Cie Organic Orchestra) — outil déjà joué en spectacle vivant.
- **Statut :** tenu
- **Note :** MaxMSP / looper restent dans les outils. Pas un nouveau hub.

## Liens vers kb-perf (pas de hiérarchie)

Ces lignes ne rangent pas la perf dans la musique. Elles disent : **ce geste-là a besoin de l’état**.

### Set DJ → kb-perf

- **Geste :** un set est un flow (corps + psy), pas seulement une playlist.
- **Statut :** tenu
- **Contre-exemple :** une perf culinaire invoquerait le **même** kb-perf, avec une autre matière. Pas un kb-perf-musique.

### Voix live → kb-perf

- **Geste :** la voix en public est un état, pas seulement une piste.
- **Statut :** tenu pour le live ; une voix seulement posée en prod **n’écrit pas** ce lien.

## Pas de lien (volontairement)

Rien d’écrit, donc pas de lien :

- Voix → Prod (pas de session nommée ici)
- Voix → djay
- djay → Ableton (deux outils ; un pont seulement si un même geste les a déjà enchaînés)
- Cuisine, herboristerie (hors de cette carte, jusqu’à un geste réel)
- kb-perf au-dessus de DJ / Ableton / Prod

## Comment tester

1. Prendre un geste musical réel de cette semaine.
2. Ouvrir la règle. Le lien a-t-il déjà servi ?
3. Si oui : une ligne `De → vers` + geste + `tenu`.
4. Si le geste demandait un flow : ajouter `→ kb-perf`, sans changer la fonction de kb-perf.
5. Si non : ne rien écrire.
