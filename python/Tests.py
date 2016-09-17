import unittest
import random
import numpy
import math

from MainComponent import Point
from MainComponent import Pod
from MainComponent import Calculator
from MainComponent import Algorithms

def generateRandomRow(size):
    result = []
    lower_bound = -1000.0;
    upper_bound = 1000.0;
    for i in range(size):
        result.append(random.uniform(lower_bound, upper_bound))
    return result;

class PointTests(unittest.TestCase):
    def setUp(self):
        pass
    def testGettersReturnsWhatWasSet(self):
        expectedX = 33
        expectedY = 44

        p1 = Point()
        p2 = Point(expectedX)
        p3 = Point(y = expectedY)

        p1.setX(expectedX)
        p1.setY(expectedY)

        p2.setY(expectedY)

        p3.setX(expectedX)

        self.assertEqual(expectedX, p1.getX())
        self.assertEqual(expectedX, p2.getX())
        self.assertEqual(expectedX, p3.getX())
        self.assertEqual(expectedY, p1.getY())
        self.assertEqual(expectedY, p2.getY())
        self.assertEqual(expectedY, p3.getY())

class PodTests(unittest.TestCase):
    def setUp(self):
        pass
    def testGettersReturnsWhatWasSet(self):
        expectedPos = Point(34,55)
        expectedVel = Point(66,77)
        expectedAngle = 0.4
        expectedNextCheckPointId = 3

        podUnderTest = Pod()

        podUnderTest.setPos(expectedPos)
        podUnderTest.setVel(expectedVel)
        podUnderTest.setAngle(expectedAngle)
        podUnderTest.setNextCheckPointId(expectedNextCheckPointId)

        self.assertEqual(expectedPos, podUnderTest.getPos())
        self.assertEqual(expectedVel, podUnderTest.getVel())
        self.assertEqual(expectedAngle, podUnderTest.getAngle())
        self.assertEqual(expectedNextCheckPointId, podUnderTest.getNextCheckPointId())

