from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    KeepTogether,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "output" / "pdf" / "technical-report.pdf"
OUTPUT.parent.mkdir(parents=True, exist_ok=True)

BODY_FONT = "STSong-Light"
TITLE_FONT = "STSong-Light"
try:
    pdfmetrics.registerFont(
        TTFont("LocalNotoSans", r"C:\Windows\Fonts\NotoSansSC-VF.ttf")
    )
    pdfmetrics.registerFont(
        TTFont("LocalNotoSerif", r"C:\Windows\Fonts\NotoSerifSC-VF.ttf")
    )
    pdfmetrics.registerFont(TTFont("LocalBold", r"C:\Windows\Fonts\simhei.ttf"))
    pdfmetrics.registerFontFamily(
        "LocalNotoSans",
        normal="LocalNotoSans",
        bold="LocalBold",
        italic="LocalNotoSans",
        boldItalic="LocalBold",
    )
    BODY_FONT = "LocalNotoSans"
    TITLE_FONT = "LocalNotoSerif"
except Exception:
    pdfmetrics.registerFont(UnicodeCIDFont("STSong-Light"))

INK = colors.HexColor("#1B1D1A")
SOFT = colors.HexColor("#5B5F57")
FAINT = colors.HexColor("#858A80")
PAPER = colors.HexColor("#F4F1E8")
ACID = colors.HexColor("#D8FF55")
LINE = colors.HexColor("#D8D4C8")

styles = {
    "eyebrow": ParagraphStyle(
        "eyebrow",
        fontName=BODY_FONT,
        fontSize=7,
        leading=9,
        textColor=FAINT,
        spaceAfter=5,
        tracking=1,
    ),
    "title": ParagraphStyle(
        "title",
        fontName=TITLE_FONT,
        fontSize=23,
        leading=28,
        textColor=INK,
        spaceAfter=5,
    ),
    "subtitle": ParagraphStyle(
        "subtitle",
        fontName=BODY_FONT,
        fontSize=8.8,
        leading=13,
        textColor=SOFT,
        spaceAfter=8,
    ),
    "section": ParagraphStyle(
        "section",
        fontName=BODY_FONT,
        fontSize=11.2,
        leading=15,
        textColor=INK,
        spaceBefore=7,
        spaceAfter=4,
    ),
    "body": ParagraphStyle(
        "body",
        fontName=BODY_FONT,
        fontSize=9,
        leading=13.2,
        textColor=SOFT,
        alignment=TA_LEFT,
        spaceAfter=3,
    ),
    "small": ParagraphStyle(
        "small",
        fontName=BODY_FONT,
        fontSize=7.3,
        leading=10.2,
        textColor=FAINT,
    ),
    "metric_value": ParagraphStyle(
        "metric_value",
        fontName=BODY_FONT,
        fontSize=19,
        leading=21,
        textColor=INK,
        alignment=TA_LEFT,
    ),
    "metric_label": ParagraphStyle(
        "metric_label",
        fontName=BODY_FONT,
        fontSize=7.1,
        leading=9.3,
        textColor=FAINT,
    ),
    "table": ParagraphStyle(
        "table",
        fontName=BODY_FONT,
        fontSize=6.9,
        leading=9,
        textColor=SOFT,
    ),
    "table_head": ParagraphStyle(
        "table_head",
        fontName=BODY_FONT,
        fontSize=6.7,
        leading=8.5,
        textColor=colors.white,
    ),
}


def p(text, style="body"):
    return Paragraph(text, styles[style])


doc = SimpleDocTemplate(
    str(OUTPUT),
    pagesize=A4,
    leftMargin=16 * mm,
    rightMargin=16 * mm,
    topMargin=13 * mm,
    bottomMargin=12 * mm,
    title="Local Lexicon - 端侧 AI 推理与 seekdb 混合检索",
    author="StepFun competition submission",
    subject="Technical report",
)

story = [
    p("STEPFUN × SEEKDB / TECHNICAL REPORT", "eyebrow"),
    p("端侧 AI 推理性能优化与 seekdb 混合检索", "title"),
    p(
        "Local Lexicon：浏览器本地向量化 · seekdb 单次全文 + 向量混合检索 · "
        "WebGPU 优先与 WASM 自动降级",
        "subtitle",
    ),
]

metric_cells = [
    [p("1.9989×", "metric_value"), p("25.15 ms", "metric_value"), p("1.000", "metric_value")],
    [
        p("FP32 → FP16 权重压缩比", "metric_label"),
        p("FP16 + WebGPU 端到端中位数", "metric_label"),
        p("FP16 与 FP32 的 Recall / MRR / nDCG", "metric_label"),
    ],
]
metrics = Table(metric_cells, colWidths=[57 * mm, 57 * mm, 57 * mm])
metrics.setStyle(
    TableStyle(
        [
            ("BACKGROUND", (0, 0), (-1, -1), PAPER),
            ("BOX", (0, 0), (-1, -1), 0.6, LINE),
            ("INNERGRID", (0, 0), (-1, -1), 0.4, LINE),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 7),
            ("RIGHTPADDING", (0, 0), (-1, -1), 7),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ]
    )
)
story.extend([Spacer(1, 6), metrics])

