# Netlist to space state

This program converts a spice like netlist into a state-space representation of the system. You can choose the input variables, linearize unlinear systems, calculate the dc operating point, and choose the output variables. The states are column vector taken as the voltage in the capacitors and the current in the inductos, respecting the same order in which they are included in the netlist from top to bottom.

More details and examples can be found below:

# Files

test: folder containing all the tests for the code. Type ./test/run_all.sh to run them. 

examples: sample netlists

/netlist2ss/netlist2ss.py: calculate the space space-state representation

/netlist2ss/sisotf.py: instantiate the netlist2ss package in order to compute the transfer function for a single input and single output system (the sisotf command is added when you install this package using the setup-tools)  

/netlist2ss/\_\_init\_\_.py: init file  

# Simple Example

1. Open python3 in a terminal

2. Calculate the space state matrices of 'cap_filt.sp' circuit by typing the following lines in the python interpreter

```
    from netlist2ss import netlist2ss 
    handle  = open('./examples/cap_filt.sp', 'r')
    netlist = handle.read()
    handle.close()
    A,B,C,D,OP = netlist2ss(netlist,['IN'],['VnOUT'])
```
    * ['IN'] is the list of the input variables. Input variables can be any variable used as value of a device in the netlist.
    * ['VnOUT'] list of output measurements. Use Vn<node> to mesaure the voltage in a specific node, Vd<dev> to measure de voltage across a device, and Id<dev> for the current across a device.

3. The transfer function can be calculated by running:

```
    import sympy as si
    s = si.symbols('s')
    H = si.simplify(C*((s*(si.eye(A.shape[0]))-A).inv())*B + D)[0,0]
```
# Netlist

As shown in the example, the netlist is composed of a list of devices. The interconections between the devices (the nets) can written as any valid spice net name. The keywords gnd (in any combination of up and lower case letters) and 0 means the reference potential node and they must be present at least once.  

The value of the device can be any variable name or constant. Don't use any reserved word of sympy! 

The device type is identified by its first letter. You can find a list of the supported devices below:

| type | Description                       |
| ---- | --------------------------------- |
| V    | Independent voltage source        |
| I    | Independent current source        |
| E    | Voltage controlled voltage source |
| F    | Current controlled current source |
| G    | Voltage controlled current source |
| H    | Current controlled voltage source |
| L    | Inductor                          |
| C    | Capacitor                         |
| R    | Resistor                          |
| T    | Ideal transformer                 |


# Limitations
    * capacitors can't be connected in parallel with voltage sources or in parallel with other capacitors.
    * inductors can't be connected in series with current sources or in series with other inductors.
