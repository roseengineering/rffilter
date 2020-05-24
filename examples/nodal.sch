<Qucs Schematic 0.0.20>
<Properties>
  <View=-92,-20,1649,1025,1,0,120>
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
  <.SP SP1 1 60 160 0 65 0 0 "lin" 1 "9.7M" 1 "10.35M" 1 "401" 1 "no" 0 "1" 0 "2" 0 "no" 0 "no" 0>
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
  <Eqn Eqn1 5 250 250 -31 17 0 0 "phi11=unwrap(angle(S[1,1]))" 1 "phi21=unwrap(angle(S[2,1]))" 1 "phase=rad2deg(angle(S[1,1]))" 1 "td=-diff(phi11,2*pi*frequency)" 1 "delay=-diff(phi21,2*pi*frequency)" 1 "yes" 0>
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
  <Rect 60 857 577 477 3 #c0c0c0 1 00 1 9.7e+06 50000 1.035e+07 1 -0.0873334 0.2 1.08853 1 -1 0.2 1 315 0 225 "" "" "" "">
	<"S[2,1]" #0000ff 0 3 0 0 0>
	<"S[1,1]" #ff0000 0 3 0 0 0>
	<"delay" #ff00ff 0 3 0 0 1>
  </Rect>
  <Polar 880 315 305 305 3 #c0c0c0 1 00 1 0 1 1 1 0 0.5 1 1 0 1 1 315 0 225 "" "" "" "">
	<"S[1,1]" #0000ff 0 3 0 0 0>
	  <Mkr 9.8365e+06 240 -306 4 1 0>
  </Polar>
  <Rect 830 817 577 477 3 #c0c0c0 1 00 1 9.7e+06 50000 1.035e+07 1 -6e-05 1e-05 1.20187e-05 1 -215.642 50 214.943 315 0 225 "" "" "" "">
	<"td" #0000ff 0 3 0 0 0>
	  <Mkr 9.999e+06 348 -555 6 0 0>
  </Rect>
</Diagrams>
<Paintings>
</Paintings>
