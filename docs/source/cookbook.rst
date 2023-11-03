====================
Cookbook
====================

If you have analytic needs that go beyond selecting pre-existing measures and sensitivities as outlined above, you may wish to edit the energy system database directly. Changing the demand side of the model can be important to understanding the relative impact of technology deployment to the success (however defined) of a developed pathway. This can be a key tool in developing robustness analysis as many projections of technology development are uncertain. It can also demonstrate conditions under which demand technologies may be cost-effectively deployed and can be a key tool in competitiveness analysis.

For example, while deployment of certain technologies today may not be economic, a variety of changing conditions including those on the grid (high penetrations of renewables and the ability of flexible loads to participate) may change that equation. The ability to model technologies and anticipate their behavior on the system and economics in a variety of scenarios is one of the primary strengths of the EnergyPATHWAYS approach.



a.	Creating a new scenario
b.	Changing model geography to focus on individual states
c.	Exporting an EP case to RIO
d.	Changing technology sales assumptions to measure impact
e.	Adding fuel-switching measures in industry
f.	Adding energy-efficiency measures for a subsector without technology stocks
g.	Changing technology cost or performance characteristics
h.	Adding a reduction in service demand


Add new demand technology definition or change demand technology parameters
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This is a user decision as to whether they would like to add an entire new technology definition or would like to simply alter the parameters of one technology. For quick, one-off analyses of the importance of different technology parameters, it may make sense to simply alter a technology definition (i.e. change its capital costs) and run a case to compare the overall impact of such a technology change. When a user is interested in a wholly new technology that may behave differently than a previously input technology or differ substantively along a variety of potential definitions, then it may make more sense to input a new technology. We will walk through the steps to input a new technology understanding that the only difference for amending a technology is to edit an existing record instead of entering an entirely new one.

1. Add a new technology to the **DemandTechs** table. This will include general parameters like lifetime, associated demand subsector, usage shape (for electric technologies), as well as flexibility parameters (max delay or advance) to inform flexible load potential on the supply-side. For a full list of input parameters and description see:
2. Input efficiency parameters using **DemandTechsMainEfficiency**; **DemandTechsMainEfficiencyData**; **DemandTechsAuxEfficiency**; and **DemandTechsAuxEfficiencyData**; **DemandTechsParasiticEnergy**(Optional); **DemandTechsParasiticEnergyData**; These efficiency inputs can be in almost any unit combination that is consistent with the energy service demand specification. So, for example, if the service demand of light-duty vehicles is in vehicle miles traveled, then the efficiency parameters can be any permutation of distance and energy (ex. Miles/GGE, kilometer/GJ, etc.). **DemandTechsAuxEfficiency** is used for defining technologies that are dual-fuel. For example, plug-in hybrid electric vehicles have an efficiency entry for both the main energy type (electricity) and the auxiliary energy type (gasoline fuels). Parasitic energy is energy associated with the use of equipment unrelated to amount of service demand. So, for example, if there is standby electricity related to a furnace that exists regardless of heating demand, this would be parasitic energy.
3. Input cost parameters using **DemandTechsCapitalCosts**; **DemandTechsCapitalCostNewData**; **DemandTechsInstallationCost**; **DemandTechsInstallationCostNewData**; **DemandTechsInstallationCostReplacementData**; **DemandTechsFuelSwitchCost**; **DemandTechsFuelSwitchCostData**; **DemandTechsFixedMaintenanceCost**; **DemandTechsFixedMaintenanceCostData**. These inputs allow a user to flexibly define the cost parameters of both owning, installing, and operating demand-side equipment. Capital costs can be input for both new installation (i.e. a new gas furnace in a home) vs. replacement (replacing a gas furnace with a newer vintage on burnout). Installation costs can be input similarly.   Fuel-switching costs add additional flexibility. This cost is assessed when a technology changes from one energy type to another. For example, when a light-duty vehicle goes from a gasoline vehicle to an electric one, we can input the cost of a new home charger. As another example, when a gas water heater changes to a heat pump, we can include any additional wiring costs in this input. Fixed maintenance costs are associated with the ongoing annual operations of a piece of equipment. Tires and oil changes for light-duty vehicles would be examples of O&M costs.
