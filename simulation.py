'''
istxxxxxxx, istxxxxxxx
File responsoble of anything related to simulation process, calcualtions and
Contains Ball, Parabola, Hoop, Simulation
'''

from graphics import *
from gui import *
import numpy as np
import time

class Ball:
    
    '''Creates ball(cirlcle projectile)'''
    '''Properties: color, size, position, velocity, acceleration'''
    
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
        '''advance properties by time step st'''
        '''sets position with x = v * dt formula and velocity with v = a * dt formlula'''
        # current postion
        x = self.pos.getX() 
        y = self.pos.getY()
        
        # current velocity
        vx = self.vel.getX() 
        vy = self.vel.getY() 
        
        # delta(change) of position 
        dx = vx * dt
        dy = vy * dt
        
        self.body.move(dx, dy)
        self.pos = Point(x + dx, y + dy)
        
        # new velocity
        new_vx = vx + self.acl.getX() * dt
        new_vy = vy + self.acl.getY() * dt
        self.vel = Point(new_vx, new_vy)
              
        
# -------------------------------------------------------------------


class Parabola:
    
    '''Draws parabola from vertice position, curvature(a) and centered width'''
    
    def __init__(self, pos:Point, curvature, left_width, right_width):
        self.pos = pos
        self.curvature = curvature
        self.left_width = left_width
        self.right_width = right_width
        self.width = left_width + right_width
        
    def getPos(self):
        return self.pos
        
    def draw(self, window: GraphWin, lines = 100):
        x0 = self.pos.getX() - self.left_width
        step = self.width / lines
        previous_point = Point(x0, self.equationGetY(x0))
        
        for i in range(1, lines + 1):
            x = x0 + i * step
            y = self.equationGetY(x)
            
            point = Point(x, y)
            
            line = Line(previous_point, point)
            line.setWidth(3)
            line.draw(window)
            
            previous_point = point
        
        
    def equationGetY(self, x):
        '''returns y (relative to window) of point of parabola with specific x'''
        return self.curvature * (x - self.pos.getX()) ** 2 + self.pos.getY()
    
    def equationGetX(self, y):
        '''returns x (relative to vertice) of point of parabola with specific y'''
        return - np.sqrt(y / self.curvature)
    
    def distanceTo(self, point):
        '''calculates distance from parabola in space to arbitrary point'''
        '''does it by calculating normal to parabola that goes trough this point'''
        '''uses deducted formula(in polynomial form) and filters all real roots. then finds nearst solution among them'''
        '''returns point of intersection normal-parabola and distance'''
        px = point.getX()
        py = point.getY()
        
        a = self.curvature
        x0 = self.pos.getX()
        y0 = self.pos.getY()
        
        nx = px - x0
        ny = py - y0
        
        x_min = -self.left_width
        x_max = self.right_width
        
        # coefficients of polinomial of 3rd degree
        coeffs = [2*a**2, 0, 1 - 2*a*ny, -nx]
        
        # roots of polynomial with those coeffs
        roots = np.roots(coeffs)
        
        # choosing only real roots
        real_roots = [r.real for r in roots ] # if abs(r.imag) < 1e-9

        candidates = []
        
        for k in real_roots:
            if x_min <= k <= x_max:
                candidates.append(Point(k + x0, a * k**2 + y0))
                
        # limits
        candidates.append(Point(x0 + x_min, self.equationGetY(x0 + x_min)))
        candidates.append(Point(x0 + x_max, self.equationGetY(x0 + x_max)))
        
        contact_point = None
        best_distance = float('inf')
        
        for cp in candidates:
            dist = np.sqrt((cp.getX() - px)**2 + (cp.getY() - py)**2)
            if dist < best_distance:
                best_distance = dist
                contact_point = cp

        return contact_point, best_distance
        
        
# -------------------------------------------------------------------


class Hoop:
    
    '''Creates hoop represented as two circles and two lines between of them'''
    
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
        '''returns True if point is within rectangle between two circles'''
        p1 = Point(self.pos.getX() - self.width / 2, self.pos.getY() + self.size)
        p2 = Point(self.pos.getX() + self.width / 2, self.pos.getY() - self.size)
        
        if min(p1.getX(), p2.getX()) <= pos.getX() <= max(p1.getX(), p2.getX()) and \
               min(p1.getY(), p2.getY()) <= pos.getY() <= max(p1.getY(), p2.getY()):
            return True
        
        return False


# -------------------------------------------------------------------


