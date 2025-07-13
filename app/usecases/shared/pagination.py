from typing import Callable, Sequence, TypeVar

from app.models.study_pal_base import StudyPalBaseModel
from app.schemas.shared.page_info import PageInfo

T = TypeVar("T", bound=StudyPalBaseModel)


def pagination(
    base_query: Callable[[], Sequence[T]],
    next_query: Callable[[], Sequence[T]] | None,
    page: PageInfo,
) -> tuple[Sequence[T], PageInfo]:

    query_func = base_query
    if page.next_page_token:
        query_func = next_query

    if not query_func:
        raise ValueError("Query function is not specified")

    results = query_func()
    next_page_token = None
    # 結果が page_size + 1 件なら次ページあり
    has_extra = len(results) > page.page_size
    if has_extra:
        next_page_token = results[-1].id
        results = results[: page.page_size]

    new_page = PageInfo(
        next_page_token=next_page_token,
        page_size=len(results),
    )

    return results, new_page
