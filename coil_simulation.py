"""
This script simulates the transient response of a series RLC circuit, 
modeling the discharge of a capacitor through a planar coil implemented 
on multiple printed circuit boards (PCBs). It calculates the time-dependent 
current through the coil and the resulting magnetic field.

The simulation includes two plots:
1. Magnetic Field vs. Time (in teslas)
2. Current vs. Time (in amperes)

Inputs:
- t = 2 * 0.0348 mm       # Total copper thickness for 2 oz copper traces
- w = 1.75 mm             # Width of the PCB trace
- s = 0.25 mm             # Spacing between traces
- n_series = 2            # Number of series-connected windings in the coil
- C_coil = 10e-3 F        # Capacitance of the capacitor bank
- R_mosfet = 0.01 ohms    # Resistance of the MOSFET switch
- numb_pcb = 10           # Number of stacked PCBs used in the coil

These parameters are used to determine the resistance, inductance, and 
geometrical characteristics of the coil, which affect the circuit's 
transient behavior. The results are useful for analyzing electromagnetic 
performance in magnetic pulsing.

"""


import numpy as np
import control as ct  # Ensure control library is installed (pip install control)

# Constants
p_copper = 1.7 * 1e-5  # Copper resistivity in ohm-mm
u_0 = 4 * np.pi * 1e-7  # Permeability of free space in H/m
K1 = 2.34  # Empirical constant for inductance calculation
K2 = 2.75  # Empirical constant for inductance calculation

# Variables
t = 2 * 0.0348  # Thickness for 2 oz of copper on PCB in mm
w = 1.75         # Width of trace in mm
s = 0.25         # Spacing between trace in mm
n_series = 2    # Number of series connections in the coil
C_coil = 10e-3  # Capacitance in Farads
R_mosfet = 0.01 # Resistance of the MOSFET in ohms
numb_pcb = 10   # Number of PCBs used

# Calculate the number of parallel coils
n_parallel = numb_pcb * n_series / n_series

# Coil Dimensions
d_out = 100     # Outer diameter of the coil in mm
d_in = 20       # Inner diameter of the coil in mm

# Calculate the number of turns based on coil geometry
N = (d_out - d_in) / (2 * (w + s))

# Calculate trace length for one coil (approximation based on geometry)
lengthTrace = 4 * (d_out + d_in) / 2 * (N + 1)

# Inductance calculation for the coil (using Wheeler's or similar approximation for square coils)
L_coil = (K1 * u_0 * N**2 * (d_out + d_in) / 2) / (1 + K2 * (d_out - d_in) / (d_out + d_in)) / 1000 * n_series**2
L_coil_single = (K1 * u_0 * N**2 * (d_out + d_in) / 2) / (1 + K2 * (d_out - d_in) / (d_out + d_in)) / 1000 

# Resistance calculation for the coil trace
R_coil = p_copper * lengthTrace / (w * t) * n_series / n_parallel + R_mosfet
R_coil_single = p_copper * lengthTrace / (w * t)

# Calculate inverse summation for magnetic field calculation
a_inv_sum = 0
for i in range(int(N)):
    a_inv_sum += 1000 * n_series / (100 - 2 * (w + s) * i)
print('a_inv_sum = ', a_inv_sum)

# Display calculated values
print('Inductance = ', L_coil * 1e6, 'uH')
print('Capacitance = ', C_coil * 1e6, 'uF')
print('Resistance = ', R_coil, 'Ohm')
print('Resistance (single) = ', R_coil_single, 'Ohm')
print('Number of Turns (1 coil) = ', int(N))
print('Trace Length (1 coil) = ', lengthTrace, 'mm')

# Define the state-space matrices for the system
A = np.array([[0, 1 / C_coil], [-1 / L_coil, -R_coil / L_coil]])
B = np.array([[0], [0]])
C = np.array([[0, 8 * 2**0.5 * u_0 / (4 * np.pi) * a_inv_sum]])
D = np.array([[0]])

# Create the state-space system
sysStateSpace = ct.ss(A, B, C, D)

# Define the time vector and initial conditions for simulation
timeVector3 = np.linspace(0, 0.01, 100000)
initialState = np.array([48, 0])

# Perform initial response simulation
timeReturned3, systemOutput3 = ct.initial_response(sysStateSpace, timeVector3, initialState)

# Display maximum magnetic field strength in Gauss
max_magnetic_field = max(abs(systemOutput3)) * 10000  # Convert from Tesla to Gauss
print('Peak Magnetic Field = ', max_magnetic_field, 'Gauss')

# Plot the results
plottingFunction(timeReturned3*1000, 
                 -systemOutput3, 
                 titleString='Peak Magnetic Field Create in Through Coil',
                 stringXaxis='Time [ms]', 
                 stringYaxis='Magnetic Field [T]', 
                 stringFileName='outputInitial.png')

plottingFunction(timeReturned3*1000, 
                 -systemOutput3 / (8 * 2**0.5 * u_0 / (4 * np.pi) * a_inv_sum), 
                 titleString='Current Running Through Coil',
                 stringXaxis='Time [ms]', 
                 stringYaxis='Current [A]', 
                 stringFileName='outputNormalized.png')
