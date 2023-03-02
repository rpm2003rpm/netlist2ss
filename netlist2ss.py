## @package netlist2ss
# 
#  @author  Rodrigo Pedroso Mendes
#  @version V1.0
#  @date    28/01/19 11:41:38
#
#  #LICENSE# 
#    
#  Copyright (c) 2019 Rodrigo Pedroso Mendes
#
#  Permission is hereby granted, free of charge, to any  person   obtaining  a 
#  copy of this software and associated  documentation files (the "Software"), 
#  to deal in the Software without restriction, including  without  limitation 
#  the rights to use, copy, modify,  merge,  publish,  distribute, sublicense, 
#  and/or sell copies of the Software, and  to  permit  persons  to  whom  the 
#  Software is furnished to do so, subject to the following conditions:        
#   
#  The above copyright notice and this permission notice shall be included  in 
#  all copies or substantial portions of the Software.                         
#   
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,  EXPRESS OR 
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE  WARRANTIES  OF  MERCHANTABILITY, 
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE 
#  AUTHORS OR COPYRIGHT HOLDERS BE  LIABLE FOR ANY  CLAIM,  DAMAGES  OR  OTHER 
#  LIABILITY, WHETHER IN AN ACTION OF  CONTRACT, TORT  OR  OTHERWISE,  ARISING 
#  FROM, OUT OF OR IN CONNECTION  WITH  THE  SOFTWARE  OR  THE  USE  OR  OTHER  
#  DEALINGS IN THE SOFTWARE. 
#    
#  #DESCRIPTION#
#
#      This module  contains functions to convert a spice netlist into a space 
#  state representation of the system
#
################################################################################

#-------------------------------------------------------------------------------
# import necessary modules
#-------------------------------------------------------------------------------
import re
import numpy as np
import sympy as si

