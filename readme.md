# Athlete Agility Test Bot 🏃‍♂️💨

This project is a small bot designed to test an athlete's agility, reaction time, and speed in different directions. The system consists of two servo motors that control the movement of a laser pointer, randomly projecting it onto the floor within a defined rectangular area. An ultrasonic sensor detects when a foot is placed on the laser point, and the system measures the reaction time and movement speed over multiple iterations to generate a performance report.

## Features ✨
- 🎯 **Laser-based agility test** with random movement  
- ⚙️ **Two servo motors** controlling horizontal and vertical laser direction  
- 🔎 **Ultrasonic sensor** detects foot placement  
- ⏱️ **Reaction time & speed measurement** for performance tracking  
- 📊 **Report generation** with recorded times and distances  

## Components Used 🛠️
- **Raspberry Pi** (for control and processing)  
- **Servo Motors (2x)** (to control the laser pointer in horizontal and vertical directions)  
- **Laser Pointer** (to mark random positions on the floor)  
- **Ultrasonic Sensor (HC-SR04)** (to detect foot placement)  
- **Wires and Power Supply** (for connections)  

## How It Works ⚡
1. The horizontal and vertical servo motors move to **random angles** within the defined range.  
2. The laser pointer moves accordingly and marks a position on the floor.  
3. The system **starts a timer** and waits for the athlete to step on the marked spot.  
4. Once the **ultrasonic sensor detects** a foot at the expected position, the timer stops.  
5. The system logs the **reaction time** and **distance moved**.  
6. This process repeats for **10-15 iterations**.  
7. A **performance report** is generated with all recorded reaction times and distances.  

## Installation & Setup 🚀
### 1. Set up Raspberry Pi:
- Install the Raspberry Pi OS and enable GPIO control.  
- Connect the **servos, ultrasonic sensor, and laser pointer**.  

### 2. Install required Python libraries:
```bash
pip install RPi.GPIO
```

### 3. Run the script:
```bash
python bot.py
```

### 4. View the report:
- After completing the test, a **report will be saved** as `agility_report.txt`.  

## Customization 🔧
- Adjust the **servo angle ranges** to modify the laser movement area.  
- Change the **ultrasonic sensor threshold** to fine-tune foot detection sensitivity.  
- Modify the **number of test iterations** based on training requirements.  

## Limitations ❗
- ❌ Works best indoors with controlled lighting.  
- 📏 The accuracy of foot detection depends on the ultrasonic sensor's precision.  
- 🤔 The test area should be **free of obstacles** to avoid incorrect detections.  

## Future Improvements 🚀
- 📷 **Use a camera-based system** for more precise movement tracking.  
- 📊 **Implement real-time visualization** of athlete movement.  
- 📱 **Develop a mobile app** to sync and analyze performance data.  

## License 📜
This project is **open-source** and free to use for **personal and educational purposes**.  
