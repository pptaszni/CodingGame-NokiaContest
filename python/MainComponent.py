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
    def __eq__(self, other):
        return self.__dict__ == other.__dict__
    def getX(self):
        return self._x_
    def getY(self):
        return self._y_
    def setX(self, x):
        self._x_ = x
    def setY(self, y):
        self._y_ = y

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
        return self._nextCheckPointId_
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
    def _inBounds_(self, val, lowerB, upperB):
        if val >= lowerB and val <= upperB:
            return True
        else:
            return False
    def polynomial(self, coefs, t):
        tVec = [t**i for i in range(len(coefs))]
        tVec.reverse()
        result = 0
        for i in range(len(coefs)):
            result = result + coefs[i]*tVec[i]
        #debugLog("Poly["+str(len(coefs))+"] = "+str(result))
        return result
    def inverse(self, matrix):
        return matrix**-1
    def getSplinesCoefficients(self, inPositions, inVelocities, time):
        assert len(inPositions) + len(inVelocities) == len(time)
        dim = len(time)
        A = numpy.matrix(numpy.zeros((dim, dim)))
        for i in range(len(inPositions)):
            row = [time[i]**j for j in range(dim)]
            row.reverse()
            A[i] = row
        for i in range(len(inPositions), dim):
            row = [j*(time[i]**(j-1)) for j in range(1,dim)]
            row.reverse()
            row.append(0.0)
            A[i] = row
        X = [it.getX() for it in inPositions]
        X.extend([it.getX() for it in inVelocities])
        Y = [it.getY() for it in inPositions]
        Y.extend([it.getY() for it in inVelocities])
        invA = self.inverse(A)
        coefsX = invA.dot(X).getA1()
        coefsY = invA.dot(Y).getA1()
        return {"xCoefs": coefsX, "yCoefs": coefsY}
    def verify3PolyVelocityInBounds(self, coefs, time, lowerB, upperB):
        assert len(coefs) == 4 # 3rd degree polynomial
        assert len(time) == 2 # only t0 and tEnd
        a = 3*coefs[0]
        assert a != 0
        b = 2*coefs[1]
        c = coefs[2]
        t0 = time[0]
        tEnd = time[1]
        tExtremum = -b/(2*a)
        if tExtremum > t0 and tExtremum < tEnd:
            if not self._inBounds_(self.polynomial([a, b, c], tExtremum), lowerB, upperB):
                return False
        if not self._inBounds_(self.polynomial([a, b, c], t0), lowerB, upperB):
            return False
        if  not self._inBounds_(self.polynomial([a, b, c], tEnd), lowerB, upperB):
            return False
        return True
    def verify3PolyThrustInBounds(self, coefs, time, lowerB, upperB):
        assert len(coefs) == 4 # 3rd degree polynomial
        assert len(time) == 2 # only t0 and tEnd
        a = 6*coefs[0]
        b = 2*coefs[1]
        t0 = time[0]
        tEnd = time[1]
        if not self._inBounds_(self.polynomial([a, b], t0), lowerB, upperB):
            return False
        if not self._inBounds_(self.polynomial([a, b], tEnd), lowerB, upperB):
            return False
        return True
    def prepare3PositionsVector(self, pod, checkpointPos):
        assert isinstance(pod, Pod)
        checkPointCount = len(checkpointPos)
        assert pod.getNextCheckPointId() < checkPointCount
        p0 = pod.getPos()
        p1 = checkpointPos[pod.getNextCheckPointId()]
        nextNextCheckPointId = pod.getNextCheckPointId() + 1
        assert nextNextCheckPointId <= checkPointCount
        if nextNextCheckPointId == checkPointCount:
            nextNextCheckPointId = 0
        p2 = checkpointPos[nextNextCheckPointId]
        return [p0, p1, p2]
    def calculateDestAndThrustValues(self, pod, splineCoefs):
        x0 = pod.getPos().getX()
        y0 = pod.getPos().getY()
        x1 = self.polynomial(splineCoefs["xCoefs"], 1) # calc x for t=1
        y1 = self.polynomial(splineCoefs["yCoefs"], 1) # calc y for t=1
        velX = pod.getVel().getX()
        velY = pod.getVel().getY()
        thrustX = x1-x0-velX
        thrustY = y1-y0-velY
        totalThrust = math.sqrt(thrustX**2 + thrustY**2)
        totalThrust = int(round(totalThrust))
        xDest = int(round(x0+thrustX))
        yDest = int(round(y0+thrustY))
        return {"dest": Point(xDest, yDest), "thrust": totalThrust}

