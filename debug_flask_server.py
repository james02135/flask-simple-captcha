from flask import Flask, request, render_template_string
from flask_simple_captcha import CAPTCHA, DEFAULT_CONFIG

app = Flask(__name__)
test_config = DEFAULT_CONFIG.copy()


print(test_config)
CAPTCHA = CAPTCHA(config=test_config)
app = CAPTCHA.init_app(app)


@app.route('/', methods=['GET', 'POST'])
def submit_captcha():
    if request.method == 'GET':
        captcha_dict = CAPTCHA.create()
        return render_template_string(CAPTCHA.captcha_html(captcha_dict))
    if request.method == 'POST':
        c_hash = request.form.get('captcha-hash')
        c_text = request.form.get('captcha-text')

        if CAPTCHA.verify(c_text, c_hash):
            return 'success'
        else:
            return 'failed captcha'


@app.route('/images')
def bulk_captchas():
    num = 50
    captchas = [CAPTCHA.create() for _ in range(int(num))]
    captchas = [
        '<img src="data:image/png;base64, %s" />' % c['img'] for c in captchas
    ]
    style = '<style>img display: inline-block; margin: 8px;</style>'
    return style + '\n'.join(captchas)


if __name__ == '__main__':
    app.run()
