<Qucs Schematic 0.0.20>
<Properties>
  <View=0,0,1161,1299,1,0,20>
  <Grid=10,10,1>
  <DataSet=lowpass.dat>
  <DataDisplay=lowpass.dpl>
  <OpenDisplay=0>
  <Script=lowpass.m>
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
  <.SP SP1 1 60 160 0 65 0 0 "lin" 1 "5M" 1 "15M" 1 "401" 1 "no" 0 "1" 0 "2" 0 "no" 0 "no" 0>
  <Pac P1 1 350 160 18 -26 0 1 "1" 1 "50" 1 "0 dBm" 0 "1 GHz" 0 "26.85" 0>
  <Pac P2 1 750 150 18 -26 0 1 "2" 1 "50" 1 "0 dBm" 0 "1 GHz" 0 "26.85" 0>
  <GND * 5 750 180 0 0 0 0>
  <GND * 5 350 190 0 0 0 0>
  <GND * 5 530 150 0 0 0 0>
  <Eqn Eqn1 5 920 130 -31 17 0 0 "phi21=unwrap(angle(S[2,1]))" 1 "delay=-diff(phi21,2*pi*frequency)" 1 "yes" 0>
  <SPICE X1 1 530 120 -26 -57 0 0 "/home/george/share/github-rffilter/examples/lowpass.cir" 1 "_net1,_net4" 0 "yes" 0 "none" 0>
</Components>
<Wires>
  <560 120 750 120 "" 0 0 0 "">
  <350 120 350 130 "" 0 0 0 "">
  <350 120 500 120 "" 0 0 0 "">
</Wires>
<Diagrams>
  <Rect 300 777 577 477 3 #c0c0c0 1 00 1 5e+06 1e+06 1.5e+07 1 -0.0656125 0.2 1.09634 1 -1 0.2 1 315 0 225 "" "" "" "">
	<"S[2,1]" #0000ff 0 3 0 0 0>
	<"S[1,1]" #ff0000 0 3 0 0 0>
	<"delay" #ff00ff 0 3 0 0 1>
  </Rect>
</Diagrams>
<Paintings>
</Paintings>
