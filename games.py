from flask import Flask, render_template, flash, redirect, url_for, request, logging
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, SelectField, validators
from src.search import namePercent, platPercent, yearPercent, genrePercent, publisherPercent

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

class SearchSales(Form):
    choices = [('naSales', 'NASales'),
               ('euSales', 'EUSales'),
               ('jpSales', 'JPSales'),
               ('otherSales', 'OtherSales'),
               ('globalSales', 'GlobalSales')]
    select = SelectField('Search Query: ', choices=choices)


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
    g = con.get('COUNT(idGame)')
    s = st.get('COUNT(idGame)')
    sum = con.get('COUNT(idGame)')+st.get('COUNT(idGame)')

    cavg = "{:.0%}".format(con.get('COUNT(idGame)')/sum)
    savg = "{:.0%}".format(st.get('COUNT(idGame)')/sum)

    return render_template('home.html', console=console, steam=steam, cavg=cavg, savg=savg, g=g, s=s, sum=sum)


@app.route('/search/', methods=['GET', 'POST'])
def search():
    c = mysql.connection.cursor()
    form = SearchForm(request.form)
    if request.method == 'POST' and form.validate():
        return search_results(form)

    return render_template('search.html', form=form)

@app.route('/search_results/<form>')
def search_results(form):
    results = []
    search_string = form.data['search']
    search_type = form.data['select']


    c = mysql.connection.cursor()
    c.execute('SELECT COUNT(idGame) from games')
    total = c.fetchone()
    if search_type == 'name':
        c.execute("SELECT * FROM games WHERE name LIKE %s;", [search_string])
        games = c.fetchall()
        return render_template('all_games.html', games=games, form=form)
    elif search_type == 'platform':
        c.execute('SELECT * FROM games WHERE platform LIKE %s;', [search_string])
        games = c.fetchall()
        c.execute('SELECT COUNT(idGame) FROM games WHERE platform LIKE %s', [search_string])
        div = c.fetchone()
        avg = div.get('COUNT(idGame)')/total.get('COUNT(idGame)')
        gavg = "{:0%}".format(avg)

        return render_template('all_games.html', games=games, form=form, gavg=gavg)
    elif search_type == 'year':
        c.execute('SELECT * FROM games WHERE year LIKE %s;', [search_string])
        games = c.fetchall()
        c.execute('SELECT COUNT(idGame) FROM games WHERE year LIKE %s', [search_string])
        div = c.fetchone()
        avg = div.get('COUNT(idGame)')/total.get('COUNT(idGame)')
        gavg = "{:0%}".format(avg)

        return render_template('all_games.html', games=games, form=form, gavg=gavg)
    elif search_type == 'genre':
        c.execute('SELECT * FROM games WHERE genre LIKE %s;', [search_string])
        games = c.fetchall()
        c.execute('SELECT COUNT(idGame) FROM games WHERE genre LIKE %s', [search_string])
        div = c.fetchone()
        avg = div.get('COUNT(idGame)')/total.get('COUNT(idGame)')
        gavg = "{:0%}".format(avg)
        return render_template('all_games.html', games=games, form=form, gavg=gavg)
    elif search_type == 'publisher':
        c.execute('SELECT * FROM games WHERE publisher LIKE %s;', [search_string])
        games = c.fetchall()
        c.execute('SELECT COUNT(idGame) FROM games WHERE publisher LIKE %s', [search_string])
        div = c.fetchone()
        avg = div.get('COUNT(idGame)')/total.get('COUNT(idGame)')
        gavg = "{:0%}".format(avg)
        return render_template('all_games.html', games=games, form=form, gavg=gavg)
    else:
        c.execute('SELECT * FROM games')
        games = c.fetchall()
        return render_template('all_games.html', games=games, form=form)

