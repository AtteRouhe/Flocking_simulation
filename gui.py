from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import Qt
from world import World
from boid_graphics_item import BoidGraphicsItem
from boid import Boid
import sys


class SimulationWindow(QMainWindow):

    def __init__(self):
        super(SimulationWindow, self).__init__()
        self.setCentralWidget(QtWidgets.QWidget())
        self.vertical = QtWidgets.QVBoxLayout()
        # vertical layout
        self.centralWidget().setLayout(self.vertical)

        # init world and a list for the graphic items
        self.world = World()
        self.boid_graphics_items = []

        # init the window
        self.setGeometry(1200, 200, 1050, 1400)
        self.setWindowTitle("Flocking Simulation")
        self.show()

        # scene for graphics
        self.scene = GraphicsScene(self.world, self)

        # sliders for changing rule weights, cohesion, separation, alignment, max speed and range
        self.c_slider = QtWidgets.QSlider(Qt.Horizontal)
        self.s_slider = QtWidgets.QSlider(Qt.Horizontal)
        self.a_slider = QtWidgets.QSlider(Qt.Horizontal)
        self.speed_slider = QtWidgets.QSlider(Qt.Horizontal)
        self.range_slider = QtWidgets.QSlider(Qt.Horizontal)

        # connect to functions
        self.c_slider.valueChanged[int].connect(self.change_cohesion)
        self.s_slider.valueChanged[int].connect(self.change_separation)
        self.a_slider.valueChanged[int].connect(self.change_alignment)
        self.speed_slider.valueChanged[int].connect(self.change_max_speed)
        self.range_slider.valueChanged[int].connect(self.change_range)

        # add a view for the scene
        self.view = QtWidgets.QGraphicsView(self.scene, self)
        self.view.adjustSize()
        self.view.show()
        self.vertical.addWidget(self.view)

        # add slider to layout
        self.vertical.addWidget(QtWidgets.QLabel("Cohesion (0 - 9.9)"))
        self.vertical.addWidget(self.c_slider)
        self.vertical.addWidget(QtWidgets.QLabel("Alignment (0 - 9.9)"))
        self.vertical.addWidget(self.a_slider)
        self.vertical.addWidget(QtWidgets.QLabel("Separation (0 - 9.9)"))
        self.vertical.addWidget(self.s_slider)
        self.vertical.addWidget(QtWidgets.QLabel("Max speed (0 - 99)"))
        self.vertical.addWidget(self.speed_slider)
        self.vertical.addWidget(QtWidgets.QLabel("Range (0 - 990)"))
        self.vertical.addWidget(self.range_slider)

        """
        # init 30 boids to simulation
        for i in range(30):
            b = Boid(500, 500, self.world)
            self.world.boids.append(b)
            item = BoidGraphicsItem(b)
            self.boid_graphics_items.append(item)
            self.scene.addItem(item)
        """

        # a timer to update simulation
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(30)  # Milliseconds

    # Update the world and re draw the boids and objects
    def update(self):
        # update boids positions
        self.world.update_all()
        # update graphics in gui
        for b in self.boid_graphics_items:
            b.update()

    # function to change worlds rules
    def change_cohesion(self):
        self.world.coh_w = self.c_slider.value() / 10

    def change_separation(self):
        self.world.sep_w = self.s_slider.value() / 10

    def change_alignment(self):
        self.world.ali_w = self.a_slider.value() / 10

    def change_max_speed(self):
        self.world.max_speed = self.speed_slider.value()

    def change_range(self):
        self.world.range = self.range_slider.value() * 10


# overwrite class to overwrite mousePressEvent
class GraphicsScene(QtWidgets.QGraphicsScene):

    def __init__(self, world, gui, parent=None):
        QtWidgets.QGraphicsScene.__init__(self, parent)
        self.setSceneRect(0, 0, 1000, 1000)
        self.world = world
        self.gui = gui

    # add a new boid to clicked x and y, create new graphics item
    def mousePressEvent(self, event):
        x = int(event.scenePos().x())
        y = int(event.scenePos().y())
        b = Boid(x, y, self.world)
        self.world.boids.append(b)
        item = BoidGraphicsItem(b)
        self.gui.boid_graphics_items.append(item)
        self.addItem(item)


# init the window and main loop
def init_window():
    global app
    app = QApplication(sys.argv)
    win = SimulationWindow()
    sys.exit(app.exec_())


init_window()
