#include "gtest/gtest.h"
#include "gmock/gmock.h"
#include <fstream>
#include <cmath>

#include "Calculator.hpp"

using namespace std;


class CalculatorFixture: public testing::Test
{
public:
    Calculator sut_;
};


TEST_F(CalculatorFixture, shouldPass)
{
    ASSERT_TRUE(true);
}
