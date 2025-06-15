from typing import Any, get_args, get_type_hints


class StudyPalBaseModelAnalyzer:
    @staticmethod
    def get_related_model_type_from_list(
        key: str, mold: type[Any]
    ) -> type[Any]:
        type_hints = get_type_hints(mold)
        # Mapped[list[ArticleLike]]
        key_type = type_hints[key]
        # (list[ArticleLike],)
        mapped_args = get_args(key_type)
        # list[ArticleLike]
        list_type = mapped_args[0]
        # (ArticleLike,)
        list_args = get_args(list_type)
        # ArticleLike
        model_type = list_args[0]

        return model_type

    @staticmethod
    def get_related_model_type(key: str, mold: type[Any]) -> type[Any]:
        type_hints = get_type_hints(mold)
        # Mapped[User]
        mapped_type = type_hints[key]
        # User
        return get_args(mapped_type)[0]
