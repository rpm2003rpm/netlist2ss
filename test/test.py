## @package test
# 
#  @author  Rodrigo Pedroso Mendes
#  @version V1.0
#  @date    24/02/23 01:05:02
#
#  #LICENSE# 
#    
#  Copyright (c) 2023 Rodrigo Pedroso Mendes
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
################################################################################
import unittest
import sympy as si
from netlist2ss import netlist2ss


class Test(unittest.TestCase):

    ############################################################################
    # Resistor
    ############################################################################
    def testRES(self):
        netlist = ("R1 GND N1  R1\n"
                   "R2 N2  GND R2\n"
                   "R3 N1  N3  R3\n"
                   "I1 N2  N3  I1\n")
        #Define symbols
        R1  = si.simplify('R1')
        R2  = si.simplify('R2')
        R3  = si.simplify('R3')
        I1  = si.simplify('I1')
        #Reference Matrices
        A_ref = si.Matrix(0, 0, [])
        A_ref = si.simplify(A_ref)

        B_ref = si.Matrix(0, 1, [])
        B_ref = si.simplify(B_ref)

        C_ref = si.Matrix(6, 0, [])
        C_ref = si.simplify(C_ref)

        D_ref = si.Matrix([[-R1], \
                           [-R2], \
                           [-R3], \
                           [-1],  \
                           [-1],  \
                           [-1] ])
        D_ref = si.simplify(D_ref)

        DC_OP_ref = si.Matrix([[-R1*I1], \
                               [-R2*I1], \
                               [-R3*I1], \
                               [-I1],    \
                               [-I1],    \
                               [-I1] ])    
        DC_OP_ref = si.simplify(DC_OP_ref)
        # Run test  
        (A, B, C, D, DC_OP) = netlist2ss( netlist, ['I1'], \
                              ['VdR1','VdR2','VdR3','IdR1','IdR2','IdR3'] )
        #Asserts
        self.assertTrue(A.equals(A_ref))
        self.assertTrue(B.equals(B_ref))
        self.assertTrue(C.equals(C_ref))
        self.assertTrue(D.equals(D_ref))
        self.assertTrue(DC_OP.equals(DC_OP_ref))                          
                                                                 
    ############################################################################
    # VSRC
    ############################################################################
    def testVSRC(self):
        netlist = ("R1 N1 N2  R1\n"
                   "R2 N2 GND R2\n"
                   "V1 N1 GND V1\n"
                   "R3 N3 GND R3\n"
                   "V2 N3 N4  V2\n"
                   "R4 N4 GND R4 \n"
                   "R5 N5 N6  R5\n"
                   "R6 N6 GND R6\n"
                   "V3 GND N5 V3\n")
        #Define symbols
        R1  = si.simplify('R1')
        R2  = si.simplify('R2')
        R3  = si.simplify('R3')
        R4  = si.simplify('R4')
        R5  = si.simplify('R5')
        R6  = si.simplify('R6')
        V1  = si.simplify('V1')
        V2  = si.simplify('V2')
        V3  = si.simplify('V3')
        #Reference Matrices
        A_ref = si.Matrix(0, 0, [])
        A_ref = si.simplify(A_ref)

        B_ref = si.Matrix(0, 3, [])
        B_ref = si.simplify(B_ref)

        C_ref = si.Matrix(6, 0, [])
        C_ref = si.simplify(C_ref)

        D_ref = si.Matrix([[            1,            0,            0], \
                           [            0,            1,            0], \
                           [            0,            0,            1], \
                           [ -1/(R1 + R2),            0,            0], \
                           [            0, -1/(R3 + R4),            0], \
                           [            0,            0, -1/(R5 + R6)]])
        D_ref = si.simplify(D_ref)

        DC_OP_ref = si.Matrix([[ V1 ], \
                               [ V2 ], \
                               [ V3 ], \
                               [ -V1/(R1 + R2) ], \
                               [ -V2/(R3 + R4) ], \
                               [ -V3/(R5 + R6) ]])
        DC_OP_ref = si.simplify(DC_OP_ref)
        # Run test  
        (A, B, C, D, DC_OP) = netlist2ss( netlist, ['V1', 'V2', 'V3'], \
                              ['VdV1','VdV2','VdV3','IdV1','IdV2','IdV3'] )


        #Asserts
        self.assertTrue(A.equals(A_ref))
        self.assertTrue(B.equals(B_ref))
        self.assertTrue(C.equals(C_ref))
        self.assertTrue(D.equals(D_ref))
        self.assertTrue(DC_OP.equals(DC_OP_ref))

    ############################################################################
    # ISRC
    ############################################################################
    def testISRC(self):
        netlist = ("R1 N1 N2 R1\n"
                   "R2 N2 GND R2\n"
                   "I1 N1 GND I1\n"
                   "R3 N3 GND R3\n"
                   "I2 N3 N4 I2\n"
                   "R4 N4 GND R4 \n"
                   "R5 N5 N6 R5\n"
                   "R6 N6 GND R6\n"
                   "I3 GND N5 I3\n")
        #Define symbols
        R1  = si.simplify('R1')
        R2  = si.simplify('R2')
        R3  = si.simplify('R3')
        R4  = si.simplify('R4')
        R5  = si.simplify('R5')
        R6  = si.simplify('R6')
        I1  = si.simplify('I1')
        I2  = si.simplify('I2')
        I3  = si.simplify('I3')
        #Reference Matrices
        A_ref = si.Matrix(0, 0, [])
        A_ref = si.simplify(A_ref)

        B_ref = si.Matrix(0, 3, [])
        B_ref = si.simplify(B_ref)

        C_ref = si.Matrix(6, 0, [])
        C_ref = si.simplify(C_ref)

        D_ref = si.Matrix([[ -R1 -R2,        0,       0], \
                           [        0, -R3 -R4,       0], \
                           [        0,       0, -R5 -R6], \
                           [        1,       0,       0], \
                           [        0,       1,       0], \
                           [        0,       0,       1]])
        D_ref = si.simplify(D_ref)

        DC_OP_ref = si.Matrix([[ -I1*(R1 + R2)], \
                               [ -I2*(R3 + R4)], \
                               [ -I3*(R5 + R6)], \
                               [ I1 ], \
                               [ I2 ], \
                               [ I3 ]])
        DC_OP_ref = si.simplify(DC_OP_ref)
        # Run test  
        (A, B, C, D, DC_OP) = netlist2ss( netlist, ['I1', 'I2', 'I3'], \
                              ['VdI1','VdI2','VdI3','IdI1','IdI2','IdI3'] )


        #Asserts
        self.assertTrue(A.equals(A_ref))
        self.assertTrue(B.equals(B_ref))
        self.assertTrue(C.equals(C_ref))
        self.assertTrue(D.equals(D_ref))
        self.assertTrue(DC_OP.equals(DC_OP_ref))    
    
    ############################################################################
    # Capacitor
    ############################################################################
    def testCAP(self):
        netlist = ("VIN N1  GND VIN\n"
                   "R1  N1  N2  R1\n"
                   "C1  N2  GND C1\n"
                   "R2  N1  N3  R2\n"
                   "C2  GND N3  C2\n"
                   "C3  N1  N4  C3\n"
                   "R3  N4  GND R3\n")
        
        #Define symbols
        R1  = si.simplify('R1')
        R2  = si.simplify('R2')
        R3  = si.simplify('R3')
        C1  = si.simplify('C1')
        C2  = si.simplify('C2')
        C3  = si.simplify('C3')
        VIN = si.simplify('VIN')
        
        #Reference Matrices
        A_ref = si.Matrix([[-1/(R1*C1),          0,          0], \
                           [         0, -1/(R2*C2),          0], \
                           [         0,          0, -1/(R3*C3)]])
        A_ref = si.simplify(A_ref)

        B_ref = si.Matrix([[ 1/(R1*C1)], \
                           [-1/(R2*C2)], \
                           [ 1/(R3*C3)]])
        B_ref = si.simplify(B_ref)
    
        C_ref = si.Matrix([[-1/R1,     0,     0], \
                           [    1,     0,     0], \
                           [    0, -1/R2,     0], \
                           [    0,     1,     0], \
                           [    0,     0, -1/R3], \
                           [    0,     0,     1]])
        C_ref = si.simplify(C_ref)
    
        D_ref = si.Matrix([[ 1/R1], \
                           [    0], \
                           [-1/R2], \
                           [    0], \
                           [ 1/R3], \
                           [    0]])
        D_ref = si.simplify(D_ref)

        DC_OP_ref = si.Matrix([[   0], \
                               [ VIN], \
                               [   0], \
                               [-VIN], \
                               [   0], \
                               [ VIN]])
        DC_OP_ref = si.simplify(DC_OP_ref)
        # Run test  
        (A, B, C, D, DC_OP) = netlist2ss( netlist, ['VIN'], \
                              ['IdC1','VdC1','IdC2','VdC2','IdC3','VdC3'] )

        #Asserts
        self.assertTrue(A.equals(A_ref))
        self.assertTrue(B.equals(B_ref))
        self.assertTrue(C.equals(C_ref))
        self.assertTrue(D.equals(D_ref))
        self.assertTrue(DC_OP.equals(DC_OP_ref))
                    
    ############################################################################
    # Current controlled current source
    ############################################################################
    def testCCCS(self):
        netlist = ("I1 N1  GND I1\n"
                   "I2 N2  GND I2\n"
                   "I3 N1a N2a I1\n"
                   "I4 N2a N1a I2\n"
                   "I5 N1b N2b I1\n"
                   "I6 N2b N1b I2\n"
                   "I7 N1c N2c I1\n"
                   "I8 N2c N1c I2\n"
                   "Ra N2a GND 1\n"
                   "Rb N2b GND 1\n"
                   "Rc N2c GND 1\n"
                   "F1 N3  GND N1   GND F1\n"
                   "F2 N4  GND GND  N2  F2\n"
                   "F3 N5  GND N1a  N2a F3\n"
                   "F4 GND N6  N1b  N2b F4\n"
                   "F5 N7  N8  N1c  N2c F5\n"
                   "R1 N3  GND R1\n"
                   "R2 N4  GND R2\n"
                   "R3 N5  GND R3\n"
                   "R4 N6  GND R4\n"
                   "R5 N7  N8  R5\n"
                   "R6 N8  GND R6")
        
        #Define symbols
        F1  = si.simplify('F1')
        F2  = si.simplify('F2')
        F3  = si.simplify('F3')
        F4  = si.simplify('F4')
        F5  = si.simplify('F5')
        R1  = si.simplify('R1')
        R2  = si.simplify('R2')
        R3  = si.simplify('R3')
        R4  = si.simplify('R4')
        R5  = si.simplify('R5')
        I1  = si.simplify('I1')
        I2  = si.simplify('I2')

        #Reference Matrices
        A_ref = si.Matrix(0, 0, [])
        A_ref = si.simplify(A_ref)

        B_ref = si.Matrix(0, 2, [])
        B_ref = si.simplify(B_ref)

        C_ref = si.Matrix(6, 0, [])
        C_ref = si.simplify(C_ref)

        D_ref = si.Matrix([[  F1*R1,      0], \
                           [      0, -F2*R2], \
                           [  F3*R3, -F3*R3], \
                           [ -F4*R4,  F4*R4], \
                           [  F5*R5, -F5*R5], \
                           [    -F5,     F5]])
        D_ref = si.simplify(D_ref)

        DC_OP_ref = si.Matrix([[  I1*F1*R1 ],       \
                               [ -I2*F2*R2 ],       \
                               [ (I1 - I2)*F3*R3 ], \
                               [ (I2 - I1)*F4*R4 ], \
                               [ (I1 - I2)*F5*R5 ], \
                               [ (I2 - I1)*F5    ]])
        DC_OP_ref = si.simplify(DC_OP_ref)

        # Run test  
        (A, B, C, D, DC_OP) = netlist2ss( netlist, ['I1', 'I2'], \
                              ['VdF1','VdF2','VnN5','VnN6','VdF5','IdF5'] )


        #Asserts
        self.assertTrue(A.equals(A_ref))
        self.assertTrue(B.equals(B_ref))
        self.assertTrue(C.equals(C_ref))
        self.assertTrue(D.equals(D_ref))
        self.assertTrue(DC_OP.equals(DC_OP_ref))

    ############################################################################
    # Inductor
    ############################################################################
    def testIND(self):
        netlist = ("I1  N1  GND IIN\n"
                   "R1  N1  GND R1\n"
                   "L1  N1  GND L1\n"
                   "I2  N2  GND IIN\n"
                   "R2  N2  GND R2\n"
                   "L2  GND N2  L2\n")
        #Define symbols
        R1  = si.simplify('R1')
        R2  = si.simplify('R2')
        R3  = si.simplify('R3')
        L1  = si.simplify('L1')
        L2  = si.simplify('L2')
        L3  = si.simplify('L3')
        IIN = si.simplify('IIN')
        #Reference Matrices
        A_ref = si.Matrix([[-R1/L1,      0], \
                           [     0, -R2/L2] ])
        A_ref = si.simplify(A_ref)

        B_ref = si.Matrix([[-R1/L1], \
                           [ R2/L2] ])
        B_ref = si.simplify(B_ref)

        C_ref = si.Matrix([[-R1,   0], \
                           [  1,   0], \
                           [  0, -R2], \
                           [  0,   1] ])
        C_ref = si.simplify(C_ref)

        D_ref = si.Matrix([[-R1], \
                           [  0], \
                           [ R2], \
                           [  0] ])
        D_ref = si.simplify(D_ref)

        DC_OP_ref = si.Matrix([[   0], \
                               [-IIN], \
                               [   0], \
                               [ IIN] ])
        DC_OP_ref = si.simplify(DC_OP_ref)
        # Run test  
        (A, B, C, D, DC_OP) = netlist2ss( netlist, ['IIN'], \
                              ['VdL1','IdL1','VdL2','IdL2'] )


        #Asserts
        self.assertTrue(A.equals(A_ref))
        self.assertTrue(B.equals(B_ref))
        self.assertTrue(C.equals(C_ref))
        self.assertTrue(D.equals(D_ref))
        self.assertTrue(DC_OP.equals(DC_OP_ref))

    ############################################################################
    # Voltage controlled voltage source
    ############################################################################
    def testVCVS(self):
        netlist = ("V1 N1  GND V1\n"
                   "V2 N2  GND V2\n"
                   "E1 N3  GND N1   GND EA\n"
                   "E2 N4  GND GND  N2  EB\n"
                   "E3 N5  GND N1   N2  EC\n"
                   "E4 GND N6  N1   N2  ED\n"
                   "E5 N7  N8  N1   N2  EE\n"
                   "R1 N3  GND R1\n"
                   "R2 N4  GND R2\n"
                   "R3 N5  GND R3\n"
                   "R4 N6  GND R4\n"
                   "R5 N7  N8  R5\n"
                   "R6 N8  GND R6\n")
        #Define symbols
        E1  = si.simplify('EA')
        E2  = si.simplify('EB')
        E3  = si.simplify('EC')
        E4  = si.simplify('ED')
        E5  = si.simplify('EE')
        R5  = si.simplify('R5')
        V1  = si.simplify('V1')
        V2  = si.simplify('V2')

        #Reference Matrices
        A_ref = si.Matrix(0, 0, [])
        A_ref = si.simplify(A_ref)

        B_ref = si.Matrix(0, 2, [])
        B_ref = si.simplify(B_ref)

        C_ref = si.Matrix(6, 0, [])
        C_ref = si.simplify(C_ref)

        D_ref = si.Matrix([[     E1,     0], \
                           [      0,   -E2], \
                           [     E3,   -E3], \
                           [    -E4,    E4], \
                           [     E5,   -E5], \
                           [ -E5/R5, E5/R5]])
        D_ref = si.simplify(D_ref)

        DC_OP_ref = si.Matrix([[  V1*E1          ], \
                               [ -V2*E2          ], \
                               [ (V1 - V2)*E3    ], \
                               [ (V2 - V1)*E4    ], \
                               [ (V1 - V2)*E5    ], \
                               [ (V2 - V1)*E5/R5 ]])
        DC_OP_ref = si.simplify(DC_OP_ref)
        # Run test  
        (A, B, C, D, DC_OP) = netlist2ss( netlist, ['V1', 'V2'], \
                              ['VdE1','VdE2','VnN5','VnN6','VdE5','IdE5'] )


        #Asserts
        self.assertTrue(A.equals(A_ref))
        self.assertTrue(B.equals(B_ref))
        self.assertTrue(C.equals(C_ref))
        self.assertTrue(D.equals(D_ref))
        self.assertTrue(DC_OP.equals(DC_OP_ref))

    ############################################################################
    # Ideal transformer
    ############################################################################
    def testTRAFO(self):
        netlist = ("V1 N1  GND V1\n"
                   "R1 N1  N2  R1\n"
                   "T1 N2  GND N3 GND Beta\n"
                   "R2 N3  GND R2")
        #Define symbols
        Beta  = si.simplify('Beta')
        R2     = si.simplify('R2')
        R1     = si.simplify('R1')
        V1     = si.simplify('V1')

        #Reference Matrices
        A_ref = si.Matrix(0, 0, [])
        A_ref = si.simplify(A_ref)

        B_ref = si.Matrix(0, 1, [])
        B_ref = si.simplify(B_ref)

        C_ref = si.Matrix(3, 0, [])
        C_ref = si.simplify(C_ref)

        D_ref = si.Matrix([[0], \
                           [(1-R1/(R2/(Beta*Beta) + R1))*Beta], \
                           [1/(R2/(Beta*Beta) + R1)/Beta]])
        D_ref = si.simplify(D_ref)

        DC_OP_ref = si.Matrix([[0], \
                               [(1-R1/(R2/(Beta*Beta) + R1))*Beta*V1], \
                               [V1/(R2/(Beta*Beta) + R1)/Beta]])

        DC_OP_ref = si.simplify(DC_OP_ref)
        # Run test  

        (A, B, C, D, DC_OP) = netlist2ss( netlist, ['V1'], ['IdT1', 'VnN3', 'IdR2'] )


        #Asserts
        self.assertTrue(A.equals(A_ref))
        self.assertTrue(B.equals(B_ref))
        self.assertTrue(C.equals(C_ref))
        self.assertTrue(D.equals(D_ref))
        self.assertTrue(DC_OP.equals(DC_OP_ref))

    ############################################################################
    # Current controlled voltage source
    ############################################################################
    def testCCVS(self):
        netlist = ("I1 N1  GND I1\n"
                   "I2 N2  GND I2\n"
                   "I3 N1a N2a I1\n"
                   "I4 N2a N1a I2\n"
                   "I5 N1b N2b I1\n"
                   "I6 N2b N1b I2\n"
                   "I7 N1c N2c I1\n"
                   "I8 N2c N1c I2\n"
                   "Ra N2a GND 1\n"
                   "Rb N2b GND 1\n"
                   "Rc N2c GND 1\n"
                   "H1 N3  GND N1   GND  H1\n"
                   "H2 N4  GND GND  N2   H2\n"
                   "H3 N5  GND N1a  N2a  H3\n"
                   "H4 GND N6  N1b  N2b  H4\n"
                   "H5 N7  N8  N1c  N2c  H5\n"
                   "R1 N3  GND R1\n"
                   "R2 N4  GND R2\n"
                   "R3 N5  GND R3\n"
                   "R4 N6  GND R4\n"
                   "R5 N7  N8  R5\n"
                   "R6 N8  GND R6\n")
        #Define symbols
        H1  = si.simplify('H1')
        H2  = si.simplify('H2')
        H3  = si.simplify('H3')
        H4  = si.simplify('H4')
        H5  = si.simplify('H5')
        R5  = si.simplify('R5')
        I1  = si.simplify('I1')
        I2  = si.simplify('I2')

        #Reference Matrices
        A_ref = si.Matrix(0, 0, [])
        A_ref = si.simplify(A_ref)

        B_ref = si.Matrix(0, 2, [])
        B_ref = si.simplify(B_ref)

        C_ref = si.Matrix(6, 0, [])
        C_ref = si.simplify(C_ref)

        D_ref = si.Matrix([[    -H1,      0], \
                           [      0,     H2], \
                           [    -H3,     H3], \
                           [     H4,    -H4], \
                           [    -H5,     H5], \
                           [  H5/R5, -H5/R5]])
        D_ref = si.simplify(D_ref)

        DC_OP_ref = si.Matrix([[ -I1*H1 ],       \
                               [  I2*H2 ],       \
                               [ (I2 - I1)*H3    ], \
                               [ (I1 - I2)*H4    ], \
                               [ (I2 - I1)*H5    ], \
                               [ (I1 - I2)*H5/R5 ]])
        DC_OP_ref = si.simplify(DC_OP_ref)
        # Run test  
        (A, B, C, D, DC_OP) = netlist2ss( netlist, ['I1', 'I2'], \
                              ['VdH1','VdH2','VnN5','VnN6','VdH5','IdH5'] )


        #Asserts
        self.assertTrue(A.equals(A_ref))
        self.assertTrue(B.equals(B_ref))
        self.assertTrue(C.equals(C_ref))
        self.assertTrue(D.equals(D_ref))
        self.assertTrue(DC_OP.equals(DC_OP_ref))

    ############################################################################
    # voltage controlled current source
    ############################################################################
    def testVCCS(self):
        netlist = ("V1 N1  GND V1\n"
                   "V2 N2  GND V2\n"
                   "G1 N3  GND N1   GND G1\n"
                   "G2 N4  GND GND  N2  G2\n"
                   "G3 N5  GND N1   N2  G3\n"
                   "G4 GND N6  N1   N2  G4\n"
                   "G5 N7  N8  N1   N2  G5\n"
                   "R1 N3  GND R1\n"
                   "R2 N4  GND R2\n"
                   "R3 N5  GND R3\n"
                   "R4 N6  GND R4\n"
                   "R5 N7  N8  R5\n"
                   "R6 N8  GND R6\n")
        #Define symbols
        G1  = si.simplify('G1')
        G2  = si.simplify('G2')
        G3  = si.simplify('G3')
        G4  = si.simplify('G4')
        G5  = si.simplify('G5')
        R1  = si.simplify('R1')
        R2  = si.simplify('R2')
        R3  = si.simplify('R3')
        R4  = si.simplify('R4')
        R5  = si.simplify('R5')
        V1  = si.simplify('V1')
        V2  = si.simplify('V2')

        #Reference Matrices
        A_ref = si.Matrix(0, 0, [])
        A_ref = si.simplify(A_ref)

        B_ref = si.Matrix(0, 2, [])
        B_ref = si.simplify(B_ref)

        C_ref = si.Matrix(6, 0, [])
        C_ref = si.simplify(C_ref)

        D_ref = si.Matrix([[ -G1*R1,      0], \
                           [      0,  G2*R2], \
                           [ -G3*R3,  G3*R3], \
                           [  G4*R4, -G4*R4], \
                           [ -G5*R5,  G5*R5], \
                           [     G5,    -G5]])
        D_ref = si.simplify(D_ref)

        DC_OP_ref = si.Matrix([[ -V1*G1*R1 ], \
                               [  V2*G2*R2 ], \
                               [ (V2 - V1)*G3*R3 ], \
                               [ (V1 - V2)*G4*R4 ], \
                               [ (V2 - V1)*G5*R5 ], \
                               [ (V1 - V2)*G5    ]])
        DC_OP_ref = si.simplify(DC_OP_ref)
        # Run test  
        (A, B, C, D, DC_OP) = netlist2ss( netlist, ['V1', 'V2'], \
                              ['VdG1','VdG2','VnN5','VnN6','VdG5','IdG5'] )


        #Asserts
        self.assertTrue(A.equals(A_ref))
        self.assertTrue(B.equals(B_ref))
        self.assertTrue(C.equals(C_ref))
        self.assertTrue(D.equals(D_ref))
        self.assertTrue(DC_OP.equals(DC_OP_ref))
        
        
                                                                                                                                                     
if __name__ == '__main__':
    unittest.main()
    

