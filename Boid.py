#! c:/Python27/python.exe
# -*- coding: utf-8 -*- 

import math
import random

class Boid:
	def __init__(self):
		self.position = [0, 0, 0]
		self.velocity = [0, 0, 0]

class Boids:
	def __init__(self):
		self.NUM_BOIDS = 75
		self.SEPARATION_DISTANCE = 6.0
		self.PARAM_COHESION = 0.01
		self.PARAM_SEPARATION = 0.5
		self.PARAM_ALINGMENT = 0.125
		self.areaWidth = 100
		
		# Create boids
		self.boids = []
		for i in range(self.NUM_BOIDS):
			self.boids.append(Boid())

		# Initialize boids
		for i in range(self.NUM_BOIDS):
			self.boids[i].position[0] = random.uniform(0, 40.0)
			self.boids[i].position[1] = random.uniform(0, 40.0)
			self.boids[i].position[2] = random.uniform(0, 40.0)
			self.boids[i].velocity[0] = 0
			self.boids[i].velocity[1] = 0
			self.boids[i].velocity[2] = 0
	
	def setAreaWidth(self, w):
		self.areaWidth = w
	
	# Get array[NUM_BOIDS][2] that represents position(x, y) of boids
	def getCoords2D(self):
		coord = []
		for i in range(self.NUM_BOIDS):
			coord.append([self.boids[i].position[0], self.boids[i].position[1]])

		return coord
	
	# Calculate the cohesion effect
	def getCohesionVelocity(self, id):
		velocity = [0, 0, 0]
		
		# Sum all other boid's position
		for i in range(self.NUM_BOIDS):
			if i != id:
				for j in range(3):
					velocity[j] = velocity[j]  + self.boids[i].position[j]
		
		# Get the center of boids
		for i in range(3):
			velocity[i] = velocity[i] / (self.NUM_BOIDS-1)
		
		# Get the veloicty toward the center of boids
		for i in range(3):
			velocity[i] = (velocity[i]  - self.boids[id].position[i]) * self.PARAM_COHESION
		
		return velocity
	
	# Calculate the distance between two vectors
	def getDistance(self, vecA, vecB):
		diff = [vecA[0] - vecB[0], vecA[1] - vecB[1], vecA[2] - vecB[2]]
		r = diff[0]*diff[0] +  diff[1]*diff[1]  +  diff[2]*diff[2] 
		return math.sqrt(r)

	# Calculate the separation effect
	def getSeparationVelocity(self, id):
		velocity = [0, 0, 0]
		
		for i in range(self.NUM_BOIDS):
			if i != id:
				# If the distance between boids is too close, add velocity in the direction of pull away
				distance = self.getDistance(self.boids[id].position, self.boids[i].position)
				if distance < self.SEPARATION_DISTANCE:
					for j in range(3):
						velocity[j] = velocity[j] - (self.boids[id].position[j] - self.boids[i].position[j])
	
		#  Scale the effect with PARAM_SEPARATION
		for i in range(3):	
			velocity[i] *= self.PARAM_SEPARATION
			
		return velocity

	# Calculate the alingment effect
	def getAlingmentVelocity(self, id):
		velocity = [0, 0, 0]
		
		# Sum all other boid's velocity
		for i in range(self.NUM_BOIDS):
			if i != id:
				for j in range(3):
					velocity[j] = velocity[j]  + self.boids[i].velocity[j]
		
		# Get average velocity
		for i in range(3):
			velocity[i] = velocity[i] / (self.NUM_BOIDS-1)
			
		# Get relative veloicty for the flock and scale it with PARAM_ALINGMENT
		for i in range(3):	
			velocity[i] = (velocity[i]  - self.boids[id].velocity[i]) * self.PARAM_ALINGMENT
			
		return velocity
	
	# Update position and velocity of boids
	def update(self):
		for i in range(self.NUM_BOIDS):
			v1= self.getCohesionVelocity(i)
			v2= self.getSeparationVelocity(i)
			v3= self.getAlingmentVelocity(i)
			
			for j in range(3):
				# Update velocity
				self.boids[i].velocity[j] = self.boids[i].velocity[j]  + v1[j] + v2[j] + + v3[j]
				# Update position
				self.boids[i].position[j] = self.boids[i].position[j]  + self.boids[i].velocity[j]
		
		for i in range(self.NUM_BOIDS):
			for j in range(3):
				# Change direction at boundary area
				if self.boids[i].position[j] < -self.areaWidth or self.areaWidth < self.boids[i].position[j]:
					self.boids[i].velocity[j] *= -1.0

if __name__ == "__main__":
	myBoids = Boids()

	# Calculate 5 steps
	for i in range(5):
		data = myBoids.getCoords2D()
		print data		
		myBoids.update()
