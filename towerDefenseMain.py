#Created by Stefan Dasbach
#Spring 2013

import math
from direct.gui.OnscreenText import OnscreenText
#Initializes entire program
from direct.showbase.ShowBase import ShowBase, Plane, Vec3, CardMaker
from direct.task import Task #Procedure called every frame
from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import Sequence
from panda3d.core import Point3
from panda3d.core import *
from direct.gui.DirectGui import *
import sys
from time import time, sleep

# #Uncomment to make full screen
# #Change resolution 
# loadPrcFileData("", "win-size 1280 800")
# #make full screen
# loadPrcFileData("", "fullscreen t")
		
class ArrowTower(object):
	def __init__(self, showbase, position):
		self.showbase = showbase
		self.position = position
		self.hasTarget = False
		self.shootProj = None
		self.target = 0
		self.towerLevel = 1 
		self.damage = 10
		self.fireRate = 0.5 #Half a second
		self.range = 30
		self.isFiringBool = False
		self.tempFlag = False
	def fire(self, task):
		if self.tempFlag == False:
			self.temp = task.time + self.fireRate
			self.tempFlag = True
		#isFiringBool is checked here to make sure this 
		#If statement isn't satisfied at the beginning
		#otherwise fire would wait until the fireRate 
		#duration has elapsed and then continue on to
		#actually firing
		if task.time < self.temp and self.isFiringBool:
			#Removes the projectile after 0.065 seconds
			#Checks if it already has been removed
			#Checks that 0.065s has passed
			if not self.shootProj.isGone() and\
				(self.temp - task.time < self.fireRate - 0.065):
				self.shootProj.remove()
			return Task.cont
		#Isfiring checked again, so will be satisfied
		#if already fired, otherwise it still needs to fire
		elif self.isFiringBool:
			self.tempFlag = False
			self.isFiringBool = False
			return Task.done
		#If no target, find one
		if self.hasTarget == False:
			self.setTarget()
		#If target was found
		if self.hasTarget:
			self.shootProj = ArrowProjectileModel(
								self.showbase, 
								Point3(self.position[0], 
										self.position[1], 
										self.position[2] + 5), 
								self.target.getPosition())
			self.target.hit(self.damage)
			#All creeps wiped out, need to remove the projectile
			#now or it will never be removed
			#Reset so when fire is called again,
			#setTarget will be called again,
			#thus ensuring the firstMost creep will be targeted
			#and won't keep attacking the creep if it dies
			self.hasTarget = False
			self.isFiringBool = True
			if self.showbase.buildTime == True or\
				self.showbase.fireTime == False:
				self.shootProj.remove()
			return Task.cont
		#No target was found, no creep to fire at
		else:
			if self.shootProj and not self.shootProj.isGone():
				self.shootProj.remove()
			self.isFiringBool = False
			self.tempFlag = False
			return Task.done
	def setTarget(self):
		#If no creep is in range, hasTarget will remain False
		self.hasTarget = False
		for creep in self.showbase.creeps:
			#If it is a creep
			if creep:
				if self.getDistance(creep) < self.range:
					self.target = creep
					self.hasTarget = True
					break
	def isFiring(self):
		return self.isFiringBool
	def getDistance(self, creep):
		xDistance = abs(creep.getPosition()[0] - self.position[0])
		yDistance = abs(creep.getPosition()[1] - self.position[1])
		return math.sqrt(xDistance**2 + yDistance**2)
	def setTowerLevel(self, level):
		self.towerLevel = level
		if self.towerLevel == 2:
			self.damage = 20
		elif self.towerLevel == 3:
			self.damage = 50

class FireTower(object):
	def __init__(self, showbase, position):
		self.showbase = showbase
		self.position = position
		self.hasTarget = False
		self.shootProj = None
		self.target = 0
		self.towerLevel = 1 
		self.damage = 7
		self.fireRate = 0.2
		self.range = 20
		self.isFiringBool = False
		self.tempFlag = False
	def fire(self, task):
		if self.tempFlag == False:
			self.temp = task.time + self.fireRate
			self.tempFlag = True
		#isFiringBool is checked here to make sure this 
		#If statement isn't satisfied at the beginning
		#otherwise fire would wait until the fireRate 
		#duration has elapsed and then continue on to
		#actually firing
		if task.time < self.temp and self.isFiringBool:
			#Removes the projectile after 0.065 seconds
			#Checks if it already has been removed
			#Checks that 0.065s has passed
			if not self.shootProj.isGone() and\
				(self.temp - task.time < self.fireRate - 0.065):
				self.shootProj.remove()
			return Task.cont
		#Isfiring checked again, so will be satisfied
		#if already fired, otherwise it still needs to fire
		elif self.isFiringBool:
			self.tempFlag = False
			self.isFiringBool = False
			return Task.done
		#If no target, find one
		if self.hasTarget == False:
			self.setTarget()
		#If target was found
		if self.hasTarget:
			self.shootProj = FireProjectileModel(
								self.showbase, 
								Point3(self.position[0], 
										self.position[1], 
										self.position[2] + 5), 
								self.target.getPosition())
			self.target.hit(self.damage)
			#All creeps wiped out, need to remove the projectile
			#now or it will never be removed
			if self.showbase.buildTime == True:
				self.shootProj.remove()
			#Reset so when fire is called again,
			#setTarget will be called again,
			#thus ensuring the firstMost creep will be targeted
			#and won't keep attacking the creep if it dies
			self.hasTarget = False
			self.isFiringBool = True
			#Restarts the task so
			return Task.cont
		#No target was found, no creep to fire at
		else:
			if self.shootProj and not self.shootProj.isGone():
				self.shootProj.remove()
			self.isFiringBool = False
			self.tempFlag = False
			return Task.done
	def setTarget(self):
		#If no creep is in range, hasTarget will remain False
		self.hasTarget = False
		for creep in self.showbase.creeps:
			#If it is a creep
			if creep:
				if self.getDistance(creep) < self.range:
					self.target = creep
					self.hasTarget = True
					break
	def isFiring(self):
		return self.isFiringBool
	def getDistance(self, creep):
		xDistance = abs(creep.getPosition()[0] - self.position[0])
		yDistance = abs(creep.getPosition()[1] - self.position[1])
		return math.sqrt(xDistance**2 + yDistance**2)
	def setTowerLevel(self, level):
		self.towerLevel = level
		if self.towerLevel == 2:
			self.damage = 60
		elif self.towerLevel == 3:
			self.damage = 150

