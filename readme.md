# Agility Testing Bot - Raspberry Pi Project

```python
"""
AGILITY TESTING BOT
A system to measure athlete reaction time and speed using servo-controlled laser targeting

HARDWARE SETUP:
- Raspberry Pi (any model with GPIO)
- 2x SG90 Servo Motors (horizontal/vertical movement)
- 5V Laser Diode Module
- HC-SR04 Ultrasonic Sensor
- 5V 2A Power Supply (recommended)

CIRCUIT CONNECTIONS:
GPIO18 → Horizontal Servo (PWM)
GPIO19 → Vertical Servo (PWM) 
GPIO23 → Ultrasonic Trig
GPIO24 → Ultrasonic Echo
5V → All VCC connections
GND → All ground connections

INSTALLATION:
1. sudo apt-get install python3-rpi.gpio
2. git clone https://github.com/your-repo/agility-testing-bot.git
3. cd agility-testing-bot
4. python3 agility_tester.py

CONFIGURATION (in agility_tester.py):
LASER_HEIGHT = 15      # Height in cm
HORIZONTAL_RANGE = 30  # Degrees (±30)
VERTICAL_RANGE = 30    # Degrees (0 to -30)
TOLERANCE = 2          # Detection threshold in cm
NUM_TRIALS = 10        # Number of test iterations

FEATURES:
- 🎯 Random laser targeting within configured range
- 🦶 Foot placement detection via ultrasonic sensor
- ⏱️ Reaction time measurement between targets
- 📏 Automatic distance calculation
- 📊 Performance report generation

SAMPLE OUTPUT:
=== Test Report ===
Trial  Distance(cm)  Time(s)  Speed(cm/s)
1      45.32         0.87     52.09
...
Average Speed: 51.25 cm/s
Total Distance: 412.50 cm
Total Time: 8.05 s

TROUBLESHOOTING:
- Servo jitter → Use dedicated 5V power supply
- False readings → Adjust TOLERANCE value
- Laser misalignment → Calibrate servo angles
