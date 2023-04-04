Write-output 'Running script....'

Write-output ' '
Write-output 'Creating flask enviroment'
python -m venv venv

Write-output ' '
Write-output 'Creating app.py file'
New-item app.py

Write-output ' '
Write-output 'Setting content of app.py'
Set-content app.py 'from flask import Flask
app = Flask(__name__)
@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"'

Write-output ' '
Write-output 'Activating venv script'
venv\scripts\activate

Write-output ' '
Write-output 'Running pip install flask'
pip install flask

Write-output ' '
Write-output 'All done!'
Write-output 'Running flask in debug'

Write-output ' '
flask run --debug