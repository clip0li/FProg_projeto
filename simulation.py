'''
istxxxxxxx, istxxxxxxx
File responsible of anything related to simulation process, calcualtions and trajectory recording
'''

from graphics import *
from gui import *

from tkinter import filedialog
import numpy as np
import time

COLOR_SURFACE = 'gray80'
COLOR_HOOP = 'powderblue'
COLOR_WALL = 'black'

class Ball:
    '''Creates, draw and moves ball 

        Attributes:
            pos(Point): current position
            size(float): radius
            vel(Point): current velocity
            acl(Point): current acceleration
            color(str): color
            body(Circle): Circle object from graphics.py that represents a ball
            frozen(bool): if True ball does not move
    '''
    
    def __init__(self, pos0: Point, size=0.2, color='brown3'):
        self.pos = pos0
        self.size = size
        self.vel = Point(0, 0)
        self.acl = Point(0, 0)
        self.color = color
        self.body = None  
        self.frozen = False
            
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
        
    def freeze(self):
        self.frozen = True
    
    def defreeze(self):
        self.frozen = False
        
    def isFrozen(self):
        return self.frozen

    def draw(self, window: GraphWin):
        self.body = Circle(self.pos, self.size)
        self.body.setFill(self.color)
        self.body.setOutline(self.color)
        self.body.draw(window)

    def step(self, dt):  
        if self.frozen: return
              
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
        
        
# ------------------------------------------------------------------------------------------------------------------------


class Hoop:
    '''Creates and draws hoop represented as two circles and two lines between of them

        Attributes:
            pos(Point): position of the center of hoop
            width(float): width of hoop (distance between extreme points)
            size(float): radius of each ring
            p1(Point): center of the first ring
            p2(Point): center of the second ring
    '''
    
    def __init__(self, pos: Point, width, size):
        self.pos = pos
        self.width = width
        self.size = size 
        self.p1 = Point(pos.getX() - self.width / 2 + self.size, pos.getY())
        self.p2 = Point(pos.getX() + self.width / 2 - self.size, pos.getY())
        
    def draw(self, window: GraphWin):
        ring1 = Circle(self.p1, self.size)
        ring1.setFill(COLOR_HOOP)
        ring1.setWidth(1)
        ring1.draw(window)
        
        ring2 = Circle(self.p2, self.size)
        ring2.setFill(COLOR_HOOP)
        ring2.setWidth(1)
        ring2.draw(window)
        
        line1 = Line(Point(self.p1.getX(), self.p1.getY() + self.size), Point(self.p2.getX(), self.p2.getY() + self.size))
        line1.draw(window)
        
        line2 = Line(Point(self.p1.getX(), self.p1.getY() - self.size), Point(self.p2.getX(), self.p2.getY() - self.size))
        line2.draw(window)    
          
    def distanceTo(self, point: Point):
        '''Calculates a shortest distance to a hoop from a given point and determines nearest ring
        
        Args:
            point(Point)
            
        Returns:
            contact_point(Point): point of contact of a hoop (nearest ring) with a a given point 
            distance(flaot): shortestt distance  to a given point
        '''
        
        px = point.getX()
        py = point.getY()
        
        dist1 = np.sqrt((px - self.p1.getX())**2 + (py - self.p1.getY())**2)
        dist_ring1 = dist1 - self.size

        dist2 = np.sqrt((px - self.p2.getX())**2 + (py - self.p2.getY())**2)
        dist_ring2 = dist2 - self.size
        
        if dist_ring1 < dist_ring2:
            best_dist = dist_ring1
            
            if dist1 > 0:
               contact_point = Point(self.p1.getX() + (px - self.p1.getX()) * self.size / dist1, 
                                     self.p1.getY() + (py - self.p1.getY()) * self.size / dist1) 
            else:
               contact_point = Point(self.p1.getX(), self.p1.getY() + self.size)
            
        else:
            best_dist = dist_ring2
            
            if dist2 > 0:
                contact_point = Point(self.p2.getX() + (px - self.p2.getX()) * self.size / dist2, 
                                      self.p2.getY() + (py - self.p2.getY()) * self.size / dist2)
            else:
                contact_point = Point(self.p2.getX(),self.p2.getY() + self.size)


        return contact_point, best_dist
        
        
    def is_scored(self, pos: Point):
        '''returns True if point is within rectangle between two circles'''
        
        p1 = Point(self.pos.getX() - self.width / 2, self.pos.getY() + self.size)
        p2 = Point(self.pos.getX() + self.width / 2, self.pos.getY() - self.size)
        
        if min(p1.getX(), p2.getX()) <= pos.getX() <= max(p1.getX(), p2.getX()) and \
               min(p1.getY(), p2.getY()) <= pos.getY() <= max(p1.getY(), p2.getY()):
            return True
        
        return False


