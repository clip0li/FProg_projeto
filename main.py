from graphics import *
from gui import *
from simulation import *
import random

def main():
    slct_win = SelectionWindow(400)

    match slct_win.select():
        case '1':
            pass
                    
        case '2':
            input_dialog = InputDialog(200, 300, ('Velocity', 'Angle', 'Height'))
            
        case '3': print(3)
        
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