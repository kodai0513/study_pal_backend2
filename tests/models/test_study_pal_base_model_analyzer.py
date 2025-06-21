from app.models.model import Article, ArticleLike, User
from app.models.study_pal_base_model_analyzer import StudyPalBaseModelAnalyzer


def test_get_related_model_type_from_list():
    model_type = StudyPalBaseModelAnalyzer.get_related_model_type_from_list(
        "article_likes", Article
    )
    assert model_type is ArticleLike


def test_get_related_model_type():
    model_type = StudyPalBaseModelAnalyzer.get_related_model_type(
        "user", Article
    )
    assert model_type is User
