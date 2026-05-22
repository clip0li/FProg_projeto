from graphics import *
from gui import *
from simulation import *
import random

slct_win = SelectionWindow(400)

def main():
    match slct_win.select():
        
# ///        
        case '1':
            score_value = 0

            while True:
                # dialog window
                dialog = InputDialog(250, 300, (('Velocity', 0, 20), ('Angle',0, 90), ('Height', 0, 7)))
                values = dialog.getValues() 
                if values is None: break 
                    
                # variables
                vel, angle, height = values
                vel = randomize(vel, 0.02)
                angle = randomize(angle, 0.05)

                # scenario
                scenario1 = Simulation('Scenario 1: Basketball', elacticity=0.85, friction=0.5)
                recorder = TrajectoryRecorder(1, dt=1/60)

                # counters
                score = Counter(Point(2, 8.5), 'Score', score_value)
                scenario1.addStaticObject(score)
                
                # hoop
                hoop = Hoop(Point(14, 5), 1, 0.1)
                scenario1.addStaticObject(hoop)
                
                # stickman
                stickman = Stickman(Point(1.5, 0.15), 3)
                scenario1.addStaticObject(stickman)
                
                # walls
                wall1 = Wall(Point(0.1, 0.1), Point(15.9, 0.1))
                scenario1.addStaticObject(wall1)
                wall2 = Wall(Point(0.1, 8.9), Point(0.1, 0.1))
                scenario1.addStaticObject(wall2)
                wall3 = Wall(Point(15.9, 0.1), Point(15.9, 8.9))
                scenario1.addStaticObject(wall3)
                wall4 = Wall(Point(15.9, 8.9), Point(0.1, 8.9))
                scenario1.addStaticObject(wall4)
                
                # ball
                ball = Ball(Point(3, height))
                scenario1.addDynamicObject(ball)
                ball.setPos(Point(ball.getPos().getX(), ball.getPos().getY() + ball.getSize()))
                vx = vel * np.cos(np.radians(angle))
                vy = vel * np.sin(np.radians(angle))
                ball.setVel(Point(vx, vy))
                ball.setAcl(Point(0, -9.8))
                

                # main scenario loop
                scored = False
                
                while scenario1.isOpen():
                    # inputs
                    mouse = scenario1.checkMouse()
                    key = scenario1.checkKey().lower()

                    if mouse != None:
                        scenario1.checkQuitButton(mouse)
                        
                    if hoop.is_scored(ball.getPos()) and not scored:
                        score.change(2)
                        score_value += 2
                        scored = True

                    if ball.getPos().getY() < ball.getSize() + 0.11: 
                            
                        scenario1.freeze()
                        
                        if key == 'g':
                            recorder.save()
                            scenario1.close()
                        if mouse != None:
                            scenario1.close()
                            break
                        
                    else:
                        recorder.record((ball,))
                        
                    scenario1.checkCollisions()
                    scenario1.tick()    
                    

                scored = False
                
            main()    
                
  # ///                   
        case '2':
            while True:
                # dialog window
                dialog = InputDialog(250, 300, (('Height',0, 6),))
                values = dialog.getValues() 
                if values == None: break
                
                # variables 
                height = values[0]
                
                # scenario
                scenario2 = Simulation('Scenario 2: Parabola', dt=1/60, friction=0.5, elacticity=0)
                recorder = TrajectoryRecorder(1, dt=1/60)
        
                surface = Surface2D(formula = lambda x: 0.25 * (x-8) ** 2 + 1,
                                    start = 3,end = 13)
                
                scenario2.addStaticObject(surface)
                
                # ball position
                x = - np.sqrt(4*(height + 1)-4) + 8 
                y = height + 1.2
                       
                # ball
                ball = Ball(Point(x, y))
                ball.setVel(Point(0,0))
                ball.setAcl(Point(0, -9.8))
                scenario2.addDynamicObject(ball)
                
                # main scenario loop
                while scenario2.isOpen():
                    key = scenario2.checkKey().lower()
                    mouse = scenario2.checkMouse()    
                    
                    if mouse != None:
                        scenario2.checkQuitButton(mouse)
                                                                
                    if ball.getPos().getY() < 1.2001 and ball.getSpeed() < 0.164 or ball.getPos().getY() < 0:
                        scenario2.freeze()
                
                        if key == 'g':
                            recorder.save()
                            scenario2.close()
                            break
                        
                        if mouse != None:
                            scenario2.defreeze()
                            ball.setPos(mouse)
                            ball.setVel(Point(0,0))
                            ball.setAcl(Point(0, -9.8))
                               
                    else:
                        recorder.record((ball,))                   
                            
                    scenario2.checkCollisions()   
                    scenario2.tick() 
            main()
            
