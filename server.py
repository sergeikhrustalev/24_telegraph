from flask import Flask, render_template, request, redirect, url_for
from article import Article, ArticleStorage


app = Flask(__name__)
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
        
        return redirect(
            url_for('show_article', article_id=article_id)
        )

    return render_template('form.html')


@app.route('/<article_id>', methods=['GET'])
def show_article(article_id):
    
    article = article_storage.get(article_id)

    return '{}<br>{}<br>{}'.format(
        article.header,
        article.signature,
        article.body,
    ) 


if __name__ == "__main__":
    app.run()