def search_sales(form):
    results = []
    search_type = form.data['select']

    c = mysql.connection.cursor()
    c.execute('SELECT COUNT(idGame) from games')
    total = c.fetchone()
    if search_type == 'naSales':
        c.execute("SELECT * FROM games WHERE naSales BETWEEN 10 AND 30")
        games = c.fetchall()
        c.execute('SELECT COUNT(idGame) FROM games WHERE naSales BETWEEN 10 AND 30')
        div = c.fetchone()
        print(div)
        avg = div.get('COUNT(idGame)')/total.get('COUNT(idGame)')
        gavg = "{:0%}".format(avg)

        return render_template('sales.html', games=games, form=form, gavg=gavg, search_type=search_type)
    elif search_type == 'euSales':
        c.execute('SELECT * FROM games WHERE euSales BETWEEN 10 AND 30')
        games = c.fetchall()
        c.execute('SELECT COUNT(idGame) FROM games WHERE euSales BETWEEN 10 AND 30')
        div = c.fetchone()
        avg = div.get('COUNT(idGame)')/total.get('COUNT(idGame)')
        gavg = "{:0%}".format(avg)

        return render_template('sales.html', games=games, form=form, gavg=gavg, search_type=search_type)
    elif search_type == 'jpSales':
        c.execute('SELECT * FROM games WHERE jpSales BETWEEN 10 AND 30')
        games = c.fetchall()
        c.execute('SELECT COUNT(idGame) FROM games WHERE jpSales BETWEEN 10 AND 30')
        div = c.fetchone()
        avg = div.get('COUNT(idGame)')/total.get('COUNT(idGame)')
        gavg = "{:0%}".format(avg)

        return render_template('sales.html', games=games, form=form, gavg=gavg, search_type=search_type)
    elif search_type == 'otherSales':
        c.execute('SELECT * FROM games WHERE otherSales BETWEEN 10 AND 30')
        games = c.fetchall()
        c.execute('SELECT COUNT(idGame) FROM games WHERE otherSales BETWEEN 10 AND 30')
        div = c.fetchone()
        avg = div.get('COUNT(idGame)')/total.get('COUNT(idGame)')
        gavg = "{:0%}".format(avg)

        return render_template('sales.html', games=games, form=form, gavg=gavg, search_type=search_type)
    elif search_type == 'globalSales':
        c.execute('SELECT * FROM games WHERE globalSales BETWEEN 10 AND 30')
        games = c.fetchall()
        c.execute('SELECT COUNT(idGame) FROM games WHERE globalSales BETWEEN 10 AND 30')
        div = c.fetchone()
        avg = div.get('COUNT(idGame)')/total.get('COUNT(idGame)')
        gavg = "{:0%}".format(avg)
        return render_template('sales.html', games=games, form=form, gavg=gavg, search_type=search_type)
    else:
        c.execute('SELECT * FROM games')
        games = c.fetchall()
        return render_template('sales.html.html', games=games, form=form)

@app.route('/all_games', methods=['GET', 'POST'])
def all_games():
    c = mysql.connection.cursor()
    form = SearchForm(request.form)
    if request.method == 'POST' and form.validate():
        return search_results(form)
    else:
        c = mysql.connection.cursor()
        type = 'Console'
        c.execute('SELECT * FROM games')
        games = c.fetchall()
        return render_template('all_games.html', games=games, form=form, type=type)

@app.route('/sales', methods=['GET', 'POST'])
def sports():
    c = mysql.connection.cursor()
    form = SearchSales(request.form)
    if request.method == 'POST' and form.validate():
        return search_sales(form)
    else:
        c.execute('SELECT * FROM games')
        games = c.fetchall()
        return render_template('sales.html', games=games, form=form)

class SearchSteam(Form):
    choices = [('multiplayer', 'Multiplayer'),
               ('singleplayer', 'SinglePlayer'),
               ('mmo', 'MMO'),
               ('VRSupport', 'VR'),
               ('isFree', 'Free'),
               ('earlyAccess', 'EarlyAccess'),
               ('windows', 'Windows'),
               ('linux', 'Linux'),
               ('mac', 'Mac')]
    select = SelectField('Search Steam', choices=choices)