class GameControllerTests(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testDummyTest(self):
        pass

class CalculatorTests(unittest.TestCase):
    def setUp(self):
        self._sut_ = Calculator()

    def tearDown(self):
        pass

    def testPolynomialReturnCorrectValue(self):
        coefs1 = [1, 2, 3]
        coefs2 = [2, -3, 4, -5, -6]
        t1 = 5
        t2 = 6
        expected1 = 38
        expected2 = 2052
        self.assertEqual(expected1, self._sut_.polynomial(coefs1, t1))
        self.assertEqual(expected2, self._sut_.polynomial(coefs2, t2))

    def testProdMatrixInverseShouldReturnIdentity(self):
        A = numpy.matrix([generateRandomRow(3) for i in range(3)])
        B = numpy.matrix([generateRandomRow(4) for i in range(4)])
        C = numpy.matrix([generateRandomRow(10) for i in range(10)])

        IA = numpy.identity(3)
        IB = numpy.identity(4)
        IC = numpy.identity(10)

        resA = self._sut_.inverse(A)*A
        resB = self._sut_.inverse(B)*B
        resC = self._sut_.inverse(C)*C

        numpy.testing.assert_array_almost_equal(resA, IA)
        numpy.testing.assert_array_almost_equal(resB, IB)
        numpy.testing.assert_array_almost_equal(resC, IC)

    def _calculateCorrectSplineCoefficients_(self, positions, velocities, time,
        expectedXCoefs, expectedYCoefs):
        result = self._sut_.getSplinesCoefficients(positions, velocities, time)
        self.assertTrue(result.has_key("xCoefs"))
        self.assertTrue(result.has_key("yCoefs"))

        self.assertEqual(len(expectedXCoefs), len(result["xCoefs"]))
        self.assertEqual(len(expectedYCoefs), len(result["yCoefs"]))

        for i in range(len(expectedXCoefs)):
            self.assertAlmostEqual(expectedXCoefs[i], result["xCoefs"][i])

        for i in range(len(expectedYCoefs)):
            self.assertAlmostEqual(expectedYCoefs[i], result["yCoefs"][i])

    def testCalculateCorrectSplineCoefficients(self):
        positions = [Point(6,4), Point(11,7), Point(3,7)]
        velocities = [Point(-1, -5)]
        time = [0, 4, 8, 0]

        expectedXCoefs = [-31/256.0, 67/64.0, -1.0, 6.0]
        expectedYCoefs = [-49/256.0, 141/64.0, -5.0, 4.0]

        self._calculateCorrectSplineCoefficients_(
            positions, velocities, time, expectedXCoefs, expectedYCoefs)

    def test3PolyDerivativesInBoundsCorrect(self):
        coefs1 = [0.5/3, -1, 3, 5]
        coefs2 = [-0.1, 0.3, 3, -4]
        time = [0,8]
        lowerB1_OK = 0
        lowerB1_NOK = 2
        upperB1_OK = 21
        upperB1_NOK = 15
        lowerB2_OK = -13
        lowerB2_NOK = -10
        upperB2_OK = 4
        upperB2_NOK = 2

        self.assertTrue(self._sut_.verify3PolyVelocityInBounds(coefs1, time, lowerB1_OK, upperB1_OK))
        self.assertTrue(self._sut_.verify3PolyVelocityInBounds(coefs2, time, lowerB2_OK, upperB2_OK))

        self.assertFalse(self._sut_.verify3PolyVelocityInBounds(coefs1, time, lowerB1_NOK, upperB1_OK))
        self.assertFalse(self._sut_.verify3PolyVelocityInBounds(coefs1, time, lowerB1_OK, upperB1_NOK))
        self.assertFalse(self._sut_.verify3PolyVelocityInBounds(coefs1, time, lowerB1_NOK, upperB1_NOK))

        self.assertFalse(self._sut_.verify3PolyVelocityInBounds(coefs2, time, lowerB2_NOK, upperB2_OK))
        self.assertFalse(self._sut_.verify3PolyVelocityInBounds(coefs2, time, lowerB2_OK, upperB2_NOK))
        self.assertFalse(self._sut_.verify3PolyVelocityInBounds(coefs2, time, lowerB2_NOK, upperB2_NOK))

        coefs = [-31/256.0, 67/64.0, -1.0, 6.0]
        lowerB_OK = -4
        lowerB_NOK = -3
        upperB_OK = 3
        upperB_NOK = 2
        self.assertTrue(self._sut_.verify3PolyThrustInBounds(coefs, time, lowerB_OK, upperB_OK))
        self.assertFalse(self._sut_.verify3PolyThrustInBounds(coefs, time, lowerB_OK, upperB_NOK))
        self.assertFalse(self._sut_.verify3PolyThrustInBounds(coefs, time, lowerB_NOK, upperB_OK))
        self.assertFalse(self._sut_.verify3PolyThrustInBounds(coefs, time, lowerB_NOK, upperB_NOK))

    def testPrepare3PositionsVectorReturn3CorrectElems(self):
        expectedP0 = Point(10,11)
        expectedP1 = Point(12,13)
        expectedP2 = Point(14,15)
        sutPod = Pod()
        sutPod.setPos(expectedP0)
        sutPod.setNextCheckPointId(5)
        checkpointPos = [Point(), Point(), Point(), Point(), Point(), expectedP1, expectedP2, Point()]
        result = self._sut_.prepare3PositionsVector(sutPod, checkpointPos)
        self.assertEqual(len(result), 3)
        self.assertEqual(expectedP0, result[0])
        self.assertEqual(expectedP1, result[1])
        self.assertEqual(expectedP2, result[2])
        checkpointPos.pop()
        checkpointPos.pop()
        expectedP2 = Point(20,21)
        checkpointPos[0] = expectedP2
        result = self._sut_.prepare3PositionsVector(sutPod, checkpointPos)
        self.assertEqual(len(result), 3)
        self.assertEqual(expectedP0, result[0])
        self.assertEqual(expectedP1, result[1])
        self.assertEqual(expectedP2, result[2])

    def testCalculateDestAndThrustValuesReturnsCorrectDirectionAndThrust(self):
        sutPod = Pod()
        sutPod.setPos(Point(7242, 3319))
        sutPod.setVel(Point(-305,188))
        xCoefs = [6000, 800, 50, 6]
        yCoefs = [3000, 500, 30, 2]
        expectedThrust = 85
        expectedAngle = math.atan(-81.0/25.0)
        result = self._sut_.calculateDestAndThrustValues(sutPod, {"xCoefs": xCoefs, "yCoefs": yCoefs})
        print result["dest"].__dict__
        self.assertTrue(result.has_key("dest"))
        self.assertTrue(result.has_key("thrust"))
        self.assertEqual(expectedThrust, result["thrust"])
        self.assertEqual(expectedAngle, math.atan((result["dest"].getX()-sutPod.getPos().getX())/(result["dest"].getY() - sutPod.getPos().getY())))

class AlgorithmsTests(unittest.TestCase):
    def setUp(self):
        self._sut_ = Algorithms()

    def tearDown(self):
        pass


    def testInterpolationStrategy(self):
        pvec = [Point(1,2), Point(3,4), Point(5,6)]
        vel = Point(-1,-1)
        result = self._sut_.InterpolationStrategy(pvec, vel)
        self.assertTrue(result.has_key("pos"))
        self.assertTrue(result.has_key("thrust"))

if __name__ == '__main__':
    unittest.main()
