#include "gtest/gtest.h"
#include "gmock/gmock.h"
#include <fstream>
#include <cmath>

#include "GameController.hpp"

using namespace std;

class GameControllerFixture: public testing::Test
{
public:
    GameController sut_;
};


TEST_F(GameControllerFixture, shouldNotCrash)
{
    ASSERT_TRUE(true);
}


TEST(SampleTest, shouldPass)
{
    ASSERT_EQ(0,0);
}
