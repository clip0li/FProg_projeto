'''
ist1118311, Oleksandr Pryshchepa e ist1118307, Eduardo Chinita
File responsible of GUI related classes
'''

from graphics import *
import numpy as np

COLOR_BUTTON_FILL = 'gray80'
COLOR_BUTTON_OUTLINE = 'black'
COLOR_BUTTON_ACCENT = 'crimson'
COLOR_STICKMAN = 'orange'

WIDTH_STICKMAN = 5 
WIDTH_BUTTON = 2


class Button:
    '''Creates and draws buttons of two shapes: rectangle and oval. Has various visual parameters that can be changed
    
    Attributes:
        p1(Point): first point thar defines rectangle or rectangle with an oval inscribed in it
        p2(Point): second point thar defines rectangle or rectangle with an oval inscribed in it
        text_string(str): text that will be displayed inside of button
        action(fucntion): function that is executed when button is pressed
        shape(str): shape of button: rectangle or oval
        background_color(str): color of background 
        outline_color(str): color of outline 
        outline_width(float): line width of outline 
        text_color(str): color of text
        text_size(float): text size. Possible values are [5 36] according to graphics.py
    '''
    
    def __init__(self, p1: Point, p2: Point, text_string: str, action=None, shape='rectangle',
                 background_color = COLOR_BUTTON_FILL,
                 outline_color = COLOR_BUTTON_OUTLINE,
                 outline_width = WIDTH_BUTTON,
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
        
    def undraw(self, window: GraphWin):
        self.body.undraw()
        self.text.undraw()
        
    def setTextColor(self, color):
        self.text.setTextColor(color)
        self.text_color = color
        
    def setTextSize(self, size):
        self.text.setSize(size)
        self.text_size = size
    
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
    
        
# ------------------------------------------------------------------------------------------------------------------------


class Stickman:
    '''Draws a stickman
    
    Attributes:
        pos(Point): position of stickman placed at the bottom between the legs
        height(float): height of stickman. Adjusts other parts of body
    '''
    
    def __init__(self, pos: Point, height):
        self.pos = pos
        self.height = height
        
    def draw(self, window: GraphWin):
        x = self.pos.getX()
        y = self.pos.getY()
        
        h = self.height
        
        head = Circle(Point(x, y + h * 0.85), h * 0.15)
        head.setWidth(WIDTH_STICKMAN)
        head.setOutline(COLOR_STICKMAN)
        head.draw(window)
        
        body = Line(Point(x, y + h * 0.4), Point(x, y + h * 0.7))
        body.setWidth(WIDTH_STICKMAN)
        body.setFill(COLOR_STICKMAN)
        body.setOutline(COLOR_STICKMAN)
        body.draw(window)
        
        left_leg = Line(Point(x, y + h * 0.4), Point(x - 0.2, y))
        left_leg.setWidth(WIDTH_STICKMAN)
        left_leg.setFill(COLOR_STICKMAN)
        left_leg.setOutline(COLOR_STICKMAN)
        left_leg.draw(window)
        
        right_leg = Line(Point(x, y + h * 0.4), Point(x + 0.2, y))
        right_leg.setWidth(WIDTH_STICKMAN)
        right_leg.setFill(COLOR_STICKMAN)
        right_leg.setOutline(COLOR_STICKMAN)
        right_leg.draw(window)
        
        left_arm = Line(Point(x, y + h * 0.7), Point(x - 0.4, y + h * 0.4))
        left_arm.setWidth(WIDTH_STICKMAN)
        left_arm.setFill(COLOR_STICKMAN)
        left_arm.setOutline(COLOR_STICKMAN)
        left_arm.draw(window)
        
        right_arm = Line(Point(x, y + h * 0.7), Point(x + 0.4, y + h * 0.4))
        right_arm.setWidth(WIDTH_STICKMAN)
        right_arm.setFill(COLOR_STICKMAN)
        right_arm.setOutline(COLOR_STICKMAN)
        right_arm.draw(window)
        

# ------------------------------------------------------------------------------------------------------------------------


class InputDialog(GraphWin):
    ''' Opens a window to get values from user. Has adjustable number of entries and error protection
    
    Attributes:
        width(int): width of window
        height(int): height of window
        inputs(list(Name: str, min: int, max: int)): list of inputs. Each input is list that contains name and minimum and maximum value
        entries(list(Entry)): list of entries objects from graphics.py
        self.entries_width(int): width of entry box
    '''
    
    def __init__(self, width: int, height: int, inputs=()):
        self.width = width
        self.height = height
        self.inputs = inputs
        self.entries = []
        self.entries_width = 5
        
        super().__init__('Insert values', width, height)

        step = self.height / (len(self.inputs) + 2)
        
        for i, input in enumerate(self.inputs):
            text = Text(Point(self.width / 3, (i + 1) * step), f'{input[0]}: ')
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
                             background_color=COLOR_BUTTON_ACCENT, text_color='white')
        self.btn_run.draw(self)
    
    def getValues(self):
        '''
        Gets values from each entry box
        
        Returns:
            List of values of variables in order which were initialized. If values are invalid return None
        '''
        
        while self.isOpen():
            mouse = self.checkMouse()
            if mouse != None:
                if self.btn_quit.is_clicked(mouse):
                    self.close()
                    return 
                
                if self.btn_run.is_clicked(mouse):
                    data = []
                    
                    for entry in self.entries:
                        value = entry.getText().replace(',', '.')
                        
                        try:
                            value = float(value)
                            
                            min = self.inputs[self.entries.index(entry)][1]
                            max = self.inputs[self.entries.index(entry)][2]
                            
                            if min <= value <= max:
                                data.append(value)
                            else:
                                raise
                        except:
                            entry.setTextColor('red')
                            
                       
                    if data != [] and len(data) == len(self.entries):
                        self.close()
                        return data
            
            # reset entry color when any key clicked 
            key = self.checkKey()
            if key != '':
                for entry in self.entries:
                    entry.setTextColor('black')
                    

