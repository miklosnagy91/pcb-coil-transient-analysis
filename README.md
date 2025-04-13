# pcb-coil-transient-analysis
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
