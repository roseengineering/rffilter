<Qucs Schematic 0.0.20>
<Properties>
  <View=-154,-199,1538,1014,1,20,300>
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
  <.SP SP1 1 790 -170 0 65 0 0 "lin" 1 "4M" 1 "4.00065M" 1 "401" 1 "no" 0 "1" 0 "2" 0 "no" 0 "no" 0>
  <GND * 5 730 260 0 0 0 0>
  <Pac P2 1 730 180 18 -26 0 1 "2" 1 "Z0" 1 "0 dBm" 0 "1 GHz" 0 "26.85" 0>
  <GND * 5 680 210 0 0 0 0>
  <Pac P1 1 60 170 -70 -26 1 1 "1" 1 "R1" 1 "0 dBm" 0 "1 GHz" 0 "26.85" 0>
  <GND * 5 60 220 0 0 0 0>
  <SPICE X1 1 410 210 -202 -93 0 1 "xtaltune.cir" 1 "_net1,_net4,_net5,_net8,_net9,_net12,_net13,_net16,_net17,_net20,_net21,_net24,_net25,_net28,_net29,_net32" 0 "yes" 0 "none" 0>
  <Eqn Eqn1 5 1080 -100 -31 17 0 0 "phi21=unwrap(angle(S[2,1]))" 1 "theta=angle(S[1,1])" 1 "phi11=unwrap(angle(S[1,1]))" 1 "delay=-diff(phi21,2*pi*frequency)" 1 "td=-diff(phi11,2*pi*frequency)" 1 "yes" 0>
  <R R1 2 110 140 -26 -51 0 2 "409.7" 1 "26.85" 0 "0.0" 0 "0.0" 0 "26.85" 0 "US" 0>
  <Eqn Eqn2 1 610 300 -31 16 0 0 "Z0=459.7" 1 "R1=400" 1 "TD=1.9204e-3" 1 "TDA=R1/Z0*TD" 1 "yes" 0>
</Components>
<Wires>
  <730 210 730 260 "" 0 0 0 "">
  <60 200 60 220 "" 0 0 0 "">
  <650 210 680 210 "" 0 0 0 "">
  <620 150 730 150 "" 0 0 0 "">
  <620 150 620 180 "" 0 0 0 "">
  <590 240 620 240 "" 0 0 0 "">
  <590 180 590 240 "" 0 0 0 "">
  <560 180 590 180 "" 0 0 0 "">
  <530 240 560 240 "" 0 0 0 "">
  <530 180 530 240 "" 0 0 0 "">
  <500 180 530 180 "" 0 0 0 "">
  <470 240 500 240 "" 0 0 0 "">
  <470 180 470 240 "" 0 0 0 "">
  <440 180 470 180 "" 0 0 0 "">
  <410 240 440 240 "" 0 0 0 "">
  <410 180 410 240 "" 0 0 0 "">
  <380 180 410 180 "" 0 0 0 "">
  <350 240 380 240 "" 0 0 0 "">
  <350 180 350 240 "" 0 0 0 "">
  <320 180 350 180 "" 0 0 0 "">
  <230 240 260 240 "" 0 0 0 "">
  <230 180 230 240 "" 0 0 0 "">
  <200 180 230 180 "" 0 0 0 "">
  <150 240 200 240 "" 0 0 0 "">
  <60 140 80 140 "" 0 0 0 "">
  <150 140 150 240 "" 0 0 0 "">
  <140 140 150 140 "" 0 0 0 "">
</Wires>
<Diagrams>
  <Polar 840 365 305 305 3 #c0c0c0 1 00 1 0 1 1 1 0 0.5 1 1 0 1 1 315 0 225 "" "" "" "">
	<"S[1,1]" #0000ff 0 3 0 0 0>
	  <Mkr 4.00065e+06 240 -306 4 1 0>
  </Polar>
  <Rect 800 907 577 477 3 #c0c0c0 1 00 1 4e+06 50 4.00065e+06 1 0.0005 0.0005 0.004 1 -1 0.2 1 315 0 225 "" "" "" "">
	<"td" #0000ff 0 3 0 0 0>
	  <Mkr 4.00033e+06 367 -547 3 0 0>
	<"theta" #ff0000 0 3 0 0 1>
  </Rect>
  <Rect 20 907 589 370 3 #c0c0c0 1 00 1 4e+06 50 4.00065e+06 1 -0.0999887 0.2 1.1 1 -1 0.2 1 315 0 225 "" "" "" "">
	<"S[2,1]" #0000ff 0 3 0 0 0>
	<"S[1,1]" #ff0000 0 3 0 0 0>
	<"delay" #ff00ff 0 3 0 0 1>
  </Rect>
  <Tab 1190 285 298 75 3 #c0c0c0 1 00 1 0 1 1 1 0 1 1 1 0 1 401 315 0 225 "" "" "" "">
	<"TDA" #0000ff 0 3 1 0 0>
	<"TD" #0000ff 0 3 0 0 0>
  </Tab>
</Diagrams>
<Paintings>
  <Text 0 300 12 #000000 0 "* ij        q,k           TD0           TDn           CBW           Q,K\n* 01     1.2510    1.5928e-03             -          399.6803e+00   10.0088e+03\n* 12     0.7280    1.9204e-03    7.3284e-03  364.0000e+00   90.9925e-06\n* 23     0.5450    4.4349e-03    9.9522e-03  272.5000e+00   68.1194e-06\n* 34     0.5160    4.0627e-03    6.1555e-03  258.0000e+00   64.4947e-06\n* 45     0.5100    7.3443e-03    7.3443e-03  255.0000e+00   63.7447e-06\n* 56     0.5160    6.1555e-03    4.0627e-03  258.0000e+00   64.4947e-06\n* 67     0.5450    9.9522e-03    4.4349e-03  272.5000e+00   68.1194e-06\n* 78     0.7280    7.3284e-03    1.9204e-03  364.0000e+00   90.9925e-06\n* 89     1.2510             -            1.5928e-03  399.6803e+00   10.0088e+03\n">
</Paintings>
