# Bush encroachment

All code necessary to reproduce the analysis of "Livestock management promotes bush encroachment in savanna systems by altering plant-herbivore feedback"  Oikos 2023.3 (2023): e09462 (https://doi.org/10.1111/oik.09462). 

# Abstract

Savannas are characterized by the coexistence of two contrasting plant life-forms: woody and herbaceous vegetation. During the last decades, there has been a global trend of an increase in woody cover and the spread of shrubs and trees into areas that were previously dominated by grasses. This process, termed bush encroachment, is associated with severe losses of ecosystem functions and typically difficult to reverse. It is assumed to be an example of a critical transition between two alternative stable states. Overgrazing due to unsustainable rangeland management has been identified as one of the main causes of this transition, as it can trigger several self-reinforcing feedback loops. However, the dynamic role of grazing within such feedback loops has received less attention. We used a set of coupled differential equations to describe the competition between shrubs and grasses, as well as plant biomass consumption via grazing and browsing. Grazers were assumed to receive a certain level of care from farmers, so that grazer densities emerge dynamically from the combined effect of vegetation abundance and farmer support. We quantified all self-reinforcing and self-dampening feedback loops at play and analyzed their relative importance in shaping system (in-)stability. Bistability, the presence of a grass dominated and a shrub dominated state, emerges for intermediate levels of farmer support due to positive feedback that arises from competition between shrubs and grasses and from herbivory. We furthermore demonstrate that disturbances, such as drought events, trigger abrupt transitions from the grass dominated to the shrub dominated state and that the system becomes more susceptible to disturbances with increasing farmer support. Our results thus highlight the potential of interaction networks in combinations with feedback loop analysis for improving our understanding of critical transitions in general, and bush encroachment in particular.

# Analysis 

This repository contains: 
- the main jupyter notebook, giving an overview over all parts of the analysis
- one python script for each figure in the manuscript
- scripts to reproduce the feedback analysis. Table 2 of the manuscript is created by "total_feedback.py". Figure S2 is created with "FigS2_loop_weight_unstable_points.py"

