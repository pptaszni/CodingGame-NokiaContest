#include "GameController.hpp"

#define DEBUG_PRINT 1
#define MY_PODS_NUM 2
#define ENEMY_PODS_NUM 2

using namespace::std;

void debugLog(string textToLog)
{
    #if DEBUG_PRINT
    cerr << textToLog << endl;
    #endif
}

PointI Pod::getPos() { return pos_; }
PointI Pod::getVel() { return vel_; }
int Pod::getAngle() { return angle_; }
int Pod::getNextCheckPointId() { return nextCheckPointId_; }

void Pod::setPos(PointI pos) { pos_ = pos; }
void Pod::setVel(PointI vel) { vel_ = vel; }
void Pod::setAngle(int angle) { angle_ = angle; }
void Pod::setNextCheckPointId(int nextCheckPointId) { nextCheckPointId_ = nextCheckPointId; }


GameController::GameController()
{
    myPods_.resize(MY_PODS_NUM);
    enemyPods_.resize(ENEMY_PODS_NUM);
}

void GameController::startGame()
{
    debugLog("Game started ...");
    loadInitialData(cin);
    debugLog("Initial data loaded ...");
    trivialStrategy();
}

void GameController::trivialStrategy()
{
    while(1)
    {
        loadRuntimeData(cin);
        PointI dest0 = checkpointPos_[myPods_[0].getNextCheckPointId()];
        PointI dest1 = checkpointPos_[myPods_[0].getNextCheckPointId()];
        int thrust0 = 150;
        int thrust1 = 50;
        writeSolution(dest0, thrust0, dest1, thrust1);
    }
}

void GameController::loadInitialData(istream& input)
{
    input >> laps_; input.ignore();
    input >> checkpointCount_; input.ignore();
    checkpointPos_.resize(checkpointCount_);
    for (auto& pos: checkpointPos_)
    {
        int checkpointX;
        int checkpointY;
        input >> checkpointX >> checkpointY; input.ignore();
        pos.setXY(checkpointX, checkpointY);
    }
}

void GameController::loadRuntimeData(istream& input)
{
    for (auto& myPod: myPods_)
    {
        int x;
        int y;
        int vx;
        int vy;
        int angle;
        int nextCheckPointId;
        input >> x >> y >> vx >> vy >> angle >> nextCheckPointId; input.ignore();
        myPod.setPos(PointI(x,y));
        myPod.setVel(PointI(vx,vy));
        myPod.setAngle(angle);
        myPod.setNextCheckPointId(nextCheckPointId);
    }
    for (auto& enemyPod: enemyPods_)
    {
        int x;
        int y;
        int vx;
        int vy;
        int angle;
        int nextCheckPointId;
        input >> x >> y >> vx >> vy >> angle >> nextCheckPointId; input.ignore();
        enemyPod.setPos(PointI(x,y));
        enemyPod.setVel(PointI(vx,vy));
        enemyPod.setAngle(angle);
        enemyPod.setNextCheckPointId(nextCheckPointId);
    }
}

void GameController::writeSolution(PointI dest0,
    int thrust0,
    PointI dest1,
    int thrust1)
{
    cout << dest0.getX() << " " << dest0.getY() << " " << thrust0 << endl;
    cout << dest1.getX() << " " << dest1.getY() << " " << thrust1 << endl;
}