# The World in One Day — Thursday 19 November 2026

![Bounty](https://make.fun/badge/news-image-20261119.svg)
![Rank](https://make.fun/badge/news-image-20261119/dylikeu/news-image-20261119/rank.svg)
![Reward](https://make.fun/badge/news-image-20261119/dylikeu/news-image-20261119/reward.svg)

One front page that sums up the world's news of **Thursday 19 November 2026**:
**42 stories across 7 regions** — politics, economy, tech, science, health,
climate, sport and culture — with a big date masthead, a world map marking
the 12 drawn stories, a DATE CHECK box, and 30 numbered one-line briefs.

The day's leads: the first Trump–Xi–Putin three-way summit in Shenzhen,
the ICJ's final Rohingya genocide ruling, a record $81.3bn Anthropic IPO,
and the worldwide launch of GTA VI.

Bounty: https://make.fun/bounty/news-image-20261119

Built with https://make.fun/r/ec115nvc

## Run it

```sh
python3 main.py
```

That renders `news.png` (1024×1024, ≤1 MiB) and copies it to
`/output/entry.png` (or `$MAKEFUN_OUTPUT_DIR/entry.png`). Stdlib + Pillow
only, no network, deterministic — two runs produce byte-identical output.

## Files

- `render.py` — draws `news.png` from scratch (masthead, map, cards, briefs).
- `main.py` — entrypoint: runs `render.py`, copies the image to the output dir.
- `news.png` — the rendered front page.
- `SOURCES.md` — one live source per story, all dated 19 November 2026.
- `LICENSE` — MIT.
