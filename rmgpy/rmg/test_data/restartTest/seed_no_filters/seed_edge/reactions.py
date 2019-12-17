#!/usr/bin/env python
# encoding: utf-8

name = "seed_edge"
shortDesc = ""
longDesc = """

"""
autoGenerated=True
entry(
    index = 0,
    label = "O(T) + OH(D) <=> [O]O",
    degeneracy = 1.0,
    kinetics = Arrhenius(A=(15.4803,'m^3/(mol*s)'), n=1.88017, Ea=(5.1666,'kJ/mol'), T0=(1,'K'), Tmin=(303.03,'K'), Tmax=(2000,'K'), comment="""Estimated using template [O_rad;O_birad] for rate rule [O_pri_rad;O_birad]
    Euclidian distance = 1.0
    family: Birad_R_Recombination"""),
    longDesc = 
"""
Estimated using template [O_rad;O_birad] for rate rule [O_pri_rad;O_birad]
Euclidian distance = 1.0
family: Birad_R_Recombination
""",
)

entry(
    index = 1,
    label = "O(T) + H <=> OH(D)",
    degeneracy = 1.0,
    kinetics = Arrhenius(A=(1e+13,'cm^3/(mol*s)'), n=0, Ea=(0,'kJ/mol'), T0=(1,'K'), Tmin=(300,'K'), Tmax=(1500,'K'), comment="""Matched reaction 4 H + O <=> HO in Birad_R_Recombination/training
    This reaction matched rate rule [H_rad;O_birad]
    family: Birad_R_Recombination"""),
    longDesc = 
"""
Matched reaction 4 H + O <=> HO in Birad_R_Recombination/training
This reaction matched rate rule [H_rad;O_birad]
family: Birad_R_Recombination
""",
)

entry(
    index = 2,
    label = "OH(D) + H2 <=> H + H2O",
    degeneracy = 2.0,
    kinetics = Arrhenius(A=(1.82e+09,'cm^3/(mol*s)'), n=1.21, Ea=(83.9729,'kJ/mol'), T0=(1,'K'), Tmin=(200,'K'), Tmax=(2400,'K'), comment="""Matched reaction 312 H2 + OH <=> H2O_p + H_p in H_Abstraction/training
    This reaction matched rate rule [H2;O_pri_rad]
    family: H_Abstraction"""),
    longDesc = 
"""
Matched reaction 312 H2 + OH <=> H2O_p + H_p in H_Abstraction/training
This reaction matched rate rule [H2;O_pri_rad]
family: H_Abstraction
""",
)

entry(
    index = 3,
    label = "O(T) + [O]O <=> O2 + OH(D)",
    degeneracy = 1.0,
    kinetics = Arrhenius(A=(3680.39,'m^3/(mol*s)'), n=0.677977, Ea=(24.6819,'kJ/mol'), T0=(1,'K'), comment="""Estimated using average of templates [X_H;O_atom_triplet] + [Orad_O_H;Y_rad_birad_trirad_quadrad] for rate rule [Orad_O_H;O_atom_triplet]
    Euclidian distance = 2.0
    family: H_Abstraction"""),
    longDesc = 
"""
Estimated using average of templates [X_H;O_atom_triplet] + [Orad_O_H;Y_rad_birad_trirad_quadrad] for rate rule [Orad_O_H;O_atom_triplet]
Euclidian distance = 2.0
family: H_Abstraction
""",
)

