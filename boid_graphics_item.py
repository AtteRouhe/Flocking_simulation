from PyQt5 import QtWidgets, QtGui, QtCore


# represents the icon drawn in the scene, connected to a boid in "world"
class BoidGraphicsItem(QtWidgets.QGraphicsPolygonItem):

    def __init__(self, boid):
        super(BoidGraphicsItem, self).__init__()
        self.boid = boid

        # brush
        brush = QtGui.QBrush(1)
        self.setBrush(brush)

        # set up the corners
        triangle = QtGui.QPolygonF()
        triangle.append(QtCore.QPointF(6, 0))  # Tip
        triangle.append(QtCore.QPointF(0, 6))  # Bottom-left
        triangle.append(QtCore.QPointF(6, 6))  # Bottom-right
        triangle.append(QtCore.QPointF(6, 0))  # Tip
        self.setPolygon(triangle)
        self.setTransformOriginPoint(6, 6)

        # paint the boid black
        QtWidgets.QAbstractGraphicsShapeItem.setBrush(self, QtGui.QColor(0))

    # update graphics item
    def update(self):
        self.update_position()

    # update the graphic items position in the scene
    def update_position(self):
        x = self.boid.position[0]
        y = self.boid.position[1]
        self.setPos(x, y)

