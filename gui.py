'''
istxxxxxxx, istxxxxxxx
File responsible of GUI classes of program
Contains: Button, InputDialog, Counter, SelectionWindow
'''

from graphics import *
import numpy as np

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
        
# -------------------------------------------------------------------


class Stickman:
    def __init__(self, pos: Point, height):
        self.pos = pos
        self.height = height
        self.body_angle = 90
        
    def draw(self, window: GraphWin):
        x = self.pos.getX()
        y = self.pos.getY()
        h = self.height
        
        angle = self.body_angle * np.pi / 180
        
        cos = np.cos(angle)
        sin = np.sin(angle)
        
        head_size = 0.1 * h
        hip_size = 0.2 * self.height
        shoulders_size = 1.5 * hip_size
        foot_size = 0.1 * self.height
        
        leg_point = Point(x, y + 0.4 * h)
        arms_point = Point(x + 0.4 * h * cos, leg_point.getY() + 0.4 * h * sin)
        head_point = Point(arms_point.getX() +  head_size * cos, arms_point.getY() +  head_size * sin)
        
        a_cos = np.cos(angle + np.pi / 2)
        a_sin = np.sin(angle + np.pi / 2)
        left_arm_point = Point(arms_point.getX() - shoulders_size / 2 * a_cos, arms_point.getY() - shoulders_size / 2 * a_sin)
        right_arm_point = Point(arms_point.getX() + shoulders_size / 2 * a_cos, arms_point.getY() + shoulders_size / 2 * a_sin)
        
        
        # hips
        hips = Line(Point(leg_point.getX() - hip_size / 2, leg_point.getY()), Point(leg_point.getX() + hip_size / 2, leg_point.getY()))
        hips.setWidth(2)
        hips.draw(window)
        
        # left leg
        left_leg = Line(Point(leg_point.getX() - hip_size / 2, leg_point.getY()), Point(leg_point.getX() - hip_size / 4, y))
        left_leg.setWidth(2)
        left_leg.draw(window)
        
        # right leg
        right_leg = Line(Point(leg_point.getX() + hip_size / 2, leg_point.getY()), Point(leg_point.getX() + hip_size / 4, y))
        right_leg.setWidth(2)
        right_leg.draw(window)
        
        # left foot 
        left_foot = Line(Point(leg_point.getX() - hip_size / 4, y), Point(leg_point.getX() - hip_size / 4 - foot_size, y))
        left_foot.setWidth(3)
        left_foot.draw(window)
        
        # right foot
        right_foot = Line(Point(leg_point.getX() + hip_size / 4, y), Point(leg_point.getX() + hip_size / 4 + foot_size, y))
        right_foot.setWidth(3)
        right_foot.draw(window)
        
        # body
        body = Line(leg_point, arms_point)
        body.setWidth(2)
        body.draw(window)
        
        # shoulders
        shoulders = Line(left_arm_point, right_arm_point)
        shoulders.setWidth(2)
        shoulders.draw(window)
        
        # head
        head = Circle(head_point, head_size)
        head.setWidth(2)
        head.setFill('white')
        head.draw(window)
        
        

                
# -------------------------------------------------------------------


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
            text = Text(Point(self.width / 3, (i + 1) * step), f'{inp[0]}: ')
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
                    return 
                
                if self.btn_run.is_clicked(mouse):
                    data = []
                    
                    for entry in self.entries:
                        value = entry.getText().replace(',', '.')
                        
                        try:
                            value = float(value)
                        except:
                            return
                        
                        if 0 < value < self.inputs[self.entries.index(entry)][1]:
                            data.append(value)
                    
                    if data != [] and len(data) == len(self.entries):
                        self.close()
                        return data


# -------------------------------------------------------------------


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


# -------------------------------------------------------------------
    

class SelectionWindow(GraphWin):
    def __init__(self, size):
        GraphWin.__init__(self, 'Select', size, 1.15 * size, autoflush=False)
        self.size = size
        self.selection_buttons = []
        self.buttons = []
        self.selected = None
        
        self.setBackground('white')
        
        # start button
        self.btn_start = Button(Point(0.3 * size , 0.3 * size), Point(0.7 * size, 0.7 * size), 'START',
                           shape='oval',
                           background_color='crimson',
                           text_color='white',
                           text_size=20,)
        
        self.buttons.append(self.btn_start)
            
        # quit button
        self.btn_quit = Button(Point(0.4 * size, size), Point(0.6 * size, 1.1 * size), 'QUIT',
                          action=self.btn_quit_action)
        
        self.buttons.append(self.btn_quit)
        
        # selection buttons
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
            
        self.selected = self.selection_buttons[n-1]    
        self.selected.setTextColor('red')
        self.update()

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
                            self.close()
                            return self.selected.getTextString()
                            
                        break