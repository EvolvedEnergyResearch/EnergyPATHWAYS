============
Introduction
============

The EnergyPATHWAYS model is a comprehensive energy accounting and analysis framework specifically designed to examine large-scale energy system transformations. It represents service demands, energy demands, stocks of energy consuming technologies, and how these might change under different assumed energy futures. EnergyPATHWAYS projects subsector energy demands based on explicit user decisions about technology adoption (e.g. electric vehicle adoption) and activity levels (e.g. reduced VMTs). 

User Guide Outline
==================
This document is meant to provide a basic guide for a new user  the EnergyPATHWAYS model. The focus is on the practical questions of how to install the model, create new scenarios, and run the model. Model methodology is discussed along the way because this understanding will make you a better user of the tool; however, this document is not meant to be a guide for developers.

Today the EnergyPATHWAYS model is maintained by Evolved Energy Research and is primarily used internally. This version of EnergyPATHWAYS focuses on the demand-side of the energy system and is designed to work in conjunction with the RIO model.

From a software design perspective, we have chosen flexibility and extensibility over simplicity, when creating EnergyPATHWAYS. This has proved to be the right trade-off internally because code changes can be minimized when pursuing new research questions; however, it does mean that the learning curve can be steep for new users. The EnergyPATHWAYS model is not warrantied in anyway, and it would be accurate to say that the code is in perpetual beta. It is likely, if you use the tool for long enough, that you will encounter new bugs or new edge cases that we did not anticipate. With this in mind, please bring a critical eye to outputs. We use the same process of output interrogation internally to catch issues and are always happy to either verify or fix a set of runs.

Purpose
=======

EnergyPATHWAYS is the offspring of an analytical approach that has already proven to be a successful strategy to dramatically change the climate policy discussion at the global, national, and subnational levels. The basic insight is that climate policy was stuck in the realm of short-term, incremental changes discussed in abstract and academic terms, and that this failure was reinforced by the analysis and modeling approaches used. The pathways strategy was to force the policy and business worlds to address, head on, the reality that achieving Paris compliant scenarios requires transformation, not incrementalism; that only a long-term perspective on the kind of infrastructure and technology changes required can prevent short-term investments that result in high-emissions lock-in; and that only an analysis that moves past the abstract focus on tons of CO2 along an emissions trajectory to a focus on the energy supply and end use equipment that produces the CO2 would speak to practical decision-makers in the regulatory, business, and investment worlds.

The value of this modeling is in building a cohesive, internally consistent story with the granularity to engage all parties involved in climate mitigation. Too often we jump straight to mechanisms for achieving climate mitigation (Ex. carbon price) without paying attention to what exactly these policies need to achieve. EnergyPATHWAYS is not a forecasting tool, but instead uses a backcasting approach--starting first with a goal and then working to demonstrate what physical infrastructure changes are required to reach that goal and when those changes must happen. This scenario approach allows the model to easily perform “what if” analysis and to reflect the underlying physics of our energy system with sufficient granularity for effective communication.

History
==========

The earliest form of this model was an Excel tool developed to support the analysis of California’s Global Warming Solutions Act of 2006 (AB 32). Subsequent analyses for California and the U.S. required advances in modeling capabilities, resulting in later versions being developed in Analytica, and at the time named the PATHWAYS model and developed at the company Energy and Environmental Economics (E3). The desire to create a more flexible platform that could be used at multiple jurisdictional levels and in a variety of energy system contexts encouraged the development of a new platform, renamed EnergyPATHWAYS, and written in Python.

Modeling Approach
=================

Top-down Versus Bottom-up
-------------------------

Whole economy energy models generally follow one of two types of modeling approaches: “top-down” or “bottom-up”. Top-down energy models focus on the macro-economy and balance supply and demand across all economic sectors. These models will sometimes use a stylistic representation of technologies. By contrast, bottom-up energy models contain richer characterizations of technology cost and performance, and technology change depends on the availability and ability of technologies to substitute for each other.

Older versions of EnergyPATHWAYS covered both demand- and supply-side outputs; however, the latest version of EnergyPATHWAYS is designed work in conjunction with the RIO model for supply side modeling.

One approach is not necessarily superior to the other but depends on the type of research question being asked. But, we believe that bottom-up energy models, which track physical flows of energy and their infrastructure, are the best suited to answer the question “How exactly do we decarbonize the energy system?”

Exploration Versus Optimization
-------------------------------

Many bottom-up energy models are optimization-based. By contrast, EnergyPATHWAYS incorporates an accounting framework that allows users to construct demand-side energy infrastructure scenarios by specifying decisions. In other words, EnergyPATHWAYS is a scenario planning tool which allows users to “simulate” the consequences of specific decisions as energy infrastructure evolves over time.

We believe that an enormous amount of the value from modeling deep decarbonization pathways comes from learning through experimenting, which is only possible when decisions are put in the hands of the modeler. It is a truism to say that all models are wrong. Economy-wide energy models are also complex, with energyPATHWAYS being no exception, and therefore become a black box to many users. Black box optimization models give a provisional “answer”, but make the underlying dynamics difficult to see, obscuring their most valuable insights. It is our hope that users find EnergyPATHWAYS to be a refreshingly transparent way of exploring demand-side pathways.