# -*- coding: utf-8 -*-
"""入口：抓取 → 摘要 → 生成日报 →（可选）飞书推送。"""
import os
from datetime import datetime

from fetch_sources import load_config, fetch_all
from summarize import summarize


def main():
    cfg = load_config("config.yaml")

    # 1. 抓取资讯
    uniq = fetch_all(cfg)
    print("共抓取去重后", len(uniq), "条资讯")

    # 2. 组装内容并调用 LLM
    content = "\n".join(
        f"- [{it['source']}] {it['title']}: {it['summary'][:200]}" for it in uniq
    )
    md = summarize(cfg, content)

    # 3. 生成日报
    date_cn = datetime.now().strftime("%Y-%m-%d")
    stamp = datetime.now().strftime("%Y%m%d")
    header = (
        f"# AI 产品经理每日行业早报 · {date_cn}\n\n"
        f"> 自动生成 | 覆盖 {len(uniq)} 条资讯 | 来源：{'、'.join(s['name'] for s in cfg['rss_sources'])}\n\n"
    )
    os.makedirs("reports", exist_ok=True)
    path = f"reports/{stamp}.md"
    with open(path, "w", encoding="utf-8") as f:
        f.write(header + md)
    print("已生成:", path)

    # 4. 飞书推送（可选）
    try:
        from push_feishu import push
        pushed = push(md)
        print("飞书推送:", "成功" if pushed else "未配置(跳过)")
    except Exception as ex:
        print("飞书推送跳过:", ex)


if __name__ == "__main__":
    main()
