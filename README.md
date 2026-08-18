# SLAM.SYSTEMS

Official website of **SLAM.SYSTEMS**, a brand of watermoon.communication gmbh (Switzerland), with R&D in Shenzhen.

Visual and information architecture follow the boss-confirmed FTP package **SLAM.SYSTEMS_FTP_UPLOAD_v1.6**.

This folder is the complete static site. It does **not** belong in the AI customer-finder repository. Publish it to its own GitHub repo: [zhangcheng0688/slam-systems-site](https://github.com/zhangcheng0688/slam-systems-site).

## Preview

```bash
python3 -m http.server 4173
```

Open http://127.0.0.1:4173/

Public working preview (GitHub Pages on this finder repo is blocked):

https://raw.githack.com/zhangcheng0688/AI_Find_Customer/gh-pages/index.html

## Hero

Theme **01 is the original handball photograph**. Ice hockey (02) and football (03) are additional sports themes. The handball file is not regenerated.

## Publish to the official repo

From the parent checkout, with write access to `slam-systems-site`:

```bash
./scripts/push-to-official-repo.sh
```
