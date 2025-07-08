from typing import Callable, Sequence, TypeVar

from app.models.study_pal_base import StudyPalBaseModel
from app.schemas.shared.page_info import PageInfo

T = TypeVar("T", bound=StudyPalBaseModel)


def pagination(
    base_query: Callable[[], Sequence[T]],
    next_query: Callable[[], Sequence[T]] | None,
    prev_query: Callable[[], Sequence[T]] | None,
    page: PageInfo,
) -> tuple[Sequence[T], PageInfo]:
    if page.next_page_token and page.prev_page_token:
        raise ValueError(
            "Both next_page_token and prev_page_token"
            "are set. Specify only one."
        )

    query_func = base_query
    if page.next_page_token:
        query_func = next_query
    elif page.prev_page_token:
        query_func = prev_query

    if not query_func:
        raise ValueError("Query function is not specified")

    results = query_func()
    next_page_token = None
    # 結果が page_size + 1 件なら次ページあり
    has_extra = len(results) > page.page_size
    if has_extra:
        next_page_token = results[-1].id
        results = results[: page.page_size]

    next_page = PageInfo(
        next_page_token=next_page_token,
        page_size=len(results),
        prev_page_token=None,
    )

    return results, next_page
