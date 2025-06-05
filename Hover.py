class Hover:
    def __init__(self, interface):
        self.inf = interface
        
    def hoverCat(self, tag: str, event):   #navstivenie tlacidla kategorie
        self.inf.c.itemconfig(tag, outline='#e5625e')
        self.inf.c.config(cursor='hand2')
    
    def unhoverCat(self, tag: str, event):   #odidenie z tlacidla kategorie
        if tag not in self.inf.catClick:
            self.inf.c.itemconfig(tag, outline='#f0f0f0')
            self.inf.c.config(cursor='arrow')
    
    def hoverFilter(self, event):
        self.inf.c.itemconfig('filter', fill='#337ca0', outline='#337ca0')
        self.inf.c.config(cursor='hand2')
    
    def unhoverFilter(self, event):
        self.inf.c.itemconfig('filter', fill='#99BED0', outline='#99BED0')
        self.inf.c.config(cursor='arrow')
    
    def hoverAddPage(self, event):
        self.inf.c.itemconfig(self.inf.addBtn, image=self.inf.addImg[1])
        self.inf.c.config(cursor='hand2')
    
    def unhoverAddPage(self, event):
        self.inf.c.itemconfig(self.inf.addBtn, image=self.inf.addImg[0])
        self.inf.c.config(cursor='arrow')
    
    def hoverBack(self, event):
        self.inf.c.itemconfig(self.inf.backBtn, image=self.inf.backImg[1])
        self.inf.c.config(cursor='hand2')
    
    def unhoverBack(self, event):
        self.inf.c.itemconfig(self.inf.backBtn, image=self.inf.backImg[0])
        self.inf.c.config(cursor='arrow')
    
    def hoverAdd(self, event):
        if self.inf.page == 'addRecipe':
            tag = self.inf.add
        elif self.inf.page == 'recipePage':
            tag = 'editRecipe'
        elif self.inf.page == 'editPage':
            tag = 'editEdit'
        self.inf.c.itemconfig(tag, fill='#337ca0', outline='#337ca0')
        self.inf.c.config(cursor='hand2')
    
    def unhoverAdd(self, event):
        if self.inf.page == 'addRecipe':
            tag = self.inf.add
        elif self.inf.page == 'recipePage':
            tag = 'editRecipe'
        elif self.inf.page == 'editPage':
            tag = 'editEdit'
        self.inf.c.itemconfig(tag, fill='#99BED0', outline='#99BED0')
        self.inf.c.config(cursor='arrow')
    
    def hoverCancel(self, event):
        if self.inf.page == 'addRecipe':
            tag = self.inf.cancel
        elif self.inf.page == 'recipePage':
            tag = 'deleteRecipe'
        elif self.inf.page == 'editPage':
            tag = 'editCancel'
        self.inf.c.itemconfig(tag, fill='#9E4441', outline='#9E4441')
        self.inf.c.config(cursor='hand2')
    
    def unhoverCancel(self, event):
        if self.inf.page == 'addRecipe':
            tag = self.inf.cancel
        elif self.inf.page == 'recipePage':
            tag = 'deleteRecipe'
        elif self.inf.page == 'editPage':
            tag = 'editCancel'
        self.inf.c.itemconfig(tag, fill='#e5625e', outline='#e5625e')
        self.inf.c.config(cursor='arrow')
    
    def hoverQuit(self, event):
        self.inf.c.itemconfig(self.inf.shutDownBtn, fill='#9E4441', outline='#9E4441')
        self.inf.c.config(cursor='hand2')
    
    def unhoverQuit(self, event):
        self.inf.c.itemconfig(self.inf.shutDownBtn, fill='#e5625e', outline='#e5625e')
        self.inf.c.config(cursor='arrow')
    
    def hoverSave(self, event):
        self.inf.c.itemconfig(self.inf.saveBtn, fill='#9E4441', outline='#9E4441')
        self.inf.c.config(cursor='hand2')
    
    def unhoverSave(self, event):
        self.inf.c.itemconfig(self.inf.saveBtn, fill='#e5625e', outline='#e5625e')
        self.inf.c.config(cursor='arrow')
    
    def hoverAddCat(self, tag: str, event):
        self.inf.c.itemconfig(tag, outline='#99BED0', width='3')
        self.inf.c.itemconfig(tag+'Txt', fill='#000000')
        self.inf.c.config(cursor='hand2')

    def unhoverAddCat(self, tag: str, event):
        if tag not in self.inf.addCat:
            self.inf.c.itemconfig(tag, outline='#ffffff', width='1')
            self.inf.c.itemconfig(tag+'Txt', fill='#5e5e5e')
            self.inf.c.config(cursor='arrow')
    
    def hoverListedRecipe(self, tag: str, event):
        self.inf.c.itemconfig(tag, outline='#8EA845', width='3')
        self.inf.c.itemconfig(tag+'Txt', fill='#8EA845')
        self.inf.c.config(cursor='hand2')
    
    def unhoverListedRecipe(self, tag: str, event):
        self.inf.c.itemconfig(tag, outline='')
        self.inf.c.itemconfig(tag+'Txt', fill='#000000')
        self.inf.c.config(cursor='arrow')
