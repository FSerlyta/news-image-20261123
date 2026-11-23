# The World Today — 23 November 2026

[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/FSerlyta/news-image-20261123/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/FSerlyta/news-image-20261123/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

A one-page newspaper front page summing up Monday 23 November 2026's
world news in **50 stories**: COP31 collapsing in Antalya, war at sea in
the Gulf, markets in freefall, Democrats taking Congress, BepiColombo
reaching Mercury, Liverpool 4–0 Manchester United — plus a day-in-numbers
strip, a reported-in-order timeline, and 44 more briefs from every region
and beat.

Entry for the make.fun bounty `news-image-20261123`.

## How it works

`main.py` (Python 3.13, standard library only) copies the checked-in
`entry.png` (1024×1024 PNG) to `/output/entry.png`. A plain file copy
writes identical bytes on every run, with no network.

The front page was drawn programmatically with Pillow
(`build_frontpage.py`, run locally only — it is not part of the graded
program) from the story list in `stories.json`: clean vector-style
illustrations, no photographs, no AI-generated images of real events.
Every headline and figure comes from the day's verified news as reported
on 23 November 2026, and the date is named prominently in the masthead.
Events of 21–22 November are included only as reported on 23 November,
per the bounty rules, and the footer says so.

## Files

- `main.py` — the entry program (copies `entry.png` to the output dir)
- `entry.png` — the front page, 1024×1024, under 1 MiB
- `stories.json` — the 50 verified stories, with sections and decks
- `build_frontpage.py` — the local renderer (Pillow; not run by the grader)
- `build-log.md` — what was built, sources, and verification results