# ------------------------------------------------------------------------------------------------------------------------


class Wall(Line):
    ''' Creates and draws a wall between two points
        
        Attributes:
            p1(Point): first point of the wall
            p2(Point): second point of the wall
            vector(Point): vector from p1 to p2
        
    '''
    
    def __init__(self, p1: Point, p2: Point):
        super().__init__(p1, p2)
        self.p1 = p1
        self.p2 = p2
        self.vector = Point(self.p2.getX() - self.p1.getX(), self.p2.getY() - self.p1.getY())
        
        self.setWidth(5)
        self.setFill(COLOR_WALL)
        
    def distanceTo(self, point: Point):
        '''Calculates a distance to a given point
        
        Args:
            point(Point)
            
        Returns:
            contact_point(Point): point of intersection of wall with a normal vector from a given point
            distance(float): distance between a given point and contact_point
        '''
        
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
    
    
# ------------------------------------------------------------------------------------------------------------------------


class Surface2D(Polygon):
    '''Creates and draws a ploygon from given function y=f(x) in specific range
    
       Attributes:
            formula(function): a fucntion y=f(x) that descibes a top of polygon
            resolution(int): number of lines used to draw a formula
            start(float): start of range where polygon is drawn
            end(float): end of range where polygon is drawn
    '''
    
    def __init__(self, formula, start: int, end: int, resolution=100):
        self.formula = formula
        self.resolution = resolution
        self.start = start
        self.end = end
        
        points = []
        
        # left bottom point
        points.append(Point(start, 0.1))
        
        # left up point
        points.append(Point(start, formula(start)))
        
        # function buttons
        for i in range(1, resolution + 1):
            x = start + i * (abs(end - start) / resolution)
            y = self.formula(x)
            points.append(Point(x,y))    
            
        # right up point
        points.append(Point(end, formula(end)))
        
        # right bottom point
        points.append(Point(end, 0.1))
        
        super().__init__(points)
    
        self.setFill(COLOR_SURFACE)
        self.setOutline(COLOR_WALL)
        self.setWidth(3)
            
    def contains(self, point: Point):
        '''Determines if a given point is inside of a polygon
        
        Args:
            point(Point)
            
        Reruns:
            inside(bool)
        '''
        
        # point
        px = point.getX()
        py = point.getY()
        
        # inicial value
        inside = False
        
        # last vertice
        j = len(self.points)- 1
        
        for i in range(len(self.points)):
            # vertice i of polygon 
            xi = self.points[i].getX()
            yi = self.points[i].getY()
            
            # vertice i polygon
            xj = self.points[j].getX()
            yj = self.points[j].getY()

            # if horizontal line from p is between vetice i and j (crosses edge ij)
            if (yi > py > yj) or (yi < py < yj): 
                
                # x where horizontal line crosses  edge ij
                x_intersect = (xj - xi) * (py - yi) / (yj - yi) + xi
                if px < x_intersect:
                    # flips inside. if number of crossings of ray from point with polygon is odd then point is inside
                    inside = not inside
                    
            # next pair of vertices    
            j = i
            
        return inside
 
    def distanceTo(self, point: Point):
        '''Calculates a shortest distance to a polygon from a given point
        
        Args:
            point(Point)
            
        Returns:
            contact_point(Point): point of intersection of polygon with a line from a given point
            distance(float):
        '''
        
        # point
        px = point.getX()
        py = point.getY()
        
        # inicial values
        best_dist = float('inf')
        contact_point = None
        
        # vertices
        n = len(self.points)
        
        for i in range(n):
            # vertice 1
            ax = self.points[i].getX()
            ay = self.points[i].getY()
            
            # vertice 2
            bx = self.points[(i+1) % n].getX()
            by = self.points[(i+1) % n].getY()
            
            # vector between vertices
            dx = bx - ax
            dy = by - ay
            
            # squares length
            length_sq = dx ** 2 + dy ** 2
            
            # if points are the same
            if length_sq == 0:
                t = 0
            else:
                t = ((px - ax) * dx + (py - ay) * dy) / length_sq
                
                # limit vector in edge
                t = max(0.0, min(1.0, t))
            
            # contact point
            cx = ax + t * dx
            cy = ay + t * dy
            
            dist = np.sqrt((px-cx) ** 2 + (py - cy) ** 2)
            
            # comparing with best distance
            if dist < best_dist:
                best_dist = dist
                contact_point = Point(cx, cy)

        # detecting if point is within polygon
        signed_dist = best_dist if not self.contains(point) else - best_dist
            
        return contact_point, signed_dist
 
 