#-------------------------------------------------------------------------------
# Error Class
# An error will be raised whenever an internal error occurs
#-------------------------------------------------------------------------------
class Error(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

#-------------------------------------------------------------------------------
# Component Class
# This class contains basic definition of a spice component
#
# The parameters of the constructor are listed bellow:
# name:  Component name (Example: V1, R1, R2, etc)
# nodes: A list with the name of the nets in  which the component is connected 
#        (Example: ['n1', 'n2', ...])
# value: An expression retrieved  from the 'value' field of  the spice netlist
#        (Example: '1e-2*a+b'). This expression is  parsed and assumed  to  be 
#        the value of the component 
#-------------------------------------------------------------------------------
class component:

    #---------------------------------------------------------------------------
    # Constructor
    #---------------------------------------------------------------------------
    def __init__(self, name, nodes, value): 
        self.type   = name[0].upper()
        self.nodes  = nodes
        try:
            self.value = si.sympify(value)
        except:
            raise Error('Unable to parse "' + value + '"')
        self.e1Idx = None
        self.e2Idx = None
        if (self.type in 'LC'):
            self.st = si.symbols('state_var_' + name)     
        else:
            self.st = None

    #---------------------------------------------------------------------------
    # Get fixed parameters of the component
    #---------------------------------------------------------------------------
    def getType(self):
        return self.type

    def getNodes(self):
        return self.nodes

    def getValue(self):
        return self.value

    def getST(self):
        return self.st

    #---------------------------------------------------------------------------
    # Get and set the indexes in the J matrix   
    #---------------------------------------------------------------------------
    def setE1Idx(self, e1Idx):
        self.e1Idx = e1Idx

    def setE2Idx(self, e2Idx):
        self.e2Idx = e2Idx

    def getE1Idx(self):
        return self.e1Idx

    def getE2Idx(self):
        return self.e2Idx

    #---------------------------------------------------------------------------
    # String callbacks in order facilitate debugging 
    #---------------------------------------------------------------------------
    def __str__(self):
        return "< " + self.type       + ", " + str(self.nodes) + ", " + \
                      str(self.value) + ", " + str(self.e1Idx) + ", " + \
                      str(self.e2Idx) + ", " + str(self.st)    + " >"

    def __repr__(self):
        return "< " + self.type       + ", " + str(self.nodes) + ", " + \
                      str(self.value) + ", " + str(self.e1Idx) + ", " + \
                      str(self.e2Idx) + ", " + str(self.st)    + " >"

#-------------------------------------------------------------------------------
# netlistParser
# Recieves a netlist as a raw string and returns a dictionary where  the  keys 
# are the names of the components and the items are composed  of  instances of  
# the component class.
#
# -Inputs
# netlist:  A spice netlist given as a raw string
# -Outputs
# compDict: The component dictionary 
#-------------------------------------------------------------------------------
def netlistParser(netlist):
    #Regex patterns
    patternEmptyLines = r"^[ \t]*$|^[ \t]*\*.*"
    pattern2tDevices  = r"^[ \t]*([VvIiLlRrCc][A-Za-z0-9_]*)[ \t]+" + \
                        r"([A-Za-z0-9_]+)[ \t]+" + \
                        r"([A-Za-z0-9_]+)[ \t]+" + \
                        r"([A-Za-z0-9+*/() -]+)[ \t]*(;.*)?$"
    pattern4tDevices  = r"^[ \t]*([EeHhGgFfTt][A-Za-z0-9_]*)[ \t]+"   + \
                        r"([A-Za-z0-9_]+)[ \t]+" + \
                        r"([A-Za-z0-9_]+)[ \t]+" + \
                        r"([A-Za-z0-9_]+)[ \t]+" + \
                        r"([A-Za-z0-9_]+)[ \t]+" + \
                        r"([A-Za-z0-9+*/() -]+)[ \t]*(;.*)?$"
    #Split the netlist in lines and fillout the component dictionary
    compDict = {}
    compList = []
    lineList = re.findall("(.*)\n*", netlist)
    for line in lineList:
        #Remove empty line and comment
        if(re.search(patternEmptyLines, line)):
            continue
        #Find 2 terminal devices
        elif(re.search(pattern2tDevices, line)):
            compDesc = re.findall(pattern2tDevices, line)[0]
            if compDesc[0] in compDict.keys():
                raise Error(compDesc[0] + ": Duplicated device.")
            compDict[compDesc[0]] = component(compDesc[0],               \
                                              [compDesc[1],compDesc[2]], \
                                              compDesc[3])
            compList.append(compDict[compDesc[0]])
        #Find 4 terminal devices
        elif(re.search(pattern4tDevices, line)):
            compDesc = re.findall(pattern4tDevices, line)[0]
            if compDesc[0] in compDict.keys():
                raise Error(compDesc[0] + ": Duplicated device.")
            compDict[compDesc[0]] = component(compDesc[0],      \
                                    [compDesc[1], compDesc[2],  \
                                     compDesc[3],compDesc[4]],  \
                                    compDesc[5])
            compList.append(compDict[compDesc[0]])
        #Invalid line
        else:
            raise Error("Error when processing the line \"" + line +
                        "\". Unsuported device, net name or device  value")

    return (compDict, compList)

#-------------------------------------------------------------------------------
# calcNodesnJ
# Calculate the size of the J matrix in the nodal analysis, update the indexes
# that each component ocupies in the J matrix,  and transforms the  net  names 
# in a sequence of integer that represents the node number.
#
# -Inputs
# compDict:  The component dictionary generated by the netlistParser
# -Outputs
# nJ:        Size of the J matrix
# nNodes:    Number of nodes in the nodal analysis
# nodesDict: Dictionary corelating the net name with the node number
#
# This function also updates the J matrix index of each afected  component  in
# the component list  
#-------------------------------------------------------------------------------
def calcNodesnJ(compList):
    nJ         = 0
    nNodes     = 0
    nodesDict  = {}
    #Loop trough all components 
    for comp in compList:
        #Independent  voltage  sources, voltage   controled  voltage  sources, 
        #current controled current sources, and capacitors
        if comp.getType() in 'VFEC':
            comp.setE1Idx(nJ)
            nJ = nJ + 1
        #Current controled voltage sources 
        elif comp.getType() in 'HT':
            comp.setE1Idx(nJ)
            nJ = nJ + 1
            comp.setE2Idx(nJ)
            nJ = nJ + 1
        #Loop trough all nodes
        for node in comp.getNodes():
            if not (node in nodesDict.keys()):
                if (node.upper() == 'GND' or node == '0'):
                    nodesDict[node] = -1
                else:
                    nodesDict[node] = nNodes   
                    nNodes = nNodes + 1
    return (nJ, nNodes, nodesDict) 

#-------------------------------------------------------------------------------
# nodalAnalysisMatrices
# Construct the nodal analysis matrices
#
# -Inputs
# compDict:  The component dictionary generated by the netlistParser
# nJ:        Size of the J matrix
# nNodes:    Number of nodes in the nodal analysis
# nodesDict: Dictionary corelating the net name with the node number 
# -Outputs:
# A: The A matrix is a concatenation of the G, B, C, and D matrices
# Z: Z is a column vector which is the concatenation of I and E matrices
#-------------------------------------------------------------------------------
def nodalAnalysisMatrices(compList, nJ, nNodes, nodesDict):

    #---------------------------------------------------------------------------
    # Alocate matrices
    #---------------------------------------------------------------------------
    G = si.zeros(nNodes, nNodes)
    I = si.zeros(nNodes, 1)
    if nJ != 0:
        B = si.zeros(nNodes, nJ)
        C = si.zeros(nJ, nNodes)
        D = si.zeros(nJ, nJ)
        E = si.zeros(nJ, 1)

    #---------------------------------------------------------------------------
    # Loop trough all components 
    #---------------------------------------------------------------------------
    for comp in compList:

        #-----------------------------------------------------------------------
        # Read nodes and J matrix indexes
        #-----------------------------------------------------------------------
        nodes = comp.getNodes()
        n1 = nodesDict[nodes[0]]
        n2 = nodesDict[nodes[1]] 
        if len(nodes) > 2:
            n3 = nodesDict[nodes[2]]
            n4 = nodesDict[nodes[3]] 
        e1 = comp.getE1Idx()
        e2 = comp.getE2Idx()

        #-----------------------------------------------------------------------
        # fill the G matrix with resistors from the netlist
        #-----------------------------------------------------------------------
        if comp.getType() == 'R':
            #If  neither  side  of  the element is  connected  to  ground then 
            #subtract it from appropriate location in matrix.
            if n1 != -1 and n2 != -1:
                G[n1, n2] = G[n1, n2] - 1/comp.getValue()
                G[n2, n1] = G[n2, n1] - 1/comp.getValue()
            #If node 1 is not connected to ground, add element to  diagonal of 
            #matrix
            if n1 != -1:
                G[n1, n1] = G[n1, n1] + 1/comp.getValue()
            #Ditto for node 2.
            if n2 != -1:
                G[n2, n2] = G[n2, n2] + 1/comp.getValue()

        #-----------------------------------------------------------------------
        # fill the G  matrix  with  voltage  controled  current  sources  from 
        # netlist
        #-----------------------------------------------------------------------
        elif comp.getType() == 'G':
            #If neither n1 and n3 is  connected  to  ground  then  sum  it  to 
            #appropriate location in matrix.
            if n1 != -1 and n3 != -1:
                G[n1, n3] = G[n1, n3] + comp.getValue()
            #If neither n1 and n4 is connected to ground then subtract it from
            #appropriate location in matrix.
            if n1 != -1 and n4 != -1:
                G[n1, n4] = G[n1, n4] - comp.getValue()
            #If neither n2 and n3 is connected to ground then subtract it from
            #appropriate location in matrix.
            if n2 != -1 and n3 != -1:
                G[n2, n3] = G[n2, n3] - comp.getValue()
            #If neither n2 and  n4  is  connected to ground  then  sum  it  to 
            #appropriate location in matrix.
            if n2 != -1 and n4 != -1:
                G[n2, n4] = G[n2, n4] + comp.getValue()

        #-----------------------------------------------------------------------
        # fill the I matrix with independent  current  sources  and  inductors 
        # from the netlist.
        #-----------------------------------------------------------------------
        elif comp.getType() in 'I':
            #Check if node 1 is connected to ground, then subtract the current 
            #in the correct location in the matrix 
            if n1 != -1:
                I[n1] = I[n1] - comp.getValue()
            #Check if node 2 is  connected to ground, then sum the  current in
            #the correct location in the matrix 
            if n2 != -1:
                I[n2] = I[n2] + comp.getValue()
        
        #-----------------------------------------------------------------------
        # fill the I matrix with inductors from the netlist.
        # In order to calculate the space  state matrices, we solve  the nodal 
        # analysis system as a function of the inductor current (which is  one
        # of the states), and then calculate  the voltage across the inductor, 
        # which will give us the derivative of the current.
        #-----------------------------------------------------------------------
        elif comp.getType() in 'L':
            #Check if node 1 is connected to ground, then subtract the current
            #in the correct location in the matrix 
            if n1 != -1:
                I[n1] = I[n1] - comp.getST()
            #Check if node 2  is  connected to ground, then sum the current in 
            #the correct location in the matrix 
            if n2 != -1:
                I[n2] = I[n2] + comp.getST()

        #-----------------------------------------------------------------------
        # Fill the C  and  B  matrices  with  independent voltage  sources and 
        # capacitors from the netlist.
        #-----------------------------------------------------------------------
        elif comp.getType() in 'V':
            #Check if node 1 is connected to ground, then fill-out the B and C 
            #matrix
            if n1 != -1:  
                B[n1, e1] = 1      
                C[e1, n1] = 1 
            #Check if node 2 is connected to ground, then fill-out the B and C
            #matrix
            if n2 != -1:  
                B[n2, e1] = -1     
                C[e1, n2] = -1
            #E matrix
            E[e1] = comp.getValue()

        #-----------------------------------------------------------------------
        # Fill the C and B matrices with capacitors from the netlist.
        # In order to calculate the space state  matrices, we solve the  nodal
        # analysis system as a function of the capacitor voltage (which is one 
        # of the states), and then calculate the current through the capacitor 
        # which will give us the derivative of the voltage
        #-----------------------------------------------------------------------
        elif comp.getType() in 'C':
            #Check if node 1 is connected to ground, then fill-out the B and C 
            #matrix
            if n1 != -1:  
                B[n1, e1] = 1      
                C[e1, n1] = 1 
            #Check if node 2 is connected to ground, then fill-out the B and C
            #matrix
            if n2 != -1:  
                B[n2, e1] = -1     
                C[e1, n2] = -1
            #E matrix
            E[e1] = comp.getST()

        #-----------------------------------------------------------------------
        # Fill the B and C matrices with  voltage controlled  voltage  sources
        #-----------------------------------------------------------------------
        elif comp.getType() in 'E':
            #Check if node 1 is connected to ground, then fill-out the B and C 
            #matrix
            if n1 != -1:  
                B[n1, e1] = 1      
                C[e1, n1] = 1 
            #Check if node 2 is connected to ground, then fill-out the B and C
            #matrix
            if n2 != -1:  
                B[n2, e1] = -1     
                C[e1, n2] = -1
            #Check if node 3  is  connected  to  ground, then  fill-out  the C 
            #matrix
            if n3 != -1:      
                C[e1, n3] = -comp.getValue()
            #Check if node 4  is  connected  to  ground, then fill-out  the  C 
            #matrix
            if n4 != -1:      
                C[e1, n4] = comp.getValue()

        #-----------------------------------------------------------------------
        # Fill the B and C matrices  with current controlled  current  sources
        #-----------------------------------------------------------------------
        elif comp.getType() in 'F':
            #Check if node 1  is  connected  to  ground, then fill-out  the  B
            #matrix
            if n1 != -1:  
                B[n1, e1] = comp.getValue() 
            #Check if node 2  is  connected  to  ground, then fill-out  the  B
            #matrix
            if n2 != -1:  
                B[n2, e1] = -comp.getValue()
            #Check if ctrl 1  is  connected  to  ground, then fill-out  the  B
            #and C matrix
            if n3 != -1:   
                B[n3, e1] = 1   
                C[e1, n3] = 1
            #Check if ctrl 2  is  connected  to  ground, then fill-out  the  B
            #and C matrix
            if n4 != -1:   
                B[n4, e1] = -1   
                C[e1, n4] = -1

        #-----------------------------------------------------------------------
        # Fill the B and C matrices with current  controlled  voltage  sources 
        #-----------------------------------------------------------------------
        elif comp.getType() in 'H':
            #Check if node 1 is connected to ground, then fill-out the B and C
            #matrix
            if n1 != -1:  
                B[n1, e2] = 1
                C[e1, n1] = 1
            #Check if node 2 is connected to ground, then fill-out the B and C
            #matrix
            if n2 != -1:  
                B[n2, e2] = -1
                C[e1, n2] = -1
            #Check if node 3 is connected to ground, then fill-out the B and C
            #matrix
            if n3 != -1:   
                B[n3, e1] = 1   
                C[e2, n3] = 1
            #Check if node 4 is connected to ground, then fill-out the B and C
            #matrix
            if n4 != -1:   
                B[n4, e1] = -1   
                C[e2, n4] = -1
            #D matrix
            D[e1, e1] = -comp.getValue()

        #-----------------------------------------------------------------------
        # Ideal transformer 
        #-----------------------------------------------------------------------
        elif comp.getType() in 'T':
            #Check if node 1 is connected to ground, then fill-out the B and C
            #matrix
            if n1 != -1:  
                B[n1, e1] = 1
                C[e2, n1] = -comp.getValue()
            #Check if node 2 is connected to ground, then fill-out the B and C
            #matrix
            if n2 != -1:  
                B[n2, e1] = -1
                C[e2, n2] = comp.getValue()
            #Check if node 3 is connected to ground, then fill-out the B and C
            #matrix
            if n3 != -1:   
                B[n3, e2] = 1   
                C[e2, n3] = 1
            #Check if node 4 is connected to ground, then fill-out the B and C
            #matrix
            if n4 != -1:   
                B[n4, e2] = -1   
                C[e2, n4] = -1
            #D matrix
            D[e1, e2] = comp.getValue()
            D[e1, e1] = 1

    #---------------------------------------------------------------------------
    # Calculate the A and Z matrices 
    #---------------------------------------------------------------------------
    if nJ != 0:
        A = (G.row_join(B)).col_join(C.row_join(D))
        Z = I.col_join(E)
    else:
        A = G
        Z = I

    return (A, Z)  

#-------------------------------------------------------------------------------
# solveSystem
# Solve the symbolic nodal analysis system 
#
# -Inputs
# A:      The A matrix is a concatenation of the G, B, C, and D matrices
# Z:      Z is a column vector which is the concatenation of I and E  matrices
# nNodes: Number of nodes in the nodal analysis
# -Outputs
# V:      The V matrix contains the voltage in all nodes of the system
# J:      The J matrix contains the current flowing trough  current  controled 
#         current  sources,  current   controled   voltage   sources,  voltage 
#         controled  voltage   sources,   independent   voltage   source,  and 
#         capacitors
#-------------------------------------------------------------------------------
def solveSystem(A, Z, nNodes):
    try:
        X = A.inv()*Z
    except: 
        raise Error('Unable to solve the linear system. Check the netlist')
    V = X[0:nNodes, 0]
    J = X[nNodes: , 0]
    V = V.col_join(si.zeros(1, 1))
    return (V, J)

#-------------------------------------------------------------------------------
# stateEquations
# Returns a vector listing all the states and a vector containing  the  set of 
# equations for each state
#
# -Inputs
# compDict:  The component dictionary generated by the netlistParser
# nodesDict: Dictionary corelating the net name with the node number 
# V: The V matrix contains the voltage in all nodes of the system
# J: The J matrix  contains  the  current  flowing  trough  current  controled 
#    current sources, current controled  voltage  sources,  voltage  controled  
#    voltage sources, independent voltage source, and capacitors
# -Outputs
# X: column vector listing all states
# F: column vector with a equation for each state
#-------------------------------------------------------------------------------
def stateEquations (compList, nodesDict, V, J):

    #---------------------------------------------------------------------------
    # Initialize variables 
    #---------------------------------------------------------------------------
    X   = []
    F   = []
    nST = 0

    #---------------------------------------------------------------------------
    # Loop trough all components 
    #---------------------------------------------------------------------------
    for comp in compList:
        #Inductor corresponds to one state
        if comp.getType() == 'L': 
            nodes = comp.getNodes()   
            F.append((V[nodesDict[nodes[0]]] - V[nodesDict[nodes[1]]])/ \
                     comp.getValue())
            X.append(comp.getST())
            nST = nST + 1
        #Capacitor corresponds to another state
        elif comp.getType() == 'C':
            F.append(J[comp.getE1Idx()]/comp.getValue())
            X.append(comp.getST())
            nST = nST + 1

    #---------------------------------------------------------------------------
    # reshape the output
    #---------------------------------------------------------------------------
    F = si.Matrix(nST, 1, F)
    X = si.Matrix(nST, 1, X)

    return (X, F)

#-------------------------------------------------------------------------------
# parseOutputs
# Build output equations
#
# -Inputs
# compDict:  The component dictionary generated by the netlistParser
# nodesDict: Dictionary corelating the net name with the node number 
# V: The V matrix contains the voltage in all nodes of the system
# J: The J matrix  contains  the  current  flowing  trough  current  controled 
#    current sources, current controled  voltage  sources,  voltage  controled  
#    voltage sources, independent voltage source, and capacitors
# outputs: A list containing the desired measurements from  which  the  output
#          equations will be built 
# -Outputs
# G : A column vector containing the set of output equations
#-------------------------------------------------------------------------------
def parseOutputs (compDict, nodesDict, V, J, outputs):

    #---------------------------------------------------------------------------
    # Alocate space 
    #---------------------------------------------------------------------------
    G = si.zeros(len(outputs), 1)

    #---------------------------------------------------------------------------
    # Loop trough all outputs      
    #---------------------------------------------------------------------------
    for i in range(0, len(outputs)):
        meas = outputs[i][0:2]
        name = outputs[i][2:]

        #-----------------------------------------------------------------------
        # Node voltage measurement
        #-----------------------------------------------------------------------
        if meas == 'Vn':
            if not name in nodesDict.keys():
                raise Error("Node " + name + " doesn't exist")
            G[i] = V[nodesDict[name]]

        #-----------------------------------------------------------------------
        # Device related measurements
        #-----------------------------------------------------------------------
        else:
            #Check if the device exists in the device list
            if not name in compDict.keys():
                raise Error("Device " + name + " doesn't exist")
            #Get device type and nodes
            compType = compDict[name].getType() 
            if compType == 'T':
                print("Warning: Measurements for transformer weren't implemented. Skipping")
                continue
            nodes    = compDict[name].getNodes()
            n1 = nodesDict[nodes[0]]
            n2 = nodesDict[nodes[1]] 
            if len(nodes) > 2:
                n3 = nodesDict[nodes[2]]
                n4 = nodesDict[nodes[3]]
            #Get the J matrix indexes
            e1 = compDict[name].getE1Idx() 
            e2 = compDict[name].getE2Idx() 
            #Get component value 
            value = compDict[name].getValue()
            #Get state name
            st = compDict[name].getST()
 
            #-------------------------------------------------------------------
            # Measurement of the voltage across a device 
            #-------------------------------------------------------------------
            if meas == 'Vd':  
                if   compType == 'C': 
                    G[i] = st 
                elif compType in 'HFEGIRL': 
                    G[i] = V[n1] - V[n2]     
                elif compType == 'V':
                    G[i] = value
 
            #-------------------------------------------------------------------
            # Measurement of the current flowing in a device
            #-------------------------------------------------------------------
            elif meas == 'Id': 
                if   compType == 'L': 
                    G[i] = st 
                elif compType in 'CVE': 
                    G[i] = J[e1]   
                elif compType == 'H': 
                    G[i] = J[e2]  
                elif compType == 'F': 
                    G[i] = J[e1]*value
                elif compType == 'I':
                    G[i] = value 
                elif compType == 'R': 
                    G[i] = (V[n1] - V[n2])/value
                elif compType == 'G': 
                    G[i] = (V[n3] - V[n4])*value

            #-------------------------------------------------------------------
            # Measurement  of  the  voltage   across  the  control  nodes of a 
            # dependent source
            #-------------------------------------------------------------------        
            elif meas == 'Vc': 
                if not compType in 'EFGH': 
                    raise Error("There isn't control pins in " + name)
                if compType in 'FH': 
                    G[i] = 0
                elif compType in 'EG': 
                    G[i] = V[n3] - V[n4]

            #-------------------------------------------------------------------
            # Measurement  of  the  current  across  the  control   nodes of a 
            # dependent source
            #-------------------------------------------------------------------  
            elif meas == 'Ic': 
                if not compType in 'EFGH': 
                    raise Error("There isn't control pins in " + name)
                if compType in 'EG': 
                    G[i] = 0
                elif compType == 'F': 
                    G[i] = J[e1]  
                elif compType == 'H':
                    G[i] = J[e1] 

            #-------------------------------------------------------------------
            # Unknown measurement tyoe
            #-------------------------------------------------------------------  
            else:
                raise Error("Unknown measuring type: " + meas)
    return G

#-------------------------------------------------------------------------------
# parseInputs
# build input equations
# 
# -Inputs 
# inputs: a list containing the name of variables consired to be the inputs of
#         the system
# -Output
# U: column vector listing all inputs of the system
#-------------------------------------------------------------------------------
def parseInputs (inputs):
    U = si.Matrix(len(inputs), 1, si.sympify(inputs)) 
    return U

#-------------------------------------------------------------------------------
# calcABCD
# Calculate A, B, C, D, and DC_OP matrices
#
# -Inputs
# F: column vector with a equation for each state
# X: column vector listing all states
# G: column vector containing the set of output equations 
# U: column vector listing all inputs of the system
# -Outputs
# A: state matrix
# B: input matrix
# C: output matrix
# D: feedforward matrix
# DC_OP: operating point
#-------------------------------------------------------------------------------
def calcABCD (F, X, G, U):
    #Calculate the state at the operating point
    nST  = len(X)
    sol  = si.solve(F, X)
    #dummy fix for the empty solution case
    if sol == [] and nST != 0:
        raise Error("The isn't a single solution. Check the netlist.")
    for stVar in X:
        if not stVar in sol.keys():
            raise Error("The isn't a single solution. Check the netlist.")
    X_OP = si.Matrix(nST, 1, [sol[X[i]] for i in range(0, nST)])
    #Linearized system (if the system is not linear) at the operating point 
    A = F.jacobian(X).subs([ (X[i], X_OP[i]) for i in range(0, nST) ])
    A = si.simplify(A)
    B = F.jacobian(U).subs([ (X[i], X_OP[i]) for i in range(0, nST) ])
    B = si.simplify(B)
    C = G.jacobian(X).subs([ (X[i], X_OP[i]) for i in range(0, nST) ])
    C = si.simplify(C)
    D = G.jacobian(U).subs([ (X[i], X_OP[i]) for i in range(0, nST) ])
    D = si.simplify(D)
    #Calculate the outputs of the system at the operating point
    DC_OP = G.subs([ (X[i], X_OP[i]) for i in range(0, nST) ])
    DC_OP = si.simplify(DC_OP)
    return (A, B, C, D, DC_OP)
       
#-------------------------------------------------------------------------------
# netlist2ss
# Convert a netlist to a space state representation of the system.
#  
# -Inputs
# netlist:  A string with a spice netlist
# inputs:   a list containing the name of variables consired to be the  inputs 
#           of the system
# outputs:  A list containing the desired measurements from  which  the output
#           equations will be built 
# -Outputs
# A: state matrix
# B: input matrix
# C: output matrix
# D: feedforward matrix
# DC_OP: operating point   
#
# -example: 
# (A, B, C, D, OP) = netlist2ss("e1 n1 gnd in\nr1 n1 c1 r1\n 
#                                c1 c1 gnd c1", ["in"], ["Vnc1"])
#-------------------------------------------------------------------------------
def netlist2ss(netlist, inputs, outputs):
    #Parse netlist
    (compDict, compList) = netlistParser(netlist)
    #Calculate the number of nodes and the size of the J matrix
    (nJ, nNodes, nodesDict) = calcNodesnJ(compList)
    #Build the nodal analysis matrices
    (A, Z) = nodalAnalysisMatrices(compList, nJ, nNodes, nodesDict)
    #Solve the linear system
    (V, J) = solveSystem(A, Z, nNodes)
    #Select which one of the nodal analysis results are state equations
    (X, F) = stateEquations (compList, nodesDict, V, J)
    #Select which one of the nodal analysis results are output equations 
    G = parseOutputs (compDict, nodesDict, V, J, outputs)
    #Input variables
    U = parseInputs (inputs)
    #Return the space state representation of the system
    return calcABCD (F, X, G, U)
