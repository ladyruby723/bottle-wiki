from bottle import request, route, run, template, post, TEMPLATE_PATH, abort, redirect
from marshmallow import Schema, fields
import dbfunctions

TEMPLATE_PATH.append('templates')
DB_PATH = './wiki.db'


class ArticleSchema(Schema):
    body = fields.Str()
    subject = fields.Str()


class Article():
    def __init__(self, body, subject):
        self.body = body
        self.subject = subject


@route('/')
def index():
    return template('index.html', subject='PySprings Wiki', body='Under Construction')


@route('/<subject>')
def view_article(subject):
    db_result = dbfunctions.search_article(subject)
    if db_result:
        _, get_function = db_result[0]
        body = get_function()
        return template('index.html', subject=subject, body=body)
    else:
        return abort(404, 'Not found.')


@route('/<subject>/edit')
def edit_view(subject):
    db_result = dbfunctions.search_article(subject)
    body = ''
    if db_result:
        _, get_function = db_result[0]
        body = get_function()
    return template('edit.html', subject=subject, body=body)


@post('/edit')
def edit():
    body = request.forms.get('article')
    subject = request.forms.get('subject')

    article = Article(body=body, subject=subject)

    schema = ArticleSchema()
    data, errors = schema.dump(article)
    if dbfunctions.search_article(subject):
        dbfunctions.update_article(subject, body)
    else:
        dbfunctions.create_article(subject, body)
    return redirect('/' + subject)


if __name__ == '__main__':
    dbfunctions.init_db(DB_PATH)
    run(host='localhost', port=8080, debug=True)
