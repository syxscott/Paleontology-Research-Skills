---
name: paleo-china-news
description: 🦕 Aggregate Chinese paleontology / fossil-discovery news from official Chinese sources (国家岩矿化石标本资源共享平台 nkocs.com, 中国古生物学会 palaeontology.cn, 中国科学院古脊椎所 ivpp.ac.cn). Use when the user asks about "中国最新化石发现", "国内古生物新闻", "中国恐龙发现", or wants recent Chinese-language reporting on fossils, paleobiology, and stratigraphy. Returns structured JSON with title, source, date, summary, URL, and tags.
---

# Chinese Paleontology News Aggregator

Fetches recent fossil news from official Chinese paleontology / geosciences institutions and renders them as structured JSON.

## When to Use

- "中国最近有什么新的恐龙化石发现?"
- "云南/辽宁/贵州的化石新闻"
- "中国古生物学会最近的学术动态"
- "热河生物群最新研究进展"
- "近期 IVPP (古脊椎所) 的成果"

## When NOT to Use

- Peer-reviewed papers in English → use `paleo-crossref`
- Specific fossil occurrence data → use `paleo-pbdb`
- International (non-Chinese) news → use general web search

## Data Sources

| Source | URL | Coverage |
|---|---|---|
| 国家岩矿化石标本资源共享平台 | nkocs.com | Specimen records, news from museums nationwide |
| 中国古生物学会 | palaeontology.cn | Society announcements, conferences, awards |
| 中国科学院古脊椎所 (IVPP) | ivpp.cas.cn | Research papers, expedition reports |

⚠️ Public web scraping with polite delays. Sites' HTML structure may change; if a fetch fails, the script returns a clear error rather than crashing.

## Usage

```bash
# Fetch latest news from all sources
python3 scripts/china_news_fetch.py --limit 20

# Filter by keyword (Chinese or English)
python3 scripts/china_news_fetch.py --keyword 恐龙 --limit 10
python3 scripts/china_news_fetch.py --keyword "Yixian"

# Only one source
python3 scripts/china_news_fetch.py --source nkocs --limit 10
python3 scripts/china_news_fetch.py --source ivpp

# Time-window filter (last N days, if dates are parseable)
python3 scripts/china_news_fetch.py --since-days 30
```

## Output

```json
{
  "source": "China Fossil News Aggregator",
  "query": {"keyword": "恐龙", "since_days": 30, "source": "all"},
  "fetched_at": "2026-06-03T14:30:00Z",
  "count": 5,
  "items": [
    {
      "title": "辽西热河生物群发现新种带羽毛恐龙",
      "source": "nkocs.com",
      "date": "2026-05-20",
      "url": "http://nkocs.com/...",
      "summary": "...",
      "tags": ["热河生物群", "辽宁", "白垩纪", "带羽毛恐龙"]
    }
  ]
}
```

## Notes

- This skill **does not** maintain its own database of news; every run fetches live from the source sites.
- Network errors return graceful empty results (`count: 0`, `errors` array populated).
- For long-term archival, pipe the output into `paleo-memory` (out of scope of this skill).
