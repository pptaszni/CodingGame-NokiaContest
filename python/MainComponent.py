import sys
import math
import numpy

DEBUG_PRINT = True

def debugLog(textToLog):
    if DEBUG_PRINT:
        print >> sys.stderr, textToLog

class Point:
    def __init__(self, x = None, y = None):
        if x == None:
            self._x_ = 0
        else:
            self._x_ = x
        if y == None:
            self._y_ = 0
        else:
            self._y_ = y
    def getX(self):
        return _x_
    def getY(self):
        return _y_
    def setX(self, x):
        _x_ = x
    def setY(self, y):
        _y_ = y

class Pod:
    def __init__(self):
        self._pos_ = Point()
        self._vel_ = Point()
        self._angle_ = 0
        self._nextCheckPointId_ = 0
    def getPos(self):
        return self._pos_
    def getVel(self):
        return self._vel_
    def getAngle(self):
        return self._angle_
    def getNextCheckPointId(self):
        return _nextCheckPointId_
    def setPos(self, pos):
        self._pos_ = pos
    def setVel(self, vel):
        self._vel_ = vel
    def setAngle(self, angle):
        self._angle_ = angle
    def setNextCheckPointId(self, nextCheckPointId):
        self._nextCheckPointId_ = nextCheckPointId

class Calculator:
    def __init__(self):
        pass

class GameController:
    def __init__(self):
        self._playerCount_ = 0
        self._laps_ = 0
        self._boosts_ = 0
        self._checkpointCount_ = 0
        self._checkpointPos_ = []
        self._myPod_ = Pod()
        self._enemyPods_ = []
        self._calculator_ = Calculator()
    def startGame(self):
        debugLog("Game started ...")
        self.loadInitialData()
        debugLog("Initial data loaded ...")
        self.trivialStrategy()
    def trivialStrategy(self):
        while True:
            self.loadRuntimeData()
            dest = _checkpointPos_[_myPod_.getNextCheckPointId()]
            thrust = 50
            self.writeSolution(dest, thrust)
    def loadInitialData(self):
        self._playerCount_ = int(raw_input())
        self._laps_ = int(raw_input())
        self._boosts_ = int(raw_input())
        self._checkpointCount_ = int(raw_input())
        for i in range(self._checkpointCount_):
            checkpoint_x, checkpoint_y = [int(j) for j in raw_input().split()]
            self._checkpointPos_.append(Point(checkpoint_x, checkpoint_y))
    def loadRuntimeData(self):
        x, y, vx, vy, next_check_point_id = [int(j) for j in raw_input().split()]
        self._myPod_.setPos(Point(x,y))
        self._myPod_.setVel(Point(vx,vy))
        self._myPod_.setAngle(0)  # not sure if needed ...
        self._myPod_.setNextCheckPointId(next_check_point_id)
        while True:
            for i in range(self._playerCount_ - 1):
                x, y, vx, vy, next_check_point_id = [int(j) for j in raw_input().split()]
                self._enemyPods_[i].setPos(Point(x,y))
                self._enemyPods_[i].setVel(Point(vx,vy))
                self._enemyPods_[i].setAngle(0)  # not sure if needed ...
                self._enemyPods_[i].setNextCheckPointId(next_check_point_id)
    def writeSolution(self, dest, thrust):
        print str(dest.getX()) + " " + str(dest.getY()) + " " + str(thrust)


GameController().startGame()