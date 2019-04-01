def namePercent():
    c = mysql.connenction.cursor()
    c.execute('SELECT COUNT(idGame) FROM games')
    total = c.fetchone()
    c.execute('SELECT COUNT(idGame) FROM games WHERE name LIKE %s', [search_string])
    div = c.fetchone()
    avg = div.get('COUNT(idGame)')/total.get('COUNT(idGame)')
    gavg = "{:.0%}".format(avg)


def platPercent():
    c = mysql.connenction.cursor()
    c.execute('SELECT COUNT(idGame) FROM games')
    total = c.fetchone()
    c.execute('SELECT COUNT(idGame) FROM games WHERE platform LIKE %s', [search_string])
    div = c.fetchone()
    avg = div.get('COUNT(idGame)')/total.get('COUNT(idGame)')
    gavg = "{:.0%}".format(avg)


def yearPercent():
    c = mysql.connenction.cursor()
    c.execute('SELECT COUNT(idGame) FROM games')
    total = c.fetchone()
    c.execute('SELECT COUNT(idGame) FROM games WHERE year LIKE %s', [search_string])
    div = c.fetchone()
    avg = div.get('COUNT(idGame)')/total.get('COUNT(idGame)')
    gavg = "{:.0%}".format(avg)




def genrePercent():
    c = mysql.connenction.cursor()
    c.execute('SELECT COUNT(idGame) FROM games')
    total = c.fetchone()
    c.execute('SELECT COUNT(idGame) FROM games WHERE genre LIKE %s', [search_string])
    div = c.fetchone()
    avg = div.get('COUNT(idGame)')/total.get('COUNT(idGame)')
    gavg = "{:.0%}".format(avg)


def publisherPercent():
    c = mysql.connenction.cursor()
    c.execute('SELECT COUNT(idGame) FROM games')
    total = c.fetchone()
    c.execute('SELECT COUNT(idGame) FROM games WHERE publisher LIKE %s', [search_string])
    div = c.fetchone()
    avg = div.get('COUNT(idGame)')/total.get('COUNT(idGame)')
    gavg = "{:.0%}".format(avg)
