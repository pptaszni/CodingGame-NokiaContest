#ifndef CALCULATOR_HPP
#define CALCULATOR_HPP

#include <boost/numeric/ublas/matrix.hpp>

typedef boost::numeric::ublas::vector<double> VectorType;
typedef boost::numeric::ublas::matrix<double> MatrixType;

class Calculator
{
public:
    VectorType solveMatrixEq(MatrixType A, VectorType C);

    MatrixType inverseMatrix(MatrixType A) const;
};

#endif  //CALCULATOR_HPP
