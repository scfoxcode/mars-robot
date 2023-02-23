# Created the repo before work, but started coding at approx 18:40
# Finished coding at 21:08, not including the readme

import os
import re

class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def add(self, position):
        self.x += position.x
        self.y += position.y

    def clone(self):
        return Position(self.x, self.y)

class Robot:
    directions = ('N', 'E', 'S', 'W')
    movements = (Position(0, 1), Position(1, 0), Position(0, -1), Position(-1, 0)) 

    def __init__(self, position, facing, instructions):
        self.position = position
        self.facing = facing
        self.facingIndex = Robot.directions.index(facing)
        self.instructions = instructions
        self.pc = 0
        self.isLost = False

    def rotateRight90(self):
        self.facingIndex += 1
        if self.facingIndex >= len(Robot.directions):
            self.facingIndex = 0
        self.facing = Robot.directions[self.facingIndex]

    def rotateLeft90(self):
        self.facingIndex -= 1
        if self.facingIndex < 0:
            self.facingIndex = len(Robot.directions) - 1 
        self.facing = Robot.directions[self.facingIndex]

    def moveForward(self, worldSize):
        currentPosition = self.position.clone() # record incase we become lost
        self.position.add(Robot.movements[self.facingIndex])
        if (self.position.x < 0 or
            self.position.y < 0 or
            self.position.x > worldSize.x or
            self.position.y > worldSize.y ):
            self.isLost = True
            # Slightly questionable as our position is beyond the grid
            # But we are pretending it isn't and simply flagging lost for reporting purposes
            self.position = currentPosition

    def update(self, worldSize):
        order = self.instructions[self.pc]
        if order == 'L':
            self.rotateLeft90()
        elif order == 'R':
            self.rotateRight90()
        elif order == 'F':
            self.moveForward(worldSize)
        else:
            raise Exception('Robot failed to understand instruction {} at pc {}'.format(order, self.pc))
        self.pc += 1

    def toString(self):
        output = '({}, {}, {})'.format(self.position.x, self.position.y, self.facing) 
        if self.isLost:
            output += ' LOST'
        return output

class Simulation:
    def __init__(self):
        self.robots = []

    def run(self):
        print('Running Simulation...')
        updatesHappened = True
        safety = 0 
        while updatesHappened and safety < 10000000:
            safety += 1
            updatesHappened = False;
            for robot in self.robots:
                if robot.isLost == False and robot.pc < len(robot.instructions):
                    robot.update(self.worldSize)                    
                    updatesHappened = True
        print('Finished running simulation')

    def addRobot(self, robot):
        self.robots.append(robot)

    def setWorldSize(self, worldSize):
        self.worldSize = worldSize

    def printResults(self):
        for r in self.robots:
            print(r.toString())

class ReadSimulation:
    def __init__(self):
        print('Reading Simulation...')

    def readFromFile(self, filepath):
        sim = Simulation()
        with open(filepath) as f:
            lines = f.read().splitlines()
            f.close()
        for line in lines:
            if line[0] == '(':
                sim.addRobot(self.buildRobotFromLine(line))
            else:
                sim.setWorldSize(self.getWorldSizeFromLine(line))
        return sim

    def getWorldSizeFromLine(self, line):
        data = re.findall(r'(\d+)\s(\d+)', line)
        if len(data[0]) != 2:
            raise Exception('Failed to set world size from line: {}'.format(line))

        return Position(int(data[0][0]), int(data[0][1]))

    def buildRobotFromLine(self, line):
        data = re.findall(r'^\((\d+), (\d+), (\S)\)\s([FLR]*)', line)
        if len(data) < 1:
            raise Exception('Failed to build Robot from line: {}'.format(line))

        return Robot(Position(int(data[0][0]), int(data[0][1])), data[0][2], data[0][3])

def main():
    print('Mars Rovers. Begin exploring the Red Planet!')
    reader = ReadSimulation();
    simulation = reader.readFromFile('input.txt')
    simulation.run()
    simulation.printResults()

    simulation = reader.readFromFile('input2.txt')
    simulation.run()
    simulation.printResults()

main()
