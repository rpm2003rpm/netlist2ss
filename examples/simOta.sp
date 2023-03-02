G1 outpair1 cm in1 cm gmpair
G2 outpair2 cm in2 cm gmpair
V1 in1 gnd vc-vd/2
V2 in2 gnd vc+vd/2
R1 outpair1 gnd 1/gm2
C1 outpair1 gnd cp2*(1+k)
R2 outpair2 gnd 1/gm2
C2 outpair2 gnd cp2*(1+k)
G3 voutn gnd outpair1 gnd gm2
G4 voutp gnd outpair2 gnd gm2
R3 voutn gnd 1/gm3
C3 voutn gnd 2*cp3
G5 voutp gnd voutn gnd gm3
CL voutp gnd cl
RO voutp gnd 1/(gds2+gds3)
