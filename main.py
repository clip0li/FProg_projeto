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
                dialog = InputDialog(250, 300, ('Velocity', 'Angle', 'Height'))
                values = dialog.getValues() 
                
                if values is None: 
                    break 
                    
                vel, angle, height = values
                vel = randomize(vel)
                angle = randomize(angle)
                
                scenary1 = Simulation('Cenário 1', elacticity=0.5, friction=0.5)
                
                counter = Counter(Point(15, 8.5), 'Score', score)
                scenary1.addStaticObject(counter)
                
                hoop = Hoop(Point(14, 5), 1, 0.1)
                scenary1.addStaticObject(hoop)
                
                stickman = Stickman(Point(1.5, 0.1), 2.6)
                scenary1.addStaticObject(stickman)
                
                wall1 = Wall(Point(0.1, 0.1), Point(15.9, 0.1))
                scenary1.addStaticObject(wall1)
                wall2 = wall1 = Wall(Point(0.1, 0.1), Point(0.1, 20))
                scenary1.addStaticObject(wall2)
                wall3 = wall2 = wall1 = Wall(Point(15.9, 0.1), Point(15.9, 20))
                scenary1.addStaticObject(wall3)
                
                
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
                    
                    scenary1.checkCollisions()
                    scenary1.tick()
                    
                    if np.sqrt(ball.getVel().getX() ** 2 + ball.getVel().getY() ** 2) < 0.1:
                        scenary1.close()
                        
                    if mouse != None:
                        scenary1.checkQuitButton(mouse)
                        
                    if hoop.is_scored(ball.getPos()) and not scored:
                        counter.change(2)
                        score += 2
                        scored = True
                
                scored = False
                
            main()    
                
                    
        case '2':
            while True:
                dialog = InputDialog(250, 300, ('Height',))
                values = dialog.getValues() 
                
                if values == None: break 
                    
                height = values[0]
                
                scenary2 = Simulation('Cenário 2', dt=1/60)
                
                parabola = Parabola(Point(8, 1), 0.25, 5, 5)
                scenary2.addStaticObject(parabola)
                
                y = height + parabola.getPos().getY()
                x = parabola.equationGetX(height) + parabola.getPos().getX()
                
                ball = Ball(Point(x, y))
                ball.setAcl(Point(0, -9.8))
                scenary2.addDynamicObject(ball)

                while scenary2.isOpen():
                    mouse = scenary2.checkMouse()
                    if mouse != None:
                        scenary2.checkQuitButton(mouse)
                        
                        if parabola.equationGetY(mouse.getX()) < mouse.getY():
                            ball.setPos(mouse)
                            ball.setVel(Point(0, 0))
                            ball.setAcl(Point(0,-9.8))
                
                    scenary2.checkCollisions()
                    scenary2.tick()
                    
                    if ball.getPos().getY() <= 0:
                        scenary2.close()
                     
            main()
    
        case '3':

            scenary3 = Simulation('Cenário 3', dt=1/60)
            
            parabola = Parabola(Point(5.1, 0.1), 0.25, 5, 2)
            scenary3.addStaticObject(parabola)
            
            wall1 = Wall(Point(0.1, 0.1), Point(15.9, 0.1))
            scenary3.addStaticObject(wall1)
            wall2 = wall1 = Wall(Point(0.1, 0.1), Point(0.1, 20))
            scenary3.addStaticObject(wall2)
            wall3 = wall2 = wall1 = Wall(Point(15.9, 0.1), Point(15.9, 20))
            scenary3.addStaticObject(wall3)
            
            while scenary3.isOpen():
                mouse = scenary3.checkMouse()
                if mouse != None:
                    scenary3.checkQuitButton(mouse)
                       
            main()
            
        case '4':
            pass
                
                
def randomize(value, percentage = 0.07):
    return value + random.uniform(- value * percentage, value * percentage)
     
     
main()