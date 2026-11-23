# Sunday 22 November 2026 — The World in One Day

[![make.fun](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/Indodegen/news-image-20261122/rank.svg)](https://make.fun/bounty/news-image-20261122/leaderboard)
[![reward](https://make.fun/badge/news-image-20261122/Indodegen/news-image-20261122/reward.svg)](https://make.fun/bounty/news-image-20261122/leaderboard)

Entry for [make.fun news-image-20261122](https://make.fun/bounty/news-image-20261122):
sum up 22 November's world news in one image.

## The image

`entry.png` is a 1024×1024 newspaper front page — **40 stories, 7 regions,
every one dated Sunday 22 November 2026** — drawn entirely in code:

- **Lead:** COP31 ends with no deal — the EU rejects a final text that never
  names fossil fuels, and the summit closes two days late with no agreement.
- **Also leading:** Russia fires 186 drones at Ukraine (161 downed; a block
  falls in Dymer), and Iran claims two US radars hit in Bahrain while Bahrain
  says a civilian plant was hit and two people were hurt.
- **Two stories the leaders missed:** Russian missiles falling inside Poland
  (NATO calls it a serious airspace violation) and Ukrainian sea drones
  hitting a Russian warship at Benghazi.
- **Date discipline:** a DATE CHECK box names what was left out because it
  belongs to an earlier day — the Peru quake (Fri 20 Nov), the Myanmar
  genocide ruling (Thu 19 Nov), the Shenzhen summit (Thu–Fri), 'El Chapo
  Isidro' (Fri), BepiColombo (Sat), the Nvidia SEC probe (Fri) and the
  Kryvyi Rih strike (Sat). Every story is tagged REPORTED, CLAIM or FORECAST,
  and every one is sourced.

## How it is built

`generate.py` draws the page with Pillow and the Liberation fonts — real,
anti-aliased type, flat vector illustrations, a dot-matrix world map with
pins at the stories' longitudes and latitudes. No network, no randomness, no
timestamps: running it twice writes a byte-identical PNG.

`main.ts` (Node 22, standard library only) copies `entry.png` to
`/output/entry.png`, exactly as the kit's starter does.

```sh
python3 generate.py entry.png
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

## Sources

Reuters · AP · AFP · Al Jazeera · The Guardian · SCMP · ESPNcricinfo · FIA ·
Vatican News · Detiknews · Xinhua · ABC · MSF. Scenes are drawn
illustrations of reported events, not photographs.