class IceTower(object):
	def __init__(self, showbase, position):
		self.showbase = showbase
		self.position = position
		self.hasTarget = False
		self.shootProj = None
		self.target = 0
		self.towerLevel = 1 
		self.damage = 5
		self.slowDuration = 1
		self.fireRate = 0.5 #Half a second
		self.range = 25
		self.isFiringBool = False
		self.tempFlag = False
	def fire(self, task):
		if self.tempFlag == False:
			self.temp = task.time + self.fireRate
			self.tempFlag = True
		#isFiringBool is checked here to make sure this 
		#If statement isn't satisfied at the beginning
		#otherwise fire would wait until the fireRate 
		#duration has elapsed and then continue on to
		#actually firing
		if task.time < self.temp and self.isFiringBool:
			#Removes the projectile after 0.065 seconds
			#Checks if it already has been removed
			#Checks that 0.065s has passed
			if not self.shootProj.isGone() and\
				(self.temp - task.time < self.fireRate - 0.065):
				self.shootProj.remove()
			return Task.cont
		#Isfiring checked again, so will be satisfied
		#if already fired, otherwise it still needs to fire
		elif self.isFiringBool:
			self.target.resume()
			self.tempFlag = False
			self.isFiringBool = False
			return Task.done
		#If no target, find one
		if self.hasTarget == False:
			self.setTarget()
		#If target was found
		if self.hasTarget:
			self.shootProj = IceProjectileModel(
								self.showbase, 
								Point3(self.position[0], 
										self.position[1], 
										self.position[2] + 5), 
								self.target.getPosition())
			self.target.hit(self.damage)
			#All creeps wiped out, need to remove the projectile
			#now or it will never be removed
			if self.showbase.buildTime == True:
				self.shootProj.remove()
			self.target.slow()
			#Reset so when fire is called again,
			#setTarget will be called again,
			#thus ensuring the firstMost creep will be targeted
			#and won't keep attacking the creep if it dies
			self.hasTarget = False
			self.isFiringBool = True
			#Restarts the task so
			return Task.cont
		#No target was found, no creep to fire at
		else:
			if self.shootProj and not self.shootProj.isGone():
				self.shootProj.remove()
			self.isFiringBool = False
			self.tempFlag = False
			return Task.done
	def setTarget(self):
		#If no creep is in range, hasTarget will remain False
		self.hasTarget = False
		for creep in self.showbase.creeps:
			#If it is a creep
			if creep:
				if self.getDistance(creep) < self.range:
					self.target = creep
					self.hasTarget = True
					break
	def isFiring(self):
		return self.isFiringBool
	def getDistance(self, creep):
		xDistance = abs(creep.getPosition()[0] - self.position[0])
		yDistance = abs(creep.getPosition()[1] - self.position[1])
		return math.sqrt(xDistance**2 + yDistance**2)
	def setTowerLevel(self, level):
		self.towerLevel = level
		if self.towerLevel == 2:
			self.damage = 20
		elif self.towerLevel == 3:
			self.damage = 50

class Tile(object):
	def __init__(self, showbase):
		self.g = 0
		self.h = 0
	def setG(self, g):
		self.g = g
	def getG(self):
		return self.g