story.extend(
    [
        p("01 / 端侧推理与降级", "section"),
        p(
            "Transformers.js 4.3.2 在专用 Web Worker 内加载 "
            "<b>onnx-community/all-MiniLM-L6-v2-ONNX</b>（revision "
            "<b>aff7a1dc</b>，Apache-2.0，384 维），文档与查询 embedding 均在用户设备计算。"
            "启动时探测 <b>navigator.gpu.requestAdapter()</b>：可用时显式选择 WebGPU + FP16；"
            "适配器缺失或初始化失败时自动回退到 WASM + FP16。界面持续显示实际后端，"
            "不使用云端 embedding API，也不回放预计算向量。",
        ),
        p("02 / 量化与质量", "section"),
        p(
            "按 ONNX 图与外部权重文件统计：FP32 为 90,318,300 bytes，FP16 为 "
            "45,184,187 bytes，压缩比 1.9989，体积减少 49.97%。固定 8 文档、8 查询，"
            "同机 Edge/WebGPU 重复 3 次；FP16 的 Recall@1/3/5、MRR@5、nDCG@5 均为 "
            "1.000，与 FP32 的差值均为 0。该小集用于提交回归，不替代更大领域评测。",
        ),
    ]
)

table_data = [
    [
        p("配置", "table_head"),
        p("8 文档向量化", "table_head"),
        p("吞吐", "table_head"),
        p("查询向量化", "table_head"),
        p("seekdb 检索", "table_head"),
        p("端到端", "table_head"),
        p("质量", "table_head"),
    ],
    [
        p("FP32 + WebGPU"),
        p("89.03 ms"),
        p("89.86 docs/s"),
        p("7.04 ms"),
        p("—"),
        p("—"),
        p("1.000"),
    ],
    [
        p("FP16 + WebGPU"),
        p("83.83 ms"),
        p("95.43 docs/s"),
        p("7.27 ms"),
        p("4.58 ms"),
        p("25.15 ms"),
        p("1.000"),
    ],
    [
        p("FP16 + WASM"),
        p("604.28 ms"),
        p("13.24 docs/s"),
        p("9.84 ms"),
        p("4.54 ms"),
        p("26.72 ms"),
        p("1.000"),
    ],
]
benchmark = Table(
    table_data,
    colWidths=[30 * mm, 30 * mm, 28 * mm, 26 * mm, 24 * mm, 22 * mm, 17 * mm],
    repeatRows=1,
)
benchmark.setStyle(
    TableStyle(
        [
            ("BACKGROUND", (0, 0), (-1, 0), INK),
            ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#FFFDF7")),
            ("GRID", (0, 0), (-1, -1), 0.35, LINE),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("ALIGN", (1, 1), (-1, -1), "RIGHT"),
            ("LEFTPADDING", (0, 0), (-1, -1), 4),
            ("RIGHTPADDING", (0, 0), (-1, -1), 4),
            ("TOPPADDING", (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ]
    )
)
story.extend(
    [
        Spacer(1, 4),
        benchmark,
        p(
            "文档向量化为 3 次中位数；查询与端到端为 5 次中位数。端到端从提交查询开始，"
            "包含 query embedding、HTTP、seekdb 混合检索和结果 DOM 渲染。"
            "测试环境：Windows 10.0.26200、Ryzen 7 9700X、RTX 5080、Edge 156、seekdb 1.4.0.0。",
            "small",
        ),
        p("03 / seekdb 数据与刷新", "section"),
        p(
            "每个知识库对应独立 collection，同时建立 smart IK 全文索引与 384 维 cosine "
            "HNSW；目录表和文档登记表持久化会话与内容哈希。写入采用确定性分块 ID 和 "
            "<b>upsert</b>，重复导入删除变短后的尾部旧分块。写后依次执行 "
            "<b>collection.refresh_index()</b> 和带 documentId 过滤的向量可见性轮询，"
            "只有新分块可检索才返回成功。",
        ),
        p("04 / 数据库内混合检索", "section"),
        p(
            "查询时调用一次 <b>collection.hybridSearch()</b>：全文条件放在 query，"
            "浏览器生成的稠密向量放在 knn，数据库内以 <b>RRF (rankConstant=60)</b> 融合；"
            "SDK 将其展开为 seekdb <b>DBMS_HYBRID_SEARCH</b>。客户端不会分别拉取两路候选再拼合。"
            "实测 8 文档、8 分块下，5 次检索中位数：WebGPU 4.58 ms，WASM 4.54 ms。",
        ),
        p("05 / 复现与证据", "section"),
        p(
            "源码目录：<b>stepfun/</b>。启动：<b>npm ci → npm run init-db → npm run dev</b>；"
            "生产构建：<b>npm run build → npm run start:win</b>。"
            "单元测试 9/9、真实 seekdb 集成测试通过；独立无头 Edge 验证 WebGPU、移除 GPU 后的 "
            "自动 WASM、8 文档导入、索引刷新、5 次混合检索，以及临时空 collection 不串结果。"
            "原始 JSON、截图、Schema 与完整方法分别保存在 results/ 和 docs/。",
        ),
    ]
)

footer = Table(
    [
        [
            p(
                "INFERENCE LOCATION: THIS DEVICE  ·  RETRIEVAL ENGINE: SEEKDB  ·  "
                "RANK: RRF",
                "small",
            )
        ]
    ],
    colWidths=[171 * mm],
)
footer.setStyle(
    TableStyle(
        [
            ("BACKGROUND", (0, 0), (-1, -1), ACID),
            ("BOX", (0, 0), (-1, -1), 0.5, INK),
            ("LEFTPADDING", (0, 0), (-1, -1), 7),
            ("TOPPADDING", (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ]
    )
)
story.extend([Spacer(1, 7), KeepTogether(footer)])

doc.build(story)
print(OUTPUT)
