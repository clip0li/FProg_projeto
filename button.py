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

        
    def setAction(self, action):
        self.action = action
        
        
    def getTextString(self):
        return self.text_string
    
    
    def is_clicked(self, pos: Point):
        if pos == None: return False
        if self.shape == 'rectangle':
            
            if min(self.p1.x, self.p2.x) <= pos.getX() <= max(self.p1.x, self.p2.x) and \
               min(self.p1.y, self.p2.y) <= pos.getY() <= max(self.p1.y, self.p2.y):

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
        
        
        
    
        