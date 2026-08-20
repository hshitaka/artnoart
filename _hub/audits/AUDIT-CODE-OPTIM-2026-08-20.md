# Audit _hub — code (optimisation)

Date : 20 août 2026  
Périmètre : le dossier code du site public (`index.html`, `index.css`, `index.js`, assets statiques, tests).  
Hors périmètre : UI visuelle, catalogue discographique, backend, `_kb`.

L’audit DWET du 17 août a rendu le site publiable. Celui-ci ne rejoue pas ce chantier : il mesure ce qui **pèse encore** au chargement et à l’usage, puis corrige.

## Question

Comment le code actuel fait-il attendre, retélécharger, ou recréer pour rien — et quoi corriger sans changer le geste (écouter, télécharger Direct / Fetch) ?

## C’est

Un audit de **poids et de travail inutile** dans le code déjà là.

## C’est pas

- Pas une refonte.
- Pas un hub artistique, pas kb-liens.
- Pas a2dd (livraison des vrais titres).
- Pas « on pourrait » : chaque P0/P1 appliqué a un geste déjà servi (page ouverte, lecture, fetch).

## Verdict

Le code est petit (HTML+CSS+JS ≈ 24 Ko). Le coût réel n’est pas un bundler manquant. Ce sont **trois polices web trop lourdes**, un **fetch qui refuse le cache**, et un **lecteur audio recréé à chaque clic**.

Les extraits WAV (4 × 215 Ko) ne se téléchargent qu’au geste : on les laisse en WAV, c’est le format démo annoncé.

## Constats

| Gravité | Fichier | Problème | Geste déjà servi |
| --- | --- | --- | --- |
| P0 | `index.html` | Google Fonts : 3 familles, **9 graisses** (`Manrope` 400–700, `Syne` 700+800, `IBM Plex Mono` 400+500). Le CSS n’utilise que 400, 700, 800. | Premier affichage |
| P0 | `index.js` | `fetch(..., { cache: "no-store" })` sur le catalogue et la voie Fetch. Chaque clic refetch le fichier alors qu’il est statique. | Téléchargement Fetch, 2ᵉ clic |
| P1 | `index.js` | `new Audio()` à chaque lecture. L’ancien nœud n’est pas réutilisé. | Play / Pause / autre piste |
| P1 | `index.js` | Pas de `playsInline` : sur iOS le player plein écran peut interrompre le flux. | Lecture mobile |
| P1 | `index.css` | Les cartes piste n’ont pas de `contain` : le navigateur repeint plus large que la carte. | Scroll, état `is-playing` |
| P2 | `index.js` | `DWET.loadCatalog()` n’est jamais appelé. Mort au runtime, pas un coût réseau. | — |
| P2 | `index.html` | Pistes recopiées à la main : les Ko affichés peuvent dériver du `catalog.json`. | Maintenance |
| P2 | WAV | 4 extraits PCM 16-bit / 22,05 kHz / 5 s. Correct pour un téléchargement WAV. Trop lourd seulement si on préchargeait tout (on ne le fait pas). | — |

## Corrections appliquées

1. **Polices** — ne demander que les graisses réellement peintes : Manrope 400+700, Syne 800, IBM Plex Mono 400. `display=swap` inchangé.
2. **Cache Fetch** — `cache: "no-store"` retiré. Fichiers versionnés avec le site : le navigateur peut les reposer.
3. **Lecteur unique** — un seul `Audio`, `playsInline`, pause/reprise sans recréer le nœud.
4. **Peinture** — `contain: layout style` sur `.track`.

## Hors correction (volontaire)

- Pas de bundler / minify : le projet n’a pas d’étape de build.
- Pas de MP3/OGG à la place du WAV : le catalogue et les tests DWET sont WAV.
- Pas de génération HTML depuis `catalog.json` : le HTML statique s’affiche sans JS.
- Pas d’auto-hébergement des woff2 dans cette passe (nouveaux binaires, autre chantier).

## Tests

```bash
cd "/workspace"
python3 -m unittest discover -s tests -p 'test_*.py' -v
```

Les tests DWET restent la porte d’entrée. `test_code_optim.py` verrouille polices, cache, et lecteur unique.

## Découvertes (pas corrigées ici)

- `loadCatalog()` est exposé sur `window.DWET` mais jamais branché à l’UI.
- Le mixeur à droite de Mix reste décoratif (`aria-hidden`).
- Les 4 WAV ont la même taille (220544 octets) mais des contenus distincts.
