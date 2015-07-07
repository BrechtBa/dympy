within ;
model test
  Modelica.Thermal.HeatTransfer.Components.HeatCapacitor C1(C=10e6, T(start=
          293.15))
    annotation (Placement(transformation(extent={{-28,4},{-8,24}})));
  Modelica.Thermal.HeatTransfer.Components.HeatCapacitor C2(C=20e6, T(start=
          293.15))
    annotation (Placement(transformation(extent={{18,4},{38,24}})));
  Modelica.Thermal.HeatTransfer.Components.ThermalConductor UA12(G=1000)
    annotation (Placement(transformation(extent={{-4,-30},{16,-10}})));
  Modelica.Thermal.HeatTransfer.Components.ThermalConductor UA2T(G=500)
    annotation (Placement(transformation(extent={{40,-30},{60,-10}})));
  Modelica.Thermal.HeatTransfer.Sources.FixedTemperature fixedTemperature(T=
        283.15) annotation (Placement(transformation(
        extent={{-10,-10},{10,10}},
        rotation=180,
        origin={86,-20})));
  Modelica.Thermal.HeatTransfer.Sources.PrescribedHeatFlow prescribedHeatFlow
    annotation (Placement(transformation(extent={{-52,-30},{-32,-10}})));
  Modelica.Blocks.Interfaces.RealInput u
    annotation (Placement(transformation(extent={{-120,50},{-80,90}})));
equation
  connect(prescribedHeatFlow.port, UA12.port_a) annotation (Line(
      points={{-32,-20},{-4,-20}},
      color={191,0,0},
      smooth=Smooth.None));
  connect(C1.port, UA12.port_a) annotation (Line(
      points={{-18,4},{-18,-20},{-4,-20}},
      color={191,0,0},
      smooth=Smooth.None));
  connect(UA12.port_b, UA2T.port_a) annotation (Line(
      points={{16,-20},{40,-20}},
      color={191,0,0},
      smooth=Smooth.None));
  connect(C2.port, UA2T.port_a) annotation (Line(
      points={{28,4},{28,-20},{40,-20}},
      color={191,0,0},
      smooth=Smooth.None));
  connect(UA2T.port_b, fixedTemperature.port) annotation (Line(
      points={{60,-20},{76,-20}},
      color={191,0,0},
      smooth=Smooth.None));
  connect(u, prescribedHeatFlow.Q_flow) annotation (Line(
      points={{-100,70},{-76,70},{-76,-20},{-52,-20}},
      color={0,0,127},
      smooth=Smooth.None));
  annotation (uses(Modelica(version="3.2")), Diagram(coordinateSystem(
          preserveAspectRatio=false, extent={{-100,-100},{100,100}}), graphics));
end test;
