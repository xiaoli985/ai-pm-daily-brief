# -*- coding: utf-8 -*-
"""飞书机器人推送（可选）。配置了 FEISHU_WEBHOOK 环境变量才会推送。"""
import os
import requests


def push(content):
    webhook = os.environ.get("FEISHU_WEBHOOK", "").strip()
    if not webhook:
        return False
    # 飞书文本消息单条有长度限制，截断
    payload = {"msg_type": "text", "content": {"text": content[:1500]}}
    requests.post(webhook, json=payload, timeout=10)
    return True
