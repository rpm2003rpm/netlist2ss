#!/usr/local/bin/python3
#  Documentation for this module.
# 
#  @author  Rodrigo Pedroso Mendes
#  @version V1.0
#  @date    27/01/19 20:19:11
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
#  Test current sources netlist
#
################################################################################


#-------------------------------------------------------------------------------
# Mocules do import
#-------------------------------------------------------------------------------
import sympy      as     si
import sys
sys.path.append('.')
from   netlist2ss import netlist2ss

#-------------------------------------------------------------------------------
# Main
#-------------------------------------------------------------------------------
if __name__ == "__main__":

    #---------------------------------------------------------------------------
    # Read netlist 
    #---------------------------------------------------------------------------
    try:
        handle  = open("test/netlist_isrc.scs", 'r')
        netlist = handle.read()
        handle.close()
    except:
        print ("File IO Exception")
        exit(-1)

    #---------------------------------------------------------------------------
    # Run test
    #---------------------------------------------------------------------------
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

    #---------------------------------------------------------------------------
    # Pass fail
    #---------------------------------------------------------------------------
    if A.equals(A_ref):
        print ("A     matrix pass") 
    else:
        print ("A     matrix fail")   

    if B.equals(B_ref):
        print ("B     matrix pass") 
    else:
        print ("B     matrix fail")   

    if C.equals(C_ref):
        print ("C     matrix pass") 
    else:
        print ("C     matrix fail")   

    if D.equals(D_ref):
        print ("D     matrix pass") 
    else:
        print ("D     matrix fail")  

    if DC_OP.equals(DC_OP_ref):
        print ("DC_OP matrix pass") 
    else:
        print ("DC_OP matrix fail")   

    exit(0)

    exit(0)
