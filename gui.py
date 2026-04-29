'''
istxxxxxxx, istxxxxxxx
File responsible of GUI classes of program
Contains: Button, InputDialog, Counter, SelectionWindow
'''

from graphics import *

class Button:
    
    def __init__(self, p1: Point, p2: Point, text_string: str, action=None, shape='rectangle',
                 background_color = 'gray80',
                 outline_color = 'gray20',
                 outline_width = 2,
                 text_color = 'black',
                 text_size = 15):
        self.p1 = p1
        self.p2 = p2
        self.shape = shape
        self.body = None
        self.background_color = background_color
        self.outline_color = outline_color
        self.outline_width = outline_width
        self.text = None
        self.text_color = text_color
        self.text_size = text_size
        self.text_string = text_string
        self.action = action
    
    def draw(self, window: GraphWin):
        if self.shape == 'rectangle':
            self.body = Rectangle(self.p1, self.p2)
        elif self.shape == 'oval':
            self.body = Oval(self.p1, self.p2)
            
        self.body.draw(window)
        self.body.setFill(self.background_color)
        self.body.setOutline(self.outline_color)
        self.body.setWidth(self.outline_width)
        
        self.text = Text(Point((self.p1.x + self.p2.x) / 2, (self.p1.y + self.p2.y) / 2), self.text_string)
        self.text.draw(window)
        self.text.setTextColor(self.text_color)
        self.text.setFace('arial')
        self.text.setSize(self.text_size)
        
        
    def setTextColor(self, color):
        self.text.setTextColor(color)
        self.text_color = color
        
        
    def setBackgroundColor(self, color):
        self.body.setFill(color)
        self.background_color = color

        
    def setAction(self, action):
        self.action = action
        
        
    def getTextString(self):
        return self.text_string
    
    
    def is_clicked(self, pos: Point):
        if pos == None: return False
        if self.shape == 'rectangle':
            
            if min(self.p1.getX(), self.p2.getX()) <= pos.getX() <= max(self.p1.getX(), self.p2.getX()) and \
               min(self.p1.getY(), self.p2.getY()) <= pos.getY() <= max(self.p1.getY(), self.p2.getY()):

                if self.action != None:
                    self.action()
                    
                return True      
            
        elif self.shape == 'oval':
            center = self.body.getCenter()
            a = abs(self.body.getP1().x - self.body.getP2().x) / 2
            b = abs(self.body.getP1().y - self.body.getP2().y) / 2
            
            if ((pos.getX() - center.getX()) ** 2 / a ** 2) + ((pos.getY() - center.getY()) ** 2 / b ** 2) <=1:
                
                if self.action != None:
                    self.action()
                
                return True 
            
        else: return False
        
        
# -----------------------------------------------------------------------------------------------------------------


class InputDialog(GraphWin):
    def __init__(self, width, height, inputs=()):
        self.width = width
        self.height = height
        self.inputs = inputs
        self.entries = []
        self.entries_width = 5
        
        GraphWin.__init__(self, 'Insert values', width, height)
        
        step = self.height / (len(self.inputs) + 2)
        
        for i, inp in enumerate(self.inputs):
           
            text = Text(Point(self.width / 3, (i + 1) * step), f'{inp}: ')
            text.setStyle('bold')
            text.setSize(14)
            text.draw(self)
            
            
            entry = Entry(Point(2 * self.width / 3, (i + 1) * step), self.entries_width)
            entry.setFill('white')
            entry.setText("0") 
            self.entries.append(entry)
            entry.draw(self)
            
        w = self.width / 7
        btn_y = (len(self.entries) + 1) * step
        
        self.btn_quit = Button(Point(self.width / 3 - w, btn_y - 0.5 * w),
                              Point(self.width / 3 + w, btn_y + 0.5 * w), 'QUIT')
        self.btn_quit.draw(self)
        
        
        self.btn_run = Button(Point(2 * self.width / 3 - w, btn_y - 0.5 * w),
                             Point(2 * self.width / 3 + w, btn_y + 0.5 * w), 'RUN',
                             background_color='crimson', text_color='white')
        self.btn_run.draw(self)
        
        
    def getValues(self):
        while self.isOpen():
            mouse = self.checkMouse()
            if mouse != None:
        
                if self.btn_quit.is_clicked(mouse):
                    self.close()
                    return None
                
                if self.btn_run.is_clicked(mouse):
                    
                    data = self.processInput()
                    
                    if data != None and data != []:
                        self.close()
                        return data

    def processInput(self):
        values = []
        
        for entry in self.entries:
            val = entry.getText().replace(',', '.')
            
            try:
                val = float(val)
            except:
                return None
            
            if val >= 0:
                values.append(val)
            
        return values


