#!/bin/bash
###
#
# file    run_all.sh
# author  Rodrigo Pedroso Mendes
# version V1.0
# date    30/01/19 20:33:30
# brief   run all testes
# 
# Copyright (c) 2019 Rodrigo Pedroso Mendes
#
# Permission is hereby granted, free of charge, to any  person   obtaining  a 
# copy of this software and associated  documentation files (the "Software"), 
# to deal in the Software without restriction, including  without  limitation 
# the rights to use, copy, modify,  merge,  publish,  distribute, sublicense, 
# and/or sell copies of the Software, and  to  permit  persons  to  whom  the 
# Software is furnished to do so, subject to the following conditions:        
# 
# The above copyright notice and this permission notice shall be included  in 
# all copies or substantial portions of the Software.                         
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,  EXPRESS OR 
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE  WARRANTIES  OF  MERCHANTABILITY, 
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE 
# AUTHORS OR COPYRIGHT HOLDERS BE  LIABLE FOR ANY  CLAIM,  DAMAGES  OR  OTHER 
# LIABILITY, WHETHER IN AN ACTION OF  CONTRACT, TORT  OR  OTHERWISE,  ARISING 
# FROM, OUT OF OR IN CONNECTION  WITH  THE  SOFTWARE  OR  THE  USE  OR  OTHER 
# DEALINGS IN THE SOFTWARE. 
# 
################################################################################

#-------------------------------------------------------------------------------
# Run all tests
#-------------------------------------------------------------------------------
DIR=$(dirname $0)
echo "-------------------------------------";
for filename in $DIR/*.py; do
    echo "Running test $filename"
    python3 $filename;
    echo "-------------------------------------";
done
