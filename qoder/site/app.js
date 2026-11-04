/* Spec Context 站点交互脚本 — 数据均取自仓库真实记录 */
"use strict";

/* ---------- 移动端导航 ---------- */
const toggle = document.querySelector(".nav-toggle");
const nav = document.getElementById("site-nav");
if (toggle && nav) {
  toggle.addEventListener("click", () => {
    const open = nav.classList.toggle("open");
    toggle.setAttribute("aria-expanded", String(open));
  });
  nav.addEventListener("click", (e) => {
    if (e.target.tagName === "A") {
      nav.classList.remove("open");
      toggle.setAttribute("aria-expanded", "false");
    }
  });
}

/* ---------- 演示步骤 tabs ---------- */
const tabs = Array.from(document.querySelectorAll('[role="tab"]'));
const panels = tabs.map((t) => document.getElementById(t.getAttribute("aria-controls")));

function selectTab(index) {
  tabs.forEach((tab, i) => {
    tab.setAttribute("aria-selected", String(i === index));
    tab.tabIndex = i === index ? 0 : -1;
    panels[i].hidden = i !== index;
  });
  tabs[index].focus();
}
tabs.forEach((tab, i) => {
  tab.addEventListener("click", () => selectTab(i));
  tab.addEventListener("keydown", (e) => {
    if (e.key === "ArrowRight" || e.key === "ArrowLeft") {
      e.preventDefault();
      selectTab((i + (e.key === "ArrowRight" ? 1 : tabs.length - 1)) % tabs.length);
    } else if (e.key === "Home") { e.preventDefault(); selectTab(0); }
    else if (e.key === "End") { e.preventDefault(); selectTab(tabs.length - 1); }
  });
});

/* ---------- 上下文列表（records/context-task-001.json 节选） ---------- */
const CTX = [
  { kind: "规格", cls: "", path: "specs/SPEC-002-书目录查询.md#SPEC-002-4", v: 1, score: 9.5521,
    text: "年份筛选必须与关键词、标签和 include_archived 条件同时生效，并继续保持既有排序。" },
  { kind: "规格", cls: "", path: "specs/SPEC-002-书目录查询.md#SPEC-002-1", v: 1, score: 7.1059,
    text: "Catalog.search 支持可选参数 min_year: int | None = None，用于按 Book.published_year 筛选。" },
  { kind: "规格", cls: "", path: "specs/SPEC-002-书目录查询.md#SPEC-002-2", v: 3, score: 3.937,
    text: "提供 min_year 时，只返回出版年份大于或等于 min_year 的书籍；等于边界时必须返回。" },
  { kind: "规格", cls: "", path: "specs/SPEC-001-工程约束.md#SPEC-001-4", v: 1, score: 3.0884,
    text: "搜索结果排序必须确定：评分降序，出版年份降序，相同年份按 book_id 升序。" },
  { kind: "规格", cls: "", path: "specs/SPEC-001-工程约束.md#SPEC-001-2", v: 1, score: 2.7623,
    text: "为既有公开接口增加参数时必须提供默认值，保证旧调用方式继续有效。" },
  { kind: "规格", cls: "", path: "specs/SPEC-001-工程约束.md#SPEC-001-3", v: 1, score: 2.455,
    text: "搜索与筛选不得修改目录中保存的书籍、标签或统计值。" },
  { kind: "规格", cls: "", path: "specs/SPEC-002-书目录查询.md#SPEC-002-3", v: 1, score: 2.345,
    text: "未提供 min_year 时，搜索结果必须与加入该参数前的行为完全一致。" },
  { kind: "规格", cls: "", path: "specs/SPEC-002-书目录查询.md#SPEC-002-5", v: 1, score: 1.4728,
    text: "年份筛选只作用于本次调用，不得影响后续不带筛选的搜索结果。" },
  { kind: "代码", cls: "k-code", path: "sample-project/src/bookdesk/catalog.py", v: 1, score: 4.2027,
    text: "Symbols: Catalog, __init__, add, get, all_books, search, _matches" },
  { kind: "代码", cls: "k-code", path: "sample-project/src/bookdesk/models.py", v: 1, score: 3.8467,
    text: "Symbols: Book" },
  { kind: "代码", cls: "k-code", path: "sample-project/src/bookdesk/__init__.py", v: 1, score: 1.9453,
    text: "Symbols: （包导出 Book、Catalog）" },
  { kind: "测试", cls: "k-test", path: "sample-project/tests/test_catalog_year_filter.py", v: 1, score: 3.8148,
    text: "目标测试 7 项：边界包含、组合筛选、不改动目录等" },
  { kind: "测试", cls: "k-test", path: "sample-project/tests/conftest.py", v: 1, score: 3.1291,
    text: "fixture：六本书（2017–2023）、归档 1 本、共享评分" },
  { kind: "测试", cls: "k-test", path: "sample-project/tests/test_catalog_regression.py", v: 1, score: 2.5713,
    text: "回归测试 5 项：默认排序、关键词、标签、归档、重复添加" },
];
const ctxList = document.getElementById("ctx-list");
if (ctxList) {
  for (const item of CTX) {
    const li = document.createElement("li");
    const kind = document.createElement("span");
    kind.className = "c-kind " + item.cls;
    kind.textContent = item.kind;
    const path = document.createElement("span");
    path.className = "c-path";
    path.textContent = item.path;
    const meta = document.createElement("span");
    meta.className = "c-meta";
    meta.textContent = `v${item.v} · score ${item.score}`;
    const text = document.createElement("span");
    text.className = "c-text";
    text.textContent = item.text;
    li.append(kind, path, meta, text);
    ctxList.appendChild(li);
  }
}

