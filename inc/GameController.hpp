#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <algorithm>
#include <set>
#include <cstdlib>
#include <ctime>
#include <cmath>

template <typename T>
class Point
{
public:
    Point(): Point(0,0) {}
    Point(T x, T y): x_(x), y_(y) {}
    T getX() { return x_; }
    T getY() { return y_; }
    void setX(T x) { x_ = x; }
    void setY(T y) { y_ = y; }
    void setXY(T x, T y) { setX(x); setY(y); }
private:
    T x_;
    T y_;
};

typedef Point<int> PointI;
typedef Point<double> PointD;

class Pod
{
public:
    PointI getPos();
    PointI getVel();
    int getAngle();
    int getNextCheckPointId();

    void setPos(PointI pos);
    void setVel(PointI vel);
    void setAngle(int angle);
    void setNextCheckPointId(int nextCheckPointId);
private:
    PointI pos_;
    PointI vel_;
    int angle_;
    int nextCheckPointId_;
};

class GameController
{
public:
    GameController();
    void startGame();

    void trivialStrategy();

    void loadInitialData(std::istream& input);
    void loadRuntimeData(std::istream& input);
    void writeSolution(PointI dest0, int thrust0, PointI dest1, int thrust1);

private:
    int laps_;
    int checkpointCount_;
    std::vector<PointI> checkpointPos_;
    std::vector<Pod> myPods_;
    std::vector<Pod> enemyPods_;
};