class Creep(object):
	def __init__(self, showbase, midPoints, positionInList):
		self.showbase = showbase
		self.startHp = 50
		self.totalHp = int(self.startHp * ( (self.showbase.level/4.0) +
										(self.showbase.level*0.1) 
									  ))
		self.showbase.totalHp = self.totalHp
		#CurrentHp that will be updated and used as value in hpBar
		self.hp = self.totalHp
		self.midPoints = midPoints
		self.end = midPoints[len(self.midPoints)-1][len(self.midPoints[0])-1]
		#Get just X and Y
		self.end = (self.end[0], self.end[1])
		self.position = positionInList
		self.start = midPoints[0][0]
		self.creep = Actor("models/panda-model",
								{"walk": "models/panda-walk4"})
		self.creep.setPos(self.start)
		self.creep.setScale(Point3(0.005,0.005,0.005))
		self.hpBar = DirectWaitBar(text = "", range = 100, value = 100)
		self.hpBar.setScale(Point3(2.5, 4, 4))
		self.hpBar.lookAt(0,0,-1)
		#Starts off running normal speed, not slowed
		self.isSlowed = False
		#For if another slow is overlapping
		self.overlapSlow = False
		#Make sure the value of hpBar shows
		self.hpBar.setDepthTest(False)
		self.hpBar.setDepthWrite(False)
		
	#Spanws the creep and its hpBar
	def spawn(self):
		self.creep.reparentTo(self.showbase.render)
		self.hpBar.reparentTo(self.showbase.render)
	
	#Makes the hpBar follow the creep
	#
	#Tried to, instead, make it reparent to self.creep
	#rather than self.showbase.render
	#So I didn't have to constantly update its position
	#But it didn't display when I tried this
	def showHpBar(self, task):
		x = self.creep.getPos()[0]
		y = self.creep.getPos()[1]
		z = self.creep.getPos()[2]
		self.hpBar.setPos(Point3(
								x,
								y+3,
								z+1))
		#Creep has reached the end
		if ( int(x), int(y) ) == self.end:
			self.remove()
		return Task.cont
	def hit(self, damage):
		self.hp -= damage
		if self.isDead():
			self.kill()
		#Update as a percentage of 100 (initial hpBar range is 100)
		self.hpBar.update(int((self.hp*100.0)/(self.totalHp)))
	def isDead(self):
		if self.hp <= 0: #Dead
			return True
		return False
	#Killed by towers, counts as kill
	def kill(self):
		#Remove the creep & hpBar from the screen
		self.creep.delete()
		self.hpBar.removeNode()
		#Set the value of this creep in the list of all creeps to 0
		self.showbase.creeps[self.position] = 0
		#Every five levels, double the gold
		self.showbase.gold += (1+(self.showbase.level/5)) #Either 1 or 2
		if self.showbase.displayGameInfoNode1 != None:
			self.showbase.displayGameInfoNode1.destroy()
		self.showbase.displayGameInfoNode.destroy()
		self.showbase.displayGameInfo()
	#Reached end of board, does not count as kill
	def remove(self):
		#Remove the creep & hpBar from the screen
		self.creep.delete()
		self.hpBar.removeNode()
		#Set the value of this creep in the list of all creeps to 0
		self.showbase.creeps[self.position] = 0
		self.showbase.lives -= 1
		if self.showbase.displayGameInfoNode1 != None:
			self.showbase.displayGameInfoNode1.destroy()
		self.showbase.displayGameInfoNode.destroy()
		self.showbase.displayGameInfo()
		#No more lives left, game over
		if self.showbase.lives == 0:
			self.showbase.displayGameOver()
			sys.exit()
	def move(self, path):
		self.pathSequence = Sequence()
		for i in xrange(len(path)-1):
			step = self.creep.posInterval(
											.4,
											path[i+1],
											startPos = path[i]
											)
			self.pathSequence.append(step)
		self.pathSequence.start()
	def slow(self):
		self.pathSequence.setPlayRate(0.4)
	def resume(self):
		self.pathSequence.setPlayRate(1)
	def getPosition(self):
		return self.creep.getPos()
	def getTotalHp(self):
		return self.totalHp

class TowerDefense(ShowBase):
	def __init__(self):
		ShowBase.__init__(self)
		self.disableMouse()
		self.camera.setPos(40, -100, 160)
		self.camera.lookAt(40,-44.5,0)
		self.rows, self.cols = 9, 8
		#Start tile & end tile
		self.start, self.end = (0, 0), (8, 7)
		self.cellSize = 10
		#Plane used for intersection of mouseLine
		#To get coords of mouse
		self.mousePlane = Plane(Vec3(0, 0, 1), Point3(0, 0, 0))
		#No click has been made
		self.mousePressed = False
		self.displayTextObject = None
		#Holds the model for all tiles
		self.tiles = []
		for row in xrange(self.rows):
			self.tiles += [[0]*self.cols]
		#Holds the texture for the grass tiles
		self.grass = loader.loadTexture("models/textures/sponge.jpg")
		#Holds the models for all the towers
		self.towerModels = []
		for row in xrange(self.rows):
			self.towerModels += [[0]*self.cols]
		#Holds the G value of each tile for pathing
		self.tileNodes = []
		for row in xrange(self.rows):
			self.tileNodes += [[0]*self.cols]
		for row in xrange(self.rows):
			for col in xrange(self.cols):
				self.tileNodes[row][col] = Tile(self)
		#Holds the towers in a 2d array
		self.towers = []
		for row in xrange(self.rows):
			self.towers += [[0]*self.cols]
		self.board = [
						['s', 0, 0, 0, 0, 0, 0, 0],
						 [ 0, 0, 0, 0, 0, 0, 0, 0],
						 [ 0, 0, 0, 0, 0, 0, 0, 0],
						 [ 0, 0, 0, 0, 0, 0, 0, 0],
						 [ 0, 0, 0, 0, 0, 0, 0, 0],
						 [ 0, 0, 0, 0, 0, 0, 0, 0],
						 [ 0, 0, 0, 0, 0, 0, 0, 0],
						 [ 0, 0, 0, 0, 0, 0, 0, 0],
						 [ 0, 0, 0, 0, 0, 0, 0,'e']
					 ]
		self.drawBoard()
		self.drawBoardLines()
		self.drawBackground()
		
		#Stores all center points of each tile
		self.midPoints= []
		startX = 5 #X Coordinate of first Square's center
		startY = -5 #Y Coordinate of first Square's center
		for row in xrange(self.rows):
			self.midPoints += [[Point3(0,0,0)]*self.cols]
		for row in xrange(self.rows):
			for col in xrange(self.cols):
				self.midPoints[row][col] = Point3(
											startX+col*self.cellSize,
											startY-row*self.cellSize,
											0)
		self.createPath(self.start, self.end)
		
#Board Information
		#Towers
		self.arrowTowerModel = loader.loadModel(
			"models/towers/arrowTowerFolder/arrowTower")
		self.fireTowerModel = loader.loadModel(
			"models/towers/fireTowerFolder/fireTower")
		self.iceTowerModel = loader.loadModel(
			"models/towers/iceTowerFolder/iceTower")

