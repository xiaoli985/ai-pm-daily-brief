# -*- coding: utf-8 -*-
"""调用大模型生成产品经理视角日报；未配置 API Key 时降级为规则摘要（方便预览）。"""
import os
from openai import OpenAI


def summarize(cfg, content):
    key = os.environ.get("LLM_API_KEY", "").strip()
    if not key:
        return fallback_summary(content)
    client = OpenAI(api_key=key, base_url=cfg["llm"]["base_url"])
    prompt = cfg["prompt"].replace("{content}", content)
    resp = client.chat.completions.create(
        model=cfg["llm"]["model"],
        messages=[{"role": "user", "content": prompt}],
        temperature=cfg["llm"].get("temperature", 0.4),
        max_tokens=cfg["llm"].get("max_tokens", 1500),
    )
    return resp.choices[0].message.content or ""


def fallback_summary(content):
    """未配置密钥时：直接列原始资讯，标注为规则摘要预览。"""
    lines = [l for l in content.splitlines() if l.strip()]
    body = "\n".join("- " + l.strip() for l in lines[:15])
    return (
        "> ⚠️ 尚未配置 LLM_API_KEY，以下为【规则摘要预览】。\n"
        "> 在 GitHub Secrets 配置密钥后，将自动生成为产品经理视角点评版。\n\n"
        "## 今日原始资讯（预览）\n" + body
    )
