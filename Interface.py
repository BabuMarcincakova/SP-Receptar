import tkinter, functools
from Database import Database
from Hover import Hover
from Click import Click

class Interface:
    def __init__(self):
        self.h = 600
        self.w = 900
        self.root = tkinter.Tk()
        self.root.title('My recipe book')
        self.c = tkinter.Canvas(height= self.h, width= self.w, bg='#ffffff')
        self.c.pack()

        self.hover = Hover(self)
        self.click = Click(self)
        
        self.db = Database()
        self.page = 'homePage'
        self.homePage()
        
        self.c.bind('<MouseWheel>', self.scroll)
    
    def scroll(self, event):
        if self.page == 'homePage':
            if event.x > 177:   #recepty
                if event.delta > 0:
                    self.recNum -= 2
                    if self.recNum < 0:
                        self.recNum = 0
                    self.listRecipes(self.filtered_recipes[self.recNum:self.recNum+4])
                elif self.recNum +4 < len(self.filtered_recipes):
                    self.recNum += 2
                    self.listRecipes(self.filtered_recipes[self.recNum:self.recNum+4])
                if self.recNum == 0:
                    self.c.create_line(246, 91, 835, 91, fill='#dedede', width='3', tags='scroll')
                if self.recNum+4 >= len(self.filtered_recipes):
                    self.c.create_line(246, 585, 835, 585, fill='#dedede', width='3', tags='scroll')
                if self.recNum > 0 and self.recNum+4 < len(self.filtered_recipes):
                    self.c.delete('scroll')
            else:   #kategorie
                if event.delta > 0:
                    self.catNum -= 1
                    if self.catNum < 0:
                        self.catNum = 0
                    self.listCategories(self.db.cat[self.catNum:self.catNum+7])
                elif self.catNum +7 < len(self.db.cat):
                    self.catNum += 1
                    self.listCategories(self.db.cat[self.catNum:self.catNum+7])
                if self.catNum == 0:
                    self.c.create_line(15, 50, 165, 50, fill='#dedede', width='3', tags='scrollCat')
                if self.catNum+7 >= len(self.db.cat):
                    self.c.create_line(15, 340, 165, 340, fill='#dedede', width='3', tags='scrollCat')
                if self.catNum > 0 and self.catNum+7 < len(self.db.cat):
                    self.c.delete('scrollCat')
        if self.page == 'recipePage':   #rozdiel ci scrollujeme ingrediencie alebo text receptu
            if event.y > 90 and event.x <= 200:
                if event.delta > 0:
                    self.ingNum -= 1
                    if self.ingNum < 0:
                        self.ingNum = 0
                    self.list_ingredients(self.listed_ing[self.ingNum:self.ingNum+20])
                elif self.ingNum +20 < len(self.listed_ing):
                    self.ingNum += 1
                    self.list_ingredients(self.listed_ing[self.ingNum:self.ingNum+20])
    
    def shutDown(self, event):
        # ulozia sa tabulky do suborov
        self.db.save()
        exitProgram = exit()
        exitProgram.pack()
    
    def saveOnly(self, event):
        self.db.save()
        self.c.create_text(300, 37, text='Recipes successfully saved', font='Dubai 15', anchor='w', fill='#22B14C', tags='saveInfo')
        self.c.after(1500, self.dele)
    
    def dele(self):
        self.c.delete('saveInfo')

    def homePage(self, recipes=None):
        self.page = 'homePage'
        self.c.delete('all')
        self.c.config(cursor='arrow')
        self.filtered_recipes = []
        self.recNum = 0 #od ktoreho receptu sa zobrazuje
        self.catNum = 0

        self.hpImg = tkinter.PhotoImage(file='bg/hpBg.png')
        self.c.create_image(self.w//2, self.h//2, image=self.hpImg, tag='bg')

        self.c.create_rectangle(15, 15, 165, 45, fill='#e5625e', outline='#e5625e')
        self.c.create_text(90, 30, text='Categories', font='Dubai 15')

        self.c.create_rectangle(15, 355, 165, 385, fill='#FFDD56', outline='#FFDD56')
        self.c.create_text(90, 370, text='Preparation time', font='Dubai 15')
        self.c.create_text(135, 415, text='(min)')

        self.c.create_rectangle(15, 440, 165, 470, fill='#8EA845', outline='#8EA845')
        self.c.create_text(90, 455, text='Portions', font='Dubai 15')

        self.prepTime = tkinter.Entry(self.root, width=10, borderwidth=2)
        self.prepTime.pack()
        self.prepTime.place(x=45, y=405)

        self.portions = tkinter.Entry(self.root, width=10, borderwidth=2)
        self.portions.pack()
        self.portions.place(x=55, y=490)
        
        self.catClick = set()
        self.buttons()

        if recipes is None or recipes == []:
            self.filtered_recipes = self.db.filter([], '', '')
        else:
            self.filtered_recipes = recipes
        self.listRecipes(self.filtered_recipes)
        self.listCategories(self.db.cat[:7])
        self.c.delete('scroll')
        self.c.delete('scrollCat')
        self.c.create_line(246, 91, 835, 91, fill='#dedede', width='3', tags='scroll')
        self.c.create_line(15, 50, 165, 50, fill='#dedede', width='3', tags='scrollCat')

    def listRecipes(self, recipes):  #zobrazenie receptov na homePage
        self.images = []
        for i in range(4):
            self.c.delete(f'recipe{i}')
            self.c.delete(f'recipe{i}Txt')
            self.c.delete(f'recipe{i}Img')
        x, y = 246, 110
        self.current_recipes = []
        for i in range(len(recipes)):
            title = recipes[i][1]
            tag = 'recipe' + str(i)
            if len(title) > 15:
                title = title[:15] + '...'
            if i%2 != 0:
                x += 328
            else:
                x = 246
            if recipes[i][4] is None:
                img = 'none.png'
            else:
                img = recipes[i][4]
            self.images.append(tkinter.PhotoImage(file=f'images/{img}'))
            r = self.c.create_rectangle(x, y, x+260, y+200, fill='#FFF0B6', outline='#FFF0B6', tags=tag)
            self.c.create_text(x+20, y+170, text=title, anchor='w', font='Dubai 15', tags=f'{tag}Txt')
            dur, port = recipes[i][2:4]
            if recipes[i][2] is None:
                dur = '-'
            if recipes[i][3] is None:
                port = '-'
            self.c.create_text(x+240, y+170, text=f'{dur} min\n{port} pt', tags=f'{tag}Txt', anchor='e', font='Dubai 12')
            img = self.c.create_image(x+130, y+75, image=self.images[i], tag=f'{tag}Img')

            recipes[i] += (r,)
            self.current_recipes.append(recipes[i])

            fun1 = functools.partial(self.hover.hoverListedRecipe, tag)
            self.c.tag_bind(tag, "<Enter>", fun1)
            self.c.tag_bind(tag+'Txt', "<Enter>", fun1)
            self.c.tag_bind(tag+'Img', "<Enter>", fun1)

            fun2 = functools.partial(self.hover.unhoverListedRecipe, tag)
            self.c.tag_bind(tag, "<Leave>", fun2)
            self.c.tag_bind(tag+'Txt', "<Leave>", fun2)
            self.c.tag_bind(tag+'Img', "<Leave>", fun2)

            fun3 = functools.partial(self.click.clickRecipe, recipes[i])
            self.c.tag_bind(tag, "<Button-1>", fun3)
            self.c.tag_bind(tag+'Txt', "<Button-1>", fun3)
            self.c.tag_bind(tag+'Img', "<Button-1>", fun3)

            if i%2 != 0:
                y += 258
    
    def listCategories(self, categories):
        x, y = 90, 70
        for c in categories:
            f = '#F0F0F0'
            if c in self.catClick:
                f = '#e5625e'
            e = self.c.create_rectangle(40, y-15, 140, y+15, width='3', outline=f, tags=c, fill='#f0f0f0')
            self.c.create_text(x, y, text=c, tags=c+'Txt', font='Dubai')

            fun1 = functools.partial(self.hover.hoverCat, c)
            self.c.tag_bind(c, "<Enter>", fun1) #nemusim samostatne opodmienkovavat
            self.c.tag_bind(c+'Txt', "<Enter>", fun1)

            fun2 = functools.partial(self.hover.unhoverCat, c)
            self.c.tag_bind(c, "<Leave>", fun2)
            self.c.tag_bind(c+'Txt', "<Leave>", fun2)

            fun3 = functools.partial(self.click.clickCat, c)
            self.c.tag_bind(c, "<Button-1>", fun3)
            self.c.tag_bind(c+'Txt', "<Button-1>", fun3)
            y += 40

    def buttons(self):  #tlacidla na homePage
        #filter
        self.filter = self.c.create_rectangle(30, self.h-45, 150, self.h-15, fill='#99BED0', outline='#99BED0', tags='filter')
        self.c.create_text(90, self.h-30, text='Filter', font='Dubai 15', tags='filterTxt')

        self.c.tag_bind('filter', "<Enter>", self.hover.hoverFilter)
        self.c.tag_bind('filterTxt', "<Enter>", self.hover.hoverFilter)
        self.c.tag_bind('filter', "<Leave>", self.hover.unhoverFilter)
        self.c.tag_bind('filterTxt', "<Leave>", self.hover.unhoverFilter)
        self.c.tag_bind('filter', "<Button-1>", self.click.filterHP)
        self.c.tag_bind('filterTxt', "<Button-1>", self.click.filterHP)

        #add
        self.addImg = [tkinter.PhotoImage(file='bg/add.png'),tkinter.PhotoImage(file='bg/addH.png')]
        self.addBtn = self.c.create_image(216, 30, image=self.addImg[0])
        self.c.create_text(216, 58, text='Add', font='Dubai 15')

        self.c.tag_bind(self.addBtn, "<Enter>", self.hover.hoverAddPage)
        self.c.tag_bind(self.addBtn, "<Leave>", self.hover.unhoverAddPage)
        self.c.tag_bind(self.addBtn, "<Button-1>", self.click.clickAddPage)

        #shut down  #osobitne save a osobitne save&quit
        self.shutDownBtn = self.c.create_rectangle(self.w-101, 21, self.w-11, 53, fill='#e5625e', outline='#e5625e', tags='shutDown')
        self.c.create_text(self.w-56, 37, text='Save & Quit', font='Dubai', tags='shutDownTxt')

        self.c.tag_bind('shutDown', "<Enter>", self.hover.hoverQuit)
        self.c.tag_bind('shutDownTxt', "<Enter>", self.hover.hoverQuit)
        self.c.tag_bind('shutDown', "<Leave>", self.hover.unhoverQuit)
        self.c.tag_bind('shutDownTxt', "<Leave>", self.hover.unhoverQuit)
        self.c.tag_bind('shutDown', "<Button-1>", self.shutDown)
        self.c.tag_bind('shutDownTxt', "<Button-1>", self.shutDown)

        self.saveBtn = self.c.create_rectangle(self.w-207, 21, self.w-116, 53, fill='#e5625e', outline='#e5625e', tags='saveBtn')
        self.c.create_text(self.w-161, 37, text='Save', font='Dubai', tags='saveBtnTxt')

        self.c.tag_bind('saveBtn', "<Enter>", self.hover.hoverSave)
        self.c.tag_bind('saveBtnTxt', "<Enter>", self.hover.hoverSave)
        self.c.tag_bind('saveBtn', "<Leave>", self.hover.unhoverSave)
        self.c.tag_bind('saveBtnTxt', "<Leave>", self.hover.unhoverSave)
        self.c.tag_bind('saveBtn', "<Button-1>", self.saveOnly)
        self.c.tag_bind('saveBtnTxt', "<Button-1>", self.saveOnly)

    #PAGE pridavanie receptov
    def addRecipe(self):
        self.page = 'addRecipe'
        self.c.delete('all')
        self.prepTime.destroy()
        self.portions.destroy()
        self.addCatClick = ()

        self.arImg = tkinter.PhotoImage(file='bg/arBg.png')
        self.c.create_image(self.w//2, self.h//2, image=self.arImg, tag='bg')

        self.add = self.c.create_rectangle(self.w-135, 15, self.w-35, 45, fill='#99BED0', outline='#99BED0', tags='addAdd')
        self.c.create_text(self.w-85, 30, text='Add', font='Dubai', tags='addAddTxt')
        self.c.tag_bind('addAdd', "<Enter>", self.hover.hoverAdd)
        self.c.tag_bind('addAddTxt', "<Enter>", self.hover.hoverAdd)
        self.c.tag_bind('addAdd', "<Leave>", self.hover.unhoverAdd)
        self.c.tag_bind('addAddTxt', "<Leave>", self.hover.unhoverAdd)
        self.c.tag_bind('addAdd', "<Button-1>", self.click.clickAdd)
        self.c.tag_bind('addAddTxt', "<Button-1>", self.click.clickAdd)

        self.cancel = self.c.create_rectangle(self.w-135, 55, self.w-35, 85, fill='#e5625e', outline='#e5625e', tags='addCancel')
        self.c.create_text(self.w-85, 70, text='Cancel', font='Dubai', tags='addCancelTxt')
        self.c.tag_bind('addCancel', "<Enter>", self.hover.hoverCancel)
        self.c.tag_bind('addCancelTxt', "<Enter>", self.hover.hoverCancel)
        self.c.tag_bind('addCancel', "<Leave>", self.hover.unhoverCancel)
        self.c.tag_bind('addCancelTxt', "<Leave>", self.hover.unhoverCancel)
        self.c.tag_bind('addCancel', "<Button-1>", self.click.clickCancel)
        self.c.tag_bind('addCancelTxt', "<Button-1>", self.click.clickCancel)

        self.c.create_text(180, 50, text="Note:\nFor a correct listing, please separate\nthe individual ingredients with a single comma ','", font='Dubai 11', fill='#5e5e5e')

        self.c.create_text(58, 132, text='Title', font='Dubai')
        self.c.create_text(118, 172, text='Preparation time (min)', font='Dubai')
        self.c.create_text(335, 172, text='Portions', font='Dubai')
        self.c.create_text(self.w-85, 132, text='Categories', font='Dubai')
        self.c.create_text(80, 212, text='Ingredients', font='Dubai')
        self.c.create_text(68, 305, text='Recipe', font='Dubai')

        y = 172
        self.addCat = set()
        for c in self.db.cat:
            self.c.create_text(self.w-85, y, text=c, font='Dubai', fill='#5e5e5e', tags=c+'Txt')
            r = self.c.create_rectangle(self.w-135, y-15, self.w-35, y+15, width='1', fill= '', outline='#ffffff', tags=c)
            fun1 = functools.partial(self.hover.hoverAddCat, c)
            self.c.tag_bind(c, "<Enter>", fun1)
            self.c.tag_bind(c+'Txt', "<Enter>", fun1)

            fun2 = functools.partial(self.hover.unhoverAddCat, c)
            self.c.tag_bind(c, "<Leave>", fun2)
            self.c.tag_bind(c+'Txt', "<Leave>", fun2)

            fun3 = functools.partial(self.click.clickAddCat, c)
            self.c.tag_bind(c, "<Button-1>", fun3)
            self.c.tag_bind(c+'Txt', "<Button-1>", fun3)
            y += 40

        self.title = tkinter.Entry(self.root, width=40, borderwidth=2, font='Dubai 10')
        self.title.pack()
        self.title.place(x=130, y=120)

        self.prepTimeA = tkinter.Entry(self.root, width=10, borderwidth=2, font='Dubai 10')
        self.prepTimeA.pack()
        self.prepTimeA.place(x=210, y=160)

        self.portionsA = tkinter.Entry(self.root, width=10, borderwidth=2, font='Dubai 10')
        self.portionsA.pack()
        self.portionsA.place(x=370, y=160)

        self.ingred = tkinter.Text(self.root, width=80, height=3, borderwidth=2, font='Dubai 10')
        self.ingred.pack()
        self.ingred.place(x=130, y=200)

        self.recipe = tkinter.Text(self.root, width=80, height=9, borderwidth=2, font='Dubai 10')
        self.recipe.pack()
        self.recipe.place(x=130, y=295)
    
    def addError(self, title, prepT, portA, recipe):
        y = self.h-80
        er = 1
        if len(title) >= 50:
            self.c.create_text(self.w//2, y, text='Recipe title is too long.', tags=f'err{er}', font='Dubai', fill='red')
            er += 1
            y += 20
        if len(title) == 0:
            self.c.create_text(self.w//2, y, text='Recipe title cannot be empty.', tags=f'err{er}', font='Dubai', fill='red')
            er += 1
            y += 20
        if prepT.isdigit() == False and prepT != '':
            self.c.create_text(self.w//2, y, text="'Preparation time' must be an integer.", tags=f'err{er}', font='Dubai', fill='red')
            er += 1
            y += 20
        if portA.isdigit() == False and portA != '':
            self.c.create_text(self.w//2, y, text="'Portions' must be an integer.", tags=f'err{er}', font='Dubai', fill='red')
            er += 1
            y += 20
        if recipe == '' or recipe.replace('\n',' ').strip() == '':
            self.c.create_text(self.w//2, y, text="Recipe cannot be empty.", tags=f'err{er}', font='Dubai', fill='red')
            er += 1
            y += 20
        
        return er

    #PAGE zobrazenia vybrateho receptu
    def recipePage(self, recipe):   #vypisanie samotneho receptu
        self.page = 'recipePage'
        self.c.delete('all')
        self.c.config(cursor='arrow')
        self.prepTime.destroy()
        self.portions.destroy()
        self.addCat = set()

        self.hpImg = tkinter.PhotoImage(file='bg/lstBg.png')
        self.c.create_image(self.w//2, self.h//2, image=self.hpImg, tag='bg')

        self.backImg = [tkinter.PhotoImage(file='bg/back.png'),tkinter.PhotoImage(file='bg/backH.png')]
        self.backBtn = self.c.create_image(50, 50, image=self.backImg[0])

        self.c.tag_bind(self.backBtn, "<Enter>", self.hover.hoverBack)
        self.c.tag_bind(self.backBtn, "<Leave>", self.hover.unhoverBack)
        self.c.tag_bind(self.backBtn, "<Button-1>", self.click.clickBack)

        self.c.create_rectangle(self.w-135, 15, self.w-35, 45, fill='#99BED0', outline='#99BED0', tags='editRecipe')
        self.c.create_text(self.w-85, 30, text='Edit', font='Dubai', tags='editRecipeTxt')
        self.c.tag_bind('editRecipe', "<Enter>", self.hover.hoverAdd)
        self.c.tag_bind('editRecipeTxt', "<Enter>", self.hover.hoverAdd)
        self.c.tag_bind('editRecipe', "<Leave>", self.hover.unhoverAdd)
        self.c.tag_bind('editRecipeTxt', "<Leave>", self.hover.unhoverAdd)
        self.c.tag_bind('editRecipe', "<Button-1>", self.click.clickAdd)
        self.c.tag_bind('editRecipeTxt', "<Button-1>", self.click.clickAdd)

        self.c.create_rectangle(self.w-135, 55, self.w-35, 85, fill='#e5625e', outline='#e5625e', tags='deleteRecipe')
        self.c.create_text(self.w-85, 70, text='Delete', font='Dubai', tags='deleteRecipeTxt')
        self.c.tag_bind('deleteRecipe', "<Enter>", self.hover.hoverCancel)
        self.c.tag_bind('deleteRecipeTxt', "<Enter>", self.hover.hoverCancel)
        self.c.tag_bind('deleteRecipe', "<Leave>", self.hover.unhoverCancel)
        self.c.tag_bind('deleteRecipeTxt', "<Leave>", self.hover.unhoverCancel)
        self.c.tag_bind('deleteRecipe', "<Button-1>", self.click.clickCancel)
        self.c.tag_bind('deleteRecipeTxt', "<Button-1>", self.click.clickCancel)

        self.c.create_text(140, 123, text='Ingredients', font='Dubai 15')

        self.forEdit = self.db.returnRecipe(recipe)[0]
        self.idRec, title, ingredients, recipe, duration, portions, img = self.db.returnRecipe(recipe)[0]
        self.c.create_text(90, 50, text=title, font='Dubai 25', anchor='w')
        if duration is None:
            duration = '-'
        if portions is None:
            portions = '-'
        self.c.create_text(290, 123, text=f'Preparation time: {duration} min', font='Dubai 15', anchor='w')
        self.c.create_text(630, 123, text=f'Portions: {portions}', font='Dubai 15', anchor='w')
        self.c.create_text(290, 165, text=f'Recipe:', font='Dubai 15', anchor='w')
        
        if ingredients is not None:
            self.listed_ing = ingredients.split(',')    #uprava ingrdiencii
            self.ingNum = 0
            i = 0
            width = 30
            while i < len(self.listed_ing): #aby netrcali z riadku
                if self.listed_ing[i] == '':
                    self.listed_ing.pop(i)
                else:
                    self.listed_ing[i] = '+ ' + self.listed_ing[i].strip()
                    if len(self.listed_ing[i]) > width:
                        ing = self.listed_ing[i]
                        self.listed_ing[i] = self.listed_ing[i][:width]
                        ing = ing[width:]
                        if ing != '':
                            if self.listed_ing[i][-1] != ' ' and ing[0] != ' ':
                                self.listed_ing[i] += '-'
                            while len(ing) > width:
                                if self.listed_ing[i][-1] != ' ' and ing[width] != ' ':
                                    self.listed_ing.insert(i+1, ing[:width])
                                else:
                                    self.listed_ing.insert(i+1, ing[:width]+'-')
                                ing = ing[width:]
                                i += 1
                            self.listed_ing.insert(i+1, ing)
                        i += 1
                    i += 1
            self.list_ingredients(self.listed_ing[:20])

        self.recipe = tkinter.Text(self.root, width=85, height=18, borderwidth=2, font='Dubai 10', pady = 10, padx = 15)
        self.recipe.pack()
        self.recipe.place(x=280, y=185)
        self.recipe.insert('1.0', recipe)

        self.recipe.config(state='disabled')

    def list_ingredients(self, ing):
        for i in range(20):
            self.c.delete(f'ing{i}')
        x, y = 20, 160
        for i in range(len(ing)):
            self.c.create_text(x, y, text=ing[i], anchor='w', font='Dubai', tags=f'ing{i}')
            y += 20
    
    def editPage(self):
        self.page = 'editPage'
        self.c.delete('all')
        self.c.config(cursor='arrow')

        self.edImg = tkinter.PhotoImage(file='bg/arBg.png')
        self.c.create_image(self.w//2, self.h//2, image=self.edImg, tag='bg')

        self.add = self.c.create_rectangle(self.w-135, 15, self.w-35, 45, fill='#99BED0', outline='#99BED0', tags='editEdit')
        self.c.create_text(self.w-85, 30, text='Save', font='Dubai', tags='editEditTxt')
        self.c.tag_bind('editEdit', "<Enter>", self.hover.hoverAdd)
        self.c.tag_bind('editEditTxt', "<Enter>", self.hover.hoverAdd)
        self.c.tag_bind('editEdit', "<Leave>", self.hover.unhoverAdd)
        self.c.tag_bind('editEditTxt', "<Leave>", self.hover.unhoverAdd)
        self.c.tag_bind('editEdit', "<Button-1>", self.click.clickAdd)
        self.c.tag_bind('editEditTxt', "<Button-1>", self.click.clickAdd)

        self.cancel = self.c.create_rectangle(self.w-135, 55, self.w-35, 85, fill='#e5625e', outline='#e5625e', tags='editCancel')
        self.c.create_text(self.w-85, 70, text='Cancel', font='Dubai', tags='editCancelTxt')
        self.c.tag_bind('editCancel', "<Enter>", self.hover.hoverCancel)
        self.c.tag_bind('editCancelTxt', "<Enter>", self.hover.hoverCancel)
        self.c.tag_bind('editCancel', "<Leave>", self.hover.unhoverCancel)
        self.c.tag_bind('editCancelTxt', "<Leave>", self.hover.unhoverCancel)
        self.c.tag_bind('editCancel', "<Button-1>", self.click.clickCancel)
        self.c.tag_bind('editCancelTxt', "<Button-1>", self.click.clickCancel)

        self.c.create_text(180, 50, text="Note:\nFor a correct listing, please separate\nthe individual ingredients with a single comma ','", font='Dubai 11', fill='#5e5e5e')

        self.c.create_text(58, 132, text='Title', font='Dubai')
        self.c.create_text(118, 172, text='Preparation time (min)', font='Dubai')
        self.c.create_text(335, 172, text='Portions', font='Dubai')
        self.c.create_text(self.w-85, 132, text='Categories', font='Dubai')
        self.c.create_text(80, 212, text='Ingredients', font='Dubai')
        self.c.create_text(68, 305, text='Recipe', font='Dubai')

        unedited_cat = self.db.catSelect(self.forEdit[0])
        y = 172
        self.addCat = set()
        for c in self.db.cat:
            fl, fd, w = '#ffffff', '#5e5e5e', '1'
            if (c,) in unedited_cat:
                fl, fd, w = '#99BED0', '#000000', '3'
                self.addCat.add(c+'Edit')
            self.c.create_text(self.w-85, y, text=c, font='Dubai', fill=fd, tags=c+'EditTxt')
            r = self.c.create_rectangle(self.w-135, y-15, self.w-35, y+15, fill= '', outline=fl, width=w, tags=c+'Edit')
            fun1 = functools.partial(self.hover.hoverAddCat, c+'Edit')
            self.c.tag_bind(c+'Edit', "<Enter>", fun1)
            self.c.tag_bind(c+'EditTxt', "<Enter>", fun1)

            fun2 = functools.partial(self.hover.unhoverAddCat, c+'Edit')
            self.c.tag_bind(c+'Edit', "<Leave>", fun2)
            self.c.tag_bind(c+'EditTxt', "<Leave>", fun2)

            fun3 = functools.partial(self.click.clickAddCat, c+'Edit')
            self.c.tag_bind(c+'Edit', "<Button-1>", fun3)
            self.c.tag_bind(c+'EditTxt', "<Button-1>", fun3)
            y += 40
        
        self.title = tkinter.Entry(self.root, width=40, borderwidth=2, font='Dubai 10')
        self.title.pack()
        self.title.place(x=130, y=120)
        self.title.insert(0, self.forEdit[1])

        self.prepTimeA = tkinter.Entry(self.root, width=10, borderwidth=2, font='Dubai 10')
        self.prepTimeA.pack()
        self.prepTimeA.place(x=210, y=160)
        if self.forEdit[4] is not None:
            self.prepTimeA.insert(0, self.forEdit[4])

        self.portionsA = tkinter.Entry(self.root, width=10, borderwidth=2, font='Dubai 10')
        self.portionsA.pack()
        self.portionsA.place(x=370, y=160)
        if self.forEdit[5] is not None:
            self.portionsA.insert(0, self.forEdit[5])

        self.ingred = tkinter.Text(self.root, width=80, height=3, borderwidth=2, font='Dubai 10')
        self.ingred.pack()
        self.ingred.place(x=130, y=200)
        if self.forEdit[2] is not None:
            self.ingred.insert(1.0, self.forEdit[2])

        self.recipe = tkinter.Text(self.root, width=80, height=9, borderwidth=2, font='Dubai 10')
        self.recipe.pack()
        self.recipe.place(x=130, y=295)
        self.recipe.insert(1.0, self.forEdit[3])