# ///   
        case '3':
            score_value = 0
            lives_value = 5
            
            while lives_value > 0:
                # dialog window
                dialog = InputDialog(250, 300, (('Velocity',0, 20), ('Angle',0, 90)))
                values = dialog.getValues() 
                if values is None: break
                
                # randomize values
                vel, angle = values
                vel = randomize(vel, 0.02)
                angle = randomize(angle, 0.05)
                
                # scenario
                scenario3 = Simulation('Scenario 3: Interception', dt=1/60)
                recorder = TrajectoryRecorder(2, dt=1/60)
                
                # counters
                score = Counter(Point(2, 8.5), 'Score', score_value)
                lives = Counter(Point(3.75, 8.5), 'Lives', lives_value)
                scenario3.addStaticObject(score)
                scenario3.addStaticObject(lives)
                
                # surface
                surface = Surface2D(formula = lambda x: 0.25 * (x-5.1) ** 2 + 0.2,
                                    start = 0.1, end = 9)
                scenario3.addStaticObject(surface)
                
                # hoop
                hoop = Hoop(Point(13.5, 5), 1, 0.1)
                scenario3.addStaticObject(hoop)
                
                # stickman
                stickman = Stickman(Point(13, 0.15), 3)
                scenario3.addStaticObject(stickman)
                
                # walls
                wall1 = Wall(Point(0.1, 0.1), Point(15.9, 0.1))
                scenario3.addStaticObject(wall1)
                wall2 = Wall(Point(0.1, 8.9), Point(0.1, 0.1))
                scenario3.addStaticObject(wall2)
                wall3 = Wall(Point(15.9, 0.1), Point(15.9, 8.9))
                scenario3.addStaticObject(wall3)
                wall4 = Wall(Point(15.9, 8.9), Point(0.1, 8.9))
                scenario3.addStaticObject(wall4)
                
                # ball 1
                ball1 = Ball(Point(0.5, 8))
                ball1.setAcl(Point(0, -9.8))
                scenario3.addDynamicObject(ball1)
                
                # ball 2
                ball2 = Ball(Point(12.5, 2), color='blue')
                ball2.setAcl(Point(0, -9.8))
                ball2.setVel(Point(-vel * np.cos(np.radians(angle)), 
                                   vel * np.sin(np.radians(angle))))
                scenario3.addDynamicObject(ball2)
                
                ball1.freeze()

                # main scenario loop
                while scenario3.isOpen():
                    mouse = scenario3.checkMouse()
                    key = scenario3.checkKey().lower()
                    
                    if key == 's':
                        ball1.defreeze()
                    
                    if mouse != None:  
                        scenario3.checkQuitButton(mouse)
                        if scenario3.isFrozen() and ball1.getPos().getY() != 8:
                            score_value += 1
                    
                    if hoop.is_scored(ball1.getPos()):
                        scenario3.close()
                        lives_value -= 1
    

                    if ball1.getSpeed() < 0.5 and ball1.getPos().getY() < 5 and not scenario3.isFrozen:  
                        scenario3.freeze()
                        scenario3.checkCollisions()
                        
                        if key == 'g':
                            recorder.save()
                            scenario3.close()
                            
                    else:
                        recorder.record((ball1, ball2))
                        
                    scenario3.checkCollisions()
                    scenario3.tick()
                    
            main()   
            
# ///
        case '4':
            score_value = 0
            
            while True:
                
                scored = False
                
                
                scenario4 = Simulation('Scenario 4: Mini Golf', dt=1/60, elacticity=0.5, friction=0.25)
                
                surface = Surface3D(pos0 = Point(8, 4.5), 
                                formula = lambda x, y: np.sin(0.6*x) * np.cos(0.6*y) + 0.2*np.sin(1.1*x - 0.5*y) - 0.8*np.exp(-((x-13)**2 + (y-4.5)**2)/2),
                                resolution=70)
                recorder = TrajectoryRecorder(1, dt=1/60)
                
                scenario4.addStaticObject(surface)
                
                score = Counter(Point(2, 8.5), 'Score', score_value)
                scenario4.addStaticObject(score)
                
                hits = Counter(Point(3.75, 8.5), 'Hits')
                scenario4.addStaticObject(hits)

                wall1 = Wall(Point(0.1, 0.1), Point(15.9, 0.1))
                scenario4.addStaticObject(wall1)
                wall2 = Wall(Point(0.1, 8.9), Point(0.1, 0.1))
                scenario4.addStaticObject(wall2)
                wall3 = Wall(Point(15.9, 0.1), Point(15.9, 8.9))
                scenario4.addStaticObject(wall3)
                wall4 = Wall(Point(15.9, 8.9), Point(0.1, 8.9))
                scenario4.addStaticObject(wall4)
                
                hole = Circle(surface.getMinimum(), 0.2)
                hole.setFill('black')
                scenario4.addStaticObject(hole)
                
                ball = Ball(Point(15, 1), color='white', size=0.15)
                ball.setVel(Point(0, 0))
                ball.setAcl(Point(0,0))
                scenario4.addDynamicObject(ball)
                
                while scenario4.isOpen():
                    mouse = scenario4.checkMouse()
                    key = scenario4.checkKey().lower()
                    
                    if mouse != None:
                        scenario4.checkQuitButton(mouse)
                        
                        if ball.isFrozen():
                            ball.defreeze()
                            scenario4.indicatorOn()
                        
                            dx = ball.getPos().getX() - mouse.getX()
                            dy = ball.getPos().getY() - mouse.getY()
                            
                            vel = np.sqrt(dx ** 2 + dy ** 2)
                            vel = min(vel, 7)
                            angle = np.arctan2(dy, dx)
                            
                            ball.setVel(Point(vel * np.cos(angle), vel * np.sin(angle)))

                            hits.change(1)
                            
                    if ball.getSpeed() < 0.1:
                        ball.freeze()
                        scenario4.indicatorOff()

                    
                
                    if np.sqrt((hole.getCenter().getX() - ball.getPos().getX()) ** 2 + (hole.getCenter().getY() - ball.getPos().getY())** 2) <= hole.getRadius() and not scored:
                        score_value += 1
                        score.change(1)
                        scored = True
                        
                        scenario4.freeze()
                    
                    else:
                        recorder.record((ball,))
                        
                    if key == 'g' and scored:
                        recorder.save()
                        scenario4.close()
                                   
                    scenario4.checkCollisions()
                    scenario4.tick()
                    
                break
            
            main()    


  
def randomize(value, percentage):
    return value + random.uniform(- value * percentage, value * percentage)
         
 

         
main()