class Wall(Line):
    def __init__(self, p1: Point, p2: Point):
        Line.__init__(self, p1, p2)
        self.p1 = p1
        self.p2 = p2
        self.vector = Point(self.p2.getX() - self.p1.getX(), self.p2.getY() - self.p1.getY())
        
        self.setWidth(5)
        
    def distanceTo(self, point: Point):
        # vector from p1 to point
        w = Point(point.getX() - self.p1.getX(), point.getY() - self.p1.getY())
        
        # project of w to vector of wall
        dot = self.vector.getX() * w.getX() + self.vector.getY() * w.getY() 
        vector_sq = (self.vector.getX()**2 + self.vector.getY()**2)
        proj = max(0, min(1, dot / vector_sq))

        # contact point
        x = self.p1.getX() + proj * self.vector.getX()
        y = self.p1.getY() + proj * self.vector.getY()
        
        
        dx = point.getX() - x 
        dy = point.getY() - y
        distance = np.sqrt(dx**2 + dy**2)
        
        return Point(x, y), distance


# -------------------------------------------------------------------
            

class Simulation(GraphWin):
    
    '''class that draws and contains all object simulation'''
    '''and process collisions''' # to do!!!
    
    def __init__(self, title: str, width=1280, height=720, dt = 1/ 60, elacticity=0, friction = 0):
        GraphWin.__init__(self, title, width, height, autoflush=False)
        self.setCoords(0, 0, 16, 9)
        self.dt = dt
        self.dynamic_objects = []
        self.static_objects = []
        self.elacticity = elacticity
        self.friction = friction
        
        self.setBackground('white')
        self.btn_quit = Button(Point(0.25, 8.75), Point(1, 8.25), 'QUIT', action=lambda: self.close())
        self.btn_quit.draw(self)
        

    def addDynamicObject(self, obj):
        self.dynamic_objects.append(obj)
        obj.draw(self)
        update(1 / self.dt)
        
    def addStaticObject(self, obj):
        self.static_objects.append(obj)
        obj.draw(self)
        update(1 / self.dt)
        
    def checkQuitButton(self, mouse):
        self.btn_quit.is_clicked(mouse)
        
    def tick(self):
        for obj in self.dynamic_objects:
            if isinstance(obj, Ball):
                obj.step(self.dt)
                time.sleep(self.dt)
                update(1 / self.dt)
                
    
    def collisionWithStaticObject(self, ball: Ball, object):
        collision_point, distance = object.distanceTo(ball.getPos())
        if distance == 0 or distance > ball.getSize(): return 
            
        # normal vector
        normalx = ball.pos.getX() -  collision_point.getX()
        normaly = ball.pos.getY() -  collision_point.getY()
        
        # normalize
        normalx /= distance
        normaly /= distance
        
        # tangent vector
        tangentx = normaly
        tangenty = -normalx
        
        # correct position
        if normaly >= 0:
            x = collision_point.getX() + normalx * ball.getSize()
            y = collision_point.getY() + normaly * ball.getSize()
        else:
            x = collision_point.getX() - normalx * ball.getSize()
            y = collision_point.getY() - normaly * ball.getSize()
            
        ball.setPos(Point(x, y))
            
        # curent velocity
        vx = ball.getVel().getX()
        vy = ball.getVel().getY()
        
        v_normal = vx * normalx + vy * normaly    # projection of velocity on normal unit vector
        v_tangent = vx * tangentx + vy * tangenty # projection of velocity on tangent unit vector
        
        # current acceleration
        ax = ball.getAcl().getX()
        ay = ball.getAcl().getY()
        a_tangent = ax * tangentx + ay * tangenty 
        
        # new velocity with normal and tangent components
        v_tangent_new = (v_tangent + a_tangent * self.dt) * (1 - self.friction)
        v_normal_new = -v_normal * self.elacticity 
        
        # new velocity with x and y components
        new_vx = v_tangent_new * tangentx + v_normal_new * normalx
        new_vy = v_tangent_new * tangenty + v_normal_new * normaly
        
        # set new velocity
        ball.setVel(Point(new_vx, new_vy))
        
        
    def checkCollisions(self):
        for dobj in self.dynamic_objects:
            for sobj in self.static_objects:
                if isinstance(dobj, Ball) and (isinstance(sobj, Parabola) or isinstance(sobj, Wall)):
                    self.collisionWithStaticObject(dobj, sobj)

            dobjects = self.dynamic_objects.copy()
            dobjects.remove(dobj)
            
            for dobj1 in dobjects:
                return
            
            