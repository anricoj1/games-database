def searchString():
    results = []
    search_string = form.data['search']
    search_type = form.data['select']

    c = mysql.connection.cursor()
    likeString = search_string
    typeString = search_type
    print(likeString)
    c.execute('SELECT * FROM games WHERE %s LIKE %s LIMIT 10;' [typeString, likeString])
    games = c.fetchall()
