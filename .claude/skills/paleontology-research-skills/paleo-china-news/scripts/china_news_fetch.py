#!/usr/bin/env python3
"""Aggregate Chinese paleontology news from public web sources.

⚠️ This script scrapes public news listings politely (default 1 req per source,
1-second delay between calls). It is best-effort: when a site's HTML changes
or is offline, the affected source is skipped with an explanatory error.
"""
from __future__ import annotations

import argparse
import datetime as dt
import html
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

_HERE = os.path.dirname(os.path.abspath(__file__))
_SHARED = os.path.normpath(os.path.join(_HERE, "..", "..", "scripts"))
if _SHARED not in sys.path:
    sys.path.insert(0, _SHARED)

from paleo_common import print_json  # noqa: E402

UA = ("Mozilla/5.0 (compatible; Paleontology-Research-Skills/1.0; "
      "+https://github.com/syxscott/Paleontology-Research-Skills; "
      "respectful crawler)")
TIMEOUT = 30

SOURCES = {
    "nkocs": {
        "name": "nkocs.com (国家岩矿化石标本资源共享平台)",
        "url": "http://www.nkocs.com/wenxian/list.aspx",
        "fallback_listing_re": re.compile(
            r'<a[^>]+href="([^"]+)"[^>]*>([^<]{6,80}?(化石|恐龙|古生物|地层|寒武|奥陶|侏罗|白垩|二叠|三叠)[^<]*)</a>',
            re.IGNORECASE,
        ),
    },
    "palaeontology": {
        "name": "中国古生物学会 (palaeontology.cn)",
        "url": "http://www.palaeontology.cn",
        "fallback_listing_re": re.compile(
            r'<a[^>]+href="([^"]+)"[^>]*>\s*([^<]{6,80}?)\s*</a>',
            re.IGNORECASE,
        ),
    },
    "ivpp": {
        "name": "中国科学院古脊椎所 (ivpp.cas.cn)",
        "url": "http://www.ivpp.cas.cn/xwdt/",
        "fallback_listing_re": re.compile(
            r'<a[^>]+href="([^"]+)"[^>]*>\s*([^<]{6,100}?)\s*</a>',
            re.IGNORECASE,
        ),
    },
}

DATE_RE = re.compile(r"(20\d{2})[-/年.](\d{1,2})[-/月.](\d{1,2})")

# Simple keyword → tag mapping for auto-tagging
TAG_MAP = {
    "恐龙": "恐龙", "鸟": "古鸟", "翼龙": "翼龙", "鱼": "古鱼",
    "三叶虫": "三叶虫", "菊石": "菊石", "腕足": "腕足类",
    "寒武": "寒武纪", "奥陶": "奥陶纪", "志留": "志留纪", "泥盆": "泥盆纪",
    "石炭": "石炭纪", "二叠": "二叠纪", "三叠": "三叠纪", "侏罗": "侏罗纪",
    "白垩": "白垩纪", "古近": "古近纪", "新近": "新近纪",
    "辽宁": "辽宁", "云南": "云南", "贵州": "贵州", "新疆": "新疆",
    "热河": "热河生物群", "澄江": "澄江生物群", "凯里": "凯里生物群",
}


def _request(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            data = resp.read()
            # Try common Chinese encodings
            for enc in ("utf-8", "gb18030", "gbk", "gb2312"):
                try:
                    return data.decode(enc), None
                except UnicodeDecodeError:
                    continue
            return data.decode("utf-8", errors="replace"), None
    except urllib.error.HTTPError as e:
        return None, f"HTTP {e.code}: {e.reason}"
    except urllib.error.URLError as e:
        return None, f"Network error: {e.reason}"
    except (TimeoutError, OSError) as e:
        return None, f"Request failed: {e}"


def _resolve(base_url, href):
    return urllib.parse.urljoin(base_url, href)


def _extract_date(text):
    m = DATE_RE.search(text)
    if m:
        try:
            y, mo, d = int(m.group(1)), int(m.group(2)), int(m.group(3))
            return dt.date(y, mo, d).isoformat()
        except (ValueError, TypeError):
            pass
    return None


def _auto_tags(title):
    tags = []
    for k, v in TAG_MAP.items():
        if k in title and v not in tags:
            tags.append(v)
    return tags


def _scrape_source(key, src_info, limit_per_source):
    body, err = _request(src_info["url"])
    if err or not body:
        return [], err or "empty body"
    items = []
    seen_urls = set()
    for m in src_info["fallback_listing_re"].finditer(body):
        href, title = m.group(1).strip(), m.group(2).strip()
        title = html.unescape(re.sub(r"<[^>]+>", "", title))
        if len(title) < 6:
            continue
        url = _resolve(src_info["url"], href)
        if url in seen_urls:
            continue
        seen_urls.add(url)
        items.append({
            "title": title,
            "source": src_info["name"],
            "source_key": key,
            "date": _extract_date(title),
            "url": url,
            "summary": title[:200],
            "tags": _auto_tags(title),
        })
        if len(items) >= limit_per_source:
            break
    return items, None


def main(argv=None):
    p = argparse.ArgumentParser(description="Aggregate Chinese paleontology news")
    p.add_argument("--source", choices=list(SOURCES) + ["all"], default="all")
    p.add_argument("--limit", type=int, default=20,
                   help="Total max items returned (across sources)")
    p.add_argument("--per-source-limit", type=int, default=10)
    p.add_argument("--keyword", help="Filter to items whose title contains this string")
    p.add_argument("--since-days", type=int, default=None,
                   help="Only include items dated within N days (if date is parseable)")
    p.add_argument("--polite-delay", type=float, default=1.0)
    args = p.parse_args(argv)

    sources_to_hit = list(SOURCES.keys()) if args.source == "all" else [args.source]
    all_items = []
    errors = {}
    for i, key in enumerate(sources_to_hit):
        if i > 0 and args.polite_delay > 0:
            time.sleep(args.polite_delay)
        items, err = _scrape_source(key, SOURCES[key], args.per_source_limit)
        if err:
            errors[key] = err
        else:
            all_items.extend(items)

    # Keyword filter
    if args.keyword:
        kw = args.keyword.lower()
        all_items = [it for it in all_items if kw in it["title"].lower()]

    # Date filter
    if args.since_days is not None:
        cutoff = dt.date.today() - dt.timedelta(days=args.since_days)
        kept = []
        for it in all_items:
            d = it.get("date")
            if not d:
                continue  # drop undated items when date filter requested
            try:
                if dt.date.fromisoformat(d) >= cutoff:
                    kept.append(it)
            except ValueError:
                pass
        all_items = kept

    # Sort newest first
    all_items.sort(key=lambda x: x.get("date") or "", reverse=True)
    all_items = all_items[: max(1, args.limit)]

    print_json({
        "source": "China Fossil News Aggregator",
        "query": {"keyword": args.keyword, "since_days": args.since_days,
                  "source": args.source, "limit": args.limit},
        "fetched_at": dt.datetime.now(tz=dt.timezone.utc).isoformat(timespec="seconds"),
        "count": len(all_items),
        "items": all_items,
        "errors": errors,
        "sources_attempted": sources_to_hit,
    })


if __name__ == "__main__":
    main()
