<Qucs Schematic 0.0.20>
<Properties>
  <View=-92,-199,1497,998,1,0,277>
  <Grid=10,10,1>
  <DataSet=xtaltune.dat>
  <DataDisplay=xtaltune.dpl>
  <OpenDisplay=0>
  <Script=xtaltune.m>
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
  <.DC DC1 1 40 -80 0 40 0 0 "26.85" 0 "0.001" 0 "1 pA" 0 "1 uV" 0 "no" 0 "150" 0 "no" 0 "none" 0 "CroutLU" 0>
  <.SP SP1 1 790 -170 0 65 0 0 "lin" 1 "4M" 1 "4.0008M" 1 "401" 1 "no" 0 "1" 0 "2" 0 "no" 0 "no" 0>
  <GND * 5 730 260 0 0 0 0>
  <Pac P2 1 730 180 18 -26 0 1 "2" 1 "459.7" 1 "0 dBm" 0 "1 GHz" 0 "26.85" 0>
  <GND * 5 680 210 0 0 0 0>
  <SPICE X1 1 410 210 -202 -93 0 1 "xtaltune.cir" 1 "_net1,_net4,_net5,_net8,_net9,_net12,_net13,_net16,_net17,_net20,_net21,_net24,_net25,_net28,_net29,_net32" 0 "yes" 0 "none" 0>
  <Pac P1 1 60 170 -70 -26 1 1 "1" 1 "459.7" 1 "0 dBm" 0 "1 GHz" 0 "26.85" 0>
  <GND * 5 60 220 0 0 0 0>
  <Eqn Eqn1 5 1080 -100 -31 17 0 0 "phi21=unwrap(angle(S[1,1]))" 1 "phase=rad2deg(angle(S[1,1]))" 1 "delay=-diff(phi21,2*pi*frequency)" 1 "yes" 0>
</Components>
<Wires>
  <730 210 730 260 "" 0 0 0 "">
  <620 150 620 180 "" 0 0 0 "">
  <620 150 730 150 "" 0 0 0 "">
  <650 210 680 210 "" 0 0 0 "">
  <150 240 200 240 "" 0 0 0 "">
  <150 140 150 240 "" 0 0 0 "">
  <60 200 60 220 "" 0 0 0 "">
  <200 180 230 180 "" 0 0 0 "">
  <230 180 230 240 "" 0 0 0 "">
  <230 240 260 240 "" 0 0 0 "">
  <260 180 290 180 "" 0 0 0 "">
  <290 180 290 240 "" 0 0 0 "">
  <290 240 320 240 "" 0 0 0 "">
  <60 140 150 140 "" 0 0 0 "">
  <320 180 350 180 "" 0 0 0 "">
  <350 180 350 240 "" 0 0 0 "">
  <350 240 380 240 "" 0 0 0 "">
  <380 180 410 180 "" 0 0 0 "">
  <410 180 410 240 "" 0 0 0 "">
  <410 240 440 240 "" 0 0 0 "">
  <440 180 470 180 "" 0 0 0 "">
  <470 180 470 240 "" 0 0 0 "">
  <470 240 500 240 "" 0 0 0 "">
  <500 180 530 180 "" 0 0 0 "">
  <530 180 530 240 "" 0 0 0 "">
  <530 240 560 240 "" 0 0 0 "">
  <560 180 590 180 "" 0 0 0 "">
  <590 180 590 240 "" 0 0 0 "">
  <590 240 620 240 "" 0 0 0 "">
</Wires>
<Diagrams>
  <Rect 60 857 577 477 3 #c0c0c0 1 00 1 4e+06 100 4.0008e+06 1 0.0003 1 1 1 -1 0.2 1 315 0 225 "" "" "" "">
	<"S[2,1]" #0000ff 0 3 0 0 0>
	<"S[1,1]" #ff0000 0 3 0 0 0>
  </Rect>
  <Polar 910 345 305 305 3 #c0c0c0 1 00 1 0 1 1 1 0 0.5 1 1 0 1 1 315 0 225 "" "" "" "">
	<"S[1,1]" #0000ff 0 3 0 0 0>
	  <Mkr 4.0008e+06 240 -306 4 1 0>
  </Polar>
  <Rect 750 887 577 477 3 #c0c0c0 1 00 1 4e+06 100 4.0008e+06 1 -1 0.2 1 1 -215.453 50 213.915 315 0 225 "" "" "" "">
	<"delay" #0000ff 0 3 0 0 0>
	  <Mkr 4.00033e+06 14 -458 8 0 0>
	<"phase" #ff0000 0 3 0 0 1>
  </Rect>
</Diagrams>
<Paintings>
</Paintings>
