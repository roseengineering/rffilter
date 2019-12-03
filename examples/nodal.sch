<Qucs Schematic 0.0.20>
<Properties>
  <View=-92,-47,1497,1385,1,36,67>
  <Grid=10,10,1>
  <DataSet=nodal.dat>
  <DataDisplay=nodal.dpl>
  <OpenDisplay=0>
  <Script=nodal.m>
  <RunScript=0>
  <showFrame=0>
  <FrameText0=Title>
  <FrameText1=Drawn By:>
  <FrameText2=Date:>
  <FrameText3=Revision:>
</Properties>
<Symbol>
  <.ID -20 -16 SUB>
  <Line -20 20 40 0 #000080 2 1>
  <Line 20 20 0 -40 #000080 2 1>
  <Line -20 -20 40 0 #000080 2 1>
  <Line -20 20 0 -40 #000080 2 1>
</Symbol>
<Components>
  <.DC DC1 1 50 70 0 40 0 0 "26.85" 0 "0.001" 0 "1 pA" 0 "1 uV" 0 "no" 0 "150" 0 "no" 0 "none" 0 "CroutLU" 0>
  <.SP SP1 1 60 160 0 65 0 0 "lin" 1 "9.5M" 1 "10.5M" 1 "401" 1 "no" 0 "1" 0 "2" 0 "no" 0 "no" 0>
  <GND * 5 750 180 0 0 0 0>
  <GND * 5 530 210 0 0 0 0>
  <GND * 5 0 0 0 0 0 0>
  <GND * 4 460 120 0 0 0 0>
  <GND * 4 610 120 0 0 0 0>
  <GND * 4 610 70 0 0 0 0>
  <SPICE X1 1 530 120 -26 -117 0 0 "nodal.cir" 1 "_net1,_net2,_net3,_net4,_net5" 0 "yes" 0 "none" 0>
  <Pac P2 1 750 100 18 -26 0 1 "2" 1 "50" 1 "0 dBm" 0 "1 GHz" 0 "26.85" 0>
  <Pac P1 1 360 100 18 -26 0 1 "1" 1 "50" 1 "0 dBm" 0 "1 GHz" 0 "26.85" 0>
  <GND * 5 360 130 0 0 0 0>
  <Eqn Eqn1 5 250 250 -31 17 0 0 "phi21=unwrap(angle(S[1,1]))" 1 "phase=angle(S[1,1])" 1 "delay_ms=-diff(phi21,2*pi*frequency)" 1 "yes" 0>
  <Eqn Eqn2 5 570 270 -31 16 0 0 "mag=2*dB(max(abs(S[1,1]))/abs(S[1,1]))" 1 "dummy=dB(2)" 1 "yes" 0>
</Components>
<Wires>
  <450 240 680 240 "" 0 0 0 "">
  <450 180 450 240 "" 0 0 0 "">
  <450 180 500 180 "" 0 0 0 "">
  <460 120 500 120 "" 0 0 0 "">
  <560 120 610 120 "" 0 0 0 "">
  <610 60 610 70 "" 0 0 0 "">
  <560 60 610 60 "" 0 0 0 "">
  <750 130 750 180 "" 0 0 0 "">
  <680 70 680 240 "" 0 0 0 "">
  <680 70 750 70 "" 0 0 0 "">
  <360 60 500 60 "" 0 0 0 "">
  <360 60 360 70 "" 0 0 0 "">
</Wires>
<Diagrams>
  <Rect 60 857 577 477 3 #c0c0c0 1 00 1 0 1e+06 1.05e+07 1 0.983544 0.002 0.996838 1 0 2 20 315 0 225 "" "" "" "">
	<"S[2,1]" #0000ff 0 3 0 0 0>
	<"S[1,1]" #ff0000 0 3 0 0 0>
	<"mag" #ff00ff 0 3 0 0 1>
  </Rect>
  <Rect 740 847 577 477 3 #c0c0c0 1 00 1 9.5e+06 100000 1.05e+07 1 -4.14403e-05 5e-06 1e-05 1 -1 0.2 1 315 0 225 "" "" "" "">
	<"delay_ms" #0000ff 0 3 0 0 0>
	  <Mkr 1e+07 -46 -348 3 0 0>
	<"phase" #ff0000 0 3 0 0 1>
	  <Mkr 1.03325e+07 447 -432 4 0 0>
  </Rect>
  <Polar 910 345 305 305 3 #c0c0c0 1 00 1 0 1 1 1 0 0.5 1 1 0 1 1 315 0 225 "" "" "" "">
	<"S[1,1]" #0000ff 0 3 0 0 0>
	  <Mkr 9.685e+06 240 -306 4 1 0>
  </Polar>
</Diagrams>
<Paintings>
</Paintings>
