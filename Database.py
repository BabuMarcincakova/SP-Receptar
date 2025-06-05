import sqlite3 as sql

class Database:
    def __init__(self):
        self.db = sql.connect(':memory:')
        self.create()
        self.tables()
        
        self.basics()
    
    def create(self):   #vytvorenie tabuliek (a vymazanie ak existuju)
        self.db.execute("DROP TABLE IF EXISTS categories")
        self.db.execute("DROP TABLE IF EXISTS conect")
        self.db.execute("DROP TABLE IF EXISTS recipes")
        self.db.execute('''CREATE TABLE categories
                        (idCat INTEGER PRIMARY KEY,
                        category TEXT NOT NULL,
                        svk TEXT NOT NULL,
                        de TEXT NOT NULL);
                        ''')
        self.db.execute('''CREATE TABLE conect
                        (idCon INTEGER PRIMARY KEY,
                        idCat INT NOT NULL,
                        idRec INT NOT NULL,
                        added DATE);
                        ''')
        self.db.execute('''CREATE TABLE recipes
                        (idRec INTEGER PRIMARY KEY,
                        title VARCHAR(50) NOT NULL,
                        ing TEXT,
                        recipe TEXT NOT NULL,
                        duration INTEGER,
                        portions INTEGER,
                        img TEXT);
                        ''')

    def tables(self):   #naplnenie tabuliek zo suboru
        with open('table/categories.dat', 'rb') as f:
            query = 'INSERT INTO categories (category, svk, de) VALUES '
            query += f.read().decode(encoding='utf-8')
        self.db.execute(query)

        with open('table/connect.dat', 'rb') as f:
            query = 'INSERT INTO conect (idCat, idRec, added) VALUES '
            query += f.read().decode(encoding='utf-8')
        self.db.execute(query)
        
        with open('table/recipes.dat', 'rb') as f:
            query = 'INSERT INTO recipes (title, ing, recipe, duration, portions, img) VALUES '
            query += f.read().decode(encoding='utf-8')
        self.db.execute(query)

    def remove(self, item): #len mazanie receptov, tagy sa nemenia (vymazeme aj connection)
        self.db.execute(f'DELETE FROM recipes WHERE idRec = {item}')
        self.db.execute(f'DELETE FROM conect WHERE idRec = {item}')

    def filter(self, category, duration, portions):
        category = list(category)
        where = ''
        category = list(map(lambda x: '"' + x + '"', category))
        if category == []:
            select = 'SELECT r.idRec, r.title, r.duration, r.portions, r.img'
            frm = 'FROM recipes as r'
            if duration != '':
                if portions != '':
                    where = f'WHERE r.portions >= {portions} AND r.duration <= {duration}'
                else:
                    where = f'WHERE r.duration <= {duration}'
            elif portions != '':
                where = f'WHERE r.portions >= {portions}'
        else:
            select = 'SELECT r.idRec, r.title,r.duration, r.portions, r.img'
            frm = 'FROM categories as c, conect as cn, recipes as r'
            where = 'WHERE c.idCat = cn.idCat AND cn.idRec = r.idRec'
            where += f" AND (c.category = {' OR c.category = '.join(category)})"
            if duration != '':
                if portions != '':
                    where += f' AND r.portions >= {portions} AND r.duration <= {duration}'
                else:
                    where += f' AND r.duration <= {duration}'
            elif portions != '':
                where += f' AND r.portions >= {portions}'

        self.query = select + ' ' + frm + ' ' + where + ' GROUP BY r.idRec ORDER BY r.idRec DESC'
        
        q = self.db.execute(self.query)
        return q.fetchall()

    def filter_again(self):
        q = self.db.execute(self.query)
        return q.fetchall()

    def addRecipe(self, title, prepTime, portions, ing, categories, recipe):
        if ing == '':
            ing = 'NULL'
        else:
            ing = "'" + ing + "'"
        query = f"INSERT INTO recipes (title, ing, recipe, duration, portions) VALUES ('{title}', {ing}, '{recipe}', {prepTime}, {portions});"
        self.db.execute(query)
        # zistime id nasho noveho receptu a podla toho doplnime conect
        id = self.db.execute('SELECT idRec FROM recipes')
        id = id.fetchall()
        id = int(id[-1][0])
        for c in categories:
            e = self.db.execute(f'SELECT idCat from categories WHERE category = "{c}"')
            e = e.fetchall()
            self.db.execute(f'INSERT INTO conect (idCat, idRec, added) VALUES ({e[0][0]}, {id}, DATE("now"))')
    
    def returnRecipe(self, id):
        recipe = self.db.execute(f'SELECT * FROM recipes WHERE idRec = {id}')
        return recipe.fetchall()

    def catSelect(self, idRec):
        cat = self.db.execute(f'SELECT cat.category FROM conect as con, categories as cat WHERE con.idRec = {idRec} AND con.idCat = cat.idCat')
        return cat.fetchall()

    def edit(self, idRec, title, duration, portions, ingred, categories, recipe):
        if ingred == '':
            ingred = 'NULL'
        else:
            ingred = "'" + ingred + "'"
        query = f"UPDATE recipes SET title = '{title}', ing = {ingred}, recipe = '{recipe}', duration = {duration}, portions = {portions} WHERE idRec = {idRec};"
        
        self.db.execute(query)
        self.db.execute(f'DELETE FROM conect WHERE idRec = {idRec}')
        
        for c in categories:
            e = self.db.execute(f'SELECT idCat from categories WHERE category = "{c[:-4]}"')
            e = e.fetchall()
            
            self.db.execute(f'INSERT INTO conect (idCat, idRec, added) VALUES ({e[0][0]}, {idRec}, DATE("now"))')

    def basics(self):
        cat = self.db.execute('SELECT category FROM categories ORDER BY category')
        self.cat = []
        for c in cat:
            self.cat.append(c[0])
    
    def save(self):
        categories = self.db.execute('SELECT category, svk, de FROM categories')
        categories = categories.fetchall()
        with open('table/categories.dat', 'wb') as f:
            c = str(categories[0])
            c = c.replace('None', 'NULL')
            data = str(c)
            categories = categories[1:]
            for c in categories:
                data += ', '
                c = str(c).replace('None', 'NULL')
                data += str(c)
            data += ';\n'
            f.write(data.encode(encoding='utf-8'))

        
        conect = self.db.execute('SELECT idCat, idRec, added FROM conect')
        conect = conect.fetchall()
        with open('table/connect.dat', 'wb') as f:
            c = str(conect[0]).replace('None', 'NULL')
            data = str(c)
            conect = conect[1:]
            for c in conect:
                data += ', '
                c = str(c).replace('None', 'NULL')
                data += str(c)
            data += ';'
            f.write(data.encode())
        
        recipes = self.db.execute('SELECT title, ing, recipe, duration, portions, img FROM recipes')
        recipes = recipes.fetchall()
        with open('table/recipes.dat', 'wb') as f:
            r = str(recipes[0]).replace('None', 'NULL').replace('\\n', '\n')
            data = str(r)
            recipes = recipes[1:]
            for r in recipes:
                data += ', \n'
                r = str(r).replace('None', 'NULL').replace('\\n', '\n')
                data += str(r)
            data += ';'
            f.write(data.encode(encoding='utf-8'))
