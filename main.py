from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
import re
from imageboard.jinja_filters import *
import imageboard.config as config

app = Flask(__name__, template_folder='imageboard_tempelates')
app.config.from_object(config)
app.jinja_env.globals.update(format_date=format_date, format_head=format_head,
                             format_text_art=format_text_art, format_text_comments=format_text_comments
                             )
db = SQLAlchemy(app)


@app.route('/post/article/', methods=['POST'])  # постит новую статью
def post_an_article():
    from imageboard.models import Article
    from imageboard.forms import ArticleForm

    print(request.form)
    form = ArticleForm(request.form)
    if form.validate():
        art_post = Article(**form.data)
        db.session.add(art_post)
        db.session.commit()
        return read_an_article_list()
    else:
        if re.findall('This field is required', str(form.errors)):
            return 'Необходимо заполнить требуемые поля - название статьи и заголовок!'
        if re.findall('Already exists', str(form.errors)):
            return 'Статья с данным заголовком уже существует изобретите что-то новое,' \
                   ' или можете просто оставить комментарий к сущесствующей статье'
        if re.findall('Field cannot be longer than 3000 characters', str(form.errors)):
            return 'Ваша статья слишком большая для борды, попробуйте опоблуковать ее ' \
                   'на НОРМАЛЬНЫХ ресурсах, а не там где собираются маргиналы'
        else:
            print(form.errors)
            return 'Что-то пошло не так... Ваша статья не добавлена'


@app.route('/', methods=['GET'])  # выводит все статьи опубликованные на борде
def read_an_article_list():
    from imageboard.models import Article
    from datetime import datetime as date

    head = Article.query.filter(Article.head != '0')
    date2 = Article.query.filter(Article.date != date.strptime('jun 1 1980', '%b %d %Y'))
    report_all_articles = ([h.head_to_dict() for h in head])
    report_all_dates = ([h.date_to_dict() for h in date2])

    return render_template('headers.txt', all_articles=report_all_articles,
                           all_articles_len=len(report_all_articles), dates=report_all_dates)


@app.route('/read/article/wc/<int:art_id>', methods=['GET'])  # выводит кокретную статью имя которой прописано в роуте
def read_an_article_with_comments(art_id):
    from imageboard.models import Article, Comments
    my_art = Article.query.filter_by(id=art_id).first()
    my_coments = Comments.query.filter(Comments.art_id == my_art.id).all()
    comments_list = []
    for i in range(len(my_coments)):
        comments_list.append(my_coments[i].comment)
    comments_list.reverse()
    com_count = len(comments_list)
    return render_template('article.txt', article_text=my_art.text,
                           all_comments=comments_list, article_name=my_art.head,
                           article_date=my_art.date, comments_count=com_count, article_id=my_art.id)


@app.route('/read/article/wc/<int:art_id>', methods=['GET'])  # то же что и выше, но возвращает другой шаблон
def read_an_article_with_comments_down_to_comment(art_id):  # для перехода сразу вниз страницы
    from imageboard.models import Article, Comments
    my_art = Article.query.filter_by(id=art_id).first()
    my_coments = Comments.query.filter(Comments.art_id == my_art.id).all()
    comments_list = []
    for i in range(len(my_coments)):
        comments_list.append(my_coments[i].comment)
    comments_list.reverse()
    com_count = len(comments_list)
    return render_template('article_down_to_comment.txt', article_text=my_art.text,
                           all_comments=comments_list, article_name=my_art.head,
                           article_date=my_art.date, comments_count=com_count, article_id=my_art.id)


@app.route('/post/comment/<int:art_id>', methods=['POST']) # постит коммент к статье
def post_comment(art_id):
    from imageboard.models import Article, Comments
    from imageboard.forms import ArticleForm, CommentsForm

    print(request.form)
    form = CommentsForm(request.form)

    if form.validate():
        some_article = Article.query.filter_by(id=art_id).first()
        comm_post = Comments(comment=form.data['comment'], art=some_article)
        db.session.add(comm_post)
        db.session.commit()
        return read_an_article_with_comments_down_to_comment(art_id)
    else:
        if re.findall('This field is required', str(form.errors)):
            return 'Необходимо хоть что-то написать...'
        if re.findall('Field cannot be longer than 1000 characters', str(form.errors)):
            return 'Слишком большой коммент, сожмите вашу мысль или разбейте на несколько комментов'
        else:
            print(form.errors)
            return 'Что-то пошло не так... Коммент не добавлен'


@app.route('/get/form', methods=['GET'])
def get_form():
    return render_template('get_form.txt')


if __name__ == '__main__':
    from imageboard.models import *
    db.create_all()
    app.run(host='localhost', port=4000)
