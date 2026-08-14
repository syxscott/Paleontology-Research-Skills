# 一套面向古生物研究的可复现工作流工具集：Paleontology Research Skills v1.0.0 开源公告

> **副标题**：为古生物学、地层学、形态计量学与文献计量学研究者设计的 13 个 Agent Skills 与 13 个斜杠命令

> **发布日期**：2026-06-05
>
> **作者 / 维护者**：syxscott（syxemail@yeah.net）
>
> **项目仓库**：https://github.com/syxscott/Paleontology-Research-Skills
>
> **许可协议**：MIT License
>
> **通讯单位**：武汉中国地质大学（China University of Geosciences, Wuhan）

---

## 摘要

Paleontology Research Skills（以下简称 PRS）是以 [Anthropic Claude Code Agent Skills 规范](https://agentskills.io/specification)为部署目标、面向古生物学及其相关地学领域研究者的开源工作流工具集。本文系统介绍该工具集的设计动机、整体架构、十二个能力子模块、关键算法实现与工程取舍，以及当前版本在科学诚信与可复现性方面的实现原则。PRS v1.0.0 以 MIT 协议发布，所有源码、文档与测试均托管于 GitHub，可通过 `pip install -e .` 或直接将 `.claude/` 目录部署至项目级（project-scope）或用户级（user-scope）位置使用。

---

## 一、引言：当大型语言模型进入古生物学研究流程

过去三年，生成式大语言模型（Large Language Models, LLMs）在生命科学与地球科学的研究与传播环节得到了广泛部署。文献综述、分类层级梳理、地质年代换算、化石鉴定辅助等任务开始被部分地委托给具备自然语言交互能力的人工智能系统。然而，此类工具在专业领域的部署仍面临三类固有挑战：

1. **第一**，模型在缺乏外部数据源约束时倾向于"幻觉"——构造貌似合理但不存在的物种名、文献 DOI 或化石产地坐标；
2. **第二**，传统 R / Python 工作流难以被非计算背景的研究者直接复用；
3. **第三**，垂直领域（古生物学、地层学、形态计量学）所需的异构数据源——古生物数据库 PBDB、引文库 CrossRef、分类库 NCBI / Wikidata、地层数据库 Macrostrat、ICS 地质时间表等——分散在不同的 API 与许可协议下，缺乏统一的调用规范与失败处理约定。

Paleontology Research Skills（PRS）的设计目标，是在不引入大型依赖、不调用任何外部嵌入 API 的前提下，为上述问题提供一套轻量、可审计、对科学诚信友好的解决方案。项目以 Anthropic 公司发布的 Claude Code Agent Skills 规范为部署形态——即在仓库的 `.claude/skills/<name>/SKILL.md` 路径下，以 YAML frontmatter + Markdown 主体声明一个"能力单元"（skill），并由宿主 LLM 在用户自然语言提示触发时自动加载。每一个 skill 同时配对一个可通过 `Bash` 工具直接执行的 Python 脚本，确保模型在生成回答前能够以结构化方式查询权威数据源。

本文第一作者 / 通讯作者为该工具集的设计者与维护者，所在单位为武汉中国地质大学（China University of Geosciences, Wuhan）。本文既是对 v1.0.0 版本的工程性总结，也是对古生物、地层、形态计量、文献计量四类研究子领域同行的方法学倡议。

## 二、项目来源与演化

PRS 工具集起源于作者在 2024–2025 年间为开展恐龙形态计量学研究与辽西热河生物群（Jehol Biota）地层学综述所搭建的本地工作流。在反复使用过程中，原型系统经历了若干次结构性重构，最终于 2026 年 6 月 3 日以 v1.0.0 正式版本发布，并完成三个阶段的代码审计与文档补全（CHANGELOG.md 中记录了 8 个被修复的早期缺陷，涵盖 SKILL.md 命名、profile 状态字段、内存归档输出、ICS 时间表层级字段、subprocess 编码、stratigraphy 空结果、taxonomy HTTP 400 映射等）。

需要说明的是，项目的内部代号在演化过程中曾先后使用"OpenClaw"（v1.7.0 之前）与"PaleoClaw"，最终定名为"paleontology-research-skills"。在 v1.0.0 版本的源代码与文档中，个别 SKILL.md 文件（如 `paleo-morphometric` 与 `paleo-morphometric-convert`）仍保留有上一代命名痕迹，作者计划在 v1.1.0 清理这些历史引用。

## 三、整体架构：嵌套式 SKILL.md 与共享运行时

PRS 采用 Anthropic Agent Skills 规范所支持的**递归式 `SKILL.md` 发现**（recursive discovery）机制部署其能力模块。具体而言，在仓库的 `.claude/skills/paleontology-research-skills/` 目录下，存在一个父级 `SKILL.md` 与十二个子级 `SKILL.md`，Claude Code 会在会话初始化时同时加载它们，并依据 `description` 字段的语义描述进行触发匹配。这种"宽入口 + 窄专才"的双层布局，在用户提出模糊问题（"帮我做点化石研究"）时由父级进行整体路由；在用户提出精确指令（"在 PBDB 找 *Allosaurus* 的产出记录"）时由对应子级接管。

父级 `SKILL.md`（`paleontology-research-skills`）的 `description` 字段约 1024 字符，列出了 12 个子模块的功能与典型触发语句；其主体部分给出一张子能力路由表，并明确数据根目录为 `~/.paleontology-research-skills/`（可通过环境变量 `PALEONTOLOGY_RESEARCH_SKILLS_HOME` 覆盖）。子级 `SKILL.md` 各自独立，亦可被独立触发。

在脚本层面，所有子模块共享一份位于父目录 `scripts/paleo_common.py`（419 行）的工具库，其功能包括：

- 路径解析（`data_home()`、`memory_root()`、`sessions_root()`）
- 文件 I/O（`read_text_file` / `write_text_file` / `read_json` / `write_json` / `print_json`）
- 基于简单 Markdown 解析的双层 profile 加载（`load_profile()`）
- 基于哈希技巧的"伪向量"语义搜索（`hashing_vector()` 与 `cosine_similarity()`）
- 统一的"任务—长期—归档"三级记忆迭代器

子模块脚本均通过以下惯用代码将 `paleo_common` 加入 `sys.path`：

```python
import os, sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_SHARED = os.path.normpath(os.path.join(_HERE, "..", "..", "scripts"))
if _SHARED not in sys.path:
    sys.path.insert(0, _SHARED)
from paleo_common import load_profile, normalize_taxon, print_json
```

这种安排的优势在于：

1. 不依赖 `pip install -e .` 即可被使用；
2. 每个子模块的 `scripts/` 目录只保留自身独有的脚本，目录树清晰；
3. 父目录与子目录之间不存在循环依赖。

`paleo_common.py` 同时被设计为"以纯标准库实现"——除 `hashlib`、`math`、`json`、`re`、`pathlib` 外不引入任何第三方包，从而保证基础工具集可以在无网络、无虚拟环境、最简 Python 3.9 解释器下直接运行。

## 四、十二个能力子模块

PRS v1.0.0 共提供 12 个能力子模块，分别对应古生物学研究流程中的一个或多个独立子任务。下文按"数据查询—文献检索—本地记忆—数据治理—研究编排"的逻辑顺序逐一介绍。

### 4.1 paleo-pbdb：古生物数据库化石产出查询

paleo-pbdb 模块对接 Paleobiology Database（PBDB，https://paleobiodb.org，CC-BY 4.0，1.5M+ 条产出记录，200K+ 分类单元），通过 `https://paleobiodb.org/data1.2/occs/list.json` 端点返回按属、种或更高分类阶元筛选的化石产出记录。脚本 `pbdb_query.py` 支持 `--genus` / `--species` / `--base-name` / `--interval` / `--min-ma` / `--max-ma` 等参数；当用户调用 `--respect-profile` 时，默认记录数将取自 `~/.paleontology-research-skills/user.md` 中 `Data Preferences → Default occurrence limit` 字段。

该脚本在收到自然语言提示时（例如在 slash command 上下文中通过 `--prompt` 传入），会通过 `paleo_common.normalize_taxon`（委托给 `scripts/taxonomy.py` 中的 `extract_taxon_candidate`）从文本中提取最可能的分类阶元候选，从而避免对常见英文动词（"Find"、"Use"、"Show" 等）与地质期名（Jurassic、Cretaceous、Permian 等）误识别。

### 4.2 paleo-crossref：跨源文献检索

paleo-crossref 模块聚合 CrossRef（https://api.crossref.org，CC-BY 4.0，1.5 亿+ 条 DOI 元数据）、Semantic Scholar（https://api.semanticscholar.org，ODC-BY 1.0）与 arXiv（https://arxiv.org，CC0）三类文献源，分别由 `crossref_search.py`、`semantic_scholar_search.py` 与 `arxiv_search.py` 实现。`summarize_paper.py` 提供基于句子打分的 3-bullet 启发式摘要，可在不调用 LLM 的前提下对摘要文本进行精简。CrossRef 端点被设置为礼貌池（polite pool）模式——`User-Agent` 字段中包含 `mailto` 联系方式，以获得更高的速率配额。

### 4.3 paleo-memory：本地研究记忆与哈希向量检索

paleo-memory 模块将用户的研究活动持久化在 `~/.paleontology-research-skills/memory/` 目录下，分为三个层级：

- `short/<task_id>.json` 存放每次任务的原始记录；
- `long_term.jsonl` 存放经过人工筛选的长期结论（JSON Lines 格式，每行一条）；
- `archive/short/<task_id>.json` 存放经 `memory_archive.py` 归档的过期短期任务。

语义检索由 `paleo_common.search_memory()` 实现，其核心是 384 维"哈希技巧向量"：将文本分词后，对每个 token 计算其 MD5 摘要的前 8 字节，模 384 得到向量维度索引；摘要第 9–10 字节的奇偶决定符号为 +1 或 −1。这一方法在工程上等价于 signed random projection 的极简实现，可在不调用任何外部嵌入 API 的前提下，对小规模（数百至数千条）语料提供可接受的近邻检索质量（作者在 `tests/test_paleo_common.py::test_cosine_similarity_self_is_one` 与 `test_cosine_similarity_unrelated_is_low` 中分别验证了自相似度恒等于 1 与跨主题相似度小于 0.5 的基本性质）。

### 4.4 paleo-session：会话历史与上下文恢复

paleo-session 模块管理 `~/.paleontology-research-skills/sessions/<session_id>.json` 下的会话文件，支持 `list` / `show` / `search` / `resume` 四种操作。`session_resume.py` 的输出被设计为可直接注入新会话上下文的"研究接续负载"（research resumption payload），包含会话标题、最近一次摘要、待解决问题以及末三条对话轮次，以减少跨会话的重复查询。

### 4.5 paleo-profile：双层研究 profile

paleo-profile 模块将用户身份分为两层存储：

- `soul.md` 描述系统身份、科学原则与安全边界（含默认的"never fabricate species names / DOIs / fossil occurrences"等约束）；
- `user.md` 描述个人研究偏好（角色、机构、首选地质期、首选研究区域、引用格式、首选期刊清单、隐私与协作期望等）。

这种"系统灵魂 + 用户偏好"的双层结构源自实践观察——单一的"用户 prompt"难以稳定表达研究者群体的方法学约束，因此将通用科学诚信规则放在 `soul.md`、将高度个人化的偏好放在 `user.md`，便于在团队共享同一 `soul.md` 时各研究者保留自身的 `user.md`。`paleo_common.load_profile()` 采用宽容的 Markdown 解析（标题、列表项、`Key: value` 行），并对缺失字段提供默认值。

### 4.6 paleo-geo-time：ICS 地质时间表

paleo-geo-time 模块以 ICS（International Commission on Stratigraphy，https://stratigraphy.org）2023 年 9 月版彩色地层表为数据源，提供按名称（如 Jurassic、Late Cretaceous）、按年代（如 `--age 100` 包含该年代的区间集合）、按父子级（`--list --parent Cenozoic --rank period`）的查询。

早期版本中，`--list --parent X` 总是返回 0 条记录，原因是脚本只查询了统一 `parent` 字段，而 ICS 数据使用 `era`、`period`、`epoch` 等不同字段表达层级。修复后，`geo_time_query.py::_matches_parent` 检查 `eonothem`、`era`、`period`、`epoch`、`stage`、`parent` 全套可能字段，从而在 v1.0.0 中正确支持中新生代各世、统、阶的子级列举（详见 `tests/test_geo_time.py::test_list_mesozoic_periods`）。

### 4.7 paleo-taxonomy：分类层级与跨库交叉验证

paleo-taxonomy 模块对接 PBDB Taxonomy API（`https://paleobiodb.org/data1.2/taxa/single.json`）以获取完整 kingdom→species 层级、命名权威人（authority）、首次与末次出现（first / last appearance）、现存状态（extant vs. extinct）、状态（valid vs. synonym vs. replaced）以及接受名（accepted name）。`taxonomy_query.py` 在收到 HTTP 400 响应时（PBDB 对未知分类阶元返回该状态），将其映射为人类可读的 `"No taxon found matching 'X' (PBDB has no record)"`，避免向用户暴露底层 HTTP 细节。

`ncbi_taxonomy.py` 与 `wikidata_taxonomy.py` 分别对接 NCBI Taxonomy（公共领域）与 Wikidata SPARQL（CC0），用于在分类阶元具有现存近亲（典型如 Aves、Mammalia）或需要俗名 / 图像交叉时提供补充信息。

### 4.8 paleo-stratigraphy：地层学与 Macrostrat 交叉

paleo-stratigraphy 模块基于 PBDB collections（`https://paleobiodb.org/data1.2/colls/list.json`）返回某一地质组（formation）所产化石的集合、年代区间、地理分布、优势分类单元与岩性摘要。`stratigraphy_query.py` 在返回空记录时仍输出结构一致的 `summary` 字段（含 `collection_count: 0`、各字段为 `null` 或空数组），以保证下游编排器（如 paleo-research-assistant）解析时不需要判空分支。`macrostrat_query.py` 用于在 Macrostrat（https://macrostrat.org，CC-BY 4.0）可用时补充岩石地层学柱状图与单元层级信息。

### 4.9 paleo-morphometric：化石轮廓的几何形态计量学地标提取

paleo-morphometric 模块实现了基于纯 Python 图像处理的几何形态计量学（Geometric Morphometrics, GM）半地标（semilandmarks）提取流程。其算法分四步：

1. 将输入图像灰度化并按阈值二值化（`--threshold`，默认 150，前景为暗于阈值的像素）；
2. 在二值掩膜上以四连通洪泛填充（4-connected flood-fill）寻找最大连通分量；
3. 使用 Moore 邻域边界追踪（Moore-neighbourhood tracing）从最顶部、最左侧的前景像素起按顺时针方向遍历外轮廓；
4. 沿累积弧长（cumulative arc length）等距重采样至 N 个点（`--num-landmarks`，默认 64）。

该模块支持菊石（ammonoids）、腕足类（brachiopods）、双壳类（bivalves）、腹足类（gastropods）、三叶虫（trilobites）以及任何具有清晰二值轮廓的化石。输出格式包括 JSON（原生）、TPS（MorphoJ / tpsdig 兼容）、CSV（长表）与 Excel（`openpyxl`，可选）。

脚本 `extract_landmarks.py` 显式声明所提取的为半地标（semilandmarks），并提醒用户在严肃研究中仍需在 TPSDig 等专业软件中补充固定同源点（fixed homologous landmarks）后方可用于下游统计分析。该算法在概念上参考了 Liu Xiaokang（武汉中国地质大学）所提出的 DeepMorph 流程，并在 README 与 SKILL.md 中明确致谢。

### 4.10 paleo-morphometric-convert：地标数据格式互转

paleo-morphometric-convert 模块在 TPS、MorphoJ / tpsdig 标准格式、NTSys（`.nts`，NTSys-PC 矩阵格式）、CSV（长表）、JSON 与 Excel 之间进行互转，并提供 `--validate` 校验以报告各地标集的地标数量是否一致、是否存在缺失值。其内部使用纯 Python 实现的 TPS 与 NTS 解析器（`convert._parse_tps`、`convert._parse_nts`、`convert._parse_csv`），在多标本 TPS 文件中自动通过空行加 `LM=` 头进行分块。

### 4.11 paleo-research-assistant：五阶段研究编排器

paleo-research-assistant 模块是 PRS 的编排入口，模拟"研究生导师式"的工作流：用户在自然语言中给出一个研究主题（topic），并可选择附加一个分类阶元（taxon）或地层（formation）作为限定条件。编排器依次调用：

1. `crossref_search.py`（寻找相关文献）
2. `summarize_paper.py`（对前 N 篇摘要做 3-bullet 启发式摘要）
3. `taxonomy_query.py`（核实分类阶元）
4. `pbdb_query.py`（产出数据）
5. `stratigraphy_query.py`（地层学语境）

并最终渲染一份含七个章节（Overview、Literature、Taxonomy、Occurrences、Stratigraphy、References、Limitations）的 Markdown 报告。任一阶段失败时（如网络中断、API 限流），对应章节会显式标注为"data unavailable"，编排器继续运行后续阶段；最终输出的 JSON manifest 与 Markdown 报告均以时间戳命名保存在 `--out-dir` 目录下（默认 `paleo_reports/`）。该模块将"失败可恢复"作为顶层设计目标，符合科学工具应"明确告知数据缺口"的方法学原则。

### 4.12 paleo-china-news：中文古生物新闻聚合

paleo-china-news 模块针对中国学界与公众对中文古生物新闻的需求，从三个官方或半官方源抓取近期化石发现与研究动态：

- 国家岩矿化石标本资源共享平台（nkocs.com，标本资源与博物馆动态）
- 中国古生物学会（palaeontology.cn，学术会议与奖项）
- 中国科学院古脊椎动物与古人类研究所（ivpp.cas.cn，研究进展与考察报告）

抓取采用礼貌型（polite）规则——`User-Agent` 显式标识为科研爬虫，源间默认间隔 1 秒。`china_news_fetch.py` 实现了对中文字符串的多种编码兼容（依次尝试 UTF-8、GB18030、GBK、GB2312），并通过关键词—标签字典（"恐龙"→恐龙、"辽宁"→辽宁、"侏罗"→侏罗纪等）实现标题的自动标签化。在 v1.0.0 中，所有抓取失败均以 JSON `errors` 字段逐源报告，而非中断整体流程。

## 五、统一工程约定

PRS v1.0.0 在工程实现层面遵循以下统一约定。这些约定不仅是代码风格层面的偏好，更是方法学可审计性的技术保障。

### （1）每个脚本输出且仅输出一个 JSON 对象至 stdout

该对象至少包含 `source`（数据源）、`query`（查询参数快照）、`count`（结果数量）与 `records` / `items` / `children` / `matches` 之一作为结果数组。`print_json()` 使用 `ensure_ascii=False, indent=2` 序列化，确保中文字符不被转义、便于人眼审阅。

### （2）失败不抛栈

网络错误（`urllib.error.URLError`、`TimeoutError`、`OSError`）、HTTP 错误（`urllib.error.HTTPError`）、文件 I/O 错误、JSON 解析错误均被捕获并嵌入至输出 JSON 的 `error` 字段。这种做法在工程上等价于"将所有失败作为数据建模"，从而保证 LLM 在接收到 stdout 后总能以结构化方式呈现给用户，而非向用户展示 Python 异常回溯。在 `paleo-research-assistant` 中，这一约定进一步被升级为"任意子脚本失败不影响整体进度"。

### （3）零运行时依赖

基础工具集不要求任何第三方包。`paleo-morphometric` 与 `paleo-morphometric-convert` 模块所必需的 Pillow 与 openpyxl 在 `pyproject.toml` 中以 optional dependency 形式声明（`pip install -e ".[morphometric]"`）；CI 在测试时会安装两者以保证 smoke test 覆盖。其余 10 个子模块在 `python -m pip install .` 之外不要求任何额外包。

### （4）科学诚信优先

任何子模块均不构造虚构数据。`paleo-pbdb`、`paleo-taxonomy` 等子模块在 PBDB 返回 HTTP 400 / 404 时被映射为"未找到"提示；`paleo-crossref` 在 rows=0 时返回空 `items` 数组而非构造空 DOI；`paleo-china-news` 在抓取失败时逐源报告 `errors`；`paleo-memory` 在记忆库为空时返回 `count: 0`。项目通过 `CONTRIBUTING.md` 中的"Scientific integrity rules"小节将这一原则固化为对贡献者的硬性要求：拒绝任何引入虚构物种名、虚构 DOI、虚构化石产地的合并请求。

### （5）可复现性

每个脚本都将查询参数完整回显至输出 JSON 的 `query` 字段；每个有副作用的脚本（`profile_init.py`、`memory_archive.py`、`session_resume.py`）均在执行前显示将要进行的操作并接受 `--force` 确认；项目根 `Makefile` 提供 `test`（`python -m unittest discover tests`）、`test-coverage`（`pytest --cov`）、`validate`（SKILL.md 合规校验）、`smoke`（逐脚本 `--help` 测试）、`all`（format + lint + test + validate + smoke）等目标，便于在本地或 CI 中一键验证。

### （6）跨平台兼容

所有 `subprocess.run` 调用均显式设置 `encoding="utf-8", errors="replace"` 与 `PYTHONIOENCODING=utf-8`，以解决 Windows PowerShell 默认 GBK 编码在处理 CJK 路径与中文字符时的解码失败问题（早期 v0.x 版本中曾出现这一问题，已在 v1.0.0 中修复）。

## 六、可复现工作流示例

为帮助读者快速评估 PRS 的实际产出形式，此处给出一个跨模块的工作流示例。假设研究者的命题是"评估辽西下白垩统热河群义县组（Yixian Formation）的今鸟型类（Ornithuromorpha）化石多样性与近 25 年研究热度"：

```bash
# 1) 初始化研究 profile（仅在首次部署时）
python3 .claude/skills/paleontology-research-skills/paleo-profile/scripts/profile_init.py

# 2) 检索义县组产出的化石集合与优势分类单元
python3 .claude/skills/paleontology-research-skills/paleo-stratigraphy/scripts/stratigraphy_query.py \
    --formation "Yixian" --country CN --taxa-limit 30

# 3) 核实"今鸟型类"的分类层级
python3 .claude/skills/paleontology-research-skills/paleo-taxonomy/scripts/taxonomy_query.py \
    --name "Ornithuromorpha"

# 4) 在 PBDB 中获取该分类阶元的产出记录
python3 .claude/skills/paleontology-research-skills/paleo-pbdb/scripts/pbdb_query.py \
    --base-name "Ornithuromorpha" --respect-profile

# 5) 在 CrossRef 中检索近 25 年相关文献
python3 .claude/skills/paleontology-research-skills/paleo-crossref/scripts/crossref_search.py \
    --query "Ornithuromorpha Yixian Formation" \
    --rows 30 --include-abstract --filter-from-year 2000

# 6) 一键生成完整研究综述
python3 .claude/skills/paleontology-research-skills/paleo-research-assistant/scripts/research_assistant.py \
    --topic "Ornithuromorpha diversity and research trends in the Yixian Formation" \
    --taxon "Ornithuromorpha" --formation "Yixian" \
    --paper-rows 12 --summarise-top 5 --out-dir reports/yixian_ornithuromorpha
```

整个工作流在网络可用条件下通常在 30–90 秒内完成（受 CrossRef 与 PBDB 端点响应时间影响），所产出的 Markdown 报告可直接作为论文 Background 与 Methods 章节的初稿，所产出的 JSON manifest 可作为附录与方法学存档提交至期刊或数据存储库（如 Zenodo、Figshare）。

## 七、关键算法的工程取舍

### （1）哈希技巧"伪向量"检索

384 维哈希技巧向量的设计动机在于：调用 OpenAI Embeddings、Cohere Embed 或本地 SentenceTransformers 任一方案均会引入数十兆至数百兆的额外依赖、可能违反离线工作环境、并在涉及化石产地的非英文专业术语上表现出不可预测的偏置。作者选择的 signed random projection 简化方案在实践中对 1000 量级以下的记忆条目提供可接受的近邻检索质量（cosine similarity > 0.2 即可视为命中），并在 `tests/test_paleo_common.py` 中以四个测试用例（确定性、自相似度、跨主题低相似度、空记忆库）保证其基础行为稳定。读者如对检索质量有更高要求，可在使用时将 `paleo_common.hashing_vector` 替换为本地 embedding 模型——所有调用方都通过 `search_memory()` 间接访问这一函数，因此替换不会影响上游 API。

### （2）Moore 邻域边界追踪

在图像形态学中，常用的边界追踪算法包括 Theo Pavlidis 算法、Moore 邻域算法与 Suzuki-Abe 轮廓追踪。PRS 选择 Moore 邻域算法的原因有二：其一是其实现简单（仅需维护 8 方向偏置），可避免引入 OpenCV；其二是其在二值掩膜上的行为可预测（前景点邻域缺失时立即终止），与"明确报错而非静默截断"的失败约定一致。

### （3）弧长等距重采样

在 64 个 semilandmark 的均匀分布中，简单"按索引等距"会在轮廓曲率大的区域产生疏密不均。PRS 采用累积弧长参数化（cumulative arc-length parameterization），将闭合轮廓的总周长除以 N 后逐段线性插值，从而保证 semilandmark 在轮廓上按真实几何距离均匀分布。该实现对单像素宽线段（boundry length 1）和退化边界（所有像素共点）均做防御性保护（`safety_cap` 与零长度段处理）。

### （4）双层 profile 解析

对 Markdown 形式的 profile 进行解析时，作者避免引入任何第三方 Markdown 解析器（如 `python-markdown`、`mistune`），转而以约 30 行正则表达式覆盖实际使用的所有格式约定（`##` 与 `###` 标题、`-` 与 `*` 与 `1.` 列表项、`---` 分隔线、`Key: value` 行）。这种宽容解析的代价是无法处理复杂嵌套与表格，但收益是 PRS 在无法访问外部包的环境（包括某些 HPC 节点与受限网络的内网开发机）下仍可工作。

## 八、与既有工具的关系

在古生物学领域，已有若干成熟的科研软件与数据平台可直接对应 PRS 的子模块：

- **PBDB Web Portal** 与 **PBDB Navigator**：paleo-pbdb 与 paleo-stratigraphy 模块在功能上与 PBDB 官方 Web 界面重叠，但通过 CLI 与 JSON 输出更易于集成至计算工作流；
- **CrossRef Web Search** 与 **Connected Papers**：paleo-crossref 模块在引文网络方面尚不覆盖 Connected Papers 的可视化能力，但通过 Semantic Scholar 子模块提供基础的引用计数；
- **Macrostrat Web Map**：paleo-stratigraphy 的 Macrostrat 子模块在功能上等同于 Macrostrat API 的薄封装；
- **MorphoJ** 与 **R geomorph**：paleo-morphometric 与 paleo-morphometric-convert 不替代这两个下游统计工具，而是为其准备数据——所输出的 TPS / CSV / Excel 文件可直接由 MorphoJ 与 geomorph 加载；
- **CNKI / Wanfang / VIP**：paleo-china-news 不替代中文文献数据库，但通过 nkocs / palaeontology.cn / IVPP 三个源补充"科研新闻"层级的信息（这些信息在 CNKI 等学术数据库中通常滞后数月）。

在 AI 工具生态中，PRS 与 Anthropic Claude Code 的"Tools"机制（function calling）形成互补：Claude Code 的 Tools 用于通用计算（文件读写、Bash、搜索），PRS 的 Skills 用于"领域知识 + 权威数据源 + 输出规范"的封装。两者的边界在 `paleo-research-assistant` 的 5 阶段编排中得到最清晰的体现——编排器本身仅用 Claude Code 的 `Bash` 工具来运行各阶段的 Python 脚本，而所有领域逻辑均在脚本中实现，避免 LLM 在编排阶段进行推测式决策。

## 九、局限性与未来工作

PRS v1.0.0 在以下方面仍有改进空间，作者在 GitHub Issues 中已建立对应追踪任务，欢迎社区贡献：

1. **数据时效性。** ICS 地质时间表当前锁定在 2023-09 彩色版本，PBDB 引用数据相对当前可能存在 6–12 个月的滞后。PRS 不内置自动更新机制（避免在无授权情况下覆盖用户本地数据），而是依赖发布新版本时由维护者手工同步；
2. **古生物分类阶元的拼写容错。** 当前 `normalize_taxon` 仅识别首字母大写且具有拉丁后缀的 token，对拼写错误（"Allosaururs" 之于 "Allosaurus"）与全小写输入不具备容错能力；
3. **中文分类名与拉丁名映射。** `paleo-china-news` 抓取的标题以中文为主，但 PRS 当前未提供从中文俗名（如"中华龙鸟"）到拉丁学名（*Sinosauropteryx prima*）的映射表；
4. **跨会话长期记忆的"晋升"机制。** 短期记忆（`short/*.json`）到长期记忆（`long_term.jsonl`）的迁移当前依赖人工或宿主 LLM 的判断，缺乏可审计的晋升规则；作者计划在 v1.1.0 中引入基于"出现频次 + 摘要置信度"的可选晋升策略；
5. **3D 形态计量学。** 当前 `paleo-morphometric` 仅支持 2D 轮廓。3D 微 CT 扫描、surface scan 等数据源需要独立的处理流水线（如 Stratovan Checkpoint、IDAV LandmarkEditor），作者考虑在 v2.0.0 中以独立 skill 形式引入 3D 半地标提取，但不会将其与 2D 流程混合以保持 API 简单性；
6. **跨语种文献的元数据规范化。** CrossRef 对中文期刊的元数据覆盖度有限，作者建议在中文语种研究中同时使用 CNKI / Wanfang 数据库——这一点已在 paleo-research-assistant 的 Limitations 章节中明确提示。

## 十、开源信息、贡献与获取

PRS 以 **MIT 协议**发布，允许学术与商业使用、修改、再分发，前提是保留版权与许可声明。所有数据源的归属与许可已在 README 末尾逐条列出：

| 数据源 | 许可协议 |
|---|---|
| PBDB（古生物数据库） | CC-BY 4.0 |
| CrossRef | CC-BY 4.0 |
| Semantic Scholar | ODC-BY 1.0 |
| arXiv | CC0 |
| NCBI Taxonomy | 公共领域 |
| Wikidata | CC0 |
| Macrostrat | CC-BY 4.0 |
| ICS（国际地层委员会） | 学术引用 |

**仓库地址**：https://github.com/syxscott/Paleontology-Research-Skills

**获取方式**（任选其一）：

```bash
# 方式一：项目级（仅当前项目生效）
git clone https://github.com/syxscott/Paleontology-Research-Skills.git
cd Paleontology-Research-Skills
pip install -e ".[morphometric]"     # 包含 Pillow + openpyxl
python -m unittest discover tests    # 运行 11 个单元测试

# 方式二：用户级（对所有项目生效）
mkdir -p ~/.claude/skills ~/.claude/commands
cp -r .claude/skills/paleontology-research-skills ~/.claude/skills/
cp    .claude/commands/paleo*.md     ~/.claude/commands/
```

**首次使用建议**：

```bash
# 初始化个人研究 profile
python3 .claude/skills/paleontology-research-skills/paleo-profile/scripts/profile_init.py

# 编辑 ~/.paleontology-research-skills/user.md 以填写真实角色、机构、首选地质期与引用格式
```

**贡献指南**：项目维护者欢迎以 Pull Request 形式提交新功能、Bug 修复、文档改进与新增子模块。`CONTRIBUTING.md` 中详细描述了添加新子模块的 10 个步骤（命名、目录结构、SKILL.md frontmatter、脚本实现、路由表登记、slash command 创建、README 更新、CHANGELOG 更新、测试编写、smoke test 验证）。所有 Pull Request 在合并前需通过：

- Python 3.9–3.12 × Ubuntu / macOS / Windows 的 CI 矩阵
- SKILL.md 合规校验（`name:` 字段与目录名一致、`description` ≤ 1024 字符）
- 11 个单元测试

Issue 模板提供 Bug report、Feature request 与"New sub-skill proposal"三类表单。代码风格遵循 PEP 8、line-length ≤ 110，并通过 `ruff check .` 与 `ruff format .` 进行可选静态检查。

**安全披露**：若读者发现 PRS 在命令注入、路径遍历、资源耗尽或凭证泄漏等层面存在可被利用的安全问题，请通过 `syxemail@yeah.net`（主题以 `SECURITY:` 起首）或 GitHub Security Advisories 通道私密报告，维护者承诺在 5 个工作日内响应、30 天内修复并发布补丁。

**依赖透明度**：项目的运行时依赖矩阵（即"哪些子模块依赖哪些上游 API"）如下：

| 子模块 | 上游 API | 必需网络 |
|---|---|---|
| paleo-pbdb | https://paleobiodb.org/data1.2/ | 是 |
| paleo-crossref | https://api.crossref.org, https://api.semanticscholar.org, https://export.arxiv.org | 是 |
| paleo-taxonomy | https://paleobiodb.org/data1.2/, https://api.ncbi.nlm.nih.gov, https://query.wikidata.org | 是 |
| paleo-stratigraphy | https://paleobiodb.org/data1.2/, https://macrostrat.org/api | 是 |
| paleo-research-assistant | 上述子模块的组合 | 是（间接） |
| paleo-china-news | nkocs.com, palaeontology.cn, ivpp.cas.cn | 是 |
| paleo-profile / paleo-memory / paleo-session / paleo-geo-time / paleo-morphometric / paleo-morphometric-convert | （仅本地文件系统 / 内置数据） | 否 |

## 十一、结语与致谢

Paleontology Research Skills 的设计初衷，是为古生物学这一兼具经验性与数据密集性的学科提供一套"开箱即用、可审计、对科学诚信友好"的工程化研究助手。它不是要替代研究者的专业判断，而是要把研究者从"在 12 个不同的网站和数据库之间复制粘贴、反复构造查询字符串"这类机械性工作中解放出来，将更多时间投入到化石观察、地层对比、形态测量、文献思辨这些无法被任何 LLM 替代的核心工作上。

作者感谢以下数据源的开放许可：Paleobiology Database（CC-BY 4.0）、CrossRef（CC-BY 4.0）、Semantic Scholar（ODC-BY 1.0）、arXiv（CC0）、NCBI Taxonomy（公共领域）、Wikidata（CC0）、Macrostrat（CC-BY 4.0）、International Commission on Stratigraphy。感谢 Anthropic 公司发布 Agent Skills 规范及 Claude Code 工具，使得本项目可以以最低的工程成本嵌入研究者的日常工作流。感谢武汉中国地质大学（China University of Geosciences, Wuhan）地球科学学院、中国古脊椎动物与古人类研究所相关团队在方法学层面的讨论。感谢 DeepMorph 算法（Xiaokang Liu, CUG Wuhan）在形态计量学模块中的算法启发。

**项目遵循学术开源原则，欢迎任何形式的引用、再使用与改进。** 若本工具集对您的研究工作有所帮助，建议在 Methods 或 Acknowledgments 中以下列方式致谢：

> Syxscott and the Paleontology Research Skills Contributors (2026).
> *Paleontology Research Skills v1.0.0: A modular, science-integrity-first
> research workflow toolkit for paleontology.* GitHub.
> https://github.com/syxscott/Paleontology-Research-Skills

**通讯方式**：syxemail@yeah.net

**项目地址**：https://github.com/syxscott/Paleontology-Research-Skills

**许可协议**：MIT License

——本文亦以项目自身的 `paleo-research-assistant` 编排器以"古生物研究工作流工具集"为命题运行了一次端到端报告生成，所得 Markdown 报告与 JSON manifest 与本文结构互为印证。

---

## 附录 A：配图建议

1. **头图（公众号题图）**：建议使用 PRS 工作流的整体示意图——中央为 Anthropic Claude Code 标志，外围以放射状分布 12 个子模块图标（建议使用线性图标库如 Lucide / Phosphor 的 `bone`、`scroll`、`book-open`、`database`、`clock`、`sitemap`、`image`、`shapes`、`file-text`、`globe`、`chart-bar`、`newspaper`），右下角小字标注 "v1.0.0 · MIT · 2026"。
2. **第二节"整体架构"配图**：仓库目录树截图（`.claude/skills/paleontology-research-skills/` 父级 + 12 个子目录），以箭头标注"递归发现"机制。
3. **第三节"十二个能力子模块"配图**：可使用 4×3 网格图，每格一个子模块，配 1024 字符 description 的一句话提炼（`化石查询` / `文献检索` / `本地记忆` / `会话历史` / `研究 profile` / `地质时间` / `分类层级` / `地层学` / `形态计量` / `格式转换` / `研究编排` / `中文新闻`）。
4. **第五节"统一工程约定"配图**：建议以表格形式呈现"零依赖、JSON 统一输出、失败不抛栈"三条核心约定的代码示例与输出示例。
5. **第六节"工作流示例"配图**：建议附终端截图（建议 Linux / macOS 终端配色），展示 `stratigraphy_query.py → taxonomy_query.py → pbdb_query.py → crossref_search.py → research_assistant.py` 的级联调用。
6. **第七节"算法"配图**：Moore 邻域边界追踪示意图（建议引用 Wikimedia Commons 的"Connected component"图并重绘），标注 8 方向偏置与起始像素选择策略。
7. **第十节"开源信息"配图**：GitHub 仓库截图或 repository insights 截图（star 趋势、CI 状态徽章矩阵、release 列表）。
8. **配图整体风格**：浅色背景、深灰文字、淡蓝/淡绿/淡赭三色辅助——避免使用过强的对比色，以契合学术严谨基调。每张图均应在文末小字注明"图源：项目仓库 / 自绘"。

## 附录 B：发布建议

1. **发布渠道**：
   - 微信公众号（主战场）：推文形式发布，建议在文末添加"赞赏"按钮与"在看"按钮；
   - 同步发布至知乎专栏、简书、古生物相关垂直社区（如小木虫化石版、中国古生物学会会员群）、OSC 开源中国；
   - GitHub 仓库 README 顶部"Announcements"段同步发布本文要点（建议在 3 个工作日后仅保留仓库地址与一句话摘要，避免与公众号版本长期不一致）。

2. **最佳发布时间**：根据古生物 / 地学受众群体的工作习惯，建议在工作日上午 9:00–10:30（教师与研究生上班 / 课间阅读高峰）或下午 15:00–17:00（咖啡 / 实验间歇）发布。**避开周一上午（行政 / 教学会议密集）与周五下午（周末活动前置）**。学术开源类文章的最佳发布窗口通常在学期初（2 月底 / 9 月初），便于教师将其作为课程材料引入。

3. **标签建议**（微信公众号 `#话题`）：
   `#古生物学` `#开源工具` `#可复现研究` `#方法学` `#PBDB` `#CrossRef` `#形态计量学` `#地层学` `#地质时间` `#AgentSkills` `#ClaudeCode` `#Python` `#MIT协议` `#PaleontologyResearchSkills`

4. **SEO 与摘要建议**：
   - **微信搜索关键词覆盖**：古生物研究工具、PBDB 查询、地质年代换算、形态计量学地标提取、文献综述自动化、可复现研究、Agent Skills 开源、Claude Code 工具集、MorphoJ 数据准备、CrossRef 学术搜索；
   - **文章摘要（用于朋友圈 / 转发卡片）**：建议 80–120 字版本——"为古生物学、地层学、形态计量学、文献计量学研究者提供一套零依赖、可审计、对科学诚信友好的研究工作流工具集：Paleontology Research Skills v1.0.0 正式开源。13 个 Agent Skills + 13 个斜杠命令，覆盖 PBDB 化石查询、CrossRef / arXiv 文献检索、ICS 地质时间表、MorphoJ 地标数据准备与五阶段文献综述自动化。MIT 协议，欢迎学术与教学使用。"
   - **视频化扩展**（可选）：将第六节"工作流示例"录制成 8–10 分钟终端演示视频（建议工具：OBS Studio + 终端录屏 + 中文字幕），同步上传至 Bilibili 知识区，链接嵌入公众号原文"阅读原文"。

5. **互动引导**：文末建议以三段式收尾：
   - 第一段致谢同行评议（"如果您在试用中发现任何 bug 或有方法学建议，请通过 GitHub Issue 与作者联系"）；
   - 第二段呼吁合作（"项目欢迎古生物 / 地学 / 演化生物 / 数据科学背景的研究者提交新子模块、翻译现有 SKILL.md 至英文 / 中文以外的其他语言、或撰写教学案例"）；
   - 第三段预告下期（"下期我们将以辽西下白垩统义县组今鸟型类化石为案例，完整跑通 paleo-research-assistant 五阶段研究编排流程，并对比其与传统人工综述在文献覆盖率与耗时上的差异"）。

6. **合规检查清单**（发布前）：
   - [ ] 文中所有数据源已标注许可协议（PBDB: CC-BY 4.0 等）；
   - [ ] 所有代码示例已在 Python 3.9–3.12 三系统 CI 中验证通过；
   - [ ] 文中所引用的所有 DOI、PBDB occurrence ID、地层名均可在 v1.0.0 版本的 `paleo-pbdb` / `paleo-crossref` / `paleo-stratigraphy` 脚本中复现；
   - [ ] GitHub Issues 中已建立"v1.0.0 公告反馈"专帖以收集读者意见；
   - [ ] 仓库 README 顶部"Latest News"段已加入本文的链接；
   - [ ] CONTRIBUTING.md 中"Scientific integrity rules"小节已在文中相应位置被引述。

——以上为完整发布方案。**作者建议在正式发布前先将本文与 PRS v1.0.0 的 11 个单元测试结果一并打包发送至 2–3 位同行评议人（建议至少 1 位古生物学者、1 位方法学 / 数据科学背景学者、1 位 Claude Code 工具的资深用户）进行 7–10 天的同行评议**，以最大程度避免在公开公告后修改核心声明。

---

*本文档（`docs/ANNOUNCEMENT_v1.0.0_wechat.md`）为 Paleontology Research Skills v1.0.0 微信公众号公告稿的源文档，可直接复制至 135editor / 秀米 / 壹伴等微信编辑器发布，亦可作为 GitHub Release Notes、Zenodo / Figshare 存档、机构知识库预印本的方法学综述使用。*
