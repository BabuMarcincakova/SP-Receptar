import tkinter

class Click:
    def __init__(self, interface):
        self.inf = interface
        
    def clickCat(self, tag: str, event):   #kliknutie na tlacidlo kategorie
        if tag in self.inf.catClick:
            self.inf.catClick.remove(tag)
            self.inf.c.itemconfig(tag, outline='#f0f0f0')
        else:
            self.inf.c.itemconfig(tag, outline='#e5625e')
            self.inf.catClick.add(tag)
    
    def clickAddPage(self, event):   #kliknutie na tlacidlo add
        self.inf.c.config(cursor='arrow')
        self.inf.addRecipe()
    
    def clickBack(self, event):
        self.inf.c.config(cursor='arrow')
        self.inf.recipe.destroy()
        self.inf.homePage()
    
    def clickAdd(self, event):  #osetrenie a pridanie receptu
        if self.inf.page == 'recipePage':
            self.inf.recipe.destroy()
            self.inf.editPage()
            return
        self.inf.c.delete('added')
        for i in range(5):
            self.inf.c.delete(f'err{i}')
        title = self.inf.title.get()
        title = title.replace("'", '"').replace('\n',' ').replace('None', 'none').strip()

        prepT = self.inf.prepTimeA.get()
        portA = self.inf.portionsA.get()

        recipe = self.inf.recipe.get('1.0', tkinter.END)
        recipe = recipe.replace("'", '"').replace('None', 'none')

        ingred = self.inf.ingred.get('1.0', tkinter.END)
        ingred = ingred.replace("'", '"').replace('\n', ' ').replace('None', 'none').strip()

        er = self.inf.addError(title, prepT, portA, recipe)

        if er == 1:
            if prepT == '':
                prepT = 'NULL'
            if portA == '':
                portA = 'NULL'

            if self.inf.page == 'addRecipe':
                self.inf.db.addRecipe(title, prepT, portA, ingred, self.inf.addCat, recipe)
            elif self.inf.page == 'editPage':
                self.inf.db.edit(self.inf.forEdit[0], title, prepT, portA, ingred, self.inf.addCat, recipe)
                self.inf.db.save()
            
            for i in range(er):
                self.inf.c.delete(f'err{i}')

            if self.inf.page == 'addRecipe':
                self.inf.c.create_text(self.inf.w//2, self.inf.h-65, text='Recipe added', fill='green', font='Dubai', tags='added')
                self.inf.title.delete(0, "end")
                self.inf.prepTimeA.delete(0, "end")
                self.inf.portionsA.delete(0, "end")
                self.inf.ingred.delete('1.0', tkinter.END)
                self.inf.recipe.delete('1.0', tkinter.END)
                for a in self.inf.addCat:
                    self.inf.c.itemconfig(a, outline='#ffffff')
                    self.inf.c.itemconfig(a+'Txt', fill='#5e5e5e')
                
                self.inf.addCat = set()
            elif self.inf.page == 'editPage':
                self.inf.c.create_text(self.inf.w//2, self.inf.h-65, text='Edit saved', fill='green', font='Dubai', tags='edited')

    def clickCancel(self, event):
        if self.inf.page == 'addRecipe':
            self.inf.c.delete('added')
            self.inf.title.destroy()
            self.inf.prepTimeA.destroy()
            self.inf.portionsA.destroy()
            self.inf.ingred.destroy()
            self.inf.recipe.destroy()
            self.inf.c.config(cursor='arrow')
            self.inf.homePage(self.inf.db.filter_again())
        elif self.inf.page == 'recipePage': #vymazanie receptu
            self.inf.db.remove(self.inf.idRec)
            self.inf.c.config(cursor='arrow')
            self.inf.recipe.destroy()
            for i in range(len(self.inf.filtered_recipes)):
                if self.inf.filtered_recipes[i][0] == self.inf.idRec:
                    self.inf.filtered_recipes.pop(i)
                    break 
            self.inf.homePage(self.inf.db.filter_again())
        elif self.inf.page == 'editPage':
            self.inf.c.delete('added')
            self.inf.title.destroy()
            self.inf.prepTimeA.destroy()
            self.inf.portionsA.destroy()
            self.inf.ingred.destroy()
            self.inf.recipe.destroy()
            self.inf.c.config(cursor='arrow')
            self.inf.recipePage(self.inf.idRec)
    
    def clickAddCat(self, tag: str, event): #vybrati category pri pridavani receptu
        if tag in self.inf.addCat:
            self.inf.addCat.remove(tag)
            self.inf.c.itemconfig(tag, outline='')
            self.inf.c.itemconfig(tag+'Txt', fill='#5e5e5e')
        else:
            self.inf.addCat.add(tag)
            self.inf.c.itemconfig(tag, outline='#99BED0', width='3')
            self.inf.c.itemconfig(tag+'Txt', fill='#000000')
    
    def clickRecipe(self, recipe, event):   #vybratie konkretneho receptu z homePage
        self.inf.recipePage(recipe[0])
    
    def filterHP(self, event):   #kliknutie na tlacidlo filter
        self.inf.listCategories(self.inf.db.cat[:7])
        self.inf.c.delete('scrollCat')
        self.inf.c.create_line(15, 50, 165, 50, fill='#dedede', width='3', tags='scrollCat')
        prep = self.inf.prepTime.get().strip()
        port = self.inf.portions.get().strip()
        if (prep.isdecimal() and port.isdecimal()) or (prep == '' and port.isdecimal()) or (port == '' and prep.isdecimal()) or (prep == '' and port == ''):
            self.inf.c.delete('errorMess')

            self.inf.filtered_recipes = self.inf.db.filter(self.inf.catClick, prep, port)
            if len(self.inf.filtered_recipes) == 0:
                self.inf.c.delete('errorMess')
                self.inf.error = self.inf.c.create_text(90, self.inf.h-65, text='No recipes found', fill='red', font='Dubai', tags='errorMess')
                self.inf.filtered_recipes = self.inf.db.filter([], '', '')
                self.inf.listRecipes(self.inf.filtered_recipes)
                self.inf.c.delete('scroll')
                self.inf.c.create_line(246, 91, 835, 91, fill='#dedede', width='3', tags='scroll')
            else:
                self.inf.listRecipes(self.inf.filtered_recipes)
                self.inf.c.delete('scroll')
                self.inf.c.create_line(246, 91, 835, 91, fill='#dedede', width='3', tags='scroll')

            for tag in self.inf.catClick:
                self.inf.c.itemconfig(tag, outline='#f0f0f0')

            self.inf.catClick = set()
            self.inf.prepTime.delete(0, "end")
            self.inf.portions.delete(0, "end")
        else:
            self.inf.c.delete('errorMess')
            self.inf.error = self.inf.c.create_text(90, self.inf.h-65, text='Input should be an integer', fill='red', font='Dubai', tags='errorMess')
    
