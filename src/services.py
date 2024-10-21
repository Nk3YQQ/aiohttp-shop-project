from src.models import Category


def serialize_category(category: Category) -> dict:
    return {
        'id': category.id,
        'title': category.title,
    }
