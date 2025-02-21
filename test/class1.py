import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import random

# Simulation parameters
N = 10          # Number of positions on the street
L = 5           # Traffic light position
T_green = 10    # Number of time steps the light is green
T_red = 10      # Number of time steps the light is red
p = 0.3         # Probability of a new car entering per time step
total_steps = 100  # Total number of time steps to simulate

# Initialize the street and traffic light
street = [0] * N  # List representing the street: 0 = empty, 1 = car
light_state = 'green'  # Initial state of the traffic light
light_timer = T_green  # Timer for the current light phase

# Set up the plot
fig, ax = plt.subplots(figsize=(10, 2))
ax.set_xlim(-1, N)    # X-axis from -1 to 9 for better visibility
ax.set_ylim(-1, 1)    # Y-axis fixed for a 2D view
ax.set_yticks([])     # Hide y-axis ticks since it's a 1D street
ax.set_xlabel('Street Position')
ax.set_title('Traffic Light Simulation on a One-Way Street')
ax.plot([0, N-1], [0, 0], 'k-')  # Draw the street as a black line

# Initialize plot elements
light_marker = ax.plot(L, 0, 'o', color='green', markersize=15)[0]  # Traffic light marker
cars = ax.scatter([], [], color='blue', s=50)  # Cars as scatter points

# Update function for each animation frame
def update(frame):
    global street, light_state, light_timer
    
    # Update traffic light state
    if light_state == 'green':
        if light_timer > 0:
            light_timer -= 1
        else:
            light_state = 'red'
            light_timer = T_red
            light_marker.set_color('red')
    else:  # red
        if light_timer > 0:
            light_timer -= 1
        else:
            light_state = 'green'
            light_timer = T_green
            light_marker.set_color('green')
    
    # Update car positions
    # Handle exit: remove car at the end of the street
    if street[N-1] == 1:
        street[N-1] = 0
    
    # Move cars from right to left (N-2 to 0) to avoid overwriting
    for i in range(N-2, -1, -1):
        if i < L - 1 or i >= L:  # Before or after the light
            if street[i] == 1 and street[i+1] == 0:
                street[i+1] = 1
                street[i] = 0
        elif i == L - 1:  # At the light (position 4)
            if street[i] == 1 and street[i+1] == 0 and light_state == 'green':
                street[i+1] = 1
                street[i] = 0
    
    # Add a new car at position 0 with probability p
    if random.random() < p and street[0] == 0:
        street[0] = 1
    
    # Update the scatter plot with current car positions
    car_positions = [i for i in range(N) if street[i] == 1]
    cars.set_offsets(np.c_[car_positions, [0]*len(car_positions)])
    
    return cars, light_marker

# Create the animation
ani = FuncAnimation(fig, update, frames=total_steps, interval=500, blit=True)

# Display the animation
plt.show()