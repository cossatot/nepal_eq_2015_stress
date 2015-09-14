import pandas as pd
import numpy as np
import pyproj as pj
import halfspace.projections as hsp


gal = pd.read_csv('review_3.3_final2.0001.inv.total',
                  skiprows=1, names=['ind', 'lon', 'lat', 'depth', 'strike',
                                     'dip', 'rise', 'duration', 'ss_slip',
                                     'ds_slip', 'ss_len', 'ds_len', 'rigidity'],
                  index_col=0, delim_whitespace=True)


wgs84 = pj.Proj(init='epsg:4326')
utm45 = pj.Proj(init='epsg:32645')

gal['east'], gal['north'] = pj.transform(wgs84, utm45, gal.lon.values, 
                                         gal.lat.values)

gal['rake'] = hsp.get_rake_from_shear_components(strike_shear=gal.ss_slip,
                                                 dip_shear=gal.ds_slip)

gal['slip_m'] = np.sqrt(gal.ss_slip**2 + gal.ds_slip**2)

gal['depth'] = gal.depth * 1000

gal['point_index'] = gal.index.values

gal['fault_name'] = 'galetzka_mainshock'

gal[['east', 'north', 'depth', 'strike', 'dip', 'slip_m', 'rake', 'fault_name',
     'point_index']].to_csv('galetzka_mainshock.csv', index=False)