#Main Menu
		self.mainFrame = DirectFrame(frameColor=(0, 0, 0, 1),
		                      frameSize=(-2, 2, -2, 2),
		                      pos=(0, 0, 0))
		instructionsText = "   Stefan Dasbach's Tower Defense\n\n\n"+\
							"Monsters move accross the screen\n" +\
							"from the green square to the red\nsquare."+\
							" Choose and build from among a \nrange" +\
							" of towers including Arrow, Fire,\nand" +\
							" Ice. Waves of monsters come in \n10 and" +\
							" will spawn every 15 seconds. You\ncan" +\
							" only build towers when creeps are\nnot" +\
							" alive.\n\nPress 'P' to play!"
		self.instructionsNode = OnscreenText(
									text=instructionsText,
									pos = (-0.9, 0.55),
									scale = (0.1),
								bg = (209/255.0, 168/255.0, 132/255.0, 1),
									frame = (1, 0, 0, 1),
									align = TextNode.ALeft
												)
		# self.fireProjectileModel = loader.loadModel(
		# 	"models/projectiles/fireProjectileFolder/fireProjectile")
		# self.iceProjectileModel = loader.loadModel(
		# "models/projectiles/iceProjectileFolder/iceProjectile")
		# 
		# self.iceProjectileModel.setScale(0.03,0.03,0.03)
		# self.iceProjectileModel.setPos(12,-5,0)
		# # self.iceProjectileModel.lookAt(15, -5, 0)
		# self.iceProjectileModel.reparentTo(self.render)
		
#Level information
		self.level = 1
		self.gold = 20
		self.lives = 20
		self.totalHp = 0
		self.arrowTowerCost = 10
		self.fireTowerCost = 25
		self.iceTowerCost = 30
		#Building period, True at beginning of game
		self.buildTime = True
		#Spawning/killing of creeps period, False at beginning
		self.fireTime = False
		self.displayGameInfoNode = None
		self.displayGameInfoNode1 = None
		
#Spawn Creeps
		self.numberOfCreeps = 10
		#Time for building
		self.waveTime = 15
		self.creeps = []
		self.hasSpawnedWave = False
		#Delay between spawning of each creep
		self.delayTime = 0
		self.interval = 0
		self.buildTimeDuration = 0
		self.alreadyInitedGame = False
		self.accept("p", self.initGame)
		
	def initGame(self):
		if self.alreadyInitedGame == False:
			self.instructionsNode.destroy()
			self.mainFrame.destroy()
			#Handle taskManager
			self.timerTask = self.taskMgr.add(self.timerTask, 'timerTask')
			self.mouseTask = self.taskMgr.add(self.mouseTask, 'mouseTask')
			self.fireTask = self.taskMgr.add(self.fireTask, 'fireTask')
			self.hpBarTask = self.taskMgr.add(self.hpBarTask, 'hpBarTask')
			self.displayGameInfo()
			self.displayTowerInfo()
			self.displayControls()
			#Selects tile
			self.accept("mouse1", self.selectTile)
			#Builds arrow Tower
			self.accept("a", self.buildTowerArrow)
			#Builds Fire Tower
			self.accept("f", self.buildTowerFire)
			#Builds Ice tower
			self.accept("i", self.buildTowerIce)
			#Quits the game
			self.accept("q", self.quit)
			self.alreadyInitedGame = True

