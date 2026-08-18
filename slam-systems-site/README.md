# SLAM.SYSTEMS

Official website of **SLAM.SYSTEMS**, a brand of watermoon.communication gmbh (Switzerland), with R&D in Shenzhen.

This folder is the complete static site. It does **not** belong in the AI customer-finder repository. Publish it to its own GitHub repo: [zhangcheng0688/slam-systems-site](https://github.com/zhangcheng0688/slam-systems-site).

## Preview

```bash
python3 -m http.server 4173
```

Open http://127.0.0.1:4173/

## Publish to the official repo

From the parent checkout, with write access to `slam-systems-site`:

```bash
./scripts/push-to-official-repo.sh
```

Or create a new empty GitHub repository and pass its URL:

```bash
./scripts/push-to-official-repo.sh git@github.com:YOUR_ORG/slam-systems-site.git
```
