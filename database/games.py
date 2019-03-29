from flask import Flask, render_template, flash, redirect, url_for, request, logging
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, SelectField, validators

app = Flask(__name__)

#Config MYSQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'games'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

#init MYSQL
mysql = MySQL(app)

#making queries by search would be a cool idea, so we can make query statements by using likeStrings
#an example would be to insert a search form under /publisher here the user can make queries by publisher name via search bar
#this can be done for all query statements to allow for more flexability
#all things considered we could techinally only have a homepage and make search bar queries from there (just an idea)
class SearchForm(Form):
    choices = [('rank', 'Rank'),
                ('name', 'Name'),
                ('platform', 'Platform'),
                ('year', 'Year'),
                ('genre', 'Genre'),
                ('publisher', 'Publisher')]
    select = SelectField('Search Query:', choices=choices)
    search = StringField('')

@app.route('/', methods=['GET', 'POST'])
def index():
    c = mysql.connection.cursor()
    c.execute('SELECT * FROM games LIMIT 10')
    console = c.fetchall()
    c.execute('SELECT * FROM steam LIMIT 10')
    steam = c.fetchall()

    c.execute('SELECT COUNT(idGame) FROM games UNION SELECT COUNT(idsteam) FROM steam')
    con = c.fetchone()
    st = c.fetchone()
    sum = con.get('COUNT(idGame)')+st.get('COUNT(idGame)')

    cavg = "{:.0%}".format(con.get('COUNT(idGame)')/sum)
    savg = "{:.0%}".format(st.get('COUNT(idGame)')/sum)

    return render_template('home.html', console=console, steam=steam, cavg=cavg, savg=savg)


#@app.route('/search', methods=['GET', 'POST'])
#def index():
#    c = mysql.connection.cursor()
#    form = SearchForm(request.form)
#    if request.method == 'POST' and form.validate():
#        return render_template('home.html')

#    return render_template('home.html', form=form)

@app.route('/search_results/<form>')
def search_results(form):
    results = []
    search_string = form.data['search']

    c = mysql.connection.cursor()
    likeString = '%%' + search_string + '%%'
    c.execute('SELECT * FROM games WHERE %s LIKE %s LIMIT %s', [likeString])
    results = c.fetchall()

    return render_template('all_games.html', results=results)

@app.route('/all_games')
def all_games():
    c = mysql.connection.cursor()

    c.execute('SELECT * FROM games')

    games = c.fetchall()

    type = 'Console'

    return render_template('all_games.html', games=games, type=type)

@app.route('/sports')
def sports():
    c = mysql.connection.cursor()
    type = 'Console Sports'

    c.execute('SELECT * FROM games WHERE genre LIKE "Sports" LIMIT 10;')

    games = c.fetchall()

    c.execute('SELECT COUNT(idGame) FROM games')
    total = c.fetchone()

    c.execute('SELECT COUNT(idGame) FROM games WHERE genre LIKE "Sports";')
    div = c.fetchone()

    avg = div.get('COUNT(idGame)')/total.get('COUNT(idGame)')
    gavg = "{:.0%}".format(avg)

    return render_template('all_games.html', games=games, gavg=gavg, type=type)

@app.route('/shooter')
def shooter():
    c = mysql.connection.cursor()
    type = 'Console Shooter'

    c.execute('SELECT * FROM games WHERE genre LIKE "Shooter" LIMIT 10;')

    games = c.fetchall()

    c.execute('SELECT COUNT(idGame) FROM games')
    total = c.fetchone()

    c.execute('SELECT COUNT(idGame) FROM games WHERE genre LIKE "Shooter";')
    div = c.fetchone()

    avg = div.get('COUNT(idGame)')/total.get('COUNT(idGame)')
    gavg = "{:.0%}".format(avg)

    return render_template('all_games.html', games=games, gavg=gavg, type=type)

@app.route('/publisher')
def publisher():
    c = mysql.connection.cursor()
    type = 'By Publisher'

    c.execute('SELECT * FROM games WHERE publisher LIKE "Activision" LIMIT 10;')

    games = c.fetchall()

    c.execute('SELECT COUNT(idGame) FROM games')
    total = c.fetchone()

    c.execute('SELECT COUNT(idGame) FROM games WHERE publisher LIKE "Activision";')
    div = c.fetchone()

    avg = div.get('COUNT(idGame)')/total.get('COUNT(idGame)')
    gavg = "{:.0%}".format(avg)

    return render_template('all_games.html', games=games, gavg=gavg, type=type)


@app.route('/steam')
def steam():
    c = mysql.connection.cursor()
    type = 'Steam'

    c.execute('SELECT * FROM steam')

    games = c.fetchall()

    return render_template('steam.html', games=games, type=type)
if __name__ == '__main__':
    app.secret_key='secret'
    app.run(debug=True)
