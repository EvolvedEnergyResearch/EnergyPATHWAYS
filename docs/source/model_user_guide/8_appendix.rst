=================================================
Appendix A: Further Model Methodology Explanation
=================================================

Stock Rollover Calculation
--------------------------

For both the “stock and service” and “stock and energy” calculation
methods, the model performs a stock rollover, in which vintaged (aged)
technology stock is decayed and replaced with new technology stock
(i.e., technology whose vintage is the current year). Stock is added
each year to meet the current year’s DemandStock.csv stock size input
(or projection), considering the decay of older stock. The three main
decay types, as specified on the technology-level in DemandTechs.csv,
include linear, exponential, and Weibull. Other relevant inputs include
the maximum and minimum lifetime (*max_lifetime* and *min­_lifetime*
columns), or (alternatively) mean lifetime and lifetime variance
(*mean_lifetime* and *lifetime_variance* columns).

Decay Type Breakdown (see shared_classes.py for decay function code):

-  linear: Up until the *min_lifetime*, there is no decay in the stock,
   making the survival probability (the fraction of original stock still
   in use) 1. From the *min_lifetime* to *max_lifetime*, the survival
   probability drops linearly each year from 1 (full survival) to 0 (no
   survival). After the *max_lifetime*, survival probability remains at
   0, indicating that no more stock of that vintage remains. If a
   *mean_lifetime* and *lifetime_variance* are inputted instead of
   maximum and minimum lifetime values, these will be used internally to
   approximate the maximum and minimum values, as per the equation
   below.

   -  :math:`minimum\ lifetime = mean\ lifetime - 2 \cdot lifetime\ {variance}^{1/2\ }`

   -  :math:`maximum\ lifetime = mean\ lifetime + 2 \cdot lifetime\ {variance}^{1/2\ }`

-  exponential: Survival probability is determined from the exponential
   decay function :math:`e^{- ct}`, where :math:`c = 1/mean\_ lifetime`
   and *t* is a time unit (e.g., year). If max and min lifetime values
   are specified rather than mean lifetime and variance, the model will
   internally approximate the mean lifetime and lifetime variance using
   the equations below.

   -  :math:`mean\ lifetime = minimum\ lifetime + \frac{maximum\ lifetime - minimum\ lifetime}{2}`

   -  :math:`lifetime\ variance = \left( \frac{maximum\ lifetime - minimum\ lifetime}{4} \right)^{2}`

-  Weibull: Survival probability is determined from the Weibull function
   :math:`e^{- \left( \frac{t}{\alpha} \right)^{\beta}}`. *t* is a time
   unit (e.g., year). :math:`\beta` is a shape parameter that determines
   the failure rate behavior over time (note: if :math:`\beta = 1`, the
   decay rate is constant (exponential decay)). :math:`\alpha` is a time
   scaling coefficient. Both coefficients are found internally using the
   mean lifetime and variance. If max and min lifetime values are
   specified rather than mean lifetime and variance, the model will
   internally approximate the mean lifetime and variance (using the same
   equations as above). This function has a longer tail, corresponding
   to small quantities of technology stock that remain in use for long
   periods of time (e.g., a small number of people still drive 30+
   vintage cars regularly).

Initial Stock Calculation
-------------------------

EnergyPATHWAYS computes an initial vintaged technology stock composition
at the start of a run. This accounts for the fact that, at the start
year of the model, not all technology is brand new. For instance, if the
current year is set to 2024, the model should not assume that all cars
on the road in 2024 began their lifetimes that year. Instead, some cars
made in 2023 will be on the road, along with others vintaged 2022, and
so on.

To compute the initial stock, EnergyPATHWAYS uses the input stock values
(in DemandStock.csv) along with technology lifetimes and decay functions
(from DemandTechs.csv). Vintage 1999 and earlier vintages of technology
are grouped together.

Pre-2000 vintage vehicles are grouped in the following manner: The model
takes the 1999 stock and evenly distributes it across "x" years before
2000. “x” can be defined differently depending on the decay function:

-  linear: :math:`x\  = \ maximum\ technology\ lifetime`

-  Weibull: :math:`x = mean\ lifetime + 10\sqrt{lifetime\ variance}`

-  exponential: :math:`x = mean\ lifetime + 10\sqrt{lifetime\ variance}`

The model then creates a single decay function such that, each year, the
decay value is equivalent to the sum of all decay of technologies
vintage (2000-x) to 1999, as per the specified decay function (linear,
exponential, or Weibull). For instance, if x = 10, the model will create
a single decay function that is the cumulative decay of all technology
vintage 1990-1999. This decay function is used for pre-2000 stock.

Each year after 2000, the model will add stock to meet the new stock
size, as specified in DemandStocks.csv (or interpolated/extrapolated
from values within), while accounting for the decay in previous years’
stock. Stock will follow the specified decay function (linear, Weibull,
or exponential) computed using the lifetime data input, as detailed in
Section :ref:`Stock Rollover Calculation`.
