from wtforms_alchemy import ModelForm
from imageboard.models import Article, Comments


class ArticleForm(ModelForm):
    class Meta:
        model = Article


class CommentsForm(ModelForm):
    class Meta:
        model = Comments
