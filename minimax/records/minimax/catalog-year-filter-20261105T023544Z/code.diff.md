# Code diff: catalog-year-filter-20261105T023544Z

## `sample-project/src/bookdesk/catalog.py`

```diff
--- a/sample-project/src/bookdesk/catalog.py
+++ b/sample-project/src/bookdesk/catalog.py
@@ -36,11 +36,8 @@
             if (include_archived or not book.archived)
             and self._matches(book, normalized_query)
             and required_tags.issubset({tag.casefold() for tag in book.tags})
+            and (min_year is None or book.published_year >= min_year)
         ]
-
-        # SPEC-002: min_year is accepted for compatibility, but filtering is
-        # intentionally not implemented in the initial validation snapshot.
-        _ = min_year

         result.sort(key=lambda book: (-book.rating, -book.published_year, book.book_id))
         return result
@@ -51,4 +48,3 @@
             return True
         haystack = " ".join((book.title, book.author, *book.tags)).casefold()
         return normalized_query in haystack
-
```
