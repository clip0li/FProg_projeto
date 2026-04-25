from graphics import *
from gui import *
from simulation import *
import random

def main():
    slct_win = SelectionWindow(400)

    match slct_win.select():
        case '1':
            dialog = InputDialog(200, 300, ('Velocity', 'Angle', 'Height'))
            values = dialog.getValues()
            
            if values == None:
                main()
            
            
            vel, angle, height, = values
            
            sim = Simulation('1')
            
            ball = Ball(Point(1, height))
            ball.setAcl(Point(0,-9.8))
            sim.addObject(ball)
            
            hoop = Hoop(Point(12,4), 1, 0.1)
            sim.addObject(hoop)
            
            ball.launch(vel, angle)
            
                    
        case '2':
            pass
    
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

main()