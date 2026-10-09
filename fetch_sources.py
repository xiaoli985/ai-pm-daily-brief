# -*- coding: utf-8 -*-
"""资讯抓取：读取 config.yaml 中的 RSS 源，去重、清洗 HTML。"""
import re
import yaml
import feedparser


def load_config(path="config.yaml"):
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def _strip_html(s):
    s = re.sub(r"<[^>]+>", " ", s or "")
    return re.sub(r"\s+", " ", s).strip()


def fetch_rss(url, limit=8):
    """抓取单个 RSS 源，返回最近 limit 条资讯。失败返回空列表，不影响整体。"""
    try:
        feed = feedparser.parse(url)
        items = []
        for e in feed.entries[:limit]:
            title = (getattr(e, "title", "") or "").strip()
            if not title:
                continue
            summary = _strip_html(getattr(e, "summary", "") or "")
            link = getattr(e, "link", "") or ""
            items.append({"title": title, "summary": summary[:500], "link": link})
        return items
    except Exception as ex:
        print("  [warn] RSS失败:", url, "->", ex)
        return []


def fetch_all(cfg):
    """抓取所有源，去重，控制数量。"""
    all_items = []
    for src in cfg["rss_sources"]:
        print("抓取:", src["name"])
        items = fetch_rss(src["url"])
        for it in items:
            it["source"] = src["name"]
        all_items += items

    seen, uniq = set(), []
    for it in all_items:
        key = it["title"].strip().lower()
        if key and key not in seen:
            seen.add(key)
            uniq.append(it)

    return uniq[: cfg.get("max_items", 25)]
