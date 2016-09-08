#include "gtest/gtest.h"
#include "gmock/gmock.h"
#include <fstream>
#include <cmath>
#include <random>

#include <boost/numeric/ublas/io.hpp>
#include <boost/numeric/ublas/matrix_proxy.hpp>

#include "Calculator.hpp"

#define EPSILON 1.0e-3

using namespace std;
using namespace boost::numeric;

VectorType generateRandomRow(int size)
{
    VectorType result(size);
    double lower_bound = -1000;
    double upper_bound = 1000;
    std::uniform_real_distribution<double> unif(lower_bound,upper_bound);
    std::default_random_engine re;
    for (auto& el : result)
    {
        el = unif(re);
    }
    return result;
}

class CalculatorFixture: public testing::Test
{
public:
    Calculator sut_;
};


TEST_F(CalculatorFixture, shouldPass)
{
    ASSERT_TRUE(true);
}

TEST_F(CalculatorFixture, ProdMatrixInverseShouldReturnIdentity)
{
    MatrixType A(3, 3), B(4, 4), C(10,10);
    MatrixType InvA(3, 3), InvB(4, 4), InvC(10, 10);
    ublas::identity_matrix<double> IA(A.size1()), IB(B.size1()), IC(C.size1());

    for (int i=0; i<A.size1(); i++)
    {
        ublas::row(A, i) = generateRandomRow(A.size2());
    }

    for (int i=0; i<B.size1(); i++)
    {
        ublas::row(B, i) = generateRandomRow(B.size2());
    }

    for (int i=0; i<C.size1(); i++)
    {
        ublas::row(C, i) = generateRandomRow(C.size2());
    }

    InvA = ublas::prod(sut_.inverseMatrix(A), A);
    InvB = ublas::prod(sut_.inverseMatrix(B), B);
    InvC = ublas::prod(sut_.inverseMatrix(C), C);

    for (int i = 0; i< A.size1(); i++)
    {
        for (int j=0; j<A.size2(); j++)
        {
            ASSERT_LE(abs(IA(i,j) - InvA(i,j)), EPSILON);
        }
    }

    for (int i = 0; i< B.size1(); i++)
    {
        for (int j=0; j<B.size2(); j++)
        {
            ASSERT_LE(abs(IB(i,j) - InvB(i,j)), EPSILON);
        }
    }

    for (int i = 0; i< C.size1(); i++)
    {
        for (int j=0; j<C.size2(); j++)
        {
            ASSERT_LE(abs(IC(i,j) - InvC(i,j)), EPSILON);
        }
    }
}