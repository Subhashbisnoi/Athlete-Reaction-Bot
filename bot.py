import RPi.GPIO as GPIO
import time
import random
import math

# Servo Motor Pins
HORIZONTAL_SERVO_PIN = 17
VERTICAL_SERVO_PIN = 27

# Ultrasonic Sensor Pins
TRIG_PIN = 23
ECHO_PIN = 24

# Laser height from ground (in cm)
LASER_HEIGHT = 15

# Servo angle limits
HORIZONTAL_ANGLE_RANGE = (-30, 30)  # Horizontal servo range
VERTICAL_ANGLE_RANGE = (-30, 0)  # Vertical servo range

# Initialize GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(HORIZONTAL_SERVO_PIN, GPIO.OUT)
GPIO.setup(VERTICAL_SERVO_PIN, GPIO.OUT)
GPIO.setup(TRIG_PIN, GPIO.OUT)
GPIO.setup(ECHO_PIN, GPIO.IN)

# Initialize PWM for servos
horizontal_servo = GPIO.PWM(HORIZONTAL_SERVO_PIN, 50)
vertical_servo = GPIO.PWM(VERTICAL_SERVO_PIN, 50)
horizontal_servo.start(0)
vertical_servo.start(0)

def set_servo_angle(servo, angle):
    duty = (angle / 18) + 2.5
    servo.ChangeDutyCycle(duty)
    time.sleep(0.5)

def get_distance():
    GPIO.output(TRIG_PIN, True)
    time.sleep(0.00001)
    GPIO.output(TRIG_PIN, False)
    
    while GPIO.input(ECHO_PIN) == 0:
        start_time = time.time()
    while GPIO.input(ECHO_PIN) == 1:
        end_time = time.time()
    
    duration = end_time - start_time
    distance = (duration * 34300) / 2  # Convert to cm
    return distance

def calculate_position(horizontal_angle, vertical_angle):
    x = LASER_HEIGHT * math.tan(math.radians(horizontal_angle))
    y = LASER_HEIGHT * math.tan(math.radians(vertical_angle))
    return (x, y)

def main():
    test_data = []
    num_tests = 10  # Number of test points
    
    print("Starting agility test...")
    
    for i in range(num_tests):
        horizontal_angle = random.randint(*HORIZONTAL_ANGLE_RANGE)
        vertical_angle = random.randint(*VERTICAL_ANGLE_RANGE)
        
        set_servo_angle(horizontal_servo, horizontal_angle)
        set_servo_angle(vertical_servo, vertical_angle)
        
        target_position = calculate_position(horizontal_angle, vertical_angle)
        print(f"Laser pointed at: {target_position}")
        
        start_time = time.time()
        while True:
            distance = get_distance()
            if distance < 5:  # Foot detected
                break
        end_time = time.time()
        
        reaction_time = end_time - start_time
        test_data.append((target_position, reaction_time))
        print(f"Reaction time: {reaction_time:.2f} seconds")
    
    print("Test complete! Generating report...")
    with open("agility_report.txt", "w") as f:
        for idx, (position, time_taken) in enumerate(test_data):
            f.write(f"Point {idx+1}: Position {position}, Time {time_taken:.2f} seconds\n")
    
    print("Report saved as agility_report.txt")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Test interrupted.")
    finally:
        horizontal_servo.stop()
        vertical_servo.stop()
        GPIO.cleanup()
