import math
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from triangle import Triangle
from trig import TrigLaw

class TrigMainWindow(QMainWindow):
    '''
    Class to create the GUI of the application.
    It uses the Triangle class to draw the triangle and show the steps involved in drawing it.
    '''
    def __init__(self):
        '''
        Constructor for the TrigMainWindow class.
        It calls the initUI() method to initialize the UI.
        '''
        super().__init__()
        self.initUI()
        
    def initUI(self):
        '''
        Initializes the UI of the application.
        It calls initWindow(), initLayout() and initComponents() methods to initialize the window, layout and components respectively.
        '''
        self.initWindow()
        self.initLayout()
        self.initComponents()
    
    def initWindow(self):
        '''
        Initializes the window of the application.
        It sets the title, icon and size of the window.
        It also initializes the default font to be used at various places.
        '''       
        screen = QApplication.primaryScreen().size()
        self.w = screen.width() // 2
        self.h = screen.height() // 2

        self.font = QFont('Sans Serif', 10)
        
        self.setFixedSize(self.w, self.h)
        self.setWindowIcon(QIcon('Files/logo.png'))
        self.setWindowTitle('Trigonometry Visual Calculator')
        
    def initLayout(self):
        '''
        Initializes layout of the application.
        It creates different layouts for the different sections of the application.
        '''
        centralWidget = QWidget(self)
        self.setCentralWidget(centralWidget)
        
        self.gridLayout = QGridLayout(centralWidget)
        self.gridLayout.setColumnStretch(0,3) # column to diplay the triangle takes 3/5th of the space
        self.gridLayout.setColumnStretch(1,2) # column to display procedures takes 2/5th of the space
        
        self.infoLayout = QHBoxLayout()   
        self.optionsLayout = QHBoxLayout()         
        self.dimensionsLayout = QHBoxLayout()
        
    def initComponents(self):
        '''
        Initializes the different components of the application.
        '''
        self.initStatusBar()
        self.initToolBar()
        self.initTriangleView()
        self.initInfoBox()
        self.initDimensionInputBoxes()
        self.initOptionsBox()
        self.initRadioBtns()
        
    def initStatusBar(self):
        '''
        Creates a Status to display messages to the user at the bottom of the window.
        '''
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
                
        self.statusBar.setStyleSheet('background-color: #d3d3d3;')        
        self.statusBar.showMessage('Input dimensions and select the operations you wish to perform!', 3000)
        
    def initToolBar(self):
        '''
        Creates a Tool Bar at the top of the window.
        It contains a Reset button to reset the input fields and a Calculate button to draw the triangle.
        '''
        toolBar = QToolBar('Tool Bar', self)
        self.addToolBar(Qt.TopToolBarArea, toolBar)  
        
        calculateAction = QAction('Calculate', self)
        calculateAction.triggered.connect(self.calculateAndUpdateDisplay)
        toolBar.addAction(calculateAction)
        
        resetAction = QAction('Reset', self)
        resetAction.triggered.connect(self.resetInput)
        toolBar.addAction(resetAction)
        
    def initTriangleView(self):
        '''
        Creates a QGraphicsView object to display the triangle.
        '''
        self.triangleView = QGraphicsView()
        self.gridLayout.addWidget(self.triangleView, 0, 0) # 0th row, 0th column
    
    def initInfoBox(self):
        '''
        Creates a Group Box to display the procedures involved in drawing the triangle.
        Group box acts as a container and header.
        '''
        infoGroupBox = QGroupBox('Procedure:')        
        infoGroupBox.setLayout(self.infoLayout)
        self.gridLayout.addWidget(infoGroupBox, 0, 1) # 0th row, 1st column
        
    def initDimensionInputBoxes(self):
        '''
        Initializes a Group Box to input the dimensions of the triangle.
        Creates 3 input boxes for the sides and 3 input boxes for the angles along with their labels.
        '''
        diemnsionsGroupBox = QGroupBox('Input Dimensions:')
        self.sideIBs = [] # to store the side input boxes for later use
        self.angleIBs = [] # to store the angle input boxes for later use

        for i in range(3): # 3 sides
            label = f'{chr(65+i)} = ' # A, B, C
            sideLabel = QLabel(label.lower()) # a, b, c
            self.dimensionsLayout.addWidget(sideLabel)
            
            sideIB = QLineEdit(self)
            sideIB.setValidator(QDoubleValidator(0,400,2))
            sideIB.setText('0.00')
            
            sideIB.textChanged.connect(self.validateSideLength)   
            sideIB.textChanged.connect(self.updateInputFieldStatus)
              
            self.dimensionsLayout.addWidget(sideIB)
            self.sideIBs.append(sideIB)
        
        for i in range(3): # 3 angles
            label = f'{chr(65+i)} = ' # A, B, C
            angleLabel = QLabel('∠' + label)
            self.dimensionsLayout.addWidget(angleLabel)
            
            angleIB = QLineEdit(self)
            angleIB.setValidator(QDoubleValidator(0,400,2))
            angleIB.setText('0.00')            
            
            angleIB.textChanged.connect(self.validateAngle)
            angleIB.textChanged.connect(self.updateInputFieldStatus)
            
            self.dimensionsLayout.addWidget(angleIB)
            self.angleIBs.append(angleIB)
            
        diemnsionsGroupBox.setLayout(self.dimensionsLayout)
        self.gridLayout.addWidget(diemnsionsGroupBox, 2, 0, 1, 2) # 2 rows, 2 columns, row span = 1, column span = 2
        
    def initOptionsBox(self):
        '''
        Creates a Group Box to select the operations to be performed on the triangle.
        '''
        optionsGroupBox = QGroupBox('Select Operation:')        
        optionsGroupBox.setLayout(self.optionsLayout)
        self.gridLayout.addWidget(optionsGroupBox, 1, 0, 1, 2) # 1 row, 2 columns, row span = 1, column span = 2   
        
    def initRadioBtns(self):
        '''
        Creates five Radio Buttons to select the operations to be performed on the triangle.
        These radio buttons are added to the optionsLayout.
        '''
        self.radioBtnSOH = QRadioButton('SOH')
        self.radioBtnCAH = QRadioButton('CAH')
        self.radioBtnTOA = QRadioButton('TOA')
        self.radioBtnSineLaw = QRadioButton('Sine Law')
        self.radioBtnCosineLaw = QRadioButton('Cosine Law')
    
        self.radioBtnSOH.setChecked(True)  # Set default selection
        self.onSohCahToaClicked(True)

        self.optionsLayout.addWidget(self.radioBtnSOH)
        self.optionsLayout.addWidget(self.radioBtnCAH)
        self.optionsLayout.addWidget(self.radioBtnTOA)
        self.optionsLayout.addWidget(self.radioBtnSineLaw)
        self.optionsLayout.addWidget(self.radioBtnCosineLaw)
    
        self.radioBtnSOH.toggled.connect(self.onSohCahToaClicked)
        self.radioBtnCAH.toggled.connect(self.onSohCahToaClicked)
        self.radioBtnTOA.toggled.connect(self.onSohCahToaClicked)
        self.radioBtnSineLaw.toggled.connect(self.onSineCosineLawClicked)
        self.radioBtnCosineLaw.toggled.connect(self.onSineCosineLawClicked)
    
    def drawTriangle(self, triangle):
        '''
        Takes a triangle object as an argument and draws it on the QGraphicsView object.
        '''      
        if self.triangle.errorMessage:
            self.statusBar.showMessage(self.triangle.errorMessage, 3000)
            return 
        
        triangle.vertices = triangle.calculateVertices()
        polygon = QPolygonF(triangle.vertices)
        triangleItem = QGraphicsPolygonItem(polygon)

        self.scaleFactor = min(triangle.a, triangle.b, triangle.c) # used to scale components of the triangle to look good on the screen  

        if not self.triangleView.scene():
            self.triangleView.setScene(QGraphicsScene())
            
        self.triangleView.scene().clear() # clear the scene before adding new items
        self.triangleView.scene().addItem(triangleItem)
        
        self.drawAngles(triangle)
        self.drawLabels(triangle)        
        
    def drawAngles(self, triangle):
        '''
        Draws representation of angles of the triangle using arcs.
        '''
        angleArcRadius = self.scaleFactor / 5 
        angles = [triangle.A, triangle.B, triangle.C]
        
        for i, angle in enumerate(angles):
            '''
            startAngle is the angle between the x-axis and the line joining the center of the circle and the vertex of the triangle.
            It is calculated as follows:
            1. For the first vertex, it is 0 since c is parallel to the x-axis.
            2. For the second vertex, it is π - B since that is the the angle between positive x axis and a. 
            3. For the third vertex, it is A - π since that is the angle between positive x axis and a.
            '''
            if (i == 0):
                startAngle = 0
            elif (i ==1):
                startAngle = math.pi - triangle.B
            else:
                startAngle = triangle.A - math.pi
        
            self.drawArc(triangle.vertices[i], math.degrees(startAngle), 
                         math.degrees(angle), angleArcRadius)  
    
    def drawArc(self, center, startAngle, angle, radius):
        '''
        Draws an arc with the given center, start angle, span angle and radius.
        '''
        rect = QRectF(center.x() - radius, center.y() - radius, 2 * radius, 2 * radius) 
        
        startAngle = startAngle * 16 # since QGraphicEllipseItem takes angles in 1/16th of a degree 
        spanAngle = angle * 16 # (idk why tho :/ so much time wasted on this for no reason)
        
        arc = QGraphicsEllipseItem(rect)
        arc.setStartAngle(int(startAngle))
        arc.setSpanAngle(int(spanAngle))
        
        pen = QPen(QColor('#f08080'), 1) # light coral to differentiate from the triangle
        arc.setPen(pen)
        
        self.triangleView.scene().addItem(arc)
        
    def drawLabels(self, triangle):  
        '''
        Draws labels for the sides and angles of the triangle.
        '''
        unit = 0.5 + self.scaleFactor / 200 # to ensure proper spacing between labels and triangle (doesn't work properly haha)
        
        sideLabels = [
            f'a={triangle.a:.2f}', 
            f'b={triangle.b:.2f}', 
            f'c={triangle.c:.2f}'
        ]
        
        angleLabels = [
            f'∠A={math.degrees(triangle.A):.2f}°',
            f'∠B={math.degrees(triangle.B):.2f}°',
            f'∠C={math.degrees(triangle.C):.2f}°'
        ]        
        
        for i, label in enumerate(sideLabels): # side labesls are positioned based on the midpoint of the side
            textItem = QGraphicsTextItem(label)
            midpoint = (triangle.vertices[(i+1) % 3] + triangle.vertices[(i+2) % 3]) / 2
            
            if (i == 2): 
                textItem.setPos(midpoint + unit * QPointF(-20,-20)) # these offsets were found by trial and error
            elif (i == 0):
                textItem.setPos(midpoint + unit * QPointF(10,-20))  # they're not perfect but they get the job done
            else:
                textItem.setPos(midpoint + unit * QPointF(-60,-20))

            textItem.setFont(self.font)
            self.triangleView.scene().addItem(textItem)
        
        for i, label in enumerate(angleLabels): # angle labels are positioned based on the vertex
            textItem = QGraphicsTextItem(label)

            vertex = triangle.vertices[i]
            if (i ==2):
                textItem.setPos(vertex + unit * QPointF(-30, -20)) # again, these offsets were found by trial and error
            else:
                textItem.setPos(vertex + unit * QPointF(-30, 5))

            textItem.setFont(self.font)
            self.triangleView.scene().addItem(textItem)
            
    def onSohCahToaClicked(self, checked):
        '''
        Called when the SOH/CAH/TOA radio button is clicked.
        '''
        if checked:     
            self.angleIBs[0].setText('90.00') # make sure A is 90 degrees in SOH/CAH/TOA            
            self.resetInput() # reset input fields
            
    def onSineCosineLawClicked(self, checked):
        '''
        Called when the Sine/Cosine Law radio button is clicked. 
        '''        
        if checked:    
            self.angleIBs[0].setText('0.00') # set A back to 0 degrees in sine/cosine law            
            self.resetInput()                 
        
    def updateInputFieldStatus(self):
        '''
        Since 3 properties determine a unique triangle (except AAA), we need to disable the input fields when we have 3 of them.
        '''
        count = sum(float(field.text()) != 0 for field in self.sideIBs + self.angleIBs) # count the number of non-zero inputs
        
        for field in self.sideIBs + self.angleIBs:
            if count >= 3 and (float(field.text()) == 0): # unique triangle              
                field.setDisabled(True)
            else:
                field.setDisabled(False)
                
        if self.radioBtnSOH.isChecked() or self.radioBtnCAH.isChecked() or self.radioBtnTOA.isChecked():
            self.angleIBs[0].setDisabled(True) # A is always 90 degrees in SOH/CAH/TOA and stays disabled to prevent user from changing it
            
    def calculateAndUpdateDisplay(self, display = False):
        '''
        Takes in the input from the input boxes and creates a Triangle object.
        Then it draws the triangle and updates the info box.
        '''        
        try:
            a = float(self.sideIBs[0].text()) if self.sideIBs[0].text() and float(self.sideIBs[0].text()) != 0 else None # if the input is 0, it is ignored
            b = float(self.sideIBs[1].text()) if self.sideIBs[1].text() and float(self.sideIBs[1].text()) != 0 else None
            c = float(self.sideIBs[2].text()) if self.sideIBs[2].text() and float(self.sideIBs[2].text()) != 0 else None
            A = float(self.angleIBs[0].text()) if self.angleIBs[0].text() and float(self.angleIBs[0].text()) != 0 else None
            B = float(self.angleIBs[1].text()) if self.angleIBs[1].text() and float(self.angleIBs[1].text()) != 0 else None
            C = float(self.angleIBs[2].text()) if self.angleIBs[2].text() and float(self.angleIBs[2].text()) != 0 else None
            
            lawChosen = TrigLaw.SOH 
            if self.radioBtnSOH.isChecked():
                lawChosen = TrigLaw.SOH
            elif self.radioBtnCAH.isChecked():
                lawChosen = TrigLaw.CAH
            elif self.radioBtnTOA.isChecked():
                lawChosen = TrigLaw.TOA
            elif self.radioBtnSineLaw.isChecked():
                lawChosen = TrigLaw.SINE_LAW
            elif self.radioBtnCosineLaw.isChecked():
                lawChosen = TrigLaw.COSINE_LAW   
                
            self.triangle = Triangle(a, b, c, A, B, C, lawChosen)
            
            if self.triangle.errorMessage: # catch errors, dsplay them and halt execution
                self.statusBar.showMessage(self.triangle.errorMessage, 3000) 
                return
            
            self.updateInfoBox(a = a, b = b, c = c, A = A, B = B, C = C) # add the procedures to the info box
            self.drawTriangle(self.triangle)   
        except ValueError: # I did do a lot of validation just in case haha
            if (display):
                self.statusBar.showMessage('Invalid input, not a feasible/unique triangle!', 3000) 
            
    def validateSideLength(self):
        '''
        Validation of the side length input to make sure the following conditions are met:
        1. The input is a valid number.
        2. The input is not negative.
        3. The input is contrstrained to prevent it from being too large to be displayed in the area.        
        '''
        sender = self.sender()
        maxLength = round(min(self.w // 1.5, self.h // 1.5))

        try:
            value = float(sender.text())
            if value < 0.0 or value > maxLength:
                sender.setText(str(maxLength)) # contrain to maxLength if it's too large or negative
                self.statusBar.showMessage(f'Side length should be between 0 and {maxLength} (to be displayed in the area)', 3000)
        except ValueError:
            sender.setText('0')  # 0 if it's not a valid number

    def validateAngle(self):
        '''
        Validation of the angle input to make sure the following conditions are met:
        1. The input is a valid number.
        2. The input is between 0 and 180 degrees.
        '''
        sender = self.sender()

        try:
            value = float(sender.text())
            if value < 0.0 or value > 180.0:
                sender.setText('180')  # 180 if it's too large or negative
                self.statusBar.showMessage('Angle should be between 0 and 180 (obviously)', 3000)
        except ValueError:
            sender.setText('0')  # 0 if it's not a valid number
            
    def updateInfoBox(self, a= None, b = None, c = None, A= None, B = None, C = None):
        '''
        Displays the procedures involved in drawing the triangle in the info box. 
        It is based on the laws obtained from the Triangle object.
        '''
        for i in reversed(range(self.infoLayout.count())): # clear all the previous procedures
            self.infoLayout.itemAt(i).widget().setParent(None)   

        jointLaws = '<br>'.join(self.triangle.lawsUsed) 
        label = QLabel(jointLaws, self)
        label.setFont(self.font)
        self.infoLayout.addWidget(label)                   
            
    def resetInput(self):
        '''
        Resets the input fields to their default values.
        '''
        for sideIB in self.sideIBs:
            sideIB.setText('0.00')
        for angleIB in self.angleIBs:
            angleIB.setText('0.00')            
       
        if self.radioBtnSOH.isChecked() or self.radioBtnCAH.isChecked() or self.radioBtnTOA.isChecked():
            self.angleIBs[0].setText('90.00') # make sure A is 90 degrees in SOH/CAH/TOA