#***********************   Board Display   ***********************
	#Displays a walkable tile or tower
	def drawTile(self, row, col):
		#Towers
		if self.board[row][col] < 0:
			if self.board[row][col] == -1: #Arrow Tower
				# tileMaker.setColor(0, 0, 0, 1)
				self.towerModels[row][col] = BuildArrowTowerModel(
											self, self.midPoints[row][col])
			elif self.board[row][col] == -2: #Fire tower
				# tileMaker.setColor(1, 136.0/255, 0, 1)
				self.towerModels[row][col] = BuildFireTowerModel(
											self, self.midPoints[row][col])
			elif self.board[row][col] == -3: #Ice tower
				self.towerModels[row][col] = BuildIceTowerModel(
											self, self.midPoints[row][col])
				# tileMaker.setColor(0, 0, 1, 1)
		#Board Tiles
		else: 
			tileMaker = CardMaker("board")
			cellSize = self.cellSize
			if self.board[row][col] == 0: #Normal/non-towered tile
				tileMaker.setColor(1, 1, 1, 1)
			elif self.board[row][col] == "s": #Start
				tileMaker.setColor(0, 1, 0, 1)
			elif self.board[row][col] == "e": #End
				tileMaker.setColor(173.0/255, 0, 0, 1)
			tileMaker.setFrame(
				col*cellSize, col*cellSize+cellSize,
				-row*cellSize-cellSize, -row*cellSize)
			self.tiles[row][col] = self.render.attachNewNode(\
									tileMaker.generate())
			self.tiles[row][col].setTexture(self.grass)
			self.tiles[row][col].lookAt(0,0,-1)
	
	#Draws all tiles from self.board
	def drawBoard(self):
		tileMaker = CardMaker("board")
		board = self.board
		cellSize = self.cellSize
		for row in xrange(len(board)):
			for col in xrange(len(board[0])):
				self.drawTile(row, col)
	
	#Draws grid line from start and end point
	#Basically adds visual separation of tiles
	def drawLine(self, start, end, thickness=1.5):
		segment = LineSegs()
		# segment.setColor(209/255.0, 168/255.0, 132/255.0, 1)
		segment.setColor(1, 1, 1, 1)
		segment.setThickness(thickness)
		segment.moveTo(start)
		segment.drawTo(end)
		line = self.render.attachNewNode(segment.create())
		
	#Draws all grid lines of the board
	def drawBoardLines(self):
		#Horizontal grid lines
		for row in xrange(self.rows):
			self.drawLine(Point3(0, -row*self.cellSize, 0.01), 
				Point3(self.cellSize*self.cols, -row*self.cellSize, 0.01))
		#Vertical grid lines
		for col in xrange(self.cols):
			self.drawLine(Point3(col*self.cellSize, 0, 0.01), 
				Point3(col*self.cellSize, -self.cellSize*self.rows, 0.01))
				
	def drawBackground(self):
		self.background = loader.loadModel("models/skySphere/skySphere")
		self.background.lookAt(0,0,-1)
		self.background.reparentTo(self.render)
	#**************************   A Star   **************************
	#Determines whether or not tile can be walked on
	def isPath(self, coord):
		row, col = coord[0], coord[1]
		if self.board[row][col] < 0: #Tower
			return False
		return True #Can walk on path

	#Determines if row and col on board or not
	def inBounds(self, coord):
		row, col = coord[0], coord[1]
		if row < len(self.board) and col < len(self.board[0]):
			if row >= 0 and col >=0:
				return True
		return False

	#A* Pathfinding Algorithm
	def createPath(self, start, end):
		#This array of array of objects keeps 
		#track of the G value of each tile

		openList = set()
		closedList = set()
		parentDict = dict()
		openList.add(start)
		newTile = start

		#If end in closedList, we've found our pathway to end
		#Or if we've exhausted all search tiles available (openList is empty)
		try:
			while (end not in closedList) or len(openList) != 0:
				#Lowest f-value among openList
				#newTile holds the coordinates of which tile to check
				newTile = self.getLowestFInOpen(start, end, openList)
				#Make self.tileNodes[newTile[0]][newTile[1]] and currentNode
				#Aliases to use currentNode instead to improve clarity
				currentNode = self.tileNodes[newTile[0]][newTile[1]]
				#Switch newTile to closedList
				openList.remove(newTile)
				closedList.add(newTile)
				#Adjacent tiles
				left = (newTile[0], newTile[1]-1)
			
				right = (newTile[0], newTile[1]+1)
			
				up = (newTile[0]-1, newTile[1])
			
				down = (newTile[0]+1, newTile[1])
			
				#Check if adjacent tiles in closedList/openList
				#If in closedList, already checked
				#If not in closedList, check if already in openList
				#If not in openList, add it, and record its parent tile
				#Down tile
				if self.inBounds(down) and self.isPath(down):
					downNode = self.tileNodes[newTile[0]+1][newTile[1]]
					#If not already checked
					if down not in closedList:
						#If should be added to openList	
						if down not in openList:
							downNode.setG(currentNode.getG() + 1)
							openList.add(down)
							#Assign newTile as down's parent tile
							parentDict[down] = (newTile)
						else:
							newG = currentNode.getG() + 1 #down so plus 1
							if downNode.getG() > newG:
								downNode.setG(newG)
								parentDict[down] = (newTile)
				#Right tile
				if self.inBounds(right) and self.isPath(right):
					rightNode = self.tileNodes[newTile[0]][newTile[1]+1]
					if right not in closedList:
						if right not in openList:
							rightNode.setG(currentNode.getG() + 1)
							openList.add(right)
							parentDict[right] = (newTile)
						else:
							newG = currentNode.getG() + 1 #right so plus 1
							if rightNode.getG() > newG:
								rightNode.setG(newG)
								parentDict[right] = (newTile)
				#Up tile
				if self.inBounds(up) and self.isPath(up):
					upNode = self.tileNodes[newTile[0]-1][newTile[1]]
					if up not in closedList:
						if up not in openList:
							upNode.setG(currentNode.getG() + 1)
							openList.add(up)
							parentDict[up] = (newTile)
						else:
							newG = currentNode.getG() + 1 #up so plus 1
							if upNode.getG() > newG:
								upNode.setG(newG)
								parentDict[up] = (newTile)
				#Left Tile
				if self.inBounds(left) and self.isPath(left):
					leftNode = self.tileNodes[newTile[0]][newTile[1]-1]
					if left not in closedList:
						if left not in openList:
							leftNode.setG(currentNode.getG() + 1)
							openList.add(left)
							parentDict[left] = (newTile)
						else:
							newG = currentNode.getG() + 1 #left so plus 1
							if leftNode.getG() > newG:
								leftNode.setG(newG)
								parentDict[left] = (newTile)
		except:
			return False

		self.tileSequence = self.getSequenceFromDict(parentDict)
		self.pathSequence = []
		for i in xrange(len(self.tileSequence)):
			self.pathSequence += [self.midPoints
										[self.tileSequence[i][0]]
										[self.tileSequence[i][1]]]
						
		return True
	#Finds lowest f value in openList
	def getLowestFInOpen(self, start, end, openList):
		lowestF = 10000000
		newTile = None
		for tile in openList:
			temp = self.getF(start, end, self.tileNodes[\
					tile[0]][tile[1]], tile[0], tile[1])
			if temp < lowestF:
				lowestF = temp
				newTile = tile
		return newTile

	#Distance from start to current tile
	def getG(self, current):
		return current.getG()
		# return abs(start[0]-current[0]) + abs(start[1]-current[1])

	#Distance from current tile to end
	def getH(self, start, end, current):
		return abs(end[1]-current[1]) + abs(end[0]-current[0])

	#Sum of g and h (total presumed distance from start to finish)
	def getF(self, start, end, current, row, col):
		g = self.getG(current)
		h = self.getH(start, end, (row,col))
		return g+h
	#Get sequence of steps from dictionary of points
	#and their parent points
	def getSequenceFromDict(self, parentDict):
		currentTile = self.end
		pathSequence = [currentTile]
		while currentTile != self.start:
			currentTile = parentDict[currentTile]
			pathSequence += [currentTile]
		return pathSequence[::-1]
	
