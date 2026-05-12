'''
istxxxxxxx, istxxxxxxx
File responsoble of anything related to simulation process, calcualtions and
Contains Ball, Parabola, Hoop, Simulation
'''

from graphics import *
from gui import *
import numpy as np
import time
from tkinter import filedialog

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
    
    def getSpeed(self):
        return np.sqrt(self.vel.getX() ** 2 + self.vel.getY() ** 2)
    
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
        real_roots = [r.real for r in roots if abs(r.imag) < 1e-9]
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
                
        if py < self.equationGetY(px) and x0 + x_min < px < x0 + x_max:
            best_distance = - best_distance        
                
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
        # 'wall' vector from p1 to p2
        wx = self.p2.getX() - self.p1.getX()
        wy = self.p2.getY() - self.p1.getY()
        
        # vector from p1 to point
        px = point.getX() - self.p1.getX()
        py = point.getY() - self.p1.getY()
        
        dot = wx * px + wy * py
        magnitude = wx ** 2 + wy ** 2
        proj = max(0, min(1, dot / magnitude))
        
        # contact point
        contact_x = self.p1.getX() + proj * wx
        contact_y = self.p1.getY() + proj * wy
        contact_point  = Point(contact_x, contact_y)
        
        # absolute distance
        dx = point.getX() - contact_x 
        dy = point.getY() - contact_y
        abs_distance = np.sqrt(dx**2 + dy**2)
        
        nx = -wy
        ny = wx
        
        # if dot product is positive then vectors (px, py) and (nx, ny) are pointed in the same direction
        sign = px * nx + py * ny
        
        signed_distance = abs_distance if sign >= 0 else -abs_distance

        return contact_point, signed_distance
# -------------------------------------------------------------------
            

