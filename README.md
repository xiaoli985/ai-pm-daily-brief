# AI 产品经理每日行业早报

一个帮你**每天早上自动整理 AI 行业资讯**的开源小工具，专为产品经理设计：抓取多家资讯源 → 大模型筛选 → 生成**产品经理视角**的点评日报 → 自动提交到 GitHub / 推送飞书。

> 全程免费（GitHub Actions 定时跑），不需要服务器，你只要配置一次。

## 效果
每天北京时间 **06:30** 自动运行，生成 `reports/20261009.md` 这样的日报，内容包括：
- 按「模型能力更新 / 产品发布与竞品 / 商业化与定价 / 行业趋势与政策 / 开源与生态」分类
- 每条资讯带**【产品经理视角】**点评（对产品方案 / 成本 / 竞品 / 机会点的影响）
- 结尾「今日一句话总结」
- 可选：推送到你的飞书群

## 项目结构
```
ai-pm-daily-brief/
├── config.yaml               # 资讯源 + 模型 + Prompt（你要改就改这个文件）
├── requirements.txt          # 依赖
├── src/
│   ├── main.py               # 入口
│   ├── fetch_sources.py      # 抓取资讯
│   ├── summarize.py          # 大模型生成 PM 点评
│   └── push_feishu.py        # 飞书推送（可选）
├── reports/                  # 自动生成的每日日报
└── .github/workflows/daily.yml  # 每天定时任务的配置
```

## 快速开始（3 步，不需要写代码）
1. **免费申请大模型 API Key**（推荐智谱，免费）：打开 `https://open.bigmodel.cn` 注册 → 左侧「API Keys」→ 创建 API Key（用默认免费模型，不花钱）
2. **建 GitHub 仓库**，把本文件夹所有内容上传
3. **配置 Secrets**：仓库 Settings → Secrets → 添加 `LLM_API_KEY`（填入你的 Key）

配好后，点一次 Actions 里的「Run workflow」测试，或等第二天早上 6:30 自动跑。之后每天打开 `reports/` 文件夹就能看到最新日报。

### 可选：推送飞书
飞书群 → 添加「自定义机器人」→ 拿到 Webhook 地址 → 同样存到 Secrets（变量名 `FEISHU_WEBHOOK`），以后日报会同时推送到群里。

## 想改关注范围？
打开 `config.yaml`：
- 增删资讯源：改 `rss_sources` 列表
- 只看某类（B端/Agent/RAG…）：在 `prompt` 第 1 条规则里加关键词
- 调每天条数：改 `max_items`

## 注意事项
- 首次配置后，务必在 Actions 手动跑一次确认成功
- API Key 必须存到 Secrets，不要写进 `config.yaml` 或代码里（防止泄露）
- 报错排查：仓库 → Actions → 点最新一次运行 → 看日志