#********************Task Manager***********************
	#Handles the switching between 
	#The building period and
	#The creep killing period
	def timerTask(self, task):
		if self.buildTime == True:
			#buildTimeDuration hasn't been set yet
			if self.buildTimeDuration == 0:
				for row in self.towers:
					for tower in row:
						#If this has been set to a tower
						if tower:
							if tower.shootProj != None and\
								not tower.shootProj.isGone():
								tower.shootProj.remove()
				self.buildTimeDuration = task.time + self.waveTime
				self.displayBuildTime(self.buildTimeDuration-task.time)
			#If a second has passed since updating the time
			elif self.buildTimeDuration-task.time < self.currentBuildTimeInt:
				self.displayNextWave.destroy()
				self.displayNextWaveTime.destroy()
				self.displayBuildTime(self.buildTimeDuration-task.time)
			#If buildTime has expired
			#Initiate fireTime, end buildTime
			if task.time > self.buildTimeDuration:
				self.displayNextWave.destroy()
				self.displayNextWaveTime.destroy()
				self.buildTime = False
				self.fireTime = True
				self.hasSpawnedWave = False
				self.buildTimeDuration = 0
				self.displayCreepHp = True
			return Task.cont
		#Start next level
		if self.fireTime == True:
			#Spawn wave
			if self.hasSpawnedWave == False:
				self.spawnWave(task)
				#Used to display CreepHP as soon as wave spawns
				if self.displayCreepHp == True:
					if self.displayGameInfoNode1 != None:
						self.displayGameInfoNode1.destroy()
					self.displayGameInfoNode.destroy()
					self.displayGameInfo()
				self.displayCreepHp = False
				return Task.cont
			#If all creeps killed/reached end
			#Initiate buildTime, end fireTime
			if self.isCreeps() == False:
				self.buildTime = True
				self.fireTime = False
				#Next level
				self.levelUp()
			return Task.cont
	#Manages the tracking of the mouse & its position
	def mouseTask(self, task):
		if base.mouseWatcherNode.hasMouse():
			tempMousePos = base.mouseWatcherNode.getMouse()
			pos3d = Point3()
			nearPoint = Point3()
			farPoint = Point3()
			base.camLens.extrude(tempMousePos, nearPoint, farPoint)
			if self.mousePlane.intersectsLine(pos3d,
				self.render.getRelativePoint(camera, nearPoint),
				self.render.getRelativePoint(camera, farPoint)):
				self.mousePos = (pos3d[0], pos3d[1])
		return Task.cont
	#Manages the firing of towers
	def fireTask(self, task):
		#Are creeps and are towers
		if len(self.creeps) > 0 and len(self.towers) > 0:
			for row in self.towers:
				for tower in row:
					#If this has been set to a tower
					if tower:
						#Tower fire isn't on cooldown
						# if not tower.isFiring():
						tower.fire(task)
							
		return Task.cont
	#Shows and positions hpBar
	def hpBarTask(self, task):
		for creep in self.creeps:
			#Is actually a creep
			if creep:
				creep.showHpBar(task)
		return Task.cont
	