class Algorithms:
    def __init__(self):
        self._calculator_ = Calculator()
        self._thrustUpperBound_ = 100
        self._thrustLowerBound_ = 100
    def InterpolationStrategy(self, pVec, vel):
        assert len(pVec) == 3 # 3 points interpolation
        assert isinstance(vel, Point)
        time = [0, 20, 40, 0]
        t0 = time[0]
        tEnd = time[2]
        splineCoefs = self._calculator_.getSplinesCoefficients(pVec, [vel], time)
        if (self._calculator_.verify3PolyThrustInBounds(
            splineCoefs["xCoefs"], [t0,tEnd], self._thrustLowerBound_, self._thrustUpperBound_)):
            debugLog("OK: X thrust in bounds")
        else:
            debugLog("NOK: X thrust out of bounds")
        if (self._calculator_.verify3PolyThrustInBounds(
            splineCoefs["yCoefs"], [t0,tEnd], self._thrustLowerBound_, self._thrustUpperBound_)):
            debugLog("OK: Y thrust in bounds")
        else:
            debugLog("NOK: Y thrust out of bounds")
        tmpPod = Pod()
        tmpPod.setPos(pVec[0])
        tmpPod.setVel(vel)
        result = self._calculator_.calculateDestAndThrustValues(tmpPod, splineCoefs)
        return {"pos": result["dest"], "thrust": result["thrust"]}

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
        self._algrithms_ = Algorithms()
        self._thrustLimit = 100
    def startGame(self):
        debugLog("Game started ...")
        self.loadInitialData()
        debugLog("Initial data loaded ...")
        self.newStrategy()
    def trivialStrategy(self):
        while True:
            debugLog("Going to load runtime data ...")
            self.loadRuntimeData()
            debugLog("Runtime data loaded")
            dest = self._checkpointPos_[self._myPod_.getNextCheckPointId()]
            thrust = 100
            self.writeSolution(dest, thrust)
    def newStrategy(self):
        while True:
            debugLog("Going to load runtime data ...")
            self.loadRuntimeData()
            debugLog("Runtime data loaded")
            pVec = self._calculator_.prepare3PositionsVector(self._myPod_, self._checkpointPos_)
            solution = self._algrithms_.InterpolationStrategy(pVec, self._myPod_.getVel())
            self.writeSolution(solution["pos"], solution["thrust"])
    def loadInitialData(self):
        self._playerCount_ = int(raw_input())
        self._enemyPods_.extend([Pod() for i in range(0,self._playerCount_-1)])
        assert len(self._enemyPods_) == self._playerCount_-1
        self._laps_ = int(raw_input())
        self._boosts_ = int(raw_input())
        self._checkpointCount_ = int(raw_input())
        for i in range(self._checkpointCount_):
            checkpoint_x, checkpoint_y = [int(j) for j in raw_input().split()]
            self._checkpointPos_.append(Point(checkpoint_x, checkpoint_y))
        debugLog("players: " + str(self._playerCount_) +
            ", laps: " + str(self._laps_) +
            ", boosts: " + str(self._boosts_) +
            ", checkpoints: " + str(self._checkpointCount_) +
            ", enemyPods: " + str(len(self._enemyPods_)))
    def loadRuntimeData(self):
        x, y, vx, vy, next_check_point_id = [int(j) for j in raw_input().split()]
        self._myPod_.setPos(Point(x,y))
        self._myPod_.setVel(Point(vx,vy))
        self._myPod_.setAngle(0)  # not sure if needed ...
        self._myPod_.setNextCheckPointId(next_check_point_id)
        for i in range(self._playerCount_ - 1):
            x, y, vx, vy, next_check_point_id = [int(j) for j in raw_input().split()]
            self._enemyPods_[i].setPos(Point(x,y))
            self._enemyPods_[i].setVel(Point(vx,vy))
            self._enemyPods_[i].setAngle(0)  # not sure if needed ...
            self._enemyPods_[i].setNextCheckPointId(next_check_point_id)
    def writeSolution(self, dest, thrust):
        print str(dest.getX()) + " " + str(dest.getY()) + " " + str(thrust)


if __name__ == '__main__':
    GameController().startGame()
