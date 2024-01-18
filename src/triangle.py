import math
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from trig import Trigonometry, TrigLaw

class Triangle:
    '''
    Class that represrnets a triangle.
    It is used to calculate the missing sides and angles of a triangle.
    It also calculates the vertices of the triangle based on the sides and angles.
    '''
    def __init__(self, a=None, b=None, c=None, A=None, B=None, C=None, law=None):
        '''
        Initializes the triangle with the given sides and angles.
        It converts the angles from degrees to radians.
        It then calculates the missing sides and angles of the triangle.
        '''
        self.lawsUsed = [] # list of laws used to calculate the triangle
        self.errorMessage = None # error message to be displayed in the GUI

        self.a = a
        self.b = b
        self.c = c
        self.A = math.radians(A) if A is not None else None 
        self.B = math.radians(B) if B is not None else None
        self.C = math.radians(C) if C is not None else None
        
        self.calculateTriangle(law)      

    def calculateTriangle(self, law: TrigLaw):
        '''
        Calculates the missing sides and angles of the triangle using the chosen trigonometric law.
        '''
        try:
            sides = [self.a, self.b, self.c]
            angles = [self.A, self.B, self.C]
            
            numSides = sum(side is not None for side in sides)
            numAngles = sum(angle is not None for angle in angles)
            
            if numAngles + numSides < 3:
                self.errorMessage = 'Need at least 3 properties to define a unique triangle!' # less than 3 properties is not a unique triangle
                return
            
            elif numAngles == 3 and numSides == 0:
                self.errorMessage = '3 angles dont determine a unique triangle!' # three angles don't determine a unique triangle
                return
            
            try:
                if law == TrigLaw.SOH:
                    self.solveSOH()
                elif law == TrigLaw.CAH:
                    self.solveCAH()
                elif law == TrigLaw.TOA:
                    self.solveTOA()
                elif law == TrigLaw.SINE_LAW:
                    self.solveSineLaw()
                elif law == TrigLaw.COSINE_LAW:
                    self.solveCosineLaw()
                    
                if (self.A is not None and self.B is not None and self.C is not None):                     
                    if abs(self.A) + abs(self.B) + abs(self.C) > math.pi:
                        print(self.A, self.B, self.C)
                        self.errorMessage = 'Angles can\'t add up to more than 180 degrees!'
            except ValueError as e:
                self.errorMessage = 'Not correct dimensions for a triangle!'
                
        except ValueError as e:
            self.errorMessage = 'Not correct dimensions for a triangle!'

    def triangleSumTheoremString(self, angle1, angle2, angleCalc):
        '''
        Returns triangle sum theorem string to be displayed in the GUI.
        '''
        angle1Val = self.formatValue(math.degrees(getattr(self, angle1)))
        angle2Val = self.formatValue(math.degrees(getattr(self, angle2)))
        angleCalcVal = self.formatValue(math.degrees(getattr(self, angleCalc)))

        return (
            f'We use the triangle sum theorem to calculate ∠{angleCalc}:<br>'
            f'∠{angleCalc} = 180° - (∠{angle1} - ∠{angle2})<br>'
            f'=> ∠{angleCalc} = 180° - ({angle1Val}° - {angle2Val}°)<br>'
            f'=> ∠{angleCalc} = {angleCalcVal}°<br>'
        )
    
    def pythagorasTheoremPlusString(self, side1, side2, sideCalc):
        '''
        Returns pythagoras theorem string to be displayed in the GUI.
        '''
        side1Val = self.formatValue(getattr(self, side1))
        side2Val = self.formatValue(getattr(self, side2))
        sideCalcVal = self.formatValue(getattr(self, sideCalc))

        return (
            f'We use Pythagoras theorem to calculate side {sideCalc}:<br>'
            f'{sideCalc}² = {side1}² + {side2}²<br>'
            f'=> {sideCalc} = sqrt({side1}² + {side2}²)<br>'
            f'=> {sideCalc} = sqrt({side1Val}² + {side2Val}²)<br>'
            f'=> {sideCalc} = {sideCalcVal}<br>'
        )
    
    def pythagorasTheoremMinusString(self, side1, side2, sideCalc):
        '''
        Returns pythagoras theorem string to be displayed in the GUI.
        '''
        side1Val = self.formatValue(getattr(self, side1))
        side2Val = self.formatValue(getattr(self, side2))
        sideCalcVal = self.formatValue(getattr(self, sideCalc))

        return (
            f'We use Pythagoras theorem to calculate side {sideCalc}:<br>'
            f'{sideCalc}² = {side1}² - {side2}²<br>'
            f'=> {sideCalc} = sqrt({side1}² - {side2}²)<br>'
            f'=> {sideCalc} = sqrt({side1Val}² - {side2Val}²)<br>'
            f'=> {sideCalc} = {sideCalcVal}<br>'
        )

    def sohSideHString(self, sideOpposite, sideCalc, knownAngle):
        '''
        Returns SOH string to be displayed in the GUI.
        Hypotenuse and an angle is known and the side opposite to the angle is calculated.
        '''
        sideOppositeVal = self.formatValue(getattr(self, sideOpposite))
        sideCalcVal = self.formatValue(getattr(self, sideCalc))
        knownAngleVal = self.formatValue(math.degrees(getattr(self, knownAngle)))

        return (
            f'We use SOH to calculate side {sideCalc}:<br>'
            f'sin({knownAngle}) = {sideOpposite} / {sideCalc}<br>'
            f'=> {sideCalc} = {sideOpposite} / sin({knownAngle})<br>'
            f'=> {sideCalc} = {sideOppositeVal} / sin({knownAngleVal}°)<br>'
            f'=> {sideCalc} = {sideCalcVal}<br>'
        )  
    
    def sohSideOString(self, sideHypotenuse, sideCalc, knownAngle):
        '''
        Returns SOH string to be displayed in the GUI.
        An angle and the side opposite to it is known and the hypotenuse is calculated.
        '''
        sideHypotenuseVal = self.formatValue(getattr(self, sideHypotenuse))
        sideCalcVal = self.formatValue(getattr(self, sideCalc))
        knownAngleVal = self.formatValue(math.degrees(getattr(self, knownAngle)))

        return (
            f'We use SOH to calculate side {sideCalc}:<br>'
            f'sin({knownAngle}) = {sideCalc} / {sideHypotenuse}<br>'
            f'=> {sideCalc} = {sideHypotenuse} * sin({knownAngle})<br>'
            f'=> {sideCalc} = {sideHypotenuseVal} * sin({knownAngleVal}°)<br>'
            f'=> {sideCalc} = {sideCalcVal}<br>'
        )
    
    def sohAngleString(self, sideOpposite, sideHypotenuse, angleCalc):
        '''
        Returns SOH string to be displayed in the GUI.
        Side opposite to an angle and the hypotenuse is known and that angle is calculated.
        '''
        sideOppositeVal = self.formatValue(getattr(self, sideOpposite))
        sideHypotenuseVal = self.formatValue(getattr(self, sideHypotenuse))
        angleCalcVal = self.formatValue(math.degrees(getattr(self, angleCalc)))

        return (
            f'We use SOH to calculate ∠{angleCalc}:<br>'
            f'sin({angleCalc}) = {sideOpposite} / {sideHypotenuse}<br>'
            f'=> ∠{angleCalc} = sin⁻¹({sideOpposite} / {sideHypotenuse})<br>'
            f'=> ∠{angleCalc} = sin⁻¹({sideOppositeVal} / {sideHypotenuseVal})<br>'
            f'=> ∠{angleCalc} = {angleCalcVal}°<br>'
        )
        
    def solveSOH(self):
        '''
        Solves the triangle using the SOH (Sine = Opposite / Hypotenuse) rule for specific cases.
        Sets an error message if the given input cannot be resolved using this rule.
        '''
        if self.A is None or self.A != math.pi/2:
            self.errorMessage = 'Angle A must be 90 degrees for SOH calculations' # just in case            

        if self.B is None and self.C is None:
            if self.a is not None and self.b is not None:
                self.B = Trigonometry.soh(h = self.a, o = self.b)
                self.C = Trigonometry.triangleSumTheorem(A=self.A, B=self.B)
                self.c = Trigonometry.soh(h = self.a, theta = self.C)
                self.lawsUsed.append(self.sohAngleString('b', 'a', 'B'))
                self.lawsUsed.append(self.triangleSumTheoremString('A', 'B', 'C'))
                self.lawsUsed.append(self.sohSideOString('a', 'c', 'C'))                
            elif self.a is not None and self.c is not None:
                self.C = Trigonometry.soh(h = self.a, o = self.c)
                self.B = Trigonometry.triangleSumTheorem(A=self.A, B=self.C)
                self.b = Trigonometry.soh(h = self.a, theta = self.B)  
                self.lawsUsed.append(self.sohAngleString('c', 'a', 'C'))
                self.lawsUsed.append(self.triangleSumTheoremString('A', 'C', 'B'))
                self.lawsUsed.append(self.sohSideOString('a', 'b', 'B'))             
            elif self.b is not None and self.c is not None:
                self.a = Trigonometry.pythagorasTheorem(o = self.b, a = self.c)
                self.B = Trigonometry.soh(h = self.a, o = self.b)
                self.C = Trigonometry.triangleSumTheorem(A=self.A, B=self.B)
                self.lawsUsed.append(self.pythagorasTheoremPlusString('b', 'c', 'a'))
                self.lawsUsed.append(self.sohAngleString('b', 'a', 'B'))
                self.lawsUsed.append(self.triangleSumTheoremString('A', 'B', 'C'))
            else:
                self.errorMessage = 'Cannot calculate, use other law!'
                
        elif (self.B is None and self.C is not None) or (self.C is None and self.B is not None):    
            if self.B is None and self.C is not None:
                self.B = Trigonometry.triangleSumTheorem(A=self.A, B=self.C)
                self.lawsUsed.append(self.triangleSumTheoremString('A', 'C', 'B'))
            elif self.C is None and self.B is not None:
                self.C = Trigonometry.triangleSumTheorem(A=self.A, B=self.B)
                self.lawsUsed.append(self.triangleSumTheoremString('A', 'B', 'C'))

            if self.a is not None:                
                self.b = Trigonometry.soh(h = self.a, theta = self.B)
                self.c = Trigonometry.soh(h = self.a, theta = self.C)
                self.lawsUsed.append(self.sohSideHString('a', 'b', 'B'))
                self.lawsUsed.append(self.sohSideHString('a', 'c', 'C'))                
            elif self.b is not None:                
                self.a = Trigonometry.soh(o = self.b, theta=self.B)
                self.c = Trigonometry.soh(h = self.a, theta=self.C)
                self.lawsUsed.append(self.sohSideOString('b', 'a', 'A'))
                self.lawsUsed.append(self.sohSideHString('a', 'c', 'C'))                
            elif self.c is not None:
                self.a = Trigonometry.soh(o = self.c, theta = self.C)
                self.b = Trigonometry.soh(h = self.a, theta = self.B)
                self.lawsUsed.append(self.sohSideOString('c', 'a', 'A'))
                self.lawsUsed.append(self.sohSideHString('a', 'b', 'B'))
            else:
                self.errorMessage = 'Cannot calculate, use other law!'
                
        else:
            self.errorMessage = 'Cannot calculate, use other law!' # just in case
            

    def cahSideHString(self, sideAdjacent, sideCalc, knownAngle):
        '''
        Returns CAH string to be displayed in the GUI.
        Hypotenuse and an angle is known and the side adjacent to the angle is calculated.
        '''
        sideAdjacentVal = self.formatValue(getattr(self, sideAdjacent))
        sideCalcVal = self.formatValue(getattr(self, sideCalc))
        knownAngleVal = self.formatValue(math.degrees(getattr(self, knownAngle)))

        return (
            f'We use CAH to calculate side {sideCalc}:<br>'
            f'cos({knownAngle}) = {sideAdjacent} / {sideCalc}<br>'
            f'=> {sideCalc} = {sideAdjacent} / cos({knownAngle})<br>'
            f'=> {sideCalc} = {sideAdjacentVal} / cos({knownAngleVal}°)<br>'
            f'=> {sideCalc} = {sideCalcVal}<br>'
        )
    
    def cahSideAString(self, sideHypotenuse, sideCalc, knownAngle):
        '''
        Returns CAH string to be displayed in the GUI.
        An angle and the hypotenuse is known and the side adjacent to the angle is calculated.
        '''
        sideHypotenuseVal = self.formatValue(getattr(self, sideHypotenuse))
        sideCalcVal = self.formatValue(getattr(self, sideCalc))
        knownAngleVal = self.formatValue(math.degrees(getattr(self, knownAngle)))

        return (
            f'We use CAH to calculate side {sideCalc}:<br>'
            f'cos({knownAngle}) = {sideCalc} / {sideHypotenuse}<br>'
            f'=> {sideCalc} = {sideHypotenuse} * cos({knownAngle})<br>'
            f'=> {sideCalc} = {sideHypotenuseVal} * cos({knownAngleVal}°)<br>'
            f'=> {sideCalc} = {sideCalcVal}<br>'
        )
    
    def cahAngleString(self, sideAdjacent, sideHypotenuse, angleCalc):
        '''
        Returns CAH string to be displayed in the GUI.
        Side adjacent to an angle and the hypotenuse is known and that angle is calculated.
        '''
        sideAdjacentVal = self.formatValue(getattr(self, sideAdjacent))
        sideHypotenuseVal = self.formatValue(getattr(self, sideHypotenuse))
        angleCalcVal = self.formatValue(math.degrees(getattr(self, angleCalc)))

        return (
            f'We use CAH to calculate ∠{angleCalc}:<br>'
            f'cos({angleCalc}) = {sideAdjacent} / {sideHypotenuse}<br>'
            f'=> {angleCalc} = cos⁻¹({sideAdjacent} / {sideHypotenuse})<br>'
            f'=> {angleCalc} = cos⁻¹({sideAdjacentVal} / {sideHypotenuseVal})<br>'
            f'=> {angleCalc} = {angleCalcVal}°<br>'
        )
    
    def solveCAH(self):
        '''
        Solves the triangle using the CAH (Cosine = Adjacent / Hypotenuse) rule for specific cases.
        Sets an error message if the given input cannot be resolved using this rule.
        '''
        if self.A is None or self.A != math.pi/2:
            self.errorMessage = 'Angle A must be 90 degrees for CAH calculations'            
        
        if self.B is None and self.C is None:
            if self.a is not None and self.b is not None:
                self.C = Trigonometry.cah(h = self.a, a = self.b)
                self.B = Trigonometry.triangleSumTheorem(A=self.A, B=self.C)
                self.c = Trigonometry.cah(h = self.a, theta = self.B)
                self.lawsUsed.append(self.cahAngleString('b', 'a', 'C'))
                self.lawsUsed.append(self.triangleSumTheoremString('A', 'C', 'B'))
                self.lawsUsed.append(self.cahSideAString('a', 'c', 'B'))
            elif self.a is not None and self.c is not None:
                self.B = Trigonometry.cah(h = self.a, a = self.c)
                self.C = Trigonometry.triangleSumTheorem(A=self.A, B=self.B)
                self.b = Trigonometry.cah(h = self.a, theta = self.C)
                self.lawsUsed.append(self.cahAngleString('c', 'a', 'B'))
                self.lawsUsed.append(self.triangleSumTheoremString('A', 'B', 'C'))
                self.lawsUsed.append(self.cahSideAString('a', 'b', 'C'))
            elif self.b is not None and self.c is not None:
                self.a = Trigonometry.pythagorasTheorem(o = self.b, a = self.c)
                self.C = Trigonometry.cah(h = self.a, a = self.b)
                self.B = Trigonometry.triangleSumTheorem(A=self.A, B=self.C)
                self.lawsUsed.append(self.pythagorasTheoremPlusString('b', 'c', 'a'))
                self.lawsUsed.append(self.cahAngleString('b', 'a', 'C'))
                self.lawsUsed.append(self.triangleSumTheoremString('A', 'C', 'B'))
        elif (self.B is None and self.C is not None) or (self.C is None and self.B is not None):    
            if self.B is None and self.C is not None:
                self.B = Trigonometry.triangleSumTheorem(A=self.A, B=self.C)
                self.lawsUsed.append(self.triangleSumTheoremString('A', 'C', 'B'))
            elif self.C is None and self.B is not None:
                self.C = Trigonometry.triangleSumTheorem(A=self.A, B=self.B)
                self.lawsUsed.append(self.triangleSumTheoremString('A', 'B', 'C'))
            if self.a is not None:
                self.b = Trigonometry.cah(h = self.a, theta = self.C)
                self.c = Trigonometry.cah(h = self.a, theta = self.B)
                self.lawsUsed.append(self.cahSideAString('a', 'b', 'C'))
                self.lawsUsed.append(self.cahSideAString('a', 'c', 'B'))
            elif self.b is not None:
                self.a = Trigonometry.cah(a = self.b, theta = self.C)
                self.c = Trigonometry.cah(h = self.a, theta = self.B)
                self.lawsUsed.append(self.cahSideHString('b', 'a', 'C'))
                self.lawsUsed.append(self.cahSideAString('a', 'c', 'B'))
            elif self.c is not None:
                self.a = Trigonometry.cah(a = self.c, theta = self.B)
                self.b = Trigonometry.cah(h = self.a, theta = self.C)
                self.lawsUsed.append(self.cahSideHString('c', 'a', 'B'))
                self.lawsUsed.append(self.cahSideAString('a', 'b', 'C'))
        else:
            self.errorMessage = 'Cannot calculate, use other law!'
            

    def toaSideAString(self, sideOpposite, sideCalc, knownAngle):
        '''
        Returns TOA string to be displayed in the GUI.
        Adjacent side and an angle is known and the side opposite to the angle is calculated.
        '''
        sideOppositeVal = self.formatValue(getattr(self, sideOpposite))
        sideCalcVal = self.formatValue(getattr(self, sideCalc))
        knownAngleVal = self.formatValue(math.degrees(getattr(self, knownAngle)))

        return (
            f'We use TOA to calculate side {sideCalc}:<br>'
            f'tan({knownAngle}) = {sideOpposite} / {sideCalc}<br>'
            f'=> {sideCalc} = {sideOpposite} / tan({knownAngle})<br>'
            f'=> {sideCalc} = {sideOppositeVal} / tan({knownAngleVal}°)<br>'
            f'=> {sideCalc} = {sideCalcVal}<br>'
        )
    
    def toaSideOString(self, sideAdjacent, sideCalc, knownAngle):
        '''
        Returns TOA string to be displayed in the GUI.
        An angle and the side opposite to it is known and the adjacent side is calculated.
        '''
        sideAdjacentVal = self.formatValue(getattr(self, sideAdjacent))
        sideCalcVal = self.formatValue(getattr(self, sideCalc))
        knownAngleVal = self.formatValue(math.degrees(getattr(self, knownAngle)))

        return (
            f'We use TOA to calculate side {sideCalc}:<br>'
            f'tan({knownAngle}) = {sideCalc} / {sideAdjacent}<br>'
            f'=> {sideCalc} = {sideAdjacent} * tan({knownAngle})<br>'
            f'=> {sideCalc} = {sideAdjacentVal} * tan({knownAngleVal}°)<br>'
            f'=> {sideCalc} = {sideCalcVal}<br>'
        )
    
    def toaAngleString(self, sideOpposite, sideAdjacent, angleCalc):
        '''
        Returns TOA string to be displayed in the GUI.
        Side opposite to an angle and the adjacent side is known and that angle is calculated.
        '''
        sideOppositeVal = self.formatValue(getattr(self, sideOpposite))
        sideAdjacentVal = self.formatValue(getattr(self, sideAdjacent))
        angleCalcVal = self.formatValue(math.degrees(getattr(self, angleCalc)))

        return (
            f'We use TOA to calculate ∠{angleCalc}:<br>'
            f'tan({angleCalc}) = {sideOpposite} / {sideAdjacent}<br>'
            f'=> ∠{angleCalc} = tan⁻¹({sideOpposite} / {sideAdjacent})<br>'
            f'=> ∠{angleCalc} = tan⁻¹({sideOppositeVal} / {sideAdjacentVal})<br>'
            f'=> ∠{angleCalc} = {angleCalcVal}°<br>'
        )

    def solveTOA(self):
        '''
        Solves the triangle using the TOA (Tangent = Opposite / Adjacent) rule for specific cases.
        Sets an error message if the given input cannot be resolved using this rule.
        '''
        if self.A is None or self.A != math.pi/2:
            self.errorMessage = 'Angle A must be pi/2 radians for TOA calculations'            
            
        if self.B is None and self.C is None:
            if self.a is not None and self.b is not None:
                self.c = Trigonometry.pythagorasTheorem(h = self.a, a = self.b)
                self.lawsUsed.append(self.pythagorasTheoremMinusString('a', 'b', 'c'))                
            elif self.a is not None and self.c is not None:
                self.b = Trigonometry.pythagorasTheorem(h = self.a, o = self.c)
                self.lawsUsed.append(self.pythagorasTheoremMinusString('a', 'c', 'b'))                
            elif self.b is not None and self.c is not None:
                self.a = Trigonometry.pythagorasTheorem(o = self.b, a = self.c)
                self.lawsUsed.append(self.pythagorasTheoremPlusString('b', 'c', 'a'))
            self.B = Trigonometry.toa(o = self.b, a = self.c)
            self.C = Trigonometry.triangleSumTheorem(A=self.A, B=self.B)  
            self.lawsUsed.append(self.toaAngleString('b', 'c', 'B'))
            self.lawsUsed.append(self.triangleSumTheoremString('A', 'B', 'C'))
        elif (self.B is None and self.C is not None) or (self.C is None and self.B is not None):
            if self.B is None and self.C is not None:
                self.B = Trigonometry.triangleSumTheorem(A=self.A, B=self.C)
                self.lawsUsed.append(self.triangleSumTheoremString('A', 'C', 'B'))
            elif self.C is None and self.B is not None:
                self.C = Trigonometry.triangleSumTheorem(A=self.A, B=self.B) 
                self.lawsUsed.append(self.triangleSumTheoremString('A', 'B', 'C'))               
            if self.a is not None:
                self.errorMessage = 'Cannot calculate, use other law!'                
            elif self.b is not None:
                self.c = Trigonometry.toa(o = self.b, theta = self.B)
                self.a = Trigonometry.pythagorasTheorem(o = self.b, a = self.c)
                self.lawsUsed.append(self.toaSideAString('b', 'c', 'B'))
                self.lawsUsed.append(self.pythagorasTheoremPlusString('b', 'c', 'a'))
            elif self.c is not None:
                self.b = Trigonometry.toa(o = self.c, theta = self.C)
                self.a = Trigonometry.pythagorasTheorem(o = self.b, a = self.c)
                self.lawsUsed.append(self.toaSideAString('c', 'b', 'C'))
                self.lawsUsed.append(self.pythagorasTheoremPlusString('b', 'c', 'a'))
        else:
            self.errorMessage = 'Cannot calculate, use other law!'  
            

    def sineLawAngleString(self, side1, angle1, side2, angleCalc):
        '''
        Returns sine law string to be displayed in the GUI.
        Calculates an angle using the sine law.
        '''
        side1Val = self.formatValue(getattr(self, side1))
        angle1Val = self.formatValue(math.degrees(getattr(self, angle1)))
        side2Val = self.formatValue(getattr(self, side2))
        angleCalcVal = self.formatValue(math.degrees(getattr(self, angleCalc)))

        return (
            f'We use the sine law to calculate ∠{angleCalc}:<br>'
            f'sin({angleCalc}) / {side2} = sin({angle1}) / {side1}<br>'
            f'=> sin({angleCalc}) = sin({angle1}) * {side2} / {side1}<br>'
            f'=> ∠{angleCalc} = sin⁻¹(sin({angle1}) * {side2} / {side1})<br>'
            f'=> ∠{angleCalc} = sin⁻¹(sin({angle1Val}°) * {side2Val} / {side1Val})<br>'
            f'=> ∠{angleCalc} = {angleCalcVal}°<br>'
        )
    
    def sineLawSideString(self, side1, angle1, angle2, sideCalc):
        '''
        Returns sine law string to be displayed in the GUI.
        Calculates a side using the sine law.
        '''
        side1Val = self.formatValue(getattr(self, side1))
        angle1Val = self.formatValue(math.degrees(getattr(self, angle1)))
        angle2Val = self.formatValue(math.degrees(getattr(self, angle2)))
        sideCalcVal = self.formatValue(getattr(self, sideCalc))

        return (
            f'We use the sine law to calculate side {sideCalc}:<br>'
            f'(sin({angle2}) / {sideCalc} = sin({angle1}) / {side1}<br>'
            f'=> {sideCalc} = sin({angle2}) * {side1} / sin({angle1})<br>'
            f'=> {sideCalc} = sin({angle2Val}°) * {side1Val} / sin({angle1Val}°)<br>'
            f'=> {sideCalc} = {sideCalcVal}<br>'
        )

    def solveSineLaw(self):
        '''
        Solves the triangle using the sine law for specific cases.
        Sets an error message if the given input cannot be resolved using this rule.
        We can solve AAS, ASA, SSA using sine law alone but not for SAS and SSS.
        '''        
        if self.A and self.B and not self.C:
            self.C = Trigonometry.triangleSumTheorem(A=self.A, B=self.B)
            self.lawsUsed.append(self.triangleSumTheoremString('A', 'B', 'C'))
            if self.a:
                self.b = Trigonometry.sine(a=self.a, A=self.A, B=self.B)
                self.c = Trigonometry.sine(a=self.a, A=self.A, B=self.C)
                self.lawsUsed.append(self.sineLawSideString('a', 'A', 'B', 'b'))
                self.lawsUsed.append(self.sineLawSideString('a', 'A', 'C', 'c'))
            elif self.b:
                self.a = Trigonometry.sine(a=self.b, A=self.B, B=self.A)
                self.c = Trigonometry.sine(a=self.b, A=self.B, B=self.C)
                self.lawsUsed.append(self.sineLawSideString('b', 'B', 'A', 'a'))
                self.lawsUsed.append(self.sineLawSideString('b', 'B', 'C', 'c'))
            elif self.c:
                self.a = Trigonometry.sine(a=self.c, A=self.C, B=self.A)
                self.b = Trigonometry.sine(a=self.c, A=self.C, B=self.B)
                self.lawsUsed.append(self.sineLawSideString('c', 'C', 'A', 'a'))
                self.lawsUsed.append(self.sineLawSideString('c', 'C', 'B', 'b'))            
        elif self.A and self.C and not self.B:
            self.B = Trigonometry.triangleSumTheorem(A=self.A, B=self.C)
            self.lawsUsed.append(self.triangleSumTheoremString('A', 'C', 'B'))
            if self.a:
                self.b = Trigonometry.sine(a=self.a, A=self.A, B=self.B)
                self.c = Trigonometry.sine(a=self.a, A=self.A, B=self.C)
                self.lawsUsed.append(self.sineLawSideString('a', 'A', 'B', 'b'))
                self.lawsUsed.append(self.sineLawSideString('a', 'A', 'C', 'c'))
            elif self.c:
                self.a = Trigonometry.sine(a=self.c, A=self.C, B=self.A)
                self.b = Trigonometry.sine(a=self.c, A=self.C, B=self.B)
                self.lawsUsed.append(self.sineLawSideString('c', 'C', 'A', 'a'))
                self.lawsUsed.append(self.sineLawSideString('c', 'C', 'B', 'b'))
            elif self.b:
                self.a = Trigonometry.sine(a=self.b, A=self.B, B=self.A)
                self.c = Trigonometry.sine(a=self.b, A=self.B, B=self.C)
                self.lawsUsed.append(self.sineLawSideString('b', 'B', 'A', 'a'))
                self.lawsUsed.append(self.sineLawSideString('b', 'B', 'C', 'c'))
        elif self.B and self.C and not self.A:
            self.A = Trigonometry.triangleSumTheorem(A=self.B, B=self.C)
            self.lawsUsed.append(self.triangleSumTheoremString('B', 'C', 'A'))
            if self.b:
                self.a = Trigonometry.sine(a=self.b, A=self.B, B=self.A)
                self.c = Trigonometry.sine(a=self.b, A=self.B, B=self.C)
                self.lawsUsed.append(self.sineLawSideString('b', 'B', 'A', 'a'))
                self.lawsUsed.append(self.sineLawSideString('b', 'B', 'C', 'c'))
            elif self.c:
                self.a = Trigonometry.sine(a=self.c, A=self.C, B=self.A)
                self.b = Trigonometry.sine(a=self.c, A=self.C, B=self.B)
                self.lawsUsed.append(self.sineLawSideString('c', 'C', 'A', 'a'))
                self.lawsUsed.append(self.sineLawSideString('c', 'C', 'B', 'b'))
            elif self.a:
                self.b = Trigonometry.sine(a=self.a, A=self.A, B=self.B)
                self.c = Trigonometry.sine(a=self.a, A=self.A, B=self.C)
                self.lawsUsed.append(self.sineLawSideString('a', 'A', 'B', 'b'))
                self.lawsUsed.append(self.sineLawSideString('a', 'A', 'C', 'c'))
            
        elif self.a and self.b and not self.c:
            if self.A:
                self.B = Trigonometry.sine(a=self.a, A=self.A, b=self.b)
                self.C = Trigonometry.triangleSumTheorem(A=self.A, B=self.B)
                self.c = Trigonometry.sine(a=self.a, A=self.A, B=self.C)
                self.lawsUsed.append(self.sineLawAngleString('a', 'A', 'b', 'B'))
                self.lawsUsed.append(self.triangleSumTheoremString('A', 'B', 'C'))
                self.lawsUsed.append(self.sineLawSideString('a', 'A', 'C', 'c'))
            elif self.B:
                self.A = Trigonometry.sine(a=self.b, A=self.B, b=self.a)
                self.C = Trigonometry.triangleSumTheorem(A=self.A, B=self.B)
                self.c = Trigonometry.sine(a=self.a, A=self.A, B=self.C)
                self.lawsUsed.append(self.sineLawAngleString('b', 'B', 'a', 'A'))
                self.lawsUsed.append(self.triangleSumTheoremString('A', 'B', 'C'))
                self.lawsUsed.append(self.sineLawSideString('a', 'A', 'C', 'c'))
            else:
                self.errorMessage = 'Cannot calculate, use other law!'                
        elif self.a and self.c and not self.b:
            if self.A:
                self.C = Trigonometry.sine(a=self.a, A=self.A, b=self.c)
                self.B = Trigonometry.triangleSumTheorem(A=self.A, B=self.C)
                self.b = Trigonometry.sine(a=self.c, A=self.C, B=self.B)
                self.lawsUsed.append(self.sineLawAngleString('a', 'A', 'c', 'C'))
                self.lawsUsed.append(self.triangleSumTheoremString('A', 'C', 'B'))
                self.lawsUsed.append(self.sineLawSideString('c', 'C', 'B', 'b'))
            elif self.C:
                self.A = Trigonometry.sine(a=self.c, A=self.C, b=self.a)
                self.B = Trigonometry.triangleSumTheorem(A=self.A, B=self.C)
                self.b = Trigonometry.sine(a=self.c, A=self.C, B=self.B)
                self.lawsUsed.append(self.sineLawAngleString('c', 'C', 'a', 'A'))
                self.lawsUsed.append(self.triangleSumTheoremString('A', 'C', 'B'))
                self.lawsUsed.append(self.sineLawSideString('c', 'C', 'B', 'b'))
            else:
                self.errorMessage = 'Cannot calculate, use other law!'                 
        elif self.b and self.c and not self.a:
            if self.B:
                self.C = Trigonometry.sine(a=self.b, A=self.B, b=self.c)
                self.A = Trigonometry.triangleSumTheorem(A=self.B, B=self.C)
                self.a = Trigonometry.sine(a=self.c, A=self.C, B=self.A)
                self.lawsUsed.append(self.sineLawAngleString('b', 'B', 'c', 'C'))
                self.lawsUsed.append(self.triangleSumTheoremString('B', 'C', 'A'))
                self.lawsUsed.append(self.sineLawSideString('c', 'C', 'A', 'a'))
            elif self.C:
                self.B = Trigonometry.sine(a=self.c, A=self.C, b=self.b)
                self.A = Trigonometry.triangleSumTheorem(A=self.B, B=self.C)
                self.a = Trigonometry.sine(a=self.c, A=self.C, B=self.A)
                self.lawsUsed.append(self.sineLawAngleString('c', 'C', 'b', 'B'))
                self.lawsUsed.append(self.triangleSumTheoremString('B', 'C', 'A'))
                self.lawsUsed.append(self.sineLawSideString('c', 'C', 'A', 'a'))  
            else:
                self.errorMessage = 'Cannot calculate, use other law!'                
        else:
            self.errorMessage = 'Cannot calculate, use other law!'
            

    def cosineLawAngleString(self, sideOpposite1, sideOpposite2, sideCorresponding, angleCalc):
        '''
        Returns cosine law string to be displayed in the GUI.
        Calculates an angle using the cosine law.
        '''
        sideOpposite1Val = self.formatValue(getattr(self, sideOpposite1))
        sideOpposite2Val = self.formatValue(getattr(self, sideOpposite2))
        sideCorrespondingVal = self.formatValue(getattr(self, sideCorresponding))
        angleCalcVal = self.formatValue(math.degrees(getattr(self, angleCalc)))

        return (
            f'We use the cosine law to calculate ∠{angleCalc}:<br>'
            f'{sideCorresponding}² = {sideOpposite1}² + {sideOpposite2}² - 2 * {sideOpposite1} * {sideOpposite2} * cos({angleCalc})<br>'
            f'=> cos({angleCalc}) = ({sideOpposite1}² + {sideOpposite2}² - {sideCorresponding}²) / 2 * {sideOpposite1} * {sideOpposite2}<br>'
            f'=> ∠{angleCalc} = cos⁻¹(({sideOpposite1}² + {sideOpposite2}² - {sideCorresponding}²) / 2 * {sideOpposite1} * {sideOpposite2})<br>'
            f'=> ∠{angleCalc} = cos⁻¹(({sideOpposite1Val}² + {sideOpposite2Val}² - {sideCorrespondingVal}²) / 2 * {sideOpposite1Val} * {sideOpposite2Val})<br>'
            f'=> ∠{angleCalc} = {angleCalcVal}°<br>'
        )
    
    def cosineLawSideString(self, side1, side2, angleCorresponding, sideCalc):
        '''
        Returns cosine law string to be displayed in the GUI.
        Calculates a side using the cosine law.
        '''
        side1Val = self.formatValue(getattr(self, side1))
        side2Val = self.formatValue(getattr(self, side2))
        angleCorrespondingVal = self.formatValue(math.degrees(getattr(self, angleCorresponding)))
        sideCalcVal = self.formatValue(getattr(self, sideCalc))

        return (
            f'We use the cosine law to calculate side {sideCalc}:<br>'
            f'{sideCalc}² = {side1}² + {side2}² - 2 * {side1} * {side2} * cos({angleCorresponding})<br>'
            f'=> {sideCalc} = sqrt({side1}² + {side2}² - 2 * {side1} * {side2} * cos({angleCorresponding}))<br>'
            f'=> {sideCalc} = sqrt({side1Val}² + {side2Val}² - 2 * {side1Val} * {side2Val} * cos({angleCorrespondingVal}))<br>'
            f'=> {sideCalc} = {sideCalcVal}<br>'
        )

    def solveCosineLaw(self):
        '''
        Solves the triangle using the cosine law for specific cases.
        Sets an error message if the given input cannot be resolved using this rule.
        We can solve SAS, SSS using cosine law alone but not for ASA, AAS and SSA.
        '''
        if self.a is not None and self.b is not None and self.c is not None:  
            self.A = Trigonometry.cosine(a=self.b, b=self.c, c=self.a)            
            self.B = Trigonometry.cosine(a=self.c, b=self.a, c=self.b)
            self.C = Trigonometry.cosine(a=self.a, b=self.b, c=self.c)
            self.lawsUsed.append(self.cosineLawAngleString('b', 'c', 'a', 'A'))
            self.lawsUsed.append(self.cosineLawAngleString('c', 'a', 'b', 'B'))
            self.lawsUsed.append(self.cosineLawAngleString('a', 'b', 'c', 'C'))
        elif self.a is not None and self.b is not None and self.C is not None:
            self.c = Trigonometry.cosine(a=self.a, b=self.b, C=self.C)
            self.A = Trigonometry.cosine(a=self.b, b=self.c, c=self.a)
            self.B = Trigonometry.cosine(a=self.c, b=self.a, c=self.b)
            self.lawsUsed.append(self.cosineLawSideString('a', 'b', 'C', 'c'))
            self.lawsUsed.append(self.cosineLawAngleString('b', 'c', 'a', 'A'))
            self.lawsUsed.append(self.cosineLawAngleString('c', 'a', 'b', 'B'))
        elif self.a is not None and self.c is not None and self.B is not None:
            self.b = Trigonometry.cosine(a=self.a, b=self.c, C=self.B)
            self.A = Trigonometry.cosine(a=self.b, b=self.c, c=self.a)
            self.C = Trigonometry.cosine(a=self.a, b=self.b, c=self.c)
            self.lawsUsed.append(self.cosineLawSideString('a', 'c', 'B', 'b'))
            self.lawsUsed.append(self.cosineLawAngleString('b', 'c', 'a', 'A'))
            self.lawsUsed.append(self.cosineLawAngleString('a', 'b', 'c', 'C'))
        elif self.b is not None and self.c is not None and self.A is not None:
            self.a = Trigonometry.cosine(a=self.b, b=self.c, C=self.A)
            self.B = Trigonometry.cosine(a=self.c, b=self.a, c=self.b)
            self.C = Trigonometry.cosine(a=self.a, b=self.b, c=self.c)
            self.lawsUsed.append(self.cosineLawSideString('b', 'c', 'A', 'a'))
            self.lawsUsed.append(self.cosineLawAngleString('c', 'a', 'b', 'B'))
            self.lawsUsed.append(self.cosineLawAngleString('a', 'b', 'c', 'C'))  
        else:
            self.errorMessage = 'Cannot calculate, use other law!'

    def formatValue(self, value):
        '''
        Formats the value to two decimal places if it is not a whole number.
        '''
        return f'{value:.2f}' if value != round(value) else str(int(value))   
    
        
    def calculateVertices(self):
        '''
        Calculates the vertices of the triangle based on the sides and angles to draw them on the GUI.        
        '''   
        pointA = QPointF(0,0) # first vertex is assumed to be at the origin
        pointB = QPointF(self.c,0) # then we assume that second side in along the x-axis, so the second vertex is at (c,0)
        pointC = QPointF(self.b * math.cos(self.A), -self.b * math.sin(self.A)) # then we use the cosine and sine of the first angle to calculate the third vertex
        return [pointA, pointB, pointC]                                         # we use the negative sine because the y-axis is inverted in the GUI