from graphics import *
from gui import *
from simulation import *
import random

def main():
    slct_win = SelectionWindow(400)

    match slct_win.select():
        case '1':
            score = 0
            # 12 45 2
            while True:
                dialog = InputDialog(250, 300, (('Velocity', 20), ('Angle', 90), ('Height', 7)))
                values = dialog.getValues() 
                if values is None: break 
                    
                vel, angle, height = values
                vel = randomize(vel, 0.02)
                angle = randomize(angle, 0.05)
                
                scenary1 = Simulation('Cenário 1', elacticity=0.5, friction=0.5)
                recorder = TrajectoryRecorder()

                counter = Counter(Point(2, 8.5), 'Score', score)
                scenary1.addStaticObject(counter)
                
                hoop = Hoop(Point(14, 5), 1, 0.1)
                scenary1.addStaticObject(hoop)
                
                stickman = Stickman(Point(1.5, 0.15), 3)
                scenary1.addStaticObject(stickman)
                
                wall1 = Wall(Point(0.1, 0.1), Point(15.9, 0.1))
                scenary1.addStaticObject(wall1)
                wall2 = Wall(Point(0.1, 8.9), Point(0.1, 0.1))
                scenary1.addStaticObject(wall2)
                wall3 = Wall(Point(15.9, 0.1), Point(15.9, 8.9))
                scenary1.addStaticObject(wall3)
                
                wall4 = Wall(Point(15.9, 8.9), Point(0.1, 8.9))
                scenary1.addStaticObject(wall4)
                
                ball = Ball(Point(3, height+0.1))
                scenary1.addDynamicObject(ball)
                ball.setPos(Point(ball.getPos().getX(), ball.getPos().getY() + ball.getSize()))
                vx = vel * np.cos(np.radians(angle))
                vy = vel * np.sin(np.radians(angle))
                ball.setVel(Point(vx, vy))
                ball.setAcl(Point(0, -9.8))

                scored = False
                
                while scenary1.isOpen():
                    mouse = scenary1.checkMouse()
                    key = scenary1.checkKey()
    
                    if mouse != None:
                        scenary1.checkQuitButton(mouse)
                        
                    if hoop.is_scored(ball.getPos()) and not scored:
                        counter.change(2)
                        score += 2
                        scored = True

                    if ball.getPos().getY() < ball.getSize() + 0.11: 
                        scenary1.stopped()
                        scenary1.checkCollisions()

                        if key == 'g':
                            recorder.save()
                        if mouse != None:
                            scenary1.close()
                            break
                        
                    else:
                        recorder.record(1/60, ball)
                        scenary1.checkCollisions()
                        scenary1.tick()
                    
                scored = False
                
            main()    
                
                    
        case '2':
            while True:
                dialog = InputDialog(250, 300, (('Height',6.1),))
                values = dialog.getValues() 
                if values == None: break 
                height = values[0]
                
                scenary2 = Simulation('Cenário 2', dt=1/60, friction=0.5, elacticity=0)
                recorder = TrajectoryRecorder()
                
                parabola = Parabola(Point(8, 1), 0.25, 5, 5)
                scenary2.addStaticObject(parabola)
                
                y = height + parabola.getPos().getY()
                x = parabola.equationGetX(height) + parabola.getPos().getX()
                
                ball = Ball(Point(x, y))
                ball.setAcl(Point(0, -9.8))
                scenary2.addDynamicObject(ball)

                while scenary2.isOpen():
                    '''
                    mouse = scenary2.checkMouse()
                    if mouse != None:
                        scenary2.checkQuitButton(mouse)
                        
                        if parabola.equationGetY(mouse.getX()) < mouse.getY():
                            ball.setPos(mouse)
                            ball.setVel(Point(0, 0))
                            ball.setAcl(Point(0,-9.8))
                    '''
                    key = scenary2.checkKey()
                    mouse = scenary2.checkMouse()    
                    
                    if mouse != None:
                        scenary2.checkQuitButton(mouse)
                        
                    if ball.getPos().getY() <= 0 or \
                    (ball.getSpeed() < 0.17 and ball.getPos().getY() < parabola.getPos().getY() + 1.0001 * ball.getSize()):
                        scenary2.stopped()
                
                        if key == 'g':
                            recorder.save()
                            scenary2.close()
                            break
                        if mouse != None:
                            scenary2.close()
                            break
                        
                    
                    else:
                        recorder.record(1/60, ball)
                        scenary2.checkCollisions()
                        scenary2.tick()                      
            main()
    
        case '3':
            
            scenary3 = Simulation('Cenário 3', dt=1/60)
            
            parabola = Parabola(Point(5.1, 0.1), 0.25, 5, 3.5) 
            scenary3.addStaticObject(parabola)
            
            hoop = Hoop(Point(13.9, 5), 1, 0.1)
            scenary3.addStaticObject(hoop)
            
            stickman = Stickman(Point(13, 0.15), 3)
            scenary3.addStaticObject(stickman)
            
            wall1 = Wall(Point(0.1, 0.1), Point(15.9, 0.1))
            scenary3.addStaticObject(wall1)
            wall2 = Wall(Point(0.1, 8.9), Point(0.1, 0.1))
            scenary3.addStaticObject(wall2)
            wall3 = Wall(Point(15.9, 0.1), Point(15.9, 8.9))
            scenary3.addStaticObject(wall3)
            wall4 = Wall(Point(15.9, 8.9), Point(0.1, 8.9))
            scenary3.addStaticObject(wall4)
            
            ball1 = Ball(Point(1, 8))
            ball1.setAcl(Point(0, -9.8))
            scenary3.addDynamicObject(ball1)
            
            ball2 = Ball(Point(12, 2), color='blue')
            ball2.setAcl(Point(0, -9.8))
            scenary3.addDynamicObject(ball2)

            while scenary3.isOpen():
                mouse = scenary3.checkMouse()
                if mouse != None:
                    scenary3.checkQuitButton(mouse)
                  
                scenary3.checkCollisions()
                scenary3.tick()     
            
            
        case '4':
            scenary4 = Simulation('Cenário 3', dt=1/60, elacticity=0.98)
            
            wall1 = Wall(Point(0.1, 0.1), Point(15.9, 0.1))
            scenary4.addStaticObject(wall1)
            wall2 = Wall(Point(0.1, 8.9), Point(0.1, 0.1))
            scenary4.addStaticObject(wall2)
            wall3 = Wall(Point(15.9, 0.1), Point(15.9, 8.9))
            scenary4.addStaticObject(wall3)
            wall4 = Wall(Point(15.9, 8.9), Point(0.1, 8.9))
            scenary4.addStaticObject(wall4)
            
            
            
            while scenary4.isOpen():
                mouse = scenary4.checkMouse()
                key = scenary4.checkKey()
                
                if mouse != None:
                    scenary4.checkQuitButton(mouse)
                
                    for _ in range(100):    
                        color = color_rgb(random.randint(0,255), random.randint(0,255), random.randint(0,255))
                        ball = Ball(Point(random.uniform(1,15),random.uniform(1,8)), color=color)
                        v = 7
                        ball.setVel(Point(random.uniform(-v,v), random.uniform(-v,v)))
                        scenary4.addDynamicObject(ball) 
                scenary4.checkCollisions()
                scenary4.tick()
                       
                       
            main()    
                
def randomize(value, percentage):
    return value + random.uniform(- value * percentage, value * percentage)
          
main()
