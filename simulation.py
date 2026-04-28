from graphics import *
from gui import *
import numpy as np

class Ball:
    def __init__(self, pos0: Point, size=0.2, color='brown3'):
        self.pos = pos0
        self.size = size
        self.vel = Point(0, 0)
        self.acl = Point(0, 0)
        self.color = color
        self.body = None  
    
    def getPos(self):
        return self.pos
    
    def getVel(self):
        return self.vel
    
    def getAcl(self):
        return self.acl
    
    def getSize(self):
        return self.size
    
    def setPos(self, point: Point):
        self.body.move(point.getX() - self.pos.getX(), point.getY() - self.pos.getY())
        self.pos = point
    
    def setVel(self, vel: Point):
        self.vel = vel
    
    def setAcl(self, acl: Point):
        self.acl = acl

    def draw(self, window: GraphWin):
        self.body = Circle(self.pos, self.size)
        self.body.setFill(self.color)
        self.body.setOutline(self.color)
        self.body.draw(window)

    def step(self, dt):
        vx = self.vel.getX() + self.acl.getX() * dt
        vy = self.vel.getY() + self.acl.getY() * dt
        self.vel = Point(vx, vy)
        
        dx = vx * dt
        dy = vy * dt
        self.body.move(dx, dy)
        self.pos = Point(self.pos.getX() + dx, self.pos.getY() + dy)
        
        
        
# ------------------------------------------------------------------------



class Parabola:
    def __init__(self, pos:Point, curvature, width):
        self.pos = pos
        self.curvature = curvature
        self.width = width
        
    def getPos(self):
        return self.pos
        
    def draw(self, window: GraphWin, lines = 100):
        x0 = self.pos.getX() - self.width / 2
        step = self.width / lines
        previous_point = Point(x0, self.equationGetY(x0))
        
        for i in range(1, lines + 1):
            x = x0 + i * step
            y = self.equationGetY(x)
            
            point = Point(x, y)
            
            line = Line(previous_point, point)
            line.setWidth(2)
            line.draw(window)
            
            previous_point = point
        
        
    def equationGetY(self, x):
        return self.curvature * (x - self.pos.getX()) ** 2 + self.pos.getY()
    
    # returns only values on left and is relative to vertice of parabola
    def equationGetX(self, y):
        return - np.sqrt(y / self.curvature)
    
    def distanceTo(self, point):
        px = point.getX()
        py = point.getY()
        
        a = self.curvature
        x0 = self.pos.getX()
        y0 = self.pos.getY()
        
        dx = px - x0
        dy = py - y0
        
        # coefficients of polinomial of 3rd degree
        coeffs = [2*a**2, 0, 1 - 2*a*dy, -dx]
        
        # roots of polynomial with those coeffs
        roots = np.roots(coeffs)
        
        # choosing only real roots
        real_roots = [r.real for r in roots ] # if abs(r.imag) < 1e-9

        collision_point = None
        best_distance = float('inf') # infinity if point is not finded
        
        for k in real_roots:
            x = k + x0
            y = a * k**2 + y0
            
            dist = np.sqrt((x - px)**2 + (y - py)**2)
            
            if dist < best_distance:
                best_distance = dist
                collision_point = Point(x, y)

        return collision_point, best_distance
        
    def checkCollision(self, ball: Ball, collision_point: Point, bounciness, friction, dt):
        friction *= dt
        # normal vector
        normalx = ball.pos.getX() -  collision_point.getX()
        normaly = ball.pos.getY() -  collision_point.getY()
        
        # distance from collision point to ball 
        distance = np.sqrt(normalx**2 + normaly**2)
        if distance == 0: return 
        
        # normalize
        normalx /= distance
        normaly /= distance
        
        # fix direction
        if normaly < 0:
            normalx = -normalx
            normaly = -normaly 
        
        # tangent vector
        tangentx = normaly
        tangenty = -normalx
        
        # fix direction
        if tangenty > 0:
            tangentx = -tangentx
            tangenty = -tangenty
        
        # correct position
        x = collision_point.getX() + normalx * ball.getSize()
        y = collision_point.getY() + normaly * ball.getSize()
        ball.setPos(Point(x, y))
        
        # curent velocity
        vx = ball.getVel().getX()
        vy = ball.getVel().getY()
        
        v_normal = vx * normalx + vy * normaly    # projection of velocity on normal unit vector
        v_tangent = vx * tangentx + vy * tangenty # projection of velocity on tangent unit vector
        
        # current acceleration
        ax = ball.getAcl().getX()
        ay = ball.getAcl().getY()
        
        # fix direction
        if ay > 0:
            ax = -ax
            ay = -ay
        
        a_tangent = ax * tangentx + ay * tangenty 
        
        # new velocity with normal and tangent components
        v_tangent_new = (v_tangent + a_tangent * dt) * (1 - friction)
        v_normal_new = -v_normal * bounciness if v_normal < 0 else v_normal
        
        # new velocity with x and y components
        new_vx = v_tangent_new * tangentx + v_normal_new * normalx
        new_vy = v_tangent_new * tangenty + v_normal_new * normaly
        
        # set new velocity
        ball.setVel(Point(new_vx, new_vy))
        
        # debugging
        
        #print('Velocity: ', new_vx, new_vy)
        #print('Acceleration: ', ax, ay, '\n')
        
