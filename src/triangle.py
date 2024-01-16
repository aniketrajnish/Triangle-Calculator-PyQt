import math
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from trig import Trigonometry

class Triangle:
    '''
    Class that represrnets a triangle.
    It is used to calculate the missing sides and angles of a triangle.
    It also calculates the vertices of the triangle based on the sides and angles.
    '''
    def __init__(self, a=None, b=None, c=None, A=None, B=None, C=None):
        '''
        Initializes the triangle with the given sides and angles.
        It converts the angles from degrees to radians.
        It then calculates the missing sides and angles of the triangle.
        '''
        self.lawsUsed = [] # list of laws used to calculate the triangle

        self.a = a
        self.b = b
        self.c = c
        self.A = math.radians(A) if A is not None else None 
        self.B = math.radians(B) if B is not None else None
        self.C = math.radians(C) if C is not None else None

        self.calculateTriangle()        
        
    def calculateTriangle(self):
        '''
        Calculates the missing sides and angles of the triangle.
        '''
        sides = [self.a, self.b, self.c]
        angles = [self.A, self.B, self.C]
        
        numSides = sum(side is not None for side in sides)
        numAngles = sum(angle is not None for angle in angles)
        
        if numAngles + numSides < 3:
            raise ValueError('Not enough information to calculate triangle') # less than 3 properties is not a unique triangle
        elif numAngles == 3 and numSides == 0:
            raise ValueError('Not enough information to calculate triangle') # three angles don't determine a unique triangle        
        
        elif numAngles == 2 and numSides == 1: # two angles and one side given
            self.solveAAS()
        elif numAngles == 1 and numSides == 2: # one angle and two sides given
            self.solveSSA()
        elif numSides == 3: # three sides given
            self.solveSSS()
            
        self.lawsUsed.append(self.stringSOHCAHTOA()) # lawsUsed[1] is meant for SOHCAHTOA procedure

    def formatValue(self, value):
        '''
        Formats the value to two decimal places if it is not a whole number.
        '''
        return f'{value:.2f}' if value != round(value) else str(int(value))
    
    def stringSOHCAHTOA(self):
        '''
        Returns the string representation of the SOHCAHTOA trigonometric ratios to be displayed in the info box of the GUI.
        '''
        BVal = self.formatValue(math.degrees(getattr(self, 'B')))
        CVal = self.formatValue(math.degrees(getattr(self, 'C')))
        aVal = self.formatValue(getattr(self, 'a'))
        bVal = self.formatValue(getattr(self, 'b'))
        cVal = self.formatValue(getattr(self, 'c'))
        sinBVal = self.formatValue(self.b/self.a)
        sinCVal = self.formatValue(self.c/self.a)
        cosBVal = self.formatValue(self.c/self.a)
        cosCVal = self.formatValue(self.b/self.a)
        tanBVal = self.formatValue(self.b/self.c)
        tanCVal = self.formatValue(self.c/self.b)

        return (
            f'SOH (sin(theta) = opposite / hypotenuse)<br>'
            f'Sin(B) = b / a<br>'
            f'Sin(B)= {bVal} / {aVal}<br>'
            f'Sin(B) = Sin({BVal}°) = {sinBVal} (Calculated)<br>'
            f'Sin(C) = c / a<br>'
            f'Sin(C)= {cVal} / {aVal}<br>'
            f'Sin(C) = Sin({CVal}°) = {sinCVal} (Calculated)<br><br>'                       
            f'CAH (cos(theta) = adjacent / hypotenuse)<br>'
            f'Cos(B) = c / a<br>'
            f'Cos(B)= {cVal} / {aVal}<br>'
            f'Cos(B) = Cos({BVal}°) = {cosBVal} (Calculated)<br>'
            f'Cos(C) = b / a<br>'
            f'Cos(C)= {bVal} / {aVal}<br>'
            f'Cos(C) = Cos({CVal}°) = {cosCVal} (Calculated)<br><br>'
            f'TOA (tan(theta) = opposite / adjacent)<br>'
            f'Tan(∠B) = b / c<br>'
            f'Tan(B)= {bVal} / {cVal}<br>'
            f'Tan(B) = Tan({BVal}°) = {tanBVal} (Calculated)<br>'
            f'Tan(C) = c / b<br>'
            f'Tan(C)= {cVal} / {bVal}<br>'
            f'Tan(C) = Tan({CVal}°) = {tanCVal} (Calculated)'  
        )

    def stringAAS(self, angleKnown1, angleKnown2, angleCalc, sideKnown, sideCalc1, sideCalc2, sineLaw1, sineLaw2):
        '''
        Returns the string representation of the AAS procedures to be displayed in the info box of the GUI.
        '''
        angleKnown1Val = self.formatValue(math.degrees(getattr(self, angleKnown1)))
        angleKnown2Val = self.formatValue(math.degrees(getattr(self, angleKnown2)))
        angleCalcVal = self.formatValue(math.degrees(getattr(self, angleCalc)))        
        
        return (
            f'First we determine ∠{angleCalc} using triangle sum theorem:<br>'
            f'∠{angleCalc} = π - {angleKnown1Val}° - {angleKnown2Val}°'
            f'=> ∠{angleCalc} = {angleCalcVal}° (Calculated)<br><br>'
            f'Then we use sine law to determine side {sideCalc1}:<br>'
            f'{sineLaw1}<br><br>'
            f'Then we use sine law to determine side {sideCalc2}:<br>'
            f'{sineLaw2}<br><br>'
        )
    
    def sineLawAAS(self, angleKnown, sideKnown, angleCalc, sideCalc):
        '''
        The sine law string that we use in AAS procedure.
        '''
        sideCalcVal = self.formatValue(getattr(self, sideCalc))
        sideKnownVal = self.formatValue(getattr(self, sideKnown))
        angleCalcVal = self.formatValue(math.degrees(getattr(self, angleCalc)))
        angleKnownVal = self.formatValue(math.degrees(getattr(self, angleKnown)))

        return (
            f'sin({angleKnown})/{sideKnown} = sin({angleCalc})/{sideCalc}<br>'
            f'=> {sideCalc} = sin({angleCalc}) * {sideKnown} / sin({angleKnown})<br>'
            f'=> {sideCalc} = sin({angleCalcVal}°) * {sideKnownVal} / sin({angleKnownVal}°)<br>'
            f'=> {sideCalc} = {sideCalcVal} (Calculated)'
        )
   
    def solveAAS(self):
        '''
        Solves for the missing sides and angle of the triangle using AAS.
        '''
        if self.A is not None and self.B is not None and self.a is not None:
            self.C = math.pi - self.A - self.B # caculate the missing angle using triangle sum theorem
            self.b = Trigonometry.sine(a=self.a, A=self.A, B=self.B) # calculate the first missing side using sine law
            self.c = Trigonometry.sine(a=self.a, A=self.A, B=self.C) # calculate the second missing side using sine law
            self.lawsUsed.append(self.stringAAS('A', 'B', 'C', 'a', 'b', 'c', self.sineLawAAS('A', 'a', 'B', 'b'), self.sineLawAAS('A', 'a', 'C', 'c'))) # lawsUsed[0] is meant for sine and cosine law procedures.         

        elif self.A is not None and self.B is not None and self.b is not None:
            self.C = math.pi - self.A - self.B
            self.a = Trigonometry.sine(a=self.b, A=self.B, B=self.A)
            self.c = Trigonometry.sine(a=self.b, A=self.B, B=self.C)
            self.lawsUsed.append(self.stringAAS('A', 'B', 'C', 'b', 'a', 'c', self.sineLawAAS('B', 'b', 'A', 'a'), self.sineLawAAS('B', 'b', 'C', 'c')))

        elif self.A is not None and self.B is not None and self.c is not None:
            self.C = math.pi - self.A - self.B
            self.a = Trigonometry.sine(a=self.c, A=self.C, B=self.A)
            self.b = Trigonometry.sine(a=self.c, A=self.C, B=self.B)
            self.lawsUsed.append(self.stringAAS('A', 'B', 'C', 'c', 'a', 'b', self.sineLawAAS('C', 'c', 'A', 'a'), self.sineLawAAS('C', 'c', 'B', 'b')))

        elif self.A is not None and self.C is not None and self.a is not None:
            self.B = math.pi - self.A - self.C
            self.b = Trigonometry.sine(a=self.a, A=self.A, B=self.B)
            self.c = Trigonometry.sine(a=self.a, A=self.A, B=self.C)
            self.lawsUsed.append(self.stringAAS('A', 'C', 'B', 'a', 'b', 'c', self.sineLawAAS('A', 'a', 'B', 'b'), self.sineLawAAS('A', 'a', 'C', 'c')))

        elif self.A is not None and self.C is not None and self.b is not None:
            self.B = math.pi - self.A - self.C
            self.a = Trigonometry.sine(a=self.b, A=self.B, B=self.A)
            self.c = Trigonometry.sine(a=self.b, A=self.B, B=self.C)
            self.lawsUsed.append(self.stringAAS('A', 'C', 'B', 'b', 'a', 'c', self.sineLawAAS('B', 'b', 'A', 'a'), self.sineLawAAS('B', 'b', 'C', 'c')))

        elif self.A is not None and self.C is not None and self.c is not None:
            self.B = math.pi - self.A - self.C
            self.a = Trigonometry.sine(a=self.c, A=self.C, B=self.A)
            self.b = Trigonometry.sine(a=self.c, A=self.C, B=self.B)
            self.lawsUsed.append(self.stringAAS('A', 'C', 'B', 'c', 'a', 'b', self.sineLawAAS('C', 'c', 'A', 'a'), self.sineLawAAS('C', 'c', 'B', 'b')))

        elif self.B is not None and self.C is not None and self.a is not None:
            self.A = math.pi - self.B - self.C
            self.b = Trigonometry.sine(a=self.a, A=self.A, B=self.B)
            self.c = Trigonometry.sine(a=self.a, A=self.A, B=self.C)
            self.lawsUsed.append(self.stringAAS('B', 'C', 'A', 'a', 'b', 'c', self.sineLawAAS('A', 'a', 'B', 'b'), self.sineLawAAS('A', 'a', 'C', 'c')))

        elif self.B is not None and self.C is not None and self.b is not None:
            self.A = math.pi - self.B - self.C
            self.a = Trigonometry.sine(a=self.b, A=self.B, B=self.A)
            self.c = Trigonometry.sine(a=self.b, A=self.B, B=self.C)
            self.lawsUsed.append(self.stringAAS('B', 'C', 'A', 'b', 'a', 'c', self.sineLawAAS('B', 'b', 'A', 'a'), self.sineLawAAS('B', 'b', 'C', 'c')))

        elif self.B is not None and self.C is not None and self.c is not None:
            self.A = math.pi - self.B - self.C
            self.a = Trigonometry.sine(a=self.c, A=self.C, B=self.A)
            self.b = Trigonometry.sine(a=self.c, A=self.C, B=self.B)
            self.lawsUsed.append(self.stringAAS('B', 'C', 'A', 'c', 'a', 'b', self.sineLawAAS('C', 'c', 'A', 'a'), self.sineLawAAS('C', 'c', 'B', 'b')))  

    def stringAdjAngleSSA(self, sideCalc, angleCalc1, angleCal2, cosineLawString, sineLaw1String, sineLaw2String):
        '''
        SSA procedure string when the known angle is in between the two known sides.
        '''
        return (
            f'We use cosine law to determine side {sideCalc}:<br>'
            f'{cosineLawString}<br><br>'
            f'Then we use sine law to determine angle {angleCalc1}:<br>'
            f'{sineLaw1String}<br><br>'
            f'Then we use sine law to determine angle {angleCal2}:<br>'
            f'{sineLaw2String}<br><br>'
        )
    
    def stringOppAngleSSA(self, angleKnown, angleCalc1, angleCal2, sideCalc, sineLaw1String, sineLaw2String):
        '''
        SSA procedure string when the known angle is not in between the two known sides.
        '''
        angleCalc1Val = self.formatValue(math.degrees(getattr(self, angleCalc1)))
        angleCal2Val = self.formatValue(math.degrees(getattr(self, angleCal2)))
        angleKnownVal = self.formatValue(math.degrees(getattr(self, angleKnown)))
        
        return (
            f'We use sine law to determine angle {angleCalc1}:<br>'
            f'{sineLaw1String}<br><br>'
            f'Then we use triangle sum theorem to determine angle {angleCal2}:<br>'
            f'∠{angleCal2} = π - ∠{angleKnown} - ∠{angleCalc1}<br>'
            f'=> ∠{angleCal2} = π - {angleKnownVal}° - {angleCalc1Val}°<br>'
            f'=> ∠{angleCal2} = {angleCal2Val}° (Calculated)<br><br>'
            f'Then we use sine law to determine side {sideCalc}:<br>'
            f'{sineLaw2String}<br><br>'
        )

    def sineAngleLawSSA(self, sideCalc, angleCalc, sideKnown, angleKnown):
        '''
        The sine law string that we use in SSA procedure to calculate the unknown angle.
        '''
        angleKnownVal = self.formatValue(math.degrees(getattr(self, angleKnown)))
        sideKnownVal = self.formatValue(getattr(self, sideKnown))
        angleCalcVal = self.formatValue(math.degrees(getattr(self, angleCalc)))
        sideCalcVal = self.formatValue(getattr(self, sideCalc))

        return (
            f'sin({angleKnown})/{sideKnown} = sin({angleCalc})/{sideCalc}<br>'
            f'=> sin({angleCalc}) = sin({angleKnown}) * {sideCalc} / {sideKnown}<br>'
            f'=> ∠{angleCalc} = sin<sup>-1</sup>((sin({angleKnownVal}°) * {sideCalcVal}) / {sideKnownVal})<br>'
            f'=> ∠{angleCalc} = {angleCalcVal}° (Calculated)'
        )

    def sineSideLawSSA(self, sideKnown, angleKnown, sideCalc, angleCalc):
        '''
        The sine law string that we use in SSA procedure to calculate the unknown side.
        '''
        sideCalcVal = self.formatValue(getattr(self, sideCalc))
        sideKnownVal = self.formatValue(getattr(self, sideKnown))
        angleCalcVal = self.formatValue(math.degrees(getattr(self, angleCalc)))
        angleKnownVal = self.formatValue(math.degrees(getattr(self, angleKnown)))

        return (
            f'sin({angleKnown})/{sideKnown} = sin({angleCalc})/{sideCalc}<br>'
            f'=> {sideCalc} = sin({angleCalc}) * {sideKnown} / sin({angleKnown})<br>'
            f'=> {sideCalc} = sin({angleCalcVal}°) * {sideKnownVal} / sin({angleKnownVal}°)<br>'
            f'=> {sideCalc} = {sideCalcVal} (Calculated)'
        )

    def cosineLawSSA(self, sideKnown1, sideKnown2, angleKnown, sideCalc):
        '''
        The cosine law string for SSA procedure.
        '''
        sideKnown1Val = self.formatValue(getattr(self, sideKnown1))
        sideKnown2Val = self.formatValue(getattr(self, sideKnown2))
        sideCalcVal = self.formatValue(getattr(self, sideCalc))
        angleVal = self.formatValue(math.degrees(getattr(self, angleKnown)))

        return (
            f'{sideCalc}² = {sideKnown1}² + {sideKnown2}² - 2 * {sideKnown1} * {sideKnown2} * cos({angleKnown})<br>'
            f'=> {sideCalc} = sqrt(({sideKnown1Val})² + ({sideKnown2Val})² - (2 * {sideKnown1Val} * {sideKnown2Val} * cos({angleVal}°)))<br>'
            f'=> {sideCalc} = {sideCalcVal} (Calculated)'
        )
                    
    def solveSSA(self):
        '''
        Solves for the missinge angles and side of the triangle using SSA.
        '''
        if self.a is not None and self.b is not None and self.C is not None: # case when the known angle is in between the two known sides
           self.c = Trigonometry.cosine(a=self.a, b=self.b, C=self.C) # calculate the missing side using cosine law
           self.A = Trigonometry.sine(a=self.c, b=self.a, A=self.C) # calculate the first missing angle using sine law
           self.B = Trigonometry.sine(a=self.c, b=self.b, A=self.C) # calculate the second missing angle using sine law
           self.lawsUsed.append(self.stringAdjAngleSSA('c', 'A', 'B', self.cosineLawSSA('a', 'b', 'C', 'c'), self.sineAngleLawSSA('a', 'A', 'c', 'C'), self.sineAngleLawSSA('b', 'B', 'c', 'C')))

        elif self.a is not None and self.b is not None and self.A is not None: # case when the known angle is not in between the two known sides
           self.B = Trigonometry.sine(a=self.a, b=self.b, A=self.A) # calculate the first missing angle using sine law
           self.C = math.pi - self.A - self.B # calculate the second missing angle using triangle sum theorem
           self.c = Trigonometry.sine(a=self.a, A=self.A, B=self.C) # calculate the missing side using sine law
           self.lawsUsed.append(self.stringOppAngleSSA('A', 'B', 'C', 'c', self.sineAngleLawSSA('b', 'B','a', 'A'), self.sineSideLawSSA('a', 'A', 'c', 'C')))
           
        elif self.a is not None and self.b is not None and self.B is not None:
           self.A = Trigonometry.sine(a=self.b, b=self.a, A=self.B)
           self.C = math.pi - self.A - self.B
           self.c = Trigonometry.sine(a=self.a, A=self.A, B=self.C)
           self.lawsUsed.append(self.stringOppAngleSSA('B', 'A', 'C', 'c', self.sineAngleLawSSA('a', 'A', 'b', 'B'), self.sineSideLawSSA('a', 'A', 'c', 'C')))
           
        elif self.a is not None and self.c is not None and self.B is not None:
           self.b = Trigonometry.cosine(a=self.a, b=self.c, C=self.B)
           self.A = Trigonometry.sine(a=self.b, b=self.a, A=self.B)
           self.C = Trigonometry.sine(a=self.b, b=self.c, A=self.B)
           self.lawsUsed.append(self.stringAdjAngleSSA('b', 'A', 'C', self.cosineLawSSA('a', 'c', 'B', 'b'), self.sineAngleLawSSA('a', 'A', 'b', 'B'), self.sineAngleLawSSA('c', 'C', 'b', 'B')))

        elif self.a is not None and self.c is not None and self.A is not None:
           self.C = Trigonometry.sine(a=self.a, b=self.c, A=self.A)
           self.B = math.pi - self.A - self.C
           self.b = Trigonometry.sine(a=self.a, A=self.A, B=self.B)
           self.lawsUsed.append(self.stringOppAngleSSA('A', 'C', 'B', 'b', self.sineAngleLawSSA('c', 'C','a', 'A'), self.sineSideLawSSA('a', 'A', 'b', 'B')))
           
        elif self.a is not None and self.c is not None and self.C is not None:
           self.A = Trigonometry.sine(a=self.c, b=self.a, A=self.C)
           self.B = math.pi - self.A - self.C
           self.b = Trigonometry.sine(a=self.a, A=self.A, B=self.B)
           self.lawsUsed.append(self.stringOppAngleSSA('C', 'A', 'B', 'b', self.sineAngleLawSSA('a', 'A', 'c', 'C'), self.sineSideLawSSA('a', 'A', 'b', 'B')))
           
        elif self.b is not None and self.c is not None and self.A is not None:
           self.a = Trigonometry.cosine(a=self.b, b=self.c, C=self.A)
           self.B = Trigonometry.sine(a=self.a, b=self.b, A=self.A)
           self.C = Trigonometry.sine(a=self.a, b=self.c, A=self.A)
           self.lawsUsed.append(self.stringAdjAngleSSA('a', 'B', 'C', self.cosineLawSSA('b', 'c', 'A', 'a'), self.sineAngleLawSSA('b', 'B', 'a', 'A'), self.sineAngleLawSSA('c', 'C', 'a', 'A')))
           
        elif self.b is not None and self.c is not None and self.B is not None:
           self.C = Trigonometry.sine(a=self.b, b=self.c, A=self.B)
           self.A = math.pi - self.B - self.C
           self.a = Trigonometry.sine(a=self.b, A=self.B, B=self.A)
           self.lawsUsed.append(self.stringOppAngleSSA('B', 'A', 'C', 'a', self.sineAngleLawSSA('c', 'C','b', 'B'), self.sineSideLawSSA('b', 'B', 'a', 'A')))
           
        elif self.b is not None and self.c is not None and self.C is not None:
           self.B = Trigonometry.sine(a=self.c, b=self.b, A=self.C)
           self.A = math.pi - self.B - self.C
           self.a = Trigonometry.sine(a=self.b, A=self.B, B=self.A)
           self.lawsUsed.append(self.stringOppAngleSSA('C', 'A', 'B', 'a', self.sineAngleLawSSA('b', 'B','c', 'C'), self.sineSideLawSSA('b', 'B', 'a', 'A')))
    
    def stringSSS(self, angleCalc1, angleCal2, angleCalc3, cosineLaw1String, cosineLaw2String, cosineLaw3String):
        '''
        SSS procedure string.
        '''
        return (
            f'We use cosine law to determine ∠{angleCalc1}:<br>'
            f'{cosineLaw1String}<br><br>'
            f'Then we use cosine law to determine ∠{angleCal2}:<br>'
            f'{cosineLaw2String}<br><br>'
            f'The we use cosine law to determine ∠{angleCalc3}:<br>'
            f'{cosineLaw3String}<br><br>'
        )
    
    def cosineLawSSS(self, sideCalc, sideKnown1, sideKnown2, angleCalc):   
        '''
        The cosine law string for SSS procedure.
        '''
        side1Val = self.formatValue(getattr(self, sideKnown1))
        side2Val = self.formatValue(getattr(self, sideKnown2))
        sideCalcVal = self.formatValue(getattr(self, sideCalc))
        angleVal = self.formatValue(math.degrees(getattr(self, angleCalc)))

        return (
            f'{sideCalc}² = {sideKnown1}² + {sideKnown2}² - 2 * {sideKnown1} * {sideKnown2} * cos({angleCalc})<br>'
            f'=> cos({angleCalc}) = ({sideKnown1}² + {sideKnown2}² - {sideCalc}²) / 2 * {sideKnown1} * {sideKnown2}<br>'
            f'=> ∠{angleCalc} = cos<sup>-1</sup>(({sideKnown1}² + {sideKnown2}² - {sideCalc}²) / 2 * {sideKnown1} * {sideKnown2})<br>'
            f'=> ∠{angleCalc} = cos<sup>-1</sup>(({side1Val})² + ({side2Val})² - ({sideCalcVal})²) / 2 * ({side1Val}) * ({side2Val})<br>'
            f'=> ∠{angleCalc} = {angleVal}° (Calculated)'
        )
            
    def solveSSS(self):
        '''
        Solve for the missing angles of the triangle using SSS.
        '''
        self.A = Trigonometry.cosine(a=self.b, b=self.c, c=self.a) # calculate all the missing angles using cosine law
        self.B = Trigonometry.cosine(a=self.a, b=self.c, c=self.b)
        self.C = Trigonometry.cosine(a=self.a, b=self.b, c=self.c)
        self.lawsUsed.append(self.stringSSS('A', 'B', 'C', self.cosineLawSSS('a', 'b', 'c', 'A'), self.cosineLawSSS('b', 'a', 'c', 'B'), self.cosineLawSSS('c', 'a', 'b', 'C')))
        
    def calculateVertices(self):
        '''
        Calculates the vertices of the triangle based on the sides and angles to draw them on the GUI.        
        '''   
        pointA = QPointF(0,0) # first vertex is assumed to be at the origin
        pointB = QPointF(self.c,0) # then we assume that second side in along the x-axis, so the second vertex is at (c,0)
        pointC = QPointF(self.b * math.cos(self.A), -self.b * math.sin(self.A)) # then we use the cosine and sine of the first angle to calculate the third vertex
        return [pointA, pointB, pointC]                                         # we use the negative sine because the y-axis is inverted in the GUI