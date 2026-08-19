# Carte musique — test kb-liens

Première carte. Pas les autres domaines (cuisine, herbe, pedago), sauf si un geste musical y a **déjà** touché.

Règle : [_kb/liens/REGLE.md](REGLE.md).
Perf : [_kb/perf/FONCTION.md](../perf/FONCTION.md).

## Nœuds (matière musicale)

| Nœud | Rôle | Pas ça |
| --- | --- | --- |
| kb-dj | Pratique, canon, sets | Pas l’état de flow |
| djay | Outil de mix DJ | Pas Ableton |
| mashup | Geste qui croise live et studio | Pas un outil, pas un hub |
| Prod | Pièces, sessions, extraits | Pas le mix d’écoute |
| Ableton | Session, clips, Push, pièce | Pas djay |
| Voix | Prise, présence, traitement | Pas « la perf » |
| Mix | Bus, balance, extraits de set | Pas la prod |

kb-perf n’est **pas** un nœud musical. Il s’attache à un geste, quel que soit le domaine.

## Losange mashup (tenu)

Un seul geste, déjà nommé : le mashup. Quatre coins. Le mashup est le croisement, pas un cinquième hub.

```
        kb-dj                 prod
           \                 /
            \               /
              mashup
            /               \
           /                 \
        djay               Ableton
```

- **kb-dj** — les sources, le canon qui entre dans le mashup
- **djay** — le mashup joué / trouvé en live
- **Ableton** — le mashup construit / figé en session
- **prod** — le mashup devenu pièce

Ce n’est pas « djay pourrait parler à Ableton ». C’est **le même mashup** qui a déjà servi des deux côtés.

Les côtés du losange ne s’écrivent pas à part. Ils tiennent **parce que** le mashup les a déjà tenus.

## Autres liens tenus

Gestes distincts du losange.

### Prod → Mix

- **Geste :** même atelier ARTNOART : extraits prod et extraits mix publiés ensemble.
- **Statut :** tenu

### Mix → kb-dj

- **Geste :** un extrait du site s’appelle *Live Set Excerpt* — le mix pointe déjà vers le set.
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

### Mashup live → kb-perf

- **Geste :** un mashup joué (djay) est un flow, pas seulement un fichier.
- **Statut :** tenu pour le live ; un mashup seulement assemblé en prod **n’écrit pas** ce lien.

### Voix live → kb-perf

- **Geste :** la voix en public est un état, pas seulement une piste.
- **Statut :** tenu pour le live ; une voix seulement posée en prod **n’écrit pas** ce lien.

## Pas de lien (volontairement)

Rien d’écrit, donc pas de lien :

- Voix → Prod (pas de session nommée ici)
- Voix → djay
- Cuisine, herboristerie (hors de cette carte, jusqu’à un geste réel)
- kb-perf au-dessus de kb-dj / Ableton / Prod
- Découper le losange en ponts séparés djay → Ableton « au cas où »

## Comment tester

1. Prendre un geste musical réel de cette semaine.
2. Ouvrir la règle. Le lien a-t-il déjà servi ?
3. Si c’est un mashup qui a touché kb-dj, djay, prod et Ableton : c’est le losange, pas quatre lignes nouvelles.
4. Si le geste demandait un flow : ajouter `→ kb-perf`, sans changer la fonction de kb-perf.
5. Si non : ne rien écrire.