# ------------------------------------------------------------------------



class Hoop:
    def __init__(self, pos: Point, width, size):
        self.pos = pos
        self.width = width
        self.size = size 
        
    def draw(self, window: GraphWin):
        w1 = self.pos.getX() - self.width / 2 - self.size
        w2 = self.pos.getX() + self.width / 2 + self.size
        
        circle1 = Circle(Point(w1, self.pos.getY()), self.size)
        circle1.setFill('powderblue')
        circle1.setWidth(1)
        circle1.draw(window)
        
        circle2 = Circle(Point(w2, self.pos.getY()), self.size)
        circle2.setFill('powderblue')
        circle2.setWidth(1)
        circle2.draw(window)
        
        line1 = Line(Point(w1, self.pos.getY() + self.size), Point(w2, self.pos.getY() + self.size))
        line1.draw(window)
        
        line2 = Line(Point(w1, self.pos.getY() - self.size), Point(w2, self.pos.getY() - self.size))
        line2.draw(window)
        
    def is_scored(self, pos: Point):
        p1 = Point(self.pos.getX() - self.width / 2, self.pos.getY() + self.size)
        p2 = Point(self.pos.getX() + self.width / 2, self.pos.getY() - self.size)
        
        if min(p1.getX(), p2.getX()) <= pos.getX() <= max(p1.getX(), p2.getX()) and \
               min(p1.getY(), p2.getY()) <= pos.getY() <= max(p1.getY(), p2.getY()):
            return True
        
        return False



# ------------------------------------------------------------------------



class Counter:
    def __init__(self,pos, text_str='Score', count=0):
        self.pos = pos
        self.text_str = text_str
        self.text = None
        self.count = count
        
    def draw(self, window):
        self.text = Text(self.pos, f'{self.text_str}: {self.count}')
        self.text.setStyle('bold')
        self.text.setFace('arial')
        self.text.setSize(20)
        self.text.draw(window)
        
    def change(self, i=1):
        self.count += i
        self.text.setText(f'{self.text_str}: {self.count}')
        
        

class Stickman:
    def __init__(self, pos: Point, height):
        self.pos = pos
        self.height = height
        
    def draw(self, window: GraphWin):
        x = self.pos.getX()
        y = self.pos.getY()
        h = self.height
        head = Circle(Point(x, y + h * 0.85), h * 0.15)
        head.setWidth(2)
        head.draw(window)
        
        body = Line(Point(x, y + h * 0.3), Point(x, y + h * 0.7))
        body.setWidth(2)
        body.draw(window)
        
        left_leg = Line(Point(x, y + h * 0.3), Point(x - 0.2, y))
        left_leg.setWidth(2)
        left_leg.draw(window)
        
        right_leg = Line(Point(x, y + h * 0.3), Point(x + 0.2, y))
        right_leg.setWidth(2)
        right_leg.draw(window)
        
        left_arm = Line(Point(x, y + h * 0.6), Point(x - 0.2, y + h * 0.3))
        left_arm.setWidth(2)
        left_arm.draw(window)
        
        right_arm = Line(Point(x, y + h * 0.6), Point(x + 0.2, y + h * 0.3))
        right_arm.setWidth(2)
        right_arm.draw(window)
    


# ------------------------------------------------------------------------ 
            

    
class Simulation(GraphWin):
    def __init__(self, title: str, width=1280, height=720):
        GraphWin.__init__(self, title, width, height, autoflush=False)
        self.setCoords(0, 0, 16, 9) 
        self.objects = []
        
        self.setBackground('white')
        self.btn_quit = Button(Point(0.25, 8.75), Point(1, 8.25), 'QUIT', action=lambda: self.close())
        self.btn_quit.draw(self)    

    def addObject(self, obj):
        self.objects.append(obj)
        obj.draw(self)
        
    def checkQuitButton(self, mouse):
        self.btn_quit.is_clicked(mouse)
        
        
        

                
    
        
    
    