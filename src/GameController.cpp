#include "GameController.hpp"

#define DEBUG_PRINT 1
#define MY_PODS_NUM 1
#define ENEMY_PODS_NUM 1

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
{}

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
        PointI dest = checkpointPos_[myPod_.getNextCheckPointId()];
        int thrust = 50;
        writeSolution(dest, thrust);
    }
}

void GameController::loadInitialData(istream& input)
{
    input >> playerCount_; input.ignore();
    enemyPods_.resize(playerCount_-1);
    input >> laps_; input.ignore();
    input >> boosts_; input.ignore();
    input >> checkpointCount_; input.ignore();
    checkpointPos_.resize(checkpointCount_);
    for (auto& pos: checkpointPos_)
    {
        int checkpointX;
        int checkpointY;
        input >> checkpointX >> checkpointY; input.ignore();
        pos.setXY(checkpointX, checkpointY);
        debugLog("Checkpoint created: "+to_string(checkpointX)+", "+to_string(checkpointY));
    }
}

void GameController::loadRuntimeData(istream& input)
{
    int x;
    int y;
    int vx;
    int vy;
    int nextCheckPointId;
    input >> x >> y >> vx >> vy >> nextCheckPointId; input.ignore();
    myPod_.setPos(PointI(x,y));
    myPod_.setVel(PointI(vx,vy));
    myPod_.setNextCheckPointId(nextCheckPointId);

    for (auto& enemyPod: enemyPods_)
    {
        int x;
        int y;
        int vx;
        int vy;
        int nextCheckPointId;
        input >> x >> y >> vx >> vy >> nextCheckPointId; input.ignore();
        enemyPod.setPos(PointI(x,y));
        enemyPod.setVel(PointI(vx,vy));
        enemyPod.setNextCheckPointId(nextCheckPointId);
    }
}

void GameController::writeSolution(PointI dest, int thrust)
{
    cout << dest.getX() << " " << dest.getY() << " " << thrust << endl;
}