from flask import Flask, request, abort, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL
from newspaper import Article


app = Flask(__name__)
app.config['SECRET_KEY'] = 'This is a secret key that will never be expose'


class URLForm(FlaskForm):
    url = StringField('url', validators=[DataRequired(), URL()])
    submit = SubmitField('Parse now')


@app.route('/', methods=['GET', 'POST'])
def index():
    form = URLForm()
    if form.validate_on_submit():
        url = form.data['url']
        article = Article(url)
        article.download()
        article.parse()
        data = {
            'url': url,
            'content': article.text,
            'image': article.top_image,
            'summary': article.summary
        }
        return render_template('result.html', news_data=data)
    return render_template('index.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
