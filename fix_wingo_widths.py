# Calculate subcatchment widths based on lengths in Example2
import numpy as np
acre = 43560.0  # square ft/acre
ex2_subcat_area_acre = [4.55,4.74,3.74,6.79,4.79,1.98,2.33]
ex2_subcat_width_ft = [1587.0,1653.0,1456.0,2331.0,1670.0,690.0,907.0]
area_acre = np.array(ex2_subcat_area_acre)
area_ft2 = area_acre*acre
width_ft = np.array(ex2_subcat_width_ft)
length_ft = area_ft2/width_ft
# print length_ft
# OK, all of the example 2 lengths are between 112 and 126 ft.
# which is around the size of a typical lot from the back
# to the street, and this makes sense
# For Wingohocking-Borg, I will use 120 ft for all subcatchments
wingo_length = 120.0
wingo_subcat_area_acre = [46.46,18.39,60.51,30.26,73.34,25.92,42.08]
wingo_area_acre = np.array(wingo_subcat_area_acre)
wingo_area_ft2 = wingo_area_acre*acre
wingo_width_ft = wingo_area_ft2/wingo_length
print "Wingohocking Subcatchment Width in order:"
print wingo_width_ft

