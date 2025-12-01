# CS 1301 - Introduction to Computing

**Georgia Institute of Technology - Fall 2025**

This folder contains my coursework and projects for CS 1301, an introductory computing course focusing on Python programming and robotics using the iRobot Create® 3 educational robot.

## Course Overview

CS 1301 introduces fundamental programming concepts through hands-on projects combining software development with physical robotics. The course emphasizes problem-solving, algorithmic thinking, and real-world applications of computing principles.

## Labs

### Lab 1: Introduction to Robotics
**Completed:** September 2025    
**Topics:** Basic robot control, event-driven programming, sensor integration

**Projects:**
- **Fill in the Blanks:** Completed robot control systems using bumpers, buttons, and IR sensors
- **CodeBreaker:** Password management system where users input passcodes via bumpers and buttons, with robot feedback through movement, lights, and sounds
- **Object Follower:** Autonomous tracking system that maintains optimal distance from a moving object using proximity sensors

**Key Skills:** Asynchronous programming, event handlers, sensor data processing, fail-safe mechanisms

---

### Lab 2: Autonomous Navigation
**Completed:** October 2025  
**Topics:** Advanced sensor fusion, autonomous navigation, obstacle avoidance

**Projects:**
- **Robot Pong:** Simulates pong mechanics with wall detection and reflection angles, changing light colors with each bounce
- **Autonomous Delivery:** Navigates to predefined destinations while avoiding obstacles, records position data to CSV for path visualization

**Key Skills:** IR proximity calculations, path planning algorithms, CSV file handling, real-time decision making, multi-modal navigation

---

### Lab 3: Advanced Robotics Systems
**Completed:** November-December 2025  
**Topics:** Object-oriented programming, maze solving, complex navigation

**Projects:**
- **Self-Parking:** Wall-following algorithm that detects gaps along walls and parks in the largest available space
- **Maze Solver:** Implementation of flood-fill algorithm using custom Cell and Maze classes to navigate unknown mazes dynamically

**Key Skills:** Object-oriented programming, flood-fill pathfinding, dynamic obstacle mapping, grid-based navigation

---

## Technologies & Tools

- **Language:** Python 3.x
- **Hardware:** iRobot Create® 3 Educational Robot
- **Libraries:** 
  - `irobot_edu_sdk` - Robot control and sensor interface
  - `matplotlib` - Data visualization (Lab 2)
  - Standard Python libraries (`math`, `csv`)

## File Organization

```
cs1301-intro-computing/
├── lab01/
│   ├── bumpers_and_buttons.py
│   ├── ir_sensors.py
│   ├── CodeBreaker.py
│   ├── ObjectFollower.py
│   └── closestSensor.py (autograder helper)
├── lab02/
│   ├── RobotPong.py
│   ├── AutonomousDelivery.py
│   ├── PointGraph.py
│   ├── roboticsLab02Aux.py (autograder helper)
│   └── PositionData.csv
├── lab03/
│   ├── selfParking.py
│   ├── MazeSolver.py
│   └── MazeSolverHelpers.py (autograder helper)
└── README.md
```

## Key Concepts Learned

### Programming Fundamentals
- Variables, data types, and operators
- Control structures (if/else, loops)
- Functions and parameters
- Lists, tuples, and dictionaries
- String manipulation
- File I/O (CSV handling)

### Advanced Python
- Asynchronous programming (`async`/`await`)
- Event-driven programming with decorators
- Global variables and scope
- Object-oriented programming (classes, objects, methods, attributes)
- Lambda functions and list comprehensions

### Robotics & Sensors
- IR proximity sensor interpretation (formula: 4095/(reading + 1))
- Event handlers for bumpers and touch buttons
- Real-time sensor data processing
- Fail-safe mechanisms for collision avoidance
- Multi-sensor fusion for decision making

### Algorithms & Problem Solving
- Angle calculations and trigonometry (`atan2`, `degrees`)
- Reflection angle computation for bouncing
- Path planning and navigation
- Flood-fill algorithm for maze solving
- Cost propagation and pathfinding
- State machine design (navigation modes)
- Grid-based spatial reasoning

### Software Engineering
- Code modularity and helper functions
- Documentation and comments
- Debugging techniques and autograders
- Version control best practices
- Following specifications and requirements

## Learning Outcomes

By completing this coursework, I developed:

- **Proficiency in Python programming fundamentals** including syntax, data structures, and control flow
- **Understanding of event-driven and asynchronous programming** for real-time systems
- **Experience with sensor data processing and interpretation** to make autonomous decisions
- **Implementation of pathfinding and navigation algorithms** including flood-fill and obstacle avoidance
- **Object-oriented design principles** through creating Cell and Maze classes
- **Integration of hardware and software systems** by controlling physical robots with code
- **Problem decomposition and algorithmic thinking** to break complex challenges into manageable pieces
- **Debugging and testing strategies** using autograders and real-world robot testing

## Highlights

- **CodeBreaker:** Creative use of robot inputs (bumpers/buttons) as a passcode entry system with multi-modal feedback
- **Autonomous Delivery:** Successfully implemented multi-mode navigation system with obstacle avoidance and path tracking
- **Maze Solver:** Designed complete OOP solution with Cell and Maze classes implementing flood-fill algorithm for unknown maze navigation
- **Self-Parking:** Developed sophisticated gap detection and selection algorithm mimicking real autonomous vehicle parking

## Grading & Assessment

All labs included:
- **Gradescope submission:** Automated and manual code review
- **Live demonstrations:** In-person demos with TAs showing robot functionality
- **Conceptual questions:** Understanding of code logic and design decisions
- **Code quality:** Documentation, style, and proper implementation

### Lab Breakdown
- **Lab 1:** 100 points (+ 10 extra credit for CodeBreaker dance celebration)
- **Lab 2:** 100 points (+ 10 extra credit for early submission)
- **Lab 3:** 100 points (+ 10 extra credit for visual/audio debugging)

## Running the Code

### Prerequisites
```bash
# Install required packages
pip install irobot-edu-sdk
pip install matplotlib  # For Lab 2 visualization
```

### Connecting to Robot
1. Turn on the iRobot Create® 3
2. Connect via Bluetooth
3. Run the Python script
4. Press the play button on the robot to start

### Testing Helper Functions
Several labs include ungraded autograders on Gradescope for testing helper functions before running on the robot. This allows for efficient debugging without physical hardware.

## Robot Specifications

**iRobot Create® 3 Educational Robot:**
- **Sensors:** 7 IR proximity sensors, 2 bumpers, 2 touch buttons, position tracking (x, y, heading)
- **Actuators:** Differential drive wheels, LED ring light, speaker
- **Programming:** Python via `irobot_edu_sdk`
- **Size:** Approximately 45 units in diameter
- **Sensor arrangement:** IR sensors positioned at -65.3°, -38.0°, -20.0°, -3.0°, 14.25°, 34.0°, 65.3° relative to front

## Additional Resources

- [iRobot Education Python SDK Documentation](https://python.irobot.com/)
- Course materials available on Canvas
- Georgia Tech CS 1301 course website

## Academic Integrity Note

All code in this repository represents my individual work completed in accordance with Georgia Tech's Academic Honor Code. These projects are shared as a portfolio of my learning. If you're currently enrolled in CS 1301, please complete your own assignments independently.

---

**Course:** CS 1301 - Introduction to Computing  
**Institution:** Georgia Institute of Technology  
**Semester:** Fall 2025  
**Format:** Individual assignments with live demos

*Last Updated: December 2025*
