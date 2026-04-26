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
        

    def moveTo(self, point: Point):
        self.body.move(point.getX() - self.pos.getX(), point.getY() - self.pos.getY())
        self.pos = point
        
        
# ------------------------------------------------------------------------

class Parabola:
    def __init__(self, pos:Point, curvature, width):
        self.pos = pos
        self.curvature = curvature
        self.width = width
        
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
    
    def equationGetDerivative(self, x):
        return 2 * self.curvature * (x - self.pos.getX())
    
    def placeBall(self, ball: Ball, height):
        pass

    def distanceTo(self, point):
        x, y = point.getX(), point.getY()
        xp, yp = self.pos.getX(), self.pos.getY()
        a = self.curvature
        
        # u = x - e
        coeffs = [
            2 * a ** 2,             # u^3
            0,                      # u^2
            2 * a * (yp - y) + 1,   # u^1
            xp - x                  # u^0
        ]
        
        # roots of polynomial with those coeffs
        roots = np.roots(coeffs)
        
        # choosing only real roots
        real_u = roots[np.isreal(roots)].real

        # collision point
        x1 = real_u + xp
        y1 = a * real_u**2 + yp
        
        distances = np.sqrt((x - x1)**2 + (y - y1)**2)
        
        # index of minimum distance
        index = np.argmin(distances)

        return distances[index], Point(x1[index], y1[index])
        
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
    
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        

    
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
        

    def run_step(self, dt):
        balls = [obj for obj in self.objects if isinstance(obj, Ball)]
        parabolas = [obj for obj in self.objects if isinstance(obj, Parabola)]
        
        for ball in balls:
            ball.acl = Point(0, -9.8) # Гравітація
            ball.step(dt)
            
            for parabola in parabolas:
                dist, contact = parabola.distanceTo(ball.pos)
                surface_y = parabola.equationGetY(ball.pos.getX())
                
                # Колізія: якщо відстань менша за радіус АБО центр під параболою
                if dist < ball.size or ball.pos.getY() < surface_y:
                    self.resolve_collision(ball, parabola, contact)
        update(1/dt)
        

    def resolve_collision(self, ball, parabola, contact):
        nx = ball.pos.getX() - contact.getX()
        ny = ball.pos.getY() - contact.getY()
        dist = np.sqrt(nx**2 + ny**2)
        
        if dist == 0: return
        nx, ny = nx/dist, ny/dist

        # Гарантуємо виштовхування вгору для "чаші"
        if ny < 0 and parabola.curvature > 0:
            ny = -ny

        # Корекція позиції
        ball.moveTo(Point(contact.getX() + nx * ball.size, contact.getY() + ny * ball.size))

        # Відскок
        v_dot_n = ball.vel.getX() * nx + ball.vel.getY() * ny
        if v_dot_n < 0:
            elasticity = 0.8
            new_vx = (ball.vel.getX() - 2 * v_dot_n * nx) * elasticity
            new_vy = (ball.vel.getY() - 2 * v_dot_n * ny) * elasticity
            ball.vel = Point(new_vx, new_vy)
        
        

                
    
        
    
    