class Simulation(GraphWin):
    
    '''class that draws and contains all object simulation'''
    '''and process collisions''' 
    
    def __init__(self, title: str, width=1280, height=720, dt = 1/ 60, elacticity=0, friction = 0):
        GraphWin.__init__(self, title, width, height, autoflush=False)
        self.setCoords(0, 0, 16, 9)
        self.dt0 = dt
        self.dt = dt
        self.dynamic_objects = []
        self.static_objects = []
        self.elacticity = elacticity
        self.friction = friction 
        
        self.setBackground('white')
        self.btn_quit = Button(Point(0.25, 8.75), Point(1, 8.25), 'QUIT', action=lambda: self.close())
        self.btn_quit.draw(self)
        
        self.indicator = Circle(Point(15.7, 8.7), 0.1)
        self.indicator.setFill('green')
        self.indicator.setWidth(0)
        self.indicator.draw(self)
    
        

    def addDynamicObject(self, obj):
        self.dynamic_objects.append(obj)
        obj.draw(self)
        update(1 / self.dt)
        
    def addStaticObject(self, obj):
        self.static_objects.append(obj)
        obj.draw(self)
        update(1 / self.dt)
        
    def getDynamicObjects(self):
        return self.dynamic_objects
        
    def checkQuitButton(self, mouse):
        self.btn_quit.is_clicked(mouse)
        
    def tick(self):
        tick_start = time.perf_counter()
        for obj in self.dynamic_objects:
            if isinstance(obj, Ball):
                obj.step(self.dt)
        update(1 / self.dt)
        
        elapsed = time.perf_counter() - tick_start
        remaining = self.dt - elapsed
        
        if remaining > 0:
            time.sleep(remaining)
                
    def stopped(self):
        self.indicator.setFill('red')
        
    
    def collisionWithStaticObject(self, ball: Ball, object):
        collision_point, distance = object.distanceTo(ball.getPos())        
        
        if distance > ball.getSize() or distance == 0: return 
                                
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
        a_tangent = ax * tangentx + ay * tangenty 
        
        # new velocity with normal and tangent components
        v_tangent_new = (v_tangent + a_tangent * self.dt) * (1 - self.friction * self.dt)
        v_normal_new = -v_normal * self.elacticity 
        
        # new velocity with x and y components
        new_vx = v_tangent_new * tangentx + v_normal_new * normalx
        new_vy = v_tangent_new * tangenty + v_normal_new * normaly
        
        # set new velocity
        ball.setVel(Point(new_vx, new_vy))
        '''
        print('Collision point: ', collision_point)
        print('Distance: ', distance, '\n')
        
        print('Normal X: ', normalx)
        print('Normal Y: ', normaly)
        print('Tangent X: ', tangentx)
        print('Tangent Y: ', tangenty, '\n')
        
        print('Velocity X:', new_vx)
        print('Velocity Y:', new_vy)
        print('Velocity n: ', v_normal_new)
        print('Velocity t: ', v_tangent_new)
        print('Velocity: ', np.sqrt(new_vx ** 2 + new_vy ** 2), '\n')
        print('-----------------------------------')
        '''    
    def collisionWithDynamicObject(self, ball1: Ball, ball2: Ball):
        dx = ball2.getPos().getX() - ball1.getPos().getX()
        dy = ball2.getPos().getY() - ball1.getPos().getY()
        collision_distance = ball1.getSize() + ball2.getSize()

        if abs(dx) > collision_distance or abs(dy) > collision_distance: return
        
        distance =  np.sqrt(dx ** 2 + dy **2)
        if distance > collision_distance or distance == 0: return
        
        # normal vector between two centers
        nx = dx / distance
        ny = dy / distance
        
        #fix position
        correction = (collision_distance - distance) / 2
        #ball1 negative and ball2 positive because normal vector is from ball1 to ball2
        ball1.setPos(Point(ball1.pos.getX() - nx * correction, ball1.pos.getY() - ny * correction))
        ball2.setPos(Point(ball2.pos.getX() + nx * correction, ball2.pos.getY() + ny * correction))
        
        rel_vx = ball1.getVel().getX() - ball2.getVel().getX()
        rel_vy = ball1.getVel().getY() - ball2.getVel().getY()

        impulse = rel_vx * nx + rel_vy * ny
        impulse *= 0.999
        if impulse < 0:
            return

        ball1.setVel(Point(ball1.vel.getX() - impulse * nx, ball1.vel.getY() - impulse * ny))
        ball2.setVel(Point(ball2.vel.getX() + impulse * nx, ball2.vel.getY() + impulse * ny))

        
    def checkCollisions(self):
        for dobj in self.dynamic_objects:
            for sobj in self.static_objects:
                if isinstance(dobj, Ball) and (isinstance(sobj, Parabola) or isinstance(sobj, Wall)):
                    self.collisionWithStaticObject(dobj, sobj)

        n = len(self.dynamic_objects)
        for i in range(n):
            for j in range(i + 1, n): 
                dobj1 = self.dynamic_objects[i]
                dobj2 = self.dynamic_objects[j]
                if isinstance(dobj1, Ball) and isinstance(dobj2, Ball):
                    self.collisionWithDynamicObject(dobj1, dobj2)
            
            
            
import time
from tkinter import filedialog

class TrajectoryRecorder:
    def __init__(self):
        self.clear() 

    def clear(self):
        self.t0 = time.time()
        self.elapsed_time = 0
        self.time_log = []
        self.x_log = []
        self.y_log = []

    def record(self, dt, ball):
        self.time_log.append(self.elapsed_time)
        self.elapsed_time += dt
        
        self.x_log.append(ball.getPos().getX())
        self.y_log.append(ball.getPos().getY())
    
    def save(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt")

        if file_path == ():  
            return
        
        with open(file_path, 'w') as file:
            local_time = time.localtime(self.t0)
            ms = int((self.t0 % 1) * 1000)
            t0_str = f"{time.strftime('%H:%M:%S', local_time)}.{ms:03d}\n"
            
            file.write(f"Start Time: {t0_str}\n")
            file.write("Elapsed Time: " + " ".join(f"{t:.3f}" for t in self.time_log) + "\n")
            file.write("X Positions:  " + " ".join(f"{x:.3f}" for x in self.x_log) + "\n")
            file.write("Y Positions:  " + " ".join(f"{y:.3f}" for y in self.y_log) + "\n")
 