entry(
    index = 4,
    label = "O2 + OH(D) <=> [O]OO",
    degeneracy = 2.0,
    kinetics = Arrhenius(A=(4e+07,'m^3/(mol*s)'), n=1.78837e-07, Ea=(20.7716,'kJ/mol'), T0=(1,'K'), Tmin=(300,'K'), Tmax=(1500,'K'), uncertainty=RateUncertainty(mu=0.0, var=33.1368631905, Tref=1000.0, N=1, correlation='Root_N-1R->H_N-1CClNOSSi->N_1COS->O_Ext-1O-R_N-2R->C_N-3R!H->N_N-2OS->S',), comment="""BM rule fitted to 2 training reactions at node Root_N-1R->H_N-1CClNOSSi->N_1COS->O_Ext-1O-R_N-2R->C_N-3R!H->N_N-2OS->S
        Total Standard Deviation in ln(k): 11.5401827615
    Exact match found for rate rule [Root_N-1R->H_N-1CClNOSSi->N_1COS->O_Ext-1O-R_N-2R->C_N-3R!H->N_N-2OS->S]
    Euclidian distance = 0
    Multiplied by reaction path degeneracy 2.0
    family: R_Recombination
    Ea raised from 16.4 to 20.8 kJ/mol to match endothermicity of reaction."""),
    longDesc = 
"""
BM rule fitted to 2 training reactions at node Root_N-1R->H_N-1CClNOSSi->N_1COS->O_Ext-1O-R_N-2R->C_N-3R!H->N_N-2OS->S
    Total Standard Deviation in ln(k): 11.5401827615
Exact match found for rate rule [Root_N-1R->H_N-1CClNOSSi->N_1COS->O_Ext-1O-R_N-2R->C_N-3R!H->N_N-2OS->S]
Euclidian distance = 0
Multiplied by reaction path degeneracy 2.0
family: R_Recombination
Ea raised from 16.4 to 20.8 kJ/mol to match endothermicity of reaction.
""",
)

entry(
    index = 5,
    label = "O(T) + H2 <=> H + OH(D)",
    degeneracy = 2.0,
    kinetics = Arrhenius(A=(3.4e+08,'cm^3/(mol*s)'), n=1.5, Ea=(96.0228,'kJ/mol'), T0=(1,'K'), Tmin=(300,'K'), Tmax=(1500,'K'), comment="""Matched reaction 285 H2 + O_rad <=> HO + H in H_Abstraction/training
    This reaction matched rate rule [OH_rad_H;H_rad]
    family: H_Abstraction"""),
    longDesc = 
"""
Matched reaction 285 H2 + O_rad <=> HO + H in H_Abstraction/training
This reaction matched rate rule [OH_rad_H;H_rad]
family: H_Abstraction
""",
)

entry(
    index = 6,
    label = "H + OH(D) <=> H2O",
    degeneracy = 1.0,
    kinetics = Arrhenius(A=(1.62e+14,'cm^3/(mol*s)'), n=0, Ea=(0.6276,'kJ/mol'), T0=(1,'K'), Tmin=(300,'K'), Tmax=(2100,'K'), comment="""Matched reaction 64 H + OH <=> H2O in R_Recombination/training
    This reaction matched rate rule [Root_1R->H_N-2R-inRing_N-2R->H_N-2CNOS->S_N-2CNO->C]
    family: R_Recombination"""),
    longDesc = 
"""
Matched reaction 64 H + OH <=> H2O in R_Recombination/training
This reaction matched rate rule [Root_1R->H_N-2R-inRing_N-2R->H_N-2CNOS->S_N-2CNO->C]
family: R_Recombination
""",
)

entry(
    index = 7,
    label = "O2 + H2O <=> OH(D) + [O]O",
    degeneracy = 4.0,
    kinetics = Arrhenius(A=(9.3e+12,'cm^3/(mol*s)'), n=0, Ea=(310.118,'kJ/mol'), T0=(1,'K'), Tmin=(300,'K'), Tmax=(1000,'K'), comment="""Matched reaction 379 H2O + O2 <=> HO2_r12 + OH_p23 in H_Abstraction/training
    This reaction matched rate rule [Orad_O_H;O_pri_rad]
    family: H_Abstraction"""),
    longDesc = 
"""
Matched reaction 379 H2O + O2 <=> HO2_r12 + OH_p23 in H_Abstraction/training
This reaction matched rate rule [Orad_O_H;O_pri_rad]
family: H_Abstraction
""",
)

