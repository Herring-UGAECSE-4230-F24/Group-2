import RPi.GPIO as GPIO
import time

# Pin Definitions
CLK_PIN = 18  # Clock pin (Rotary Encoder)
DT_PIN = 23   # Data pin (Rotary Encoder)
SW_PIN = 24   # Switch pin (Rotary Encoder Button)
IR_PIN = 12   # IR Sensor pin
MOTOR_PIN = 13  # Motor control pin

# Constants
DEBOUNCE_TIME = 0.002  # Debounce time in seconds
BASE_RPM_STEP = 25     # RPM increment per encoder pulse
RPM_PER_TURN = 500     # Approximate RPM change per full turn of encoder
FAN_BLADES = 3         # Number of fan blades for RPM calculation

# Global variables
desired_rpm = 25  # Initial desired RPM
motor_running = True  # Motor state
rotary_encoder_pos = 1  # Encoder position
blade_counter = 0
blade_counter_window = time.time()
last_clk_state = GPIO.HIGH  # Previous CLK state
same_blade = False
motor_pwm = None  # Motor PWM object


def setup_gpio():
    """Configures GPIO pins."""
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)

    # Setup pins
    GPIO.setup(CLK_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(DT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(SW_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(IR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(MOTOR_PIN, GPIO.OUT)
    GPIO.output(MOTOR_PIN, GPIO.HIGH)  # Default high for motor control


def calculate_rpm(blades, edge_count, time_elapsed):
    """Calculate RPM using edge count and elapsed time."""
    return (edge_count * 60) / (blades * time_elapsed)


def initialize_motor():
    """Initializes motor PWM."""
    global motor_pwm
    frequency = desired_rpm * FAN_BLADES / 60
    motor_pwm = GPIO.PWM(MOTOR_PIN, frequency)
    motor_pwm.start(0)  # Start with 0 duty cycle


def update_motor():
    """Updates motor speed based on desired RPM."""
    global motor_pwm
    frequency = desired_rpm * FAN_BLADES / 60
    duty_cycle = min(100, 5 + desired_rpm * 0.1)  # Example duty cycle adjustment
    motor_pwm.ChangeFrequency(frequency)
    motor_pwm.ChangeDutyCycle(duty_cycle)


def read_rotary_encoder():
    """Reads and processes rotary encoder input."""
    global last_clk_state, rotary_encoder_pos, desired_rpm
    clk_state = GPIO.input(CLK_PIN)
    if clk_state != last_clk_state:  # Detected a state change
        if GPIO.input(DT_PIN) != clk_state:  # Clockwise
            rotary_encoder_pos += 1
        else:  # Counter-clockwise
            rotary_encoder_pos -= 1

        desired_rpm = BASE_RPM_STEP * rotary_encoder_pos
        if desired_rpm < 0:  # Prevent negative RPM
            desired_rpm = 0

        update_motor()
        print(f"Desired RPM: {desired_rpm}")
    last_clk_state = clk_state


def toggle_motor():
    """Toggles motor on/off."""
    global motor_running
    motor_running = not motor_running
    if motor_running:
        update_motor()
    else:
        motor_pwm.ChangeDutyCycle(0)  # Stop the motor


def read_ir_sensor():
    """Reads and processes IR sensor input to calculate actual RPM."""
    global blade_counter, blade_counter_window, same_blade

    current_time = time.time()
    if GPIO.input(IR_PIN) == GPIO.LOW:  # Detecting blade
        if not same_blade:
            same_blade = True
            blade_counter += 1
    else:
        same_blade = False

    if current_time - blade_counter_window >= 1:  # Every second
        measured_rpm = calculate_rpm(FAN_BLADES, blade_counter, current_time - blade_counter_window)
        print(f"Measured RPM: {measured_rpm}")
        blade_counter = 0
        blade_counter_window = current_time


def main():
    """Main program loop."""
    setup_gpio()
    initialize_motor()
    print("Press Ctrl+C to exit.")
    try:
        while True:
            read_rotary_encoder()  # Check encoder for RPM adjustment
            if GPIO.input(SW_PIN) == GPIO.LOW:  # Check button press
                toggle_motor()
                time.sleep(0.2)  # Debounce for button

            if motor_running:
                read_ir_sensor()  # Read IR sensor for RPM monitoring

            time.sleep(0.01)  # Small delay to avoid excessive CPU usage
    except KeyboardInterrupt:
        print("Exiting program...")
    finally:
        GPIO.cleanup()


if __name__ == "__main__":
    main()
