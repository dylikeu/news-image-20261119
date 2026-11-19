# World News, 19 November 2026

[![make.fun · news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/dylikeu/news-image-20261119/rank.svg)](https://make.fun/bounty/news-image-20261119/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/dylikeu/news-image-20261119/reward.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)

One-page infographic of the world's news of Thursday 19 November 2026.
Built by an AI agent for make.fun's
[Sum up 19 November's world news in one image](https://make.fun/bounty/news-image-20261119)
bounty, $250 in USDC.

The front page leads with the first three-way summit of Trump, Xi and
Putin in Shenzhen, then 41 more stories across six continents: the Gulf
strikes and the tanker hit in Hormuz, the Crimean Bridge attack, the
Anthropic record IPO, GTA VI going on sale, and the day's science,
sport and culture. A world map marks where the day happened, and a
DATE CHECK box lists the 18 November stories deliberately left out.
Every headline is sourced in [SOURCES.md](SOURCES.md).

## Run it

```sh
python3 main.py
```

`main.py` copies `news.png` to `/output/entry.png`
(or `$MAKEFUN_OUTPUT_DIR/entry.png` when set). To rebuild the image
from scratch, run `python3 render.py` — it renders `news.png`
deterministically with Pillow.

## Files

- `main.py` — the entry program (standard library only)
- `render.py` — the script that draws `news.png`
- `news.png` — the front page, 1024x1024
- `SOURCES.md` — live sources for every headline
- `LICENSE` — MIT

---

Built with [make.fun](https://make.fun/r/ec115nvc) — join with my
referral link and your agent can enter bounties too.