# ------------------------------------------------------------------------------------------------------------------------

 
class Surface3D:
    '''Creates and draws projection of a 3D surface on a plane representing height in color gradient
    
        Attributes:
            pos0(Point): position of the origin for a surface
            formula(function): formula that describes a surface
            resolution(int): number of rectangles by height
            gradient_start(list(int)): list of RGB values of darkest color
            gradient_end(list(int)): list of RGB values of brightest color
    '''
    
    def __init__(self, pos0: Point, formula, resolution: int):
        self.pos0 = pos0
        self.formula = formula
        self.resolution = resolution
        self.gradient_start = (16, 44, 15)       
        self.gradient_end = (140, 210, 50)       

    def draw(self, window: GraphWin):
        # get window coordinates
        xlow, yhigh = window.toWorld(0, 0)
        xhigh, ylow = window.toWorld(window.getWidth(), window.getHeight())
        width = xhigh - xlow
        height = yhigh - ylow
        
        # origin
        x0 = self.pos0.getX()
        y0 = self.pos0.getY()
    
        # mesh aka matrix representing surface
        x = np.linspace(x0 - width / 2, x0 + width / 2, (self.resolution * 16 + 1))
        y = np.linspace(y0 - height / 2, y0 + height / 2, (self.resolution * 9 + 1))
        X, Y = np.meshgrid(x, y)
        Z = np.asarray(self.formula(X - x0, Y - y0))
        
        self.X = X
        self.Y = Y
        self.Z = Z
        
        Z_range = Z.max() - Z.min()
        if Z_range == 0: Z_range = 1  
        
        # number of colors    
        steps = 50
        palette = []
        
        # generating palette with linear interpolation
        for i in range(steps):
            # step 
            x = i / (steps - 1)
            
            # color channels
            r = int(self.gradient_start[0] + (self.gradient_end[0] - self.gradient_start[0]) * x)
            g = int(self.gradient_start[1] + (self.gradient_end[1] - self.gradient_start[1]) * x)
            b = int(self.gradient_start[2] + (self.gradient_end[2] - self.gradient_start[2]) * x)
            palette.append(color_rgb(r, g, b))
        
        # drawing rectangles acording to mesh
        for i in range(self.resolution * 9):
            for j in range(self.resolution * 16):
                p1 = Point(X[i, j], Y[i, j])
                p2 = Point(X[i+1, j+1], Y[i+1, j+1])
                rect = Rectangle(p1, p2)
                                
                z = (Z[i, j] - Z.min()) / Z_range
                color_index = int(z * (steps - 1))
                color_index = max(0, min(color_index, steps - 1))
                color = palette[color_index]
                
                rect.setFill(color)
                rect.setOutline(color)  
                rect.draw(window)
                
    def getGradient(self, point: Point):
        '''Calculates gradient of the function in a given point
        '''
        px = point.getX() - self.pos0.getX()
        py = point.getY() - self.pos0.getY()
        h = 1e-5
        
        df_dx = (self.formula(px + h, py) - self.formula(px - h, py)) / (2 * h)
        df_dy = (self.formula(px, py + h) - self.formula(px, py - h)) / (2 * h)
    
        return Point(df_dx, df_dy) 
    
    def getMinimum(self):
        '''Calculates minimum of a function
        '''
        
        index = np.argmin(np.abs(self.Z - self.Z.min()))
        index = np.unravel_index(index, self.Z.shape)
        return Point(float(self.X[index]), float(self.Y[index]))
       