#*************************Building Objects*************************
	#onClick of mouse selects a tile
	def selectTile(self):
		row, col = self.mousePos[1], self.mousePos[0]
		#Check if click is on the grid or not
		if (row < 0 and row > -self.rows*self.cellSize) and (
			col > 0 and col <  self.cols*self.cellSize):
			self.mousePressed = True
			self.currentRow = abs(int(row/10))
			self.currentCol = abs(int(col/10))
			#If displayText already exists, destroy and rewrite it
			if self.displayTextObject != None:
				self.displayTextObject.destroy()
			self.displayText()
	def buildTowerArrow(self):
		#Row and col of tile selected
		#A tile is selected
		if self.mousePressed == True:
			#Makes sure not building while attacking creeps
			if self.buildTime == False:
				self.displayTextObject.destroy()
				self.displayError("You cannot build while attacking")
			else:
				row = self.currentRow
				col = self.currentCol
				originalVal = self.board[row][col]
				self.board[row][col] = -1
				#Checks if the tower is blocking
				#Or if tower already built there
				#Create path return false if no path
				if (not self.createPath(self.start, self.end) or 
									  (row == 0 and col == 0) or 
									  (originalVal < 0) #Already a tower
									  ):
					self.board[row][col] = originalVal
					self.displayTextObject.destroy()
					self.displayError("You can't build there")
				elif self.gold < self.arrowTowerCost:
					self.board[row][col] = originalVal
					self.displayTextObject.destroy()
					self.displayError("Not enough gold")
				else:
					self.towers[row][col] = ArrowTower(
									self, self.midPoints[row][col])
					#Delete current square
					# self.tiles[row][col].removeNode()
					#Redraw it as tower
					self.drawTile(row, col)
					#Built a tower, so no longer highlighting tile
					self.mousePressed = False
					#No need for text; no tile selected
					self.displayTextObject.destroy()
					self.createPath(self.start, self.end)
					self.gold -= self.arrowTowerCost
					if self.displayGameInfoNode1 != None:
						self.displayGameInfoNode1.destroy()
					self.displayGameInfoNode.destroy()
					self.displayGameInfo()
	def buildTowerFire(self):
		#Row and col of tile selected
		#A tile is selected
		if self.mousePressed == True:
			#Makes sure not building while attacking creeps
			if self.buildTime == False:
				self.displayTextObject.destroy()
				self.displayError("You cannot build while attacking")
			else:
				row = self.currentRow
				col = self.currentCol
				originalVal = self.board[row][col]
				self.board[row][col] = -2
				#Checks if the tower is blocking
				#Or if tower already built there
				#Create path return false if no path
				if (not self.createPath(self.start, self.end) or 
									  (row == 0 and col == 0) or 
									  (originalVal < 0) #Already a tower
									  ):
					self.board[row][col] = originalVal
					self.displayTextObject.destroy()
					self.displayError("You can't build there")
				elif self.gold < self.fireTowerCost:
					self.board[row][col] = originalVal
					self.displayTextObject.destroy()
					self.displayError("Not enough gold")
				else:
					self.towers[row][col] = FireTower(
									self, self.midPoints[row][col])
					#Delete current square
					# self.tiles[row][col].removeNode()
					#Redraw it as tower
					self.drawTile(row, col)
					#Built a tower, so no longer highlighting tile
					self.mousePressed = False
					#No need for text; no tile selected
					self.displayTextObject.destroy()
					self.createPath(self.start, self.end)
					self.gold -= self.fireTowerCost
					if self.displayGameInfoNode1 != None:
						self.displayGameInfoNode1.destroy()
					self.displayGameInfoNode.destroy()
					self.displayGameInfo()
	def buildTowerIce(self):
		#Row and col of tile selected
		#A tile is selected
		if self.mousePressed == True:
			#Makes sure not building while attacking creeps
			if self.buildTime == False:
				self.displayTextObject.destroy()
				self.displayError("You cannot build while attacking")
			else:
				row = self.currentRow
				col = self.currentCol
				originalVal = self.board[row][col]
				self.board[row][col] = -3
				#Checks if the tower is blocking
				#Or if tower already built there
				#Create path return false if no path
				if (not self.createPath(self.start, self.end) or 
									  (row == 0 and col == 0) or 
									  (originalVal < 0) #Already a tower
									  ):
					self.board[row][col] = originalVal
					self.displayTextObject.destroy()
					self.displayError("You can't build there")
				elif self.gold < self.iceTowerCost:
					self.board[row][col] = originalVal
					self.displayTextObject.destroy()
					self.displayError("Not enough gold")
				else:
					self.towers[row][col] = IceTower(
							self, self.midPoints[row][col])
					#Delete current square
					# self.tiles[row][col].removeNode()
					#Redraw it as tower
					self.drawTile(row, col)
					#Built a tower, so no longer highlighting tile
					self.mousePressed = False
					#No need for text; no tile selected
					self.displayTextObject.destroy()
					self.createPath(self.start, self.end)
					self.gold -= self.iceTowerCost
					if self.displayGameInfoNode1 != None:
						self.displayGameInfoNode1.destroy()
					self.displayGameInfoNode.destroy()
					self.displayGameInfo()
		
#*************************UI Display*************************
	def displayText(self):
		text = "Row: " + str(self.currentRow)+\
			" Col: " + str(self.currentCol) +\
			"\nPress to build       ' a '  Arrow Tower" +\
			"       ' f '  Fire Tower"+\
			"       ' i '  Ice Tower"
		self.displayTextObject = OnscreenText(
								text=text, 
								pos = (0.005, 0.95), 
								scale = (0.05),
								bg = (209/255.0, 168/255.0, 132/255.0, 1),
								frame = (1, 0, 0, 1)
											  )
	def displayError(self, text):
		text = text
		self.displayTextObject = OnscreenText(
								text=text, 
								pos = (0.005, 0.91), 
								scale = (0.1),
								bg = (209/255.0, 168/255.0, 132/255.0, 1),
								frame = (1, 0, 0, 1)
											  )
	def displayBuildTime(self, time):
		text = "Next wave"
		self.displayNextWave = OnscreenText(
								text=text, 
								pos = (1.05, 0.91), 
								scale = (0.06),
								bg = (209/255.0, 168/255.0, 132/255.0, 1),
								frame = (1, 0, 0, 1)
											  )
		self.currentBuildTimeInt = int(time)
		text = str(self.currentBuildTimeInt)
		self.displayNextWaveTime = OnscreenText(
								text=text, 
								pos = (1.0485, 0.69), 
								scale = (0.2253),
								bg = (209/255.0, 168/255.0, 132/255.0, 1),
								frame = (1, 0, 0, 1)
											  )
	def displayGameInfo(self):
		text = "Level: " + str(self.level) + "\n" +\
			   "Gold:  " + str(self.gold) + "\n" +\
			   "Lives: " + str(self.lives)
		self.displayGameInfoNode = OnscreenText(
									text=text,
									pos = (-1.3, 0.88),
									scale = (0.09),
								bg = (209/255.0, 168/255.0, 132/255.0, 1),
									frame = (1, 0, 0, 1),
									align = TextNode.ALeft
												)
		#Has a value other than 0
		if self.fireTime == True:
			text = "Creep HP:   " + str(self.totalHp)
			self.displayGameInfoNode1 = OnscreenText(
										text=text,
										pos = (-1.12, 0.55),
										scale = (0.06),
								bg = (209/255.0, 168/255.0, 132/255.0, 1),
										frame = (1, 0, 0, 1)
													)
	def displayTowerInfo(self):
		text = "Arrow\nDmg: 10\nRate: 0.5s\nRange: 30\nCost: 10\n\n" +\
			   "Fire \nDmg: 7\nRate: 0.2s\nRange: 20\nCost: 25\n\n" +\
			   "Ice  \nDmg: 5\nRate: 0.5s\nRange: 25\nSlow: 60%\nCost: 30"
		self.displayTowerInfoNode = OnscreenText(
									text=text,
									pos = (-1.32, 0.0),
									scale = (0.05),
								bg = (209/255.0, 168/255.0, 132/255.0, 1),
									frame = (1, 0, 0, 1),
									align = TextNode.ALeft
												)
	def displayControls(self):
		text = "Select A Tile\n" +\
				"a - Arrow Tower\n" +\
				"f - Fire Tower\n" +\
				"i - Ice Tower\n" +\
				"q - quit"
		self.displayControlsNode = OnscreenText(
									text=text,
									pos = (.95, 0),
									scale = (0.05),
								bg = (209/255.0, 168/255.0, 132/255.0, 1),
									frame = (1, 0, 0, 1),
									align = TextNode.ALeft
												)
		
	def displayGameOver(self):
		text = "GAME OVER"
		self.displayGameOverNode = OnscreenText(
									text=text,
									pos = (0, 0),
									scale = (0.3),
									bg = (0, 0, 1, 1),
									frame = (1, 0, 0, 1)
												)
		sleep(1)
		sleep(5)
	def quit(self):
		sys.exit()