entry(
    index = 8,
    label = "O(T) + OO <=> OH(D) + [O]O",
    degeneracy = 2.0,
    kinetics = Arrhenius(A=(1.74e+13,'cm^3/(mol*s)'), n=0, Ea=(19.874,'kJ/mol'), T0=(1,'K'), comment="""Estimated using template [O/H/NonDeO;O_atom_triplet] for rate rule [H2O2;O_atom_triplet]
    Euclidian distance = 1.0
    Multiplied by reaction path degeneracy 2.0
    family: H_Abstraction"""),
    longDesc = 
"""
Estimated using template [O/H/NonDeO;O_atom_triplet] for rate rule [H2O2;O_atom_triplet]
Euclidian distance = 1.0
Multiplied by reaction path degeneracy 2.0
family: H_Abstraction
""",
)

entry(
    index = 9,
    label = "OH(D) + [O]O <=> OOO",
    degeneracy = 1.0,
    kinetics = Arrhenius(A=(2e+07,'m^3/(mol*s)'), n=1.78837e-07, Ea=(0,'kJ/mol'), T0=(1,'K'), Tmin=(300,'K'), Tmax=(1500,'K'), uncertainty=RateUncertainty(mu=0.0, var=33.1368631905, Tref=1000.0, N=1, correlation='Root_N-1R->H_N-1CClNOSSi->N_1COS->O_Ext-1O-R_N-2R->C_N-3R!H->N_N-2OS->S',), comment="""BM rule fitted to 2 training reactions at node Root_N-1R->H_N-1CClNOSSi->N_1COS->O_Ext-1O-R_N-2R->C_N-3R!H->N_N-2OS->S
        Total Standard Deviation in ln(k): 11.5401827615
    Exact match found for rate rule [Root_N-1R->H_N-1CClNOSSi->N_1COS->O_Ext-1O-R_N-2R->C_N-3R!H->N_N-2OS->S]
    Euclidian distance = 0
    family: R_Recombination"""),
    longDesc = 
"""
BM rule fitted to 2 training reactions at node Root_N-1R->H_N-1CClNOSSi->N_1COS->O_Ext-1O-R_N-2R->C_N-3R!H->N_N-2OS->S
    Total Standard Deviation in ln(k): 11.5401827615
Exact match found for rate rule [Root_N-1R->H_N-1CClNOSSi->N_1COS->O_Ext-1O-R_N-2R->C_N-3R!H->N_N-2OS->S]
Euclidian distance = 0
family: R_Recombination
""",
)

entry(
    index = 10,
    label = "OH(D) + OO <=> [O]O + H2O",
    degeneracy = 2.0,
    kinetics = Arrhenius(A=(0.4995,'m^3/(mol*s)'), n=1.9275, Ea=(26.4644,'kJ/mol'), T0=(1,'K'), comment="""Estimated using average of templates [O/H/NonDeO;O_pri_rad] + [H2O2;O_rad] for rate rule [H2O2;O_pri_rad]
    Euclidian distance = 1.0
    Multiplied by reaction path degeneracy 2.0
    family: H_Abstraction"""),
    longDesc = 
"""
Estimated using average of templates [O/H/NonDeO;O_pri_rad] + [H2O2;O_rad] for rate rule [H2O2;O_pri_rad]
Euclidian distance = 1.0
Multiplied by reaction path degeneracy 2.0
family: H_Abstraction
""",
)

entry(
    index = 11,
    label = "O(T) + H2O <=> OH(D) + OH(D)",
    degeneracy = 2.0,
    kinetics = Arrhenius(A=(5.26e+09,'cm^3/(mol*s)'), n=1.2, Ea=(74.6007,'kJ/mol'), T0=(1,'K'), Tmin=(298,'K'), Tmax=(1000,'K'), comment="""Matched reaction 380 H2O + O_rad <=> HO + OH_p23 in H_Abstraction/training
    This reaction matched rate rule [OH_rad_H;O_pri_rad]
    family: H_Abstraction"""),
    longDesc = 
"""
Matched reaction 380 H2O + O_rad <=> HO + OH_p23 in H_Abstraction/training
This reaction matched rate rule [OH_rad_H;O_pri_rad]
family: H_Abstraction
""",
)

