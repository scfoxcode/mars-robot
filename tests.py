from main import ReadSimulation, Robot, Position

def printTestResult(result):
    output = '{} - {}'.format('Pass' if result[0] else 'FAIL', result[1])
    print(output)

def testRobotRotate():
    robot = Robot(Position(3, 2), 'E', 'FFFF')
    robot.rotateLeft90()
    if robot.facing != 'N':
        return (False, 'Failed to rotate left (1)')
    robot.rotateLeft90()
    if robot.facing != 'W':
        return (False, 'Failed to rotate left (2)')
    robot.rotateRight90()
    if robot.facing != 'N':
        return (False, 'Failed to rotate right')
    return (True, 'testRobotRotate')

def testRobotMove():
    robot = Robot(Position(3, 2), 'E', 'FFFF')
    worldSize = Position(6, 6)
    robot.moveForward(worldSize)
    if robot.position.x != 4:
        return (False, 'Failed to move forward (1)')
    robot.moveForward(worldSize)
    if robot.position.x != 5:
        return (False, 'Failed to move forward (2)')
    robot.rotateLeft90()
    robot.moveForward(worldSize)
    if robot.position.y != 3:
        return (False, 'Failed to move forward (3)')
    robot.rotateLeft90()
    robot.moveForward(worldSize)
    if robot.position.x != 4:
        return (False, 'Failed to move forward (4)')
    return (True, 'testRobotMove')


def testReader():
    reader = ReadSimulation()
    robot = reader.buildRobotFromLine('(1, 4, W) FLLRRRF')
    if (robot == None or
        robot.position.x != 1 or
        robot.position.y != 4 or
        robot.facing != 'W' or
        robot.instructions != 'FLLRRRF'):
        return (False, 'Failed to buildRobotFromLine')
    return (True, 'buildRobotFromLine')

def tests():
    print('Running tests')
    results = [
        testRobotRotate(),
        testRobotMove(),
        testReader(),
    ]
    for r in results:
        printTestResult(r)

tests()
