import math

class Trigonometry:
    '''
    Class having helper functions to solve trigonometry problems.
    This includes the following:
    - SOHCAHTOA
    - Sine Rule and Cosine Rule    
    '''
    @staticmethod
    def soh(o = None, h = None, theta = None):
        '''
        Solves for the opposite, hypotenuse or angle of a right angled triangle using SOH.
        It takes in two of them as arguments and returns the third.
        '''
        if theta is not None:
           if o is not None:
               return o / math.sin(theta)
           elif h is not None:
               return h * math.sin(theta)
        elif o is not None and h is not None:
            return o/h
        else:
            raise ValueError('Insufficient info')
    
    @staticmethod
    def cah(a = None, h = None, theta = None):
        '''
        Solves for the adjacent, hypotenuse or angle of a right angled triangle using CAH.
        It takes in two of them as arguments and returns the third.
        '''
        if theta is not None:
           if a is not None:
               return a / math.cos(theta)
           elif h is not None:
               return h * math.cos(theta)
        elif a is not None and h is not None:
            return math.acos(a/h)
        else:
            raise ValueError('Insufficient info')
        
    @staticmethod
    def toa(o = None, a = None, theta = None):
        '''
        Solves for the opposite, adjacent or angle of a right angled triangle using TOA.
        It takes in two of them as arguments and returns the third.
        '''
        if theta is not None:
           if o is not None:
               return o / math.tan(theta)
           elif a is not None:
               return a * math.tan(theta)
        elif o is not None and a is not None:
            return math.atan(o/a)
        else:
            raise ValueError('Insufficient info')
    
    @staticmethod
    def sine(a = None, A = None, b = None, B = None):
        '''
        Solves for an unknown side or angle of a triangle using the sine rule.
        It takes in a side and its corresponding angle, other side or angle as arguments and returns the unknown side or angle.
        '''        
        if a and A and b and not B:   
            return math.asin(b * math.sin(A)/a)           
        elif a and A and B and not b:
            return a * math.sin(B) / math.sin(A)  
        else:
            raise ValueError('Insufficient info')
        
    @staticmethod
    def cosine(a = None, b = None, c = None, C = None):
        '''
        Solves for an unknown side or angle of a triangle using the cosine rule.
        It takes in two sides and their included angle or three sides as arguments and returns the unknown side or angle.
        '''
        if a and b and C and not c:   
            return math.sqrt(a ** 2 + b ** 2 - 2 * a * b * math.cos(C))           
        elif a and b and c and not C:
            return math.acos((a ** 2 + b ** 2 - c ** 2) / (2 * a * b))
        else:
            raise ValueError('Insufficient info')