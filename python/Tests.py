import unittest
import random
import numpy

from MainComponent import Point
from MainComponent import Pod
from MainComponent import Calculator

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


if __name__ == '__main__':
    unittest.main()