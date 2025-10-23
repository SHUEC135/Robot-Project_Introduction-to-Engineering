import motor_pair
import distance_sensor
import runloop
from hub import port, light_matrix

# Configuration constants
DETECTION_DISTANCE = 150  # 15cm in millimeters
DRIVE_VELOCITY = 500      # Speed when going straight
TURN_VELOCITY = 400       # Speed when rotating

async def main():
    # Pair motors for the car (left motor on A, right motor on B)
    motor_pair.pair(motor_pair.PAIR_1, port.A, port.B)
    
    # Show ready indicator
    light_matrix.show_image(light_matrix.IMAGE_HAPPY)
    await runloop.sleep_ms(1000)
    
    while True:
        # Read distance from sensor on port C
        dist = distance_sensor.distance(port.C)
        
        # Check if obstacle detected within 15cm
        if dist != -1 and dist < DETECTION_DISTANCE:
            # ROTATE STATE: Obstacle detected - turn clockwise
            # Show alert on display
            light_matrix.show_image(light_matrix.IMAGE_ARROW_E)
            
            # Rotate clockwise (right motor forward, left motor slower/stopped)
            motor_pair.move_tank(motor_pair.PAIR_1, 0, TURN_VELOCITY)
        else:
            # DRIVE_STRAIGHT STATE: No obstacle - go forward
            # Show forward arrow
            light_matrix.show_image(light_matrix.IMAGE_ARROW_N)
            
            # Drive straight at constant speed
            motor_pair.move(motor_pair.PAIR_1, 0, velocity=DRIVE_VELOCITY)
        
        # Small delay to prevent overwhelming the system
        await runloop.sleep_ms(50)

# Start the main control loop
runloop.run(main())
