# Inspired by PyQt5 Creating Paint Application In 40 Minutes
#  https://www.youtube.com/watch?v=qEgyGyVA1ZQ

# NB If the menus do not work then click on another application ad then click back
# and they will work https://python-forum.io/Thread-Tkinter-macOS-Catalina-and-Python-menu-issue

# PyQt documentation links are prefixed with the word 'documentation' in the code below and can be accessed automatically
#  in PyCharm using the following technique https://www.jetbrains.com/help/pycharm/inline-documentation.html

from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QFileDialog, QMessageBox, QToolBar, QLabel
from PyQt5.QtGui import QIcon, QImage, QPainter, QPen, QPixmap
import sys
from PyQt5.QtCore import Qt, QPoint
from qtpy import QtCore


class PaintingApplication(QMainWindow): # documentation https://doc.qt.io/qt-5/qmainwindow.html
    '''
    Painting Application class
    '''

    def __init__(self):
        super().__init__()

        # set window title
        self.setWindowTitle("Paint Application")

        # set the windows dimensions
        top = 400
        left = 400
        width = 800
        height = 600
        self.setGeometry(top, left, width, height)

        #set the icon
        # windows version
        self.setWindowIcon(QIcon("./icons/paint-brush.png")) # documentation: https://doc.qt.io/qt-5/qwidget.html#windowIcon-prop
        # mac version - not yet working
        # self.setWindowIcon(QIcon(QPixmap("./icons/paint-brush.png")))

        # create toolbar
        toolBar = QToolBar("Brush Size") # brush size toolbar
        self.addToolBar(toolBar)

        colorToolBar = QToolBar("Brush Color") # color toolbar
        self.addToolBar(colorToolBar)
        styleToolBar = QToolBar("Brush Style") # style toolbar
        self.addToolBar(styleToolBar)
        capToolBar = QToolBar("Brush Cap")
        self.addToolBar(QtCore.Qt.LeftToolBarArea, capToolBar)
        typeToolBar = QToolBar("Brush Type")
        self.addToolBar(QtCore.Qt.LeftToolBarArea, typeToolBar)


       # self.setBrushStyle()


        # image settings (default)
        self.image = QImage(self.size(), QImage.Format_RGB32) # documentation: https://doc.qt.io/qt-5/qimage.html#QImage-1
        self.image.fill(Qt.white) # documentation: https://doc.qt.io/qt-5/qimage.html#fill-1

        # draw settings (default)
        self.drawing = False
        self.brushSize = 3
        self.brushColor = Qt.black # documenation: https://doc.qt.io/qtforpython/PySide2/QtCore/Qt.html
        self.brushStyle = Qt.SolidLine
        self.brushCap = Qt.RoundCap
        self.brushJoin = Qt.RoundJoin

        # reference to last point recorded by mouse
        self.lastPoint = QPoint() # documenation: https://doc.qt.io/qt-5/qpoint.html

        # set up menus
        mainMenu = self.menuBar() # create and a menu bar
        fileMenu = mainMenu.addMenu(" File") # add the file menu to the menu bar, the space is required as "File" is reserved in Mac
        helpMenu = mainMenu.addMenu(" Help")  # add the "Help" menu to the menu bar

        # save menu item
        saveAction = QAction(QIcon("./icons/save.png"), "Save", self)   # create a save action with a png as an icon, documenation: https://doc.qt.io/qt-5/qaction.html
        saveAction.setShortcut("Ctrl+S")                                # connect this save action to a keyboard shortcut, documentation: https://doc.qt.io/qt-5/qaction.html#shortcut-prop
        fileMenu.addAction(saveAction)                                  # add the save action to the file menu, documentation: https://doc.qt.io/qt-5/qwidget.html#addAction
        saveAction.triggered.connect(self.save)                         # when the menu option is selected or the shortcut is used the save slot is triggered, documenation: https://doc.qt.io/qt-5/qaction.html#triggered

        # clear
        clearAction = QAction(QIcon("./icons/clear.png"), "Clear", self) # create a clear action with a png as an icon
        clearAction.setShortcut("Ctrl+C")                                # connect this clear action to a keyboard shortcut
        fileMenu.addAction(clearAction)                                  # add this action to the file menu
        clearAction.triggered.connect(self.clear)                        # when the menu option is selected or the shortcut is used the clear slot is triggered

        # open
        openAction = QAction(QIcon("./icons/open.png"), "Open", self)
        openAction.setShortcut("Ctrl+O")
        fileMenu.addAction(openAction)
        openAction.triggered.connect(self.open)

        # exit
        exitAction = QAction(QIcon("./icons/exit.png"), "Exit", self)
        exitAction.setShortcut("Ctrl+E")
        fileMenu.addAction(exitAction)
        exitAction.triggered.connect(self.exit)

        # help
        helpAction = QAction(QIcon("./icons/help.png"), "Help", self)
        helpAction.setShortcut("Ctrl+H")
        helpMenu.addAction(helpAction)
        helpAction.triggered.connect(self.help)

        # about
        aboutAction = QAction(QIcon("./icons/about.png"), "About", self)
        aboutAction.setShortcut("Ctrl+A")
        helpMenu.addAction(aboutAction)
        aboutAction.triggered.connect(self.about)


        # brush thickness
        sizeLabel = QLabel("Size ") #label for toolbar
        toolBar.addWidget(sizeLabel)
        toolBar.addSeparator()

        threepxAction = QAction(QIcon("./icons/3.png"), "3px", self)
        threepxAction.setShortcut("3")  # TODO changed the control options to be numbers
        toolBar.addAction(threepxAction)  # connect the action to the function below
        threepxAction.triggered.connect(self.threepx)

        fivepxAction = QAction(QIcon("./icons/5.png"), "5px", self)
        fivepxAction.setShortcut("5")
        toolBar.addAction(fivepxAction)
        fivepxAction.triggered.connect(self.fivepx)

        sevenpxAction = QAction(QIcon("./icons/7.png"), "7px", self)
        sevenpxAction.setShortcut("7")
        toolBar.addAction(sevenpxAction)
        sevenpxAction.triggered.connect(self.sevenpx)

        ninepxAction = QAction(QIcon("./icons/9.png"), "9px", self)
        ninepxAction.setShortcut("9")
        toolBar.addAction(ninepxAction)
        ninepxAction.triggered.connect(self.ninepx)

        # brush colors
        colorLabel = QLabel("Color ") # label for toolbar
        colorToolBar.addWidget(colorLabel)
        colorToolBar.addSeparator()

        blueAction = QAction(QIcon("./icons/blue.png"), "Blue", self)
        blueAction.setShortcut("Ctrl+D")
        colorToolBar.addAction(blueAction);
        blueAction.triggered.connect(self.blue)

        redAction = QAction(QIcon("./icons/red.png"), "Red", self)
        redAction.setShortcut("Ctrl+R")
        colorToolBar.addAction(redAction);
        redAction.triggered.connect(self.red)

        blackAction = QAction(QIcon("./icons/black.png"), "Black", self)
        blackAction.setShortcut("Ctrl+B")
        colorToolBar.addAction(blackAction);
        blackAction.triggered.connect(self.black)

        greenAction = QAction(QIcon("./icons/green.png"), "Green", self)
        greenAction.setShortcut("Ctrl+G")
        colorToolBar.addAction(greenAction);
        greenAction.triggered.connect(self.green)

        yellowAction = QAction(QIcon("./icons/yellow.png"), "Yellow", self)
        yellowAction.setShortcut("Ctrl+Y")
        colorToolBar.addAction(yellowAction);
        yellowAction.triggered.connect(self.yellow)

        cyanAction = QAction(QIcon("./icons/cyan.png"), "Cyan", self)
        cyanAction.setShortcut("Ctrl+N")
        colorToolBar.addAction(cyanAction);
        cyanAction.triggered.connect(self.cyan)



        # Brush style
        styleLabel = QLabel("Style ") # ;abel for toolbar
        styleToolBar.addWidget(styleLabel)
        styleToolBar.addSeparator()

        solidAction = QAction(QIcon("./icons/solid.png"), "Solid", self)
        styleToolBar.addAction(solidAction);
        solidAction.triggered.connect(self.solid)

        dashAction = QAction(QIcon("./icons/dash.png"), "Dash", self)
        styleToolBar.addAction(dashAction);
        dashAction.triggered.connect(self.dash)

        dotAction = QAction(QIcon("./icons/dot.png"), "Dot", self)
        styleToolBar.addAction(dotAction);
        dotAction.triggered.connect(self.dot)

        dashDotDotAction = QAction(QIcon("./icons/dot.png"), "Dash Dot Dot", self)
        styleToolBar.addAction(dashDotDotAction);
        dashDotDotAction.triggered.connect(self.dashDotDot)

        # Brush Type
        typeLabel = QLabel(" Cap ") # label for toolbar
        typeToolBar.addWidget(typeLabel)
        typeToolBar.addSeparator()

        squareAction = QAction(QIcon("./icons/square.png"), "Square", self)
        typeToolBar.addAction(squareAction);
        squareAction.triggered.connect(self.square)

        roundAction = QAction(QIcon("./icons/round.png"), "Round", self)
        typeToolBar.addAction(roundAction);
        roundAction.triggered.connect(self.round)

        flatAction = QAction(QIcon("./icons/flat.png"), "flat", self)
        typeToolBar.addAction(flatAction);
        dotAction.triggered.connect(self.flat)

        # Brush Cap
        capLabel = QLabel(" Join ") # label for toolbar
        capToolBar.addWidget(capLabel)
        capToolBar.addSeparator()

        bevelJoinAction = QAction(QIcon("./icons/bevel.png"), "Bevel", self)
        capToolBar.addAction(bevelJoinAction);
        bevelJoinAction.triggered.connect(self.bevelJoin)

        miterJoinAction = QAction(QIcon("./icons/miter.png"), "Miter", self)
        capToolBar.addAction(miterJoinAction);
        miterJoinAction.triggered.connect(self.miterJoin)

        roundAction = QAction(QIcon("./icons/roundJ.png"), "Round", self)
        capToolBar.addAction(roundAction);
        roundAction.triggered.connect(self.roundJoin)


    # event handlers
    def mousePressEvent(self, event):       # when the mouse is pressed, documentation: https://doc.qt.io/qt-5/qwidget.html#mousePressEvent
        if event.button() == Qt.LeftButton:  # if the pressed button is the left button
            painter = QPainter(self.image)
            painter.setPen(QPen(self.brushColor, self.brushSize, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
            self.drawing = True             # enter drawing mode
            self.lastPoint = event.pos()    # save the location of the mouse press as the lastPoint
            print(self.lastPoint)           # print the lastPoint for debigging purposes

    def mouseMoveEvent(self, event):                        # when the mouse is moved, documenation: documentation: https://doc.qt.io/qt-5/qwidget.html#mouseMoveEvent
     if event.buttons() & Qt.LeftButton & self.drawing:     # if there was a press, and it was the left button and we are in drawing mode
            painter = QPainter(self.image)                  # object which allows drawing to take place on an image
            # allows the selection of brush colour, brish size, line type, cap type, join type. Images available here http://doc.qt.io/qt-5/qpen.html
            #painter.setPen(QPen(self.brushColor, self.brushSize, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
            painter.setPen(QPen(self.brushColor, self.brushSize, self.brushStyle, self.brushCap, self.brushJoin))
            painter.drawLine(self.lastPoint, event.pos())   # draw a line from the point of the orginal press to the point to where the mouse was dragged to
            self.lastPoint = event.pos()                     # set the last point to refer to the point we have just moved to, this helps when drawing the next line segment
            self.update()                                   # call the update method of the widget which calls the paintEvent of this class

    def mouseReleaseEvent(self, event):                     # when the mouse is released, documentation: https://doc.qt.io/qt-5/qwidget.html#mouseReleaseEvent
        if event.button == Qt.LeftButton:                   # if the released button is the left button, documenation: https://doc.qt.io/qt-5/qt.html#MouseButton-enum ,
            self.drawing = False                            # exit drawing mode

    # paint events
    def paintEvent(self, event):
        # you should only create and use the QPainter object in this method, it should be a local variable
        canvasPainter = QPainter(self)                      # create a new QPainter object, documenation: https://doc.qt.io/qt-5/qpainter.html
        canvasPainter.drawImage(self.rect(), self.image, self.image.rect()) # draw the image , documentation: https://doc.qt.io/qt-5/qpainter.html#drawImage-1

    # resize event - this function is called
    def resizeEvent(self, event):
        self.image = self.image.scaled(self.width(), self.height())

    # slots
    def save(self):
        filePath, _ = QFileDialog.getSaveFileName(self, "Save Image","", "PNG(*.png);;JPG(*.jpg *.jpeg);;All Files (*.*)")
        if filePath =="": # if the file path is empty
            return # do nothing and return
        self.image.save(filePath) # save file image to the file path

    # clear
    def clear(self):
        self.image.fill(Qt.white)   # fill the image with white, documentaiton: https://doc.qt.io/qt-5/qimage.html#fill-2
        self.update()               # call the update method of the widget which calls the paintEvent of this class

    def threepx(self):              # the brush size is set to 3
        self.brushSize = 3

    def fivepx(self):
        self.brushSize = 5

    def sevenpx(self):
        self.brushSize = 7

    def ninepx(self):
        self.brushSize = 9

    def black(self):                # the brush color is set to black
        self.brushColor = Qt.black

    def red(self):
        self.brushColor = Qt.red

    def green(self):
        self.brushColor = Qt.green

    def yellow(self):
        self.brushColor = Qt.yellow

    def blue(self):
        self.brushColor = Qt.blue

    def cyan(self):
        self.brushColor = Qt.cyan

    #function for style
    def solid(self):
        self.brushStyle = Qt.SolidLine

    def dash(self):
        self.brushStyle = Qt.DashLine

    def dot(self):
        self.brushStyle = Qt.DotLine

    def dashDotDot(self):
        self.brushStyle = Qt.DashDotDotLine

    # function for cap
    def square(self):
        self.brushCap = Qt.SquareCap

    def flat(self):
        self.brushCap = Qt.FlatCap

    def round(self):
        self.brushCap = Qt.RoundCap

    # function for join
    def roundJoin(self):
        self.brushJoin = Qt.RoundJoin

    def miterJoin(self):
        self.brushJoin = Qt.MiterJoin

    def bevelJoin(self):
        self.brushJOin = Qt.BevelJoin


    # exit file
    def exit(self):
        QtCore.QCoreApplication.quit()

    # about
    def about(self):
        msg = QMessageBox()
        msg.setText(
                    "<p>This PyQt Application is a painting Program. "
                    "You can draw something by yourself and then save it as a picture. "
                    "</p>")
        msg.setWindowTitle("About")
        msg.exec_()

    # help
    def help(self):
        msg = QMessageBox()
        msg.setText(
                    "<p>Welcome</p> "
                    "<p>On the top of the screen you can see toolbars with brush size, brush color, brush style. "
                    "On the left side of the screen there are two toolbar, onr for brush cap and other for brush type. "
                    "Each of these toolbar contains icon which allow you to customize the brush you want to"
                    "draw with.</p>"
                    "<p>The right size of the screen is the drawing area, where you can draw.</p> "
                    "<p>The program also has different menus you can see at the top of the window. "
                    "<p>These menus allow you to save, clear, open a file and exit the program.</p>")
        msg.setWindowTitle("Help")
        msg.exec_()

    # open a file
    def open(self):
        '''
        This is an additional function which is not part of the tutorial. It will allow you to:
         - open a file doalog box,
         - filter the list of files according to file extension
         - set the QImage of your application (self.image) to a scaled version of the file)
         - update the widget
        '''
        filePath, _ = QFileDialog.getOpenFileName(self, "Open Image", "",
                                                  "PNG(*.png);;JPG(*.jpg *.jpeg);;All Files (*.*)")
        if filePath == "":   # if not file is selected exit
            return
        with open(filePath, 'rb') as f: #open the file in binary mode for reading
            content = f.read() # read the file
        self.image.loadFromData(content) # load the data into the file
        width = self.width() # get the width of the current QImage in your application
        height = self.height() # get the height of the current QImage in your application
        self.image = self.image.scaled(width, height) # scale the image from file and put it in your QImage
        self.update() # call the update method of the widget which calls the paintEvent of this class


# this code will be executed if it is the main module but not if the module is imported
#  https://stackoverflow.com/questions/419163/what-does-if-name-main-do
if __name__=="__main__":
    app = QApplication(sys.argv)
    window = PaintingApplication()
    window.show()
    app.exec() # start the event loop running