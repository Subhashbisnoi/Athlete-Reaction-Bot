import RPi.GPIO as GPIO
import time
import math
import random

# GPIO Setup
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Pin Configuration
HORIZONTAL_SERVO_PIN = 18
VERTICAL_SERVO_PIN = 19
TRIG_PIN = 23
ECHO_PIN = 24

# Servo Parameters
LASER_HEIGHT = 15  # cm
HORIZONTAL_MIN_ANGLE = -30
HORIZONTAL_MAX_ANGLE = 30
VERTICAL_MIN_ANGLE = -30
VERTICAL_MAX_ANGLE = 0

# Servo PWM Setup
GPIO.setup(HORIZONTAL_SERVO_PIN, GPIO.OUT)
GPIO.setup(VERTICAL_SERVO_PIN, GPIO.OUT)
horizontal_pwm = GPIO.PWM(HORIZONTAL_SERVO_PIN, 50)
vertical_pwm = GPIO.PWM(VERTICAL_SERVO_PIN, 50)
horizontal_pwm.start(0)
vertical_pwm.start(0)

# Ultrasonic Sensor Setup
GPIO.setup(TRIG_PIN, GPIO.OUT)
GPIO.setup(ECHO_PIN, GPIO.IN)
GPIO.output(TRIG_PIN, False)
time.sleep(0.1)

# Configuration Parameters
TOLERANCE = 2  # cm tolerance for obstacle detection
NUM_TRIALS = 10
DEBOUNCE_TIME = 0.5  # seconds between detections

def set_servo_angle(pwm, angle, min_angle, max_angle):
    duty = 2.5 + (12.5 - 2.5) * (angle - min_angle) / (max_angle - min_angle)
    pwm.ChangeDutyCycle(duty)
    time.sleep(0.5)

def set_horizontal_angle(angle):
    angle = max(min(angle, HORIZONTAL_MAX_ANGLE), HORIZONTAL_MIN_ANGLE)
    set_servo_angle(horizontal_pwm, angle, HORIZONTAL_MIN_ANGLE, HORIZONTAL_MAX_ANGLE)

def set_vertical_angle(angle):
    angle = max(min(angle, VERTICAL_MAX_ANGLE), VERTICAL_MIN_ANGLE)
    set_servo_angle(vertical_pwm, angle, VERTICAL_MIN_ANGLE, VERTICAL_MAX_ANGLE)

def calculate_position(horizontal_angle, vertical_angle):
    theta = math.radians(abs(vertical_angle))
    phi = math.radians(horizontal_angle)
    L = LASER_HEIGHT * math.tan(theta)
    return (L * math.cos(phi), L * math.sin(phi))

def calculate_expected_distance(vertical_angle):
    return LASER_HEIGHT / math.cos(math.radians(abs(vertical_angle)))

def measure_distance():
    GPIO.output(TRIG_PIN, True)
    time.sleep(0.00001)
    GPIO.output(TRIG_PIN, False)

    start_time = time.time()
    timeout = start_time + 0.04  # 40ms timeout (~4m range)

    while GPIO.input(ECHO_PIN) == 0 and start_time < timeout:
        start_time = time.time()

    if time.time() > timeout:
        return -1

    pulse_end = time.time()
    while GPIO.input(ECHO_PIN) == 1 and pulse_end < timeout:
        pulse_end = time.time()

    if time.time() > timeout:
        return -1

    duration = pulse_end - start_time
    return (duration * 34300) / 2  # cm

def wait_for_detection(expected_distance):
    while True:
        measured_distance = measure_distance()
        if 0 < measured_distance < (expected_distance - TOLERANCE):
            time.sleep(DEBOUNCE_TIME)  # Debounce
            return True
        time.sleep(0.1)

def generate_report(data):
    print("\n\n=== Test Report ===")
    print(f"Total Trials: {len(data)}")
    print("Trial\tDistance (cm)\tTime (s)\tSpeed (cm/s)")
    
    total_dist = 0
    total_time = 0
    for i, (dist, t, spd) in enumerate(data):
        print(f"{i+1}\t{dist:.2f}\t\t{t:.2f}\t\t{spd:.2f}")
        total_dist += dist
        total_time += t
    
    avg_speed = total_dist / total_time if total_time > 0 else 0
    print(f"\nAverage Speed: {avg_speed:.2f} cm/s")
    print(f"Total Distance: {total_dist:.2f} cm")
    print(f"Total Time: {total_time:.2f} s")

def main():
    try:
        test_data = []
        previous_position = None
        current_position = None

        # Initial position
        set_horizontal_angle(0)
        set_vertical_angle(-15)
        print("Calibrating... Wait for initial detection")
        expected_dist = calculate_expected_distance(-15)
        wait_for_detection(expected_dist)

        for trial in range(NUM_TRIALS):
            # Generate new target
            h_angle = random.uniform(HORIZONTAL_MIN_ANGLE, HORIZONTAL_MAX_ANGLE)
            v_angle = random.uniform(-25, -5)  # Ensure floor projection
            
            set_horizontal_angle(h_angle)
            set_vertical_angle(v_angle)
            
            expected_dist = calculate_expected_distance(v_angle)
            current_position = calculate_position(h_angle, v_angle)
            start_time = time.time()

            print(f"\nTrial {trial+1}: Target at {current_position}")
            
            # Wait for detection
            wait_for_detection(expected_dist)
            reaction_time = time.time() - start_time
            
            # Calculate metrics
            if previous_position:
                dx = current_position[0] - previous_position[0]
                dy = current_position[1] - previous_position[1]
                distance = math.hypot(dx, dy)
                speed = distance / reaction_time if reaction_time > 0 else 0
                test_data.append((distance, reaction_time, speed))
            
            previous_position = current_position

        generate_report(test_data)

    finally:
        horizontal_pwm.stop()
        vertical_pwm.stop()
        GPIO.cleanup()

if __name__ == "__main__":
    main()
