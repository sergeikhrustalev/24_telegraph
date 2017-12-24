from flask import Flask, render_template, request, redirect, url_for, session
from article import Article, ArticleStorage


app = Flask(__name__)
app.secret_key = 'secret 12345'

article_storage = ArticleStorage('articles')


@app.route('/', methods=['GET', 'POST'])
def form():

    if request.method == 'POST':

        article_id = article_storage.add(

            Article(
                request.form.get('header'),
                request.form.get('signature'),
                request.form.get('body'),
            )

        )

        session['article_id'] = article_id

        return redirect(
            url_for('show_article', article_id=article_id)
        )

    return render_template('form.html')


@app.route('/<article_id>', methods=['GET', 'POST'])
def show_article(article_id):

    if request.method == 'POST':

        article_storage.rewrite(

            article_id,

            Article(
                request.form.get('header'),
                request.form.get('signature'),
                request.form.get('body'),
            )

        )

        return redirect(
            url_for('show_article', article_id=article_id)
        )

    article = article_storage.get(article_id)

    if not article:
        return 'Article page not found', 404

    return render_template(
        'article.html',
        article_id=article_id,
        header=article.header,
        signature=article.signature,
        body=article.body,
    )


if __name__ == "__main__":
    app.run(host='0.0.0.0')
