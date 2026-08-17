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
python3 tests/test_downloads.py
```

Vérifie le catalogue, les codes HTTP, l’identité binaire disque/réseau, et le câblage HTML des deux voies.

## Audit

Le rapport (constats d’origine, corrections, UI) est dans [`AUDIT.md`](AUDIT.md).
