from sddctx.analyzer import analyze_text, extract_identifiers, query_terms


def test_analyzer_is_deterministic_and_case_insensitive() -> None:
    first = analyze_text("Catalog.search min_year 年份筛选")
    second = analyze_text("catalog SEARCH MIN_YEAR 年份筛选")
    assert first == second


def test_analyzer_emits_chinese_unigrams_and_bigrams() -> None:
    terms = query_terms("年份下限")
    assert "u_年" in terms
    assert "b_年份" in terms
    assert "b_份下" in terms
    assert "b_下限" in terms


def test_identifier_extraction_keeps_code_symbols() -> None:
    assert extract_identifiers("修改 Catalog.search 的 min_year 与 Book.published_year") == [
        "Catalog",
        "search",
        "min_year",
        "Book",
        "published_year",
    ]
