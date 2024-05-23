from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def form():
    name = None
    email = None
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
    return render_template('form.html', name=name, email=email)

if __name__ == '__main__':
    app.run(debug=True, port=80, host='0.0.0.0')
