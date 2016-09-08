#include "Calculator.hpp"

using namespace boost::numeric;

VectorType Calculator::solveMatrixEq(MatrixType A, VectorType C)
{
    return ublas::prod(inverseMatrix(A), C);
}

MatrixType Calculator::inverseMatrix(MatrixType A) const
{
    return A;
}