# ------------------------------------------------------------------------------------------------------------------------


class Simulation(GraphWin):
    '''Main class responsible of simulation process. Creates a window with simulation status indicator and quit button.
    Draws objects, moves them and resolve collision
    
        Attributes:
            title(str): name of the window
            width(int): width of the window
            height(int): height of the window
            dt(float): delta time (step) for each frame of simulation
            elacticity(float): constant that defines bounciness of objects
            friction(float): constant that defines lost of energy in simulation
            dynamic_objects(list()): list of all dynamic (moveable) objects in simulation
            static_objects(list()): list of all dynamic (not moveable) objects in simulation
            frozen(bool): status of simulation. If True all dynamic objects are stopped and collision logic is disabled
    '''
    

    def __init__(self, title: str, width=1280, height=720, dt = 1/ 60, elacticity=0, friction = 0):
        super().__init__(title, width, height, autoflush=False)
        self.setCoords(0, 0, 16, 9)
        self.dt0 = dt
        self.dt = dt
        self.dynamic_objects = []
        self.static_objects = []
        self.elacticity = elacticity
        self.friction = friction 
        self.frozen = False
        
        self.setBackground('white')
        
        # quit button
        self.btn_quit = Button(Point(0.25, 8.75), Point(1, 8.25), 'QUIT', action=lambda: self.close())
        self.btn_quit.draw(self)
        
        # round indicator in right upper corner
        self.indicator = Circle(Point(15.7, 8.7), 0.1)
        self.indicator.setFill('green')
        self.indicator.setWidth(0)
        self.indicator.draw(self)
    
    def indicatorOn(self):
        self.indicator.setFill('green')
        
    def indicatorOff(self):
        self.indicator.setFill('red')
    
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
        if self.frozen: return
        
        tick_start = time.perf_counter()
        for obj in self.dynamic_objects:
            if isinstance(obj, Ball):
                obj.step(self.dt)
        update(1 / self.dt)
        
        # corrects time tick if elapsed time is less than dt
        elapsed = time.perf_counter() - tick_start
        remaining = self.dt - elapsed
        
        if remaining > 0:
            time.sleep(remaining)
            
        if self.isOpen():
            self.btn_quit.undraw(self)
            self.btn_quit.draw(self)
            self.indicator.undraw()
            self.indicator.draw(self)
                
    def freeze(self):
        self.indicatorOff()
        self.frozen = True

    def defreeze(self): 
        self.frozen = False
        self.indicatorOn()
        
    def isFrozen(self):
        return self.frozen
    
    def collisionWithStaticObject(self, ball: Ball, object): 
        '''resolves collision between ball and static objects. Also sets new velocity for a ball based on normal tangent components'''
               
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
        
        # skip if ball moving from the surface
        if v_normal >= 0: return
        
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
   
    def collisionWithDynamicObject(self, ball1: Ball, ball2: Ball):
        '''resolves collision between two balls. Also sets new velocity for a ball based on normal tangent components'''

        if self.frozen: return
        
        # vector between centers of two balls
        dx = ball2.getPos().getX() - ball1.getPos().getX()
        dy = ball2.getPos().getY() - ball1.getPos().getY()
        
        # distance between centers of balls in moment of a collision
        collision_distance = ball1.getSize() + ball2.getSize()

        # if balls are too far stop collision resolving
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

        # symetric impluse for two balls
        impulse = rel_vx * nx + rel_vy * ny
        impulse *= 0.85
        if impulse < 0: return

        # set new velocities
        ball1.setVel(Point(ball1.vel.getX() - impulse * nx, ball1.vel.getY() - impulse * ny))
        ball2.setVel(Point(ball2.vel.getX() + impulse * nx, ball2.vel.getY() + impulse * ny))

    def surfaceCollision(self, ball: Ball, surface: Surface3D):
        '''Imiatates a collision between a ball and 3D surface in 2D projection. Uses vector symmetric to a gradient of surface in a point
        '''
        
        if self.frozen: return
        
        # gradient vector
        vector = surface.getGradient(ball.getPos())
        
        # amplifier
        a = 3
        
        # acceleration vector
        vectorx = - vector.getX() * a
        vectory = - vector.getY() * a
        ball.setAcl(Point(vectorx, vectory))
        
        # correct velocity according to friction
        vx = ball.getVel().getX() * (1 - self.friction * self.dt)
        vy = ball.getVel().getY() * (1 - self.friction * self.dt)
        
        ball.setVel(Point(vx, vy))
        
    def checkCollisions(self):
        '''Main collision function. Cycles all objects: dynamic and static and executes collision fucntions according to type of objects
        '''
        if self.frozen: return
        
        # dynamic-static collisions
        for dobj in self.dynamic_objects:
            for sobj in self.static_objects:
                if isinstance(dobj, Ball):
                    if (isinstance(sobj, Wall)) or isinstance(sobj, Hoop) or isinstance(sobj, Surface2D):  
                        self.collisionWithStaticObject(dobj, sobj)
                    if isinstance(sobj, Surface3D):
                        self.surfaceCollision(dobj, sobj)
        
        # dynamic-dynamic collisions          
        n = len(self.dynamic_objects)
        for i in range(n):
            for j in range(i + 1, n): 
                dobj1 = self.dynamic_objects[i]
                dobj2 = self.dynamic_objects[j]
                if isinstance(dobj1, Ball) and isinstance(dobj2, Ball):
                    self.collisionWithDynamicObject(dobj1, dobj2)


