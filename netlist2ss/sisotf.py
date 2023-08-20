#!/usr/bin/python3
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
#  Calculate the transfer function the circuit represented by a netlist
#
################################################################################


#-------------------------------------------------------------------------------
# Mocules do import
#-------------------------------------------------------------------------------
import sys
from   netlist2ss import netlist2ss
import sympy as  si

#-------------------------------------------------------------------------------
# CLI
#-------------------------------------------------------------------------------
def cli():
    #---------------------------------------------------------------------------
    # Check Arguments 
    #---------------------------------------------------------------------------
    if (len(sys.argv) != 4):
        print ('Usage:')
        print ('    ' + sys.argv[0] + \
               ' filename input_variable output_measurement') 
        exit(-1)
    
    #---------------------------------------------------------------------------
    # Read netlist 
    #---------------------------------------------------------------------------
    try:
        handle  = open(sys.argv[1], 'r')
        netlist = handle.read()
        handle.close()
    except:
        print ("File IO Exception")
        exit(-1)

    #---------------------------------------------------------------------------
    # Run netlist2ss and calculate the transfer function
    #---------------------------------------------------------------------------
    s = si.symbols('s')
    try:
        (A, B, C, D, DC_OP) = netlist2ss(netlist, [sys.argv[2]], [sys.argv[3]])
    except Exception as e:
        print("Error: " + str(e))
        exit(-1)
    H = si.simplify(C*((s*(si.eye(A.shape[0]))-A).inv())*B + D)[0,0]
    n, d = si.fraction(H)   

    #---------------------------------------------------------------------------
    # Print result
    #---------------------------------------------------------------------------
    n = str(n)                        
    d = str(d)
    sizen = len(n)
    sized = len(d)
    sizet = max(sizen, sized) + 2 
    print(" ") 
    print(" Transfer function of " + sys.argv[1])
    print(" Input variable: "  + sys.argv[2]) 
    print(" Output variable: " + sys.argv[3][0:2] + "(" + sys.argv[3][2:] + ")")
    print(" ") 
    print("        " + " "*round((sizet - sizen)/2) + n) 
    print(" H(s) = " + "-"*sizet)
    print("        " + " "*round((sizet - sized)/2) + d) 
    print(" ") 

    exit(0)
    
    
#-------------------------------------------------------------------------------
# Main
#-------------------------------------------------------------------------------
if __name__ == "__main__":
    cli()