class Counter:
    
    '''Displays text with number to count varibales such as score and lives'''
    '''Arguments: position, text as string and initial value of variable'''
    
    def __init__(self, pos, text_str, value=0):
        self.pos = pos
        self.text_str = text_str
        self.value = value
        self.text = None
        
    def draw(self, window: GraphWin):
        self.text = Text(self.pos, f'{self.text_str}: {self.value}')
        self.text.setStyle('bold')
        self.text.setFace('arial')
        self.text.setSize(20)
        self.text.draw(window)
        
    def change(self, i=1):
        '''increments and decrements value by i'''
        self.value += i
        self.text.setText(f'{self.text_str}: {self.value}')

# -----------------------------------------------------------------------------------------------------------------        
    

class SelectionWindow(GraphWin):
    def __init__(self, size):
        GraphWin.__init__(self, 'Select', size, 1.15 * size)
        self.size = size
        self.selected = None
        self.selection_buttons = None
        
    def btn_select_action(self, button: Button):
        for btn in self.selection_buttons:
            btn.setTextColor('black')
            
        self.selected = button    
        button.setTextColor('red')
        
        self.update()

    def btn_quit_action(self):
        self.close()
    
    def select(self):
        self.setBackground('white')
        
        size = self.size
        
        btn1 = Button(Point(0.05 * size, 0.05 * size), Point(0.5 * size, 0.5 * size), '1',
                      action=lambda:self.btn_select_action(btn1))
        btn1.draw(self)
        
        
        btn2 = Button(Point(0.5 * size, 0.05 * size), Point(0.95 * size, 0.5 * size), '2',
                      action=lambda:self.btn_select_action(btn2))
        btn2.draw(self)
        
        
        btn3 = Button(Point(0.05 * size, 0.5 * size), Point(0.5 * size, 0.95 * size), '3',
                      action=lambda:self.btn_select_action(btn3))
        btn3.draw(self)
        
        
        btn4 = Button(Point(0.5 * size, 0.5 * size), Point(0.95 * size, 0.95 * size), '4',
                      action=lambda:self.btn_select_action(btn4))
        btn4.draw(self)
        
        
        btn_quit = Button(Point(0.4 * size, size), Point(0.6 * size, 1.1 * size), 'QUIT',
                          action=self.btn_quit_action)
        btn_quit.draw(self)
        
        
        btn_start = Button(Point(0.3 * size , 0.3 * size), Point(0.7 * size, 0.7 * size), 'START',
                           shape='oval',
                           background_color='crimson',
                           text_color='white',
                           text_size=20,)
        
        btn_start.draw(self)
    
        buttons = [btn_start, btn_quit, btn1, btn2, btn3, btn4]
        self.selection_buttons = [btn1, btn2, btn3, btn4]
        
        while self.isOpen():
            mouse = self.checkMouse()
            if mouse != None:
                
                for btn in buttons:
                    if btn.is_clicked(mouse):
                        
                        if btn == btn_start and self.selected != None:
                            self.close()
                            return self.selected.getTextString()
                            
                        break
             