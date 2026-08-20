# ARTNOART

Site d’atelier d’**Arnaud Bannais** : production, mix, extraits téléchargeables.

## Lancer en local

```bash
python3 -m http.server 4173
```

Ouvrir [http://127.0.0.1:4173](http://127.0.0.1:4173).

## Voies de téléchargement (DWET)

Chaque fichier expose deux voies :

| Voie | Déclencheur | Mécanisme |
| --- | --- | --- |
| **Direct** | lien `a[download]` | le navigateur enregistre l’URL telle quelle |
| **Fetch** | bouton `data-dwet-mode="fetch"` | `fetch` → `Blob` → `URL.createObjectURL` |

Le module navigateur est exposé sur `window.DWET`.
Le catalogue machine est dans `assets/downloads/catalog.json`.

## Tests

```bash
python3 -m unittest discover -s tests -p 'test_*.py' -v
```

Vérifie le catalogue, les voies HTTP, le câblage HTML Direct/Fetch, et les corrections d’optimisation (polices, cache, lecteur unique).

## Audit

Le rapport d’origine (constats, UI, DWET) est dans [`AUDIT.md`](AUDIT.md).  
L’audit **optimisation du code** est dans [`_hub/audits/AUDIT-CODE-OPTIM-2026-08-20.md`](_hub/audits/AUDIT-CODE-OPTIM-2026-08-20.md).
