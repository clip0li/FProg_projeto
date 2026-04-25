from graphics import *
from gui import *
import numpy as np

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

class Ball:
    def __init__(self, pos0: Point, size=0.2, color='brown3', ball = None,):
        self.pos = pos0
        self.size = size
        self.vel = Point(0,0)
        self.acl = Point(0,0)
        self.mass = 1
        self.color = color
        self.ball = ball
        
        
    def getPos(self):
        return self.pos
    
    
    def getSize(self):
        return self.size
    
    
    def setAcl(self, acl):
        self.acl = acl

        
    def draw(self, window: GraphWin):
        self.ball = Circle(self.pos, self.size)
        self.ball.setFill(self.color)
        self.ball.setWidth(0)
        self.ball.draw(window)
        
        
    def step(self, dt):
        velx_new = self.vel.getX() + self.acl.getX() * dt
        vely_new = self.vel.getY() + self.acl.getY() * dt
        self.vel = Point(velx_new, vely_new)
        
        dx = self.vel.getX() * dt
        dy = self.vel.getY() * dt
        self.ball.move(dx, dy)
        
        self.pos = Point(self.pos.getX() + dx, self.pos.getY() + dy)
        

    def launch(self, vel, angle):
        velx = vel * np.cos(angle * np.pi / 180)
        vely = vel * np.sin(angle * np.pi / 180)
        self.vel = Point(velx, vely)
        
        while self.getPos().getY() - self.getSize() > 0:
            self.step(1 / 60) 
            update(60)
            

    
    def step(self, dt):
        vx = self.vel.getX() + self.acl.getX() * dt
        vy = self.vel.getY() + self.acl.getY() * dt
        self.vel = Point(vx, vy)
        
        new_x = self.pos.getX() + vx * dt
        new_y = self.pos.getY() + vy * dt
        
        dx = new_x - self.pos.getX()
        dy = new_y - self.pos.getY()
        self.ball.move(dx, dy)
        self.pos = Point(new_x, new_y)

    def moveTo(self, point: Point):
        self.ball.move(point.getX() - self.pos.getX(), point.getY() - self.pos.getY())
        self.pos = point
        
        
# ------------------------------------------------------------------------

class Hoop:
    def __init__(self, pos: Point, width, size):
        self.pos = pos
        self.width = width
        self.size = size
        
    def draw(self, window: GraphWin):
        w1 = self.pos.getX()  - self.width / 2 - self.size
        w2 = self.pos.getX()  + self.width / 2 + self.size
        
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


# ------------------------------------------------------------------------


class Counter:
    def __init__(self,pos, text_str, count=0):
        self.pos = pos
        self.text_str = text_str
        self.text = None
        self.count = count
        
        
    def draw(self, window):
        self.text = Text(self.pos, f'{self.text_str}: {self.count}')
        self.text.setStyle('bold')
        self.text.setFace('arial')
        self.text.draw(window)
        
    def change(self, i=1):
        self.count += i
        self.text.setText(f'{self.text_str}: {self.count}')
        

        
    

# ------------------------------------------------------------------------


class Simulation(GraphWin):
    def __init__(self, name):
        GraphWin.__init__(self, name, 1280, 720, autoflush = False)
        self.setCoords(0, 0, 16, 9)
        self.setBackground('white')
        
        self.objects = []
        
        self.quit_button = Button(Point(0.25, 8.75), Point(1, 8.25), 'QUIT', action=lambda: self.close())
        self.quit_button.draw(self)
        
    def addObject(self, obj):
        self.objects.append(obj)
        obj.draw(self)
                
    def getObjects(self):
            return self.objects
    
    def checkQuitButton(self, mouse):
        self.quit_button.is_clicked(mouse)
        
    
    
    
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    
    
    def run_step(self, dt):
        balls = [obj for obj in self.objects if isinstance(obj, Ball)]
        parabolas = [obj for obj in self.objects if isinstance(obj, Parabola)]
        
        for ball in balls:
            ball.setAcl(Point(0, -9.8)) 
            ball.step(dt)
            
            for parabola in parabolas:
                dist, contact = parabola.distanceTo(ball.pos)
                
                # РІШЕННЯ ПРОБЛЕМИ "ПРОВАЛЮВАННЯ":
                # Перевіряємо дві умови: 
                # 1. Математична відстань менша за радіус.
                # 2. Центр м'яча знаходиться нижче лінії параболи (для чаші).
                
                surface_y = parabola.equationGetY(ball.pos.getX())
                
                # Якщо м'яч торкається АБО вже встиг зайти за межу
                if dist < ball.size or ball.pos.getY() < surface_y + ball.size:
                    self.resolve_collision(ball, parabola, contact, dist)
                
        # Оновлюємо вікно один раз після прорахунку всіх об'єктів
        update(1 / dt)

    def resolve_collision(self, ball, parabola, contact_point, dist):
        # 1. Визначаємо, чи м'яч знаходиться "під" параболою
        # Для y = a(x-e)^2 + d, м'яч "всередині" (над чашею), якщо y > equationGetY(x)
        is_inside = ball.pos.getY() > parabola.equationGetY(ball.pos.getX())
        
        # Якщо м'яч випав знизу (is_inside = False для чаші), нам треба його ігнорувати 
        # або повернути назад. Але зазвичай м'яч падає ЗВЕРХУ.
        
        # bormal vector from contact point to ball
        nx = ball.pos.getX() - contact_point.getX()
        ny = ball.pos.getY() - contact_point.getY()
        magnitude = np.sqrt(nx**2 + ny**2)
        # if current_dist == 0: return 
        nx /= magnitude
        ny /= magnitude

        if ny < 0:
            ny = -ny # correction if ball is under of parabola
        
        # position correction
        ball.moveTo(Point(contact_point.getX() + nx * ball.size, contact_point.getY() + ny * ball.size))

        # 4. Відскок
        v_dot_n = ball.vel.getX() * nx + ball.vel.getY() * ny
        
        # Відбиваємо тільки якщо м'яч рухається НАЗУСТРІЧ поверхні
        if v_dot_n < 0:
            elasticity = np.sqrt(1) # Втрата енергії
            new_vx = (ball.vel.getX() - 2 * v_dot_n * nx) * elasticity
            new_vy = (ball.vel.getY() - 2 * v_dot_n * ny) * elasticity
            ball.vel = Point(new_vx, new_vy)
        
        

                
    
        
    
    