#********************* Spawn Creeps ************************
	def spawnWave(self, task):
		if self.interval < task.time:
			if len(self.creeps) < self.numberOfCreeps:
				self.spawnCreep()
				self.interval = task.time+1
			else:
				self.hasSpawnedWave = True
	def spawnCreep(self):
		if len(self.creeps) < self.numberOfCreeps:
			currentCreep = len(self.creeps)
			self.creeps.append(Creep(self, self.midPoints, currentCreep))
			self.creeps[currentCreep].spawn() #Most recently added creep
			self.creeps[currentCreep].move(self.pathSequence)
	#Checks to see if any creeps left
	def isCreeps(self):
		for creep in self.creeps:
			#Creep exists
			if creep:
				return True
		self.creeps = []
		return False

#********************* Level Handler ********************* 
	def levelUp(self):
		self.level += 1
		if self.displayGameInfoNode1 != None:
			self.displayGameInfoNode1.destroy()
		self.displayGameInfoNode.destroy()
		self.displayGameInfo()

class BuildArrowTowerModel(object):
	def __init__(self, showbase, position):
		self.model = showbase.arrowTowerModel
		self.model.setPos(position)
		self.model.setScale(Point3(0.15,0.15,0.15))
		self.model.copyTo(showbase.render)

class BuildFireTowerModel(object):
	def __init__(self, showbase, position):
		self.model = showbase.fireTowerModel
		self.model.setPos(position)
		self.model.setScale(Point3(0.08,0.08,0.08))
		self.model.copyTo(showbase.render)

class BuildIceTowerModel(object):
	def __init__(self, showbase, position):
		self.model = showbase.iceTowerModel
		self.model.setPos(position)
		self.model.setScale(Point3(0.21,0.21,0.21))
		self.model.copyTo(showbase.render)
	
class ArrowProjectileModel(object):
	def __init__(self, showbase, position1, position2):
		self.isRemoved = False
		self.model = loader.loadModel(
			"models/projectiles/arrowProjectileFolder/arrowProjectile")
		self.model.setScale(0.07,0.07,0.07)
		self.model.setPos(position1)
		self.model.lookAt(position2)
		self.model.reparentTo(showbase.render)
		mySequence = Sequence()
		step = self.model.posInterval(	.1,
										position2,
										startPos = position1
										)
		mySequence.append(step)
		mySequence.start()
	def remove(self):
		self.model.removeNode()
		self.model = None
		self.isRemoved = True
	def isGone(self):
		return self.isRemoved

class FireProjectileModel(object):
	def __init__(self, showbase, position1, position2):
		self.isRemoved = False
		self.model = loader.loadModel(
			"models/projectiles/fireProjectileFolder/fireProjectile")
		self.model.setScale(0.02,0.02,0.02)
		self.model.setPos(position1)
		self.model.lookAt(position2)
		self.model.reparentTo(showbase.render)
		mySequence = Sequence()
		step = self.model.posInterval(	.1,
										position2,
										startPos = position1
										)
		mySequence.append(step)
		mySequence.start()
	def remove(self):
		self.model.removeNode()
		self.model = None
		self.isRemoved = True
	def isGone(self):
		return self.isRemoved

class IceProjectileModel(object):
	def __init__(self, showbase, position1, position2):
		self.isRemoved = False
		self.model = loader.loadModel(
			"models/projectiles/iceProjectileFolder/iceProjectile")
		self.model.setScale(0.03,0.03,0.03)
		self.model.setPos(position1)
		self.model.setColor(212.0/255, 240.0/255, 1, 1)
		self.model.lookAt(position2)
		self.model.reparentTo(showbase.render)
		mySequence = Sequence()
		step = self.model.posInterval(	.1,
										position2,
										startPos = position1
										)
		mySequence.append(step)
		mySequence.start()
	def remove(self):
		self.model.removeNode()
		self.model = None
		self.isRemoved = True
	def isGone(self):
		return self.isRemoved
		self.model.removeNode()

newGame = TowerDefense()
newGame.run()