# ------------------------------------------------------------------------------------------------------------------------


class Counter:
    '''Displays text with number to count varibales in form 'Name: {value}'
    
    Attributes: 
        pos(Point): position of the center of counter
        text_str(str): name of counter 
        value(float): value of counter
        text(Text): text object of counter from graphics.py
        color(str): color of counter
    '''
    
    def __init__(self, pos: Point, text_str: str, value=0, color='black'):
        self.pos = pos
        self.text_str = text_str
        self.value = value
        self.text = None
        self.color = color
        
    def draw(self, window: GraphWin):
        self.text = Text(self.pos, f'{self.text_str}: {self.value}')
        self.text.setTextColor(self.color)
        self.text.setStyle('bold')
        self.text.setFace('arial')
        self.text.setSize(20)
        self.text.draw(window)
        
    def change(self, i=1):
        '''increments and decrements value by i'''
        
        self.value += int(i)
        self.text.setText(f'{self.text_str}: {self.value}')
    
    def clear(self):
        self.value = 0
        self.text.setText(f'{self.text_str}: {self.value}')
# ------------------------------------------------------------------------------------------------------------------------
    

class SelectionWindow(GraphWin):
    '''Creates and displays menu window with 4 buttons for each scenario, start and quit button
    
    Attributes:
        size(int): width and height of window (1:1.15)
        selection_buttons(list(Button)): list of selection buttons (1,2,3,4)
        buttons(list(Button)): list of all buttons
        selected(Button): currently selected button of there is one, otherwise None
    '''
    
    def __init__(self, size):
        super().__init__('Menu', size, 1.15 * size, autoflush=False)
        self.size = size
        self.selection_buttons = []
        self.buttons = []
        self.selected = None
        
        self.setBackground('white')
        
        self.btn_start = Button(Point(0.3 * size , 0.3 * size), Point(0.7 * size, 0.7 * size), 'START',
                           shape='oval',
                           background_color=COLOR_BUTTON_ACCENT,
                           text_color='white',
                           text_size=20,)
        
        self.buttons.append(self.btn_start)
            
        self.btn_quit = Button(Point(0.4 * size, size), Point(0.6 * size, 1.1 * size), 'QUIT',
                          action=self.btn_quit_action)
        self.buttons.append(self.btn_quit)
        
        for i in range(1, 5):
            if i % 2 == 0:
                x1 = 0.5 * size
                x2 = 0.95 * size
            else:
                x1 = 0.05 * size
                x2 = 0.5 * size
                
            if i == 1 or i == 2:
                y1 = 0.05 * size
                y2 = 0.5 * size
            else:
                y1 = 0.5 * size
                y2 = 0.95 * size
        
            btn = Button(Point(x1, y1), Point(x2, y2), str(i), action=lambda n=i: self.btn_select_action(n))
            btn.draw(self)
            self.selection_buttons.append(btn)
            self.buttons.append(btn)
        
        self.btn_start.draw(self)
        self.btn_quit.draw(self)
        self.update()
        
    def btn_select_action(self, n):
        for btn in self.selection_buttons:
            btn.setTextColor('black')
            btn.setTextSize(15)
            
        self.selected = self.selection_buttons[n-1]    
        self.selected.setTextColor(COLOR_BUTTON_ACCENT)
        self.selected.setTextSize(20)

    def btn_quit_action(self):
        self.selected = None
        self.close()
    
    def select(self):
        while self.isOpen():
            mouse = self.checkMouse()
            if mouse != None:
                for btn in self.buttons:
                    if btn.is_clicked(mouse):
                        if btn == self.btn_start and self.selected != None:
                            return self.selected.getTextString()
                        break
# ------------------------------------------------------------------------------------------------------------------------