/* ---------- 目录行为模拟器 ---------- */
/* 真实 fixture：sample-project/tests/conftest.py */
const BOOKS = [
  { id: "B-001", title: "数据库系统", year: 2018, rating: 4.8, archived: false },
  { id: "B-002", title: "查询优化", year: 2020, rating: 4.7, archived: false },
  { id: "B-003", title: "向量检索", year: 2021, rating: 4.9, archived: false },
  { id: "B-004", title: "旧版检索手册", year: 2017, rating: 5.0, archived: true },
  { id: "B-005", title: "上下文工程", year: 2023, rating: 4.7, archived: false },
  { id: "B-006", title: "搜索引擎实践", year: 2020, rating: 4.2, archived: false },
];

/* SPEC-001-4 的确定性排序 */
function sortBooks(list) {
  return [...list].sort(
    (a, b) => b.rating - a.rating || b.year - a.year || (a.id < b.id ? -1 : 1)
  );
}

/* 初版实现：接受 min_year 但忽略之（catalog.py 中 `_ = min_year`） */
function beforeImpl(minYear, includeArchived) {
  return sortBooks(BOOKS.filter((b) => includeArchived || !b.archived));
}

/* 规格实现：SPEC-002-2 包含边界 + SPEC-002-4 与归档选项组合 */
function specImpl(minYear, includeArchived) {
  return sortBooks(
    BOOKS.filter(
      (b) => (includeArchived || !b.archived) && (minYear === null || b.year >= minYear)
    )
  );
}

function noteFor(year, archived) {
  if (year === null)
    return "断言来源：test_min_year_none_keeps_existing_results 与回归 test_empty_search_keeps_existing_sort——两种实现结果应完全相同。";
  if (year === 2021)
    return "断言来源：test_min_year_returns_only_matching_books——规格侧期望 [B-003, B-005]。";
  if (year === 2020)
    return "断言来源：test_min_year_includes_boundary——等于边界必须返回，期望 [B-003, B-005, B-002, B-006]。";
  if (year === 2017 && archived)
    return "断言来源：test_min_year_combines_with_archived_option——首元素必须为 B-004（评分 5.0，已归档）。";
  if (year === 2017)
    return "2017 是全库下界：SPEC-002-2 下筛选不应移除任何书；B-004 仅在 include_archived=True 时可见。";
  if (year === 2023)
    return "由 SPEC-002-2 规则计算（仓库测试未直接断言 2023）：仅 B-005 满足年份下限。";
  if (year === 9999)
    return "断言来源：test_min_year_above_everything_returns_empty——规格侧必须为空列表。";
  return "";
}

const yearSel = document.getElementById("sim-year");
const archChk = document.getElementById("sim-arch");
const beforeOl = document.getElementById("sim-before");
const afterOl = document.getElementById("sim-after");
const simNote = document.getElementById("sim-note");

function renderBookList(ol, list) {
  ol.textContent = "";
  if (list.length === 0) {
    const li = document.createElement("li");
    li.className = "empty";
    li.textContent = "（空结果）";
    ol.appendChild(li);
    return;
  }
  for (const b of list) {
    const li = document.createElement("li");
    if (b.archived) li.classList.add("archived");
    const name = document.createElement("span");
    const id = document.createElement("span");
    id.className = "bk-id";
    id.textContent = b.id;
    name.append(id, document.createTextNode(` ${b.title}${b.archived ? "（归档）" : ""}`));
    const year = document.createElement("span");
    year.className = "bk-year";
    year.textContent = `${b.year} · ${b.rating.toFixed(1)}`;
    li.append(name, year);
    ol.appendChild(li);
  }
}

function updateSim() {
  const raw = yearSel.value;
  const year = raw === "" ? null : Number(raw);
  const archived = archChk.checked;
  renderBookList(beforeOl, beforeImpl(year, archived));
  renderBookList(afterOl, specImpl(year, archived));
  simNote.textContent = noteFor(year, archived);
}
if (yearSel && archChk) {
  yearSel.addEventListener("change", updateSim);
  archChk.addEventListener("change", updateSim);
  updateSim();
}
