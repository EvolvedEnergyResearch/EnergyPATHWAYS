

import os
import pandas as pd
import geopandas as gpd

directory = r'D:\Dropbox (EER)\Evolved Energy Research\Projects & Marketing\Third Way\Decarb Europe\Work Files\Geographies\shapefile\ref-nuts-2013-10m.shp\NUTS_RG_10M_2013_3035_LEVL_1.shp'

poly = gpd.read_file(os.path.join(directory, "NUTS_RG_10M_2013_3035_LEVL_1.shp"))

# poly = poly.to_crs("EPSG:3395")
poly = poly.to_crs("WGS_84")

# temp=poly.centroid
# poly['x'] = temp.x
# poly['y'] = temp.y
#
# centroid=poly[['x','y']]

rep_points = poly.representative_point()

outputs = poly[['NUTS_ID', 'LEVL_CODE', 'CNTR_CODE', 'NAME_LATN', 'NUTS_NAME', 'FID']]
outputs['long'] = rep_points.x
outputs['lat'] = rep_points.y

outputs.to_csv(r'D:\Dropbox (EER)\Evolved Energy Research\Projects & Marketing\Third Way\Decarb Europe\Work Files\Geographies\shapefile\nuts1_coord.csv', index=False)
