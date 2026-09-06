# SLAM.SYSTEMS

Official website of **SLAM.SYSTEMS**, a brand of watermoon.communication GmbH (Switzerland), with R&D in Shenzhen.

This build follows the boss-confirmed package **SLAM.SYSTEMS_v2.2.6**:

- script-aligned titles, taglines and body copy
- activated project emails (`i@slam.systems`)
- Swiss address in Bülach alongside Shenzhen
- landing pages with title artwork
- three languages: German (default), English (`/en/`), Simplified Chinese (`/zh/`)
- Start Your Project video overlay + on-page embed

The earlier FTP v1.6 reconstruction remains in `vendor/ftp-v1.6/`. The v2.2.6 HTML snapshot is in `vendor/v2.2.6/`.

The original handball hero photograph is not regenerated.

## Preview

```bash
python3 -m http.server 4173
```

Open http://127.0.0.1:4173/

Public GitHub Pages previews:

- https://zhangcheng0688.github.io/slam-systems-site/
- https://zhangcheng0688.github.io/AI_Find_Customer/

## Publish to the official repo

From the parent checkout, with write access to `slam-systems-site`:

```bash
./scripts/push-to-official-repo.sh
```
