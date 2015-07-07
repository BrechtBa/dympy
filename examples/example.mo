within ;
model example
  Modelica.Thermal.HeatTransfer.Components.HeatCapacitor C_em(C=1) annotation (
      Placement(transformation(
        extent={{-10,-10},{10,10}},
        rotation=180,
        origin={-30,-26})));
  Modelica.Thermal.HeatTransfer.Components.HeatCapacitor C_in(C=1) annotation (
      Placement(transformation(
        extent={{-10,-10},{10,10}},
        rotation=180,
        origin={10,-26})));
  Modelica.Thermal.HeatTransfer.Components.ThermalConductor UA_em_in(G=1)
    annotation (Placement(transformation(extent={{-20,-10},{0,10}})));
  Modelica.Thermal.HeatTransfer.Components.ThermalConductor UA_in_amb(G=1)
    annotation (Placement(transformation(extent={{20,-10},{40,10}})));
  Modelica.Thermal.HeatTransfer.Sources.PrescribedTemperature
    prescribedTemperature_amb annotation (Placement(transformation(
        extent={{-10,-10},{10,10}},
        rotation=180,
        origin={70,0})));
  Modelica.Thermal.HeatTransfer.Sources.PrescribedHeatFlow
    prescribedHeatFlow_hp annotation (Placement(transformation(
        extent={{-10,-10},{10,10}},
        rotation=270,
        origin={-58,30})));
  Modelica.Blocks.Interfaces.RealInput Q_flow_hp
    annotation (Placement(transformation(extent={{-120,30},{-80,70}})));
  Modelica.Blocks.Interfaces.RealInput T_amb annotation (Placement(
        transformation(
        extent={{-20,-20},{20,20}},
        rotation=270,
        origin={50,100})));
  Modelica.Blocks.Interfaces.RealInput Q_flow_sol annotation (Placement(
        transformation(
        extent={{-20,-20},{20,20}},
        rotation=270,
        origin={10,100})));
  Modelica.Thermal.HeatTransfer.Sources.PrescribedHeatFlow
    prescribedHeatFlow_sol annotation (Placement(transformation(
        extent={{-10,-10},{10,10}},
        rotation=270,
        origin={10,30})));
equation
  connect(UA_in_amb.port_b, prescribedTemperature_amb.port)
    annotation (Line(points={{40,0},{60,0}}, color={191,0,0}));
  connect(UA_in_amb.port_a, C_in.port)
    annotation (Line(points={{20,0},{10,0},{10,-16}}, color={191,0,0}));
  connect(UA_em_in.port_b, C_in.port)
    annotation (Line(points={{0,0},{10,0},{10,-16}}, color={191,0,0}));
  connect(UA_em_in.port_a, C_em.port)
    annotation (Line(points={{-20,0},{-30,0},{-30,-16}}, color={191,0,0}));
  connect(prescribedHeatFlow_hp.port, C_em.port) annotation (Line(points={{-58,
          20},{-58,0},{-30,0},{-30,-16}}, color={191,0,0}));
  connect(prescribedHeatFlow_sol.port, C_in.port)
    annotation (Line(points={{10,20},{10,-16}}, color={191,0,0}));
  connect(Q_flow_hp, prescribedHeatFlow_hp.Q_flow)
    annotation (Line(points={{-100,50},{-58,50},{-58,40}}, color={0,0,127}));
  connect(Q_flow_sol, prescribedHeatFlow_sol.Q_flow) annotation (Line(points={{
          10,100},{10,100},{10,40},{10,40}}, color={0,0,127}));
  connect(T_amb, prescribedTemperature_amb.T) annotation (Line(points={{50,100},
          {50,100},{50,46},{88,46},{88,0},{82,0}}, color={0,0,127}));
  annotation (uses(Modelica(version="3.2.1")), Diagram(coordinateSystem(
          preserveAspectRatio=false, extent={{-100,-100},{100,100}})));
end example;
