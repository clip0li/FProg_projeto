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
                
                scenary1 = Simulation('Cenário 1')
                scenary1.setCoords(0, 0, 16, 9)
                
                counter = Counter(Point(15, 8.5), count=score)
                counter.draw(scenary1)
                
                hoop = Hoop(Point(14, 5), 1, 0.1)
                hoop.draw(scenary1)
                
                stickman = Stickman(Point(1.5, 0), 2.6)
                stickman.draw(scenary1)
                
                ball = Ball(Point(3, height))
                ball.draw(scenary1)
                ball.moveTo(Point(ball.getPos().getX(), ball.getPos().getY() + ball.getSize()))
                
                vx = vel * np.cos(np.radians(angle))
                vy = vel * np.sin(np.radians(angle))
                ball.vel = Point(vx, vy)
                ball.acl = Point(0, -9.8)

                while scenary1.isOpen():
                    mouse = scenary1.checkMouse()
                    
                    if ball.getPos().getY() - ball.getSize() >= 0 \
                       and ball.getPos().getX() + ball.getSize() < 16:
                        ball.step(1/60)
                        update(60)
                        
                    else:
                        if mouse != None:
                            scenary1.close()
                            break
                        
                    if mouse != None:
                        scenary1.checkQuitButton(mouse)
                        
                    if hoop.is_scored(ball.getPos()):
                        counter.change(1)
                        score += 1
            
            main()    
                
                    
        case '2':
            while True:
                dialog = InputDialog(250, 300, ('Height',))
                values = dialog.getValues() 
                
                if values is None: 
                    break 
                    
                height = values
                height = height[0]
                
                scenary2 = Simulation('Cenário 2')
                scenary2.setCoords(0, 0, 16, 9)

                parabola = Parabola(Point(8, 1), 0.25, 10)
                parabola.draw(scenary2)
                
                ball = Ball(Point(0, 0))
                ball.draw(scenary2)
                ball.moveTo(parabola.placeBall(ball, height))
                

                while scenary2.isOpen():
                    mouse = scenary2.checkMouse()
                    
                    if True:
                        #ball.step(1/60)
                        #update(60)
                        pass
                    else:
                        if mouse != None:
                            scenary2.close()
                            break
                        
                    if mouse != None:
                        scenary2.checkQuitButton(mouse)
                        
                    
            
            main()
    
        case '3':
            pass
        
        case '4':
            scenary4 = Simulation('Cenário 2')
            parabola = Parabola(Point(8, 1), 0.25, 10)
            scenary4.addObject(parabola)
    
            while scenary4.isOpen():
                
                mouse = scenary4.checkMouse()
                if mouse:
                    scenary4.checkQuitButton(mouse)
                    
                    ball = Ball(mouse)
                    scenary4.addObject(ball)
                
                scenary4.run_step(1/60)
                
                
def randomize(value, percentage = 0):
    return value + random.uniform(- value * percentage, value * percentage)
     
     
main()