#! c:/Python27/python.exe
# -*- coding: utf-8 -*- 

from PyQt4 import QtGui, QtCore, QtOpenGL
from PyQt4.QtOpenGL import QGLWidget
from PyQt4 import Qt
import OpenGL.GL as gl
import OpenGL.arrays.vbo as glVBO
import Boid

class GLPlotWidget(QGLWidget):
	# Set window size
	width, height = 800, 600
	
	def __init__(self, parent = 0, name = '' ,flags = 0):
		QtOpenGL.QGLWidget.__init__(self)

	def set_data(self, data):
		self.data = data
		self.count = data.shape[0]
		
	def initializeGL(self):
		# background color
		gl.glClearColor(0, 0, 0, 0)
		self.vbo = glVBO.VBO(self.data)

	def paintGL(self):
		self.vbo = glVBO.VBO(self.data)		
		gl.glClear(gl.GL_COLOR_BUFFER_BIT)
		gl.glColor(1, 1, 0)
		gl.glPointSize(5)
		self.vbo.bind()
		gl.glEnableClientState(gl.GL_VERTEX_ARRAY)
		gl.glVertexPointer(2, gl.GL_FLOAT, 0, self.vbo)
		gl.glDrawArrays(gl.GL_POINTS, 0, self.count)

	def resizeGL(self, width, height):
		self.width, self.height = width, height
		gl.glViewport(0, 0, width, height)
		gl.glMatrixMode(gl.GL_PROJECTION)
		gl.glLoadIdentity()
		#glOrtho(left, rught, bottom, top, nearX, farZ)
		gl.glOrtho(-200, 200, -200, 200, -1, 1)
 
if __name__ == '__main__':
	import sys
	import numpy
	import time
	
	myBoids = Boid.Boids()
	myBoids.setAreaWidth(200)
	
	class MainWindow(QtGui.QMainWindow):
		def __init__(self):
			super(MainWindow, self).__init__()
			coord = myBoids.getCoords2D()
			self.data = numpy.array(coord, dtype=numpy.float32)
			
			self.widget = GLPlotWidget()
			self.widget.set_data(self.data)
			
			# Put the window at (100, 100)
			self.setGeometry(100, 100, self.widget.width, self.widget.height)
			self.setCentralWidget(self.widget)

			self.timer = Qt.QTimer()
			self.timer.setInterval(100)
			QtCore.QObject.connect(self.timer, QtCore.SIGNAL("timeout()"), self.draw)
			self.timer.start(100)
			
			self.show()
		
		def draw(self):
			myBoids.update()	
			coord = myBoids.getCoords2D()			
			self.data = numpy.array(coord, dtype=numpy.float32)
			self.widget.set_data(self.data)
			self.widget.update()

	app = QtGui.QApplication(sys.argv)
	window = MainWindow()
	window.show()
	app.exec_()
	