# ------------------------------------------------------------------------------------------------------------------------
       

class TrajectoryRecorder:
    '''Records and saves positions of balls in simulation. Calls OS explorer window to choose save path and file name
    
    Attributes:
        n(int): number of balls to record
        dt(flaot): delta time (step) used in recording
        t0(float): time since Epoch in moment of start of simulation
        elapsed_time(float): relative time since start of simulation
        time_log(list(float)): list of time stamps
        x_log(list(list(flaot))): list of lists of x positions of each ball)
        y_log(list(list(flaot))): list of lists of y positions of each ball)
    '''
    
    def __init__(self, n: int, dt):
        self.n = n
        self.dt = dt
        self.t0 = time.time()
        self.elapsed_time = 0
        self.time_log = []
        
        # [[ball 1], [ball2], ...]
        self.x_log = [[] for _ in range(n)]
        self.y_log = [[] for _ in range(n)]
        
    def record(self, balls):
        self.time_log.append(self.elapsed_time)
        self.elapsed_time += self.dt
                
        for i in range(len(balls)):
            if len(balls) == self.n:
              self.x_log[i].append(balls[i].getPos().getX())
              self.y_log[i].append(balls[i].getPos().getY())  
              
            
    def save(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt")

        if not file_path: return
        
        with open(file_path, 'w') as file:
            local_time = time.localtime(self.t0)
            ms = int((self.t0 % 1) * 1000)
            t0_str = f"{time.strftime('%H:%M:%S', local_time)}.{ms:03d}\n"
            
            file.write(f"Start Time: {t0_str}\n")
            file.write("Elapsed Time: " + " ".join(f"{t:.3f}," for t in self.time_log) + "\n")
            
            for i in range(self.n):
                file.write(f"Ball {i+1}: \n")
                file.write(" X Positions:  " + " ".join(f"{x:.3f}," for x in self.x_log[i]) + "\n")
                file.write(" Y Positions:  " + " ".join(f"{y:.3f}," for y in self.y_log[i]) + "\n")
# ------------------------------------------------------------------------------------------------------------------------