def search_steam(form):
    results = []
    search_type = form.data['select']

    c = mysql.connection.cursor()
    if search_type == 'multiplayer':
        c.execute('SELECT * FROM steam WHERE multiplayer=1')
        games = c.fetchall()

        return render_template('steam.html', games=games, form=form)
    elif search_type == 'singleplayer':
        c.execute('SELECT * FROM steam WHERE singleplayer=1')
        games = c.fetchall()

        return render_template('steam.html', games=games, form=form)
    elif search_type == 'mmo':
        c.execute('SELECT * FROM steam WHERE mmo=1')
        games = c.fetchall()

        return render_template('steam.html', games=games, form=form)
    elif search_type == 'VRSupport':
        c.execute('SELECT * FROM steam WHERE VRSupport=1')
        games = c.fetchall()

        return render_template('steam.html', games=games, form=form)
    elif search_type == 'isFree':
        c.execute('SELECT * FROM steam WHERE isFree=1')
        games = c.fetchall()

        return render_template('steam.html', games=games, form=form)

    elif search_type == 'earlyAccess':
        c.execute('SELECT * FROM steam WHERE earlyAccess=1')
        games = c.fetchall()

        return render_template('steam.html', games=games, form=form)

    elif search_type == 'windows':
        c.execute('SELECT * FROM steam WHERE windows=1')
        games = c.fetchall()

        return render_template('steam.html', games=games, form=form)
    elif search_type == 'linux':
        c.execute('SELECT * FROM steam WHERE linux=1')
        games = c.fetchall()

        return render_template('steam.html', games=games, form=form)
    elif search_type == 'mac':
        c.execute('SELECT * FROM steam WHERE mac=1')
        games = c.fetchall()

        return render_template('steam.html', games=games, form=form)
    else:
        c.execute('SELECT * FROM steam')
        games = c.fetchall()

        return render_template('steam.html', games=games, form=form)

@app.route('/steam', methods=['GET', 'POST'])
def steam():
    c = mysql.connection.cursor()
    form = SearchSteam(request.form)
    if request.method == 'POST' and form.validate():
        return search_steam(form)
    else:
        c.execute('SELECT * FROM steam')
        games = c.fetchall()
        return render_template('steam.html', games=games, form=form)

class SearchRequire(Form):
    choices = [('responseName', 'Name'),
               ('windows', 'Windows'),
               ('linux', 'Linux'),
               ('mac', 'Mac')]
    select = SelectField('Search Query:', choices=choices)
    search = StringField('')


def search_req(form):
    results = []
    search_type = form.data['select']
    search_string = form.data['search']

    c = mysql.connection.cursor()
    if search_type == 'responseName':
        c.execute('SELECT idsysRequire, idsteam, winReq, linuxReq, macReq, responseName FROM sysRequire r INNER JOIN steam s ON r.idsysRequire=s.idsteam WHERE responseName=%s', [search_string])
        games = c.fetchall()
        return render_template('requirements.html', form=form, games=games)
    elif search_type == 'windows':
        c.execute('SELECT idsysRequire, idsteam, winReq, responseName FROM sysRequire r INNER JOIN steam s ON r.idsysRequire=s.idsteam')
        games = c.fetchall()
        return render_template('requirements.html', form=form, games=games)
    elif search_type == 'linux':
        c.execute('SELECT idsysRequire, idsteam, linuxReq, responseName FROM sysRequire r INNER JOIN steam s ON r.idsysRequire=s.idsteam')
        games = c.fetchall()
        return render_template('requirements.html', form=form, games=games)
    elif search_type == 'mac':
        c.execute('SELECT idsysRequire, idsteam, macReq, responseName FROM sysRequire r INNER JOIN steam s ON r.idsysRequire=s.idsteam')
        games = c.fetchall()
        return render_template('requirements.html', form=form, games=games)
    else:
        c.execute('SELECT idsysRequire, idsteam, winReq, linuxReq, macReq, responseName FROM sysRequire r INNER JOIN steam s ON r.idsysRequire=s.idsteam')
        games = c.fetchall()
        return render_template('requirements.html', form=form, games=games)

@app.route('/min_requirements', methods=['GET', 'POST'])
def min_requirements():
    c = mysql.connection.cursor()
    form = SearchRequire(request.form)
    if request.method == 'POST' and form.validate():
        return search_req(form)
    else:
        c.execute('SELECT idsysRequire, idsteam, winReq, linuxReq, macReq, responseName FROM sysRequire r INNER JOIN steam s ON r.idsysRequire=s.idsteam')
        games = c.fetchall()
        return render_template('requirements.html', games=games, form=form)


@app.route('/structure', methods=['GET', 'POST'])
def structure():
    return render_template('structure.html')

if __name__ == '__main__':
    app.secret_key='secret'
    app.run(debug=True)
