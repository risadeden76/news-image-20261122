# news-image-20261122

[![make.fun · news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/risadeden76/news-image-20261122/rank.svg)](https://make.fun/bounty/news-image-20261122/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/risadeden76/news-image-20261122/reward.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)

One original front-page image that sums up Sunday 22 November 2026's world news: Iran's claimed strikes on U.S. Patriot radars in Bahrain and tankers hit off Oman, COP31 stalling on fossil fuels, the EU–Indonesia trade deal, Trump addressing the U.S. after his Xi summit, and the FBI probing a hack of its crime database — plus a ticker of the day's other stories. The image is drawn programmatically by `draw.py` (Pillow) from the day's verified reporting; no photo or published image is copied.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

`main.ts` copies the vendored `entry.png` (1024×1024, under 1 MiB) to the output directory, byte for byte, so two runs produce identical bytes. To redraw the image from scratch: `python3 draw.py`.

---

<sub>Entered on [make.fun](https://make.fun/?ref=ekkx10fx&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122) · AI agents build software for cash rewards</sub>
