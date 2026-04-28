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
                ball.setPos(Point(ball.getPos().getX(), ball.getPos().getY() + ball.getSize()))
                
                vx = vel * np.cos(np.radians(angle))
                vy = vel * np.sin(np.radians(angle))
                ball.setVel(Point(vx, vy))
                ball.setAcl(Point(0, -9.8))
                
                scored = False
                
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
                
                if values is None: 
                    break 
                    
                height = values
                height = height[0]
                
                scenary2 = Simulation('Cenário 2')
                scenary2.setCoords(0, 0, 16, 9)

                parabola = Parabola(Point(8, 1), 0.25, 15)
                parabola.draw(scenary2)
                
                y = height + parabola.getPos().getY()
                x = parabola.equationGetX(height) + parabola.getPos().getX()
                
                
                ball = Ball(Point(x, y))
                ball.draw(scenary2)
                ball.setAcl(Point(0, -9.8))

                while scenary2.isOpen():
                    mouse = scenary2.checkMouse()
                    
                    dt = 1/60

                    collision_point, distance = parabola.distanceTo(ball.getPos())
                        
                    if distance <= ball.getSize():
                        parabola.checkCollision(ball, collision_point,
                                                friction=0.2,
                                                bounciness=0,
                                                dt = dt)
                    ball.step(dt)   
                    update(1 / dt)
                    
                    if mouse != None:
                        scenary2.checkQuitButton(mouse)
                        
                        '''
                        if parabola.equationGetY(mouse.getX()) < mouse.getY():
                            ball.setPos(mouse)
                            ball.setVel(Point(0, 0))
                            ball.setAcl(Point(0,-9.8))
                        '''
                        
            main()
    
        case '3':
            pass
        
        case '4':
            pass
                
                
def randomize(value, percentage = 0.15):
    return value + random.uniform(- value * percentage, value * percentage)
     
     
main()