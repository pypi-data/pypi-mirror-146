Description by Motohiko Kusakabe (Dec. 2, 2020)
-----------------------------------------------------

Yields of the W7 model in SNe Ia

(1) yield_nucl.d

Nuclear yield: nuclear id, mass #, atomic #, yield (M_sun)
format(2x,a5,2(i5),es14.5)

(2) yield_elem.d

Elemental yield: atomic #, yield (M_sun)
format (2x,i3, es14.5e3)
-----------------------------------------------------

[Note] The yields are based on the following nucleosynthesis calculations:

(1) Central NSE+O-burning layers (M_r < 1.14 M_sun)
    <--Mori et al. ApJ 904, 29 (2020)
https://ui.adsabs.harvard.edu/abs/2020ApJ...904...29M/abstract

There, screening effects on electron capture rates of Fe-peak elements have been taken into account. Fe-peak and alpha-elements are predominantly produced here.

(2) the p-process layer (explosive C-burning layer) (M_r /M_sun =[1.14,1.31])
    <--Kusakabe et al. ApJ 726, 25 (2011)
https://ui.adsabs.harvard.edu/abs/2011ApJ...726...25K/abstract

!Case A1 has been adopted for this yield. This p-process layer experiences an s-process episode during the mass accretion phase, and photodisintegration reactions during the SN. Some p- as well as s-nuclei are produced here.

!Case A1 explains solar abundances of p-nuclei.

(3) outer unburned layer (M_r /M_sun =[1.31,1.38])

!A deflagration wave is extinguished before it arrives at this layer. As a result, this layer keeps the abundances immediately before the SN. The abundances are adopted from Case A nuclear abundances in Kusakabe et al. (2011). The composition here is rich in s-nuclei.
