'''
import urllib.request
url = "https://raw.githubusercontent.com/syedhamidali/test_scripts/master/map_features.py"
urllib.request.urlretrieve(url, "map_features.py")
import map_features as mf
'''

import os
import urllib.request
import cartopy.crs as ccrs
import cartopy.feature as feat
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
from metpy.plots import USCOUNTIES

def map_features(ax, b=False, l=False, t=False, r=False, coastline=False, 
                     borders=False, ocean=False, states=True, counties=False, 
                     land=False, grids=False, roads=False):
    '''
    Add cartopy features to the axis.

    Parameters:
    - ax (matplotlib.axes.Axes): The target axes to add the features to.
    - b (bool): Whether to show gridline labels at the bottom (default: False).
    - l (bool): Whether to show gridline labels on the left (default: False).
    - t (bool): Whether to show gridline labels at the top (default: False).
    - r (bool): Whether to show gridline labels on the right (default: False).
    - coastline (bool): Whether to show coastlines (default: False).
    - borders (bool): Whether to show country borders (default: False).
    - ocean (bool): Whether to show ocean fill (default: False).
    - states (bool): Whether to show state boundaries (default: True).
    - counties (bool): Whether to show county boundaries (default: False).
    - land (bool): Whether to show land fill (default: False).
    - grids (bool): Whether to show gridlines (default: False).
    - highways (bool): Whether to show highways (default: False).
    - roads (bool): Whether to show roads (default: False).
    '''
    gl = ax.gridlines(crs=ccrs.PlateCarree(), linewidth=0.1, color='black', 
                      alpha=0.2, linestyle='-', draw_labels=True)
    gl.top_labels = t
    gl.bottom_labels = b
    gl.left_labels = l
    gl.right_labels = r
    if grids:
        gl.xlines = True
        gl.ylines = True
    gl.xformatter = LONGITUDE_FORMATTER
    gl.yformatter = LATITUDE_FORMATTER
    if borders:
        ax.add_feature(feat.BORDERS, lw=0.5)
    if land:
        ax.add_feature(feat.LAND, lw=0.3, fc=[0.9, 0.9, 0.9])
    if coastline:
        ax.add_feature(feat.COASTLINE, lw=0.5)
    if ocean:
        ax.add_feature(feat.OCEAN, alpha=0.5)
    if states:
        ax.add_feature(feat.STATES.with_scale("10m"), alpha=0.5, lw=0.5)
    if counties:
        ax.add_feature(USCOUNTIES.with_scale('500k'), alpha=0.3, linestyle=':', lw=0.3)
    if roads:
        ax.add_feature(feat.NaturalEarthFeature(category='cultural', name='roads', 
                        scale='10m', facecolor='none', edgecolor='orange', linewidth=0.3))

def main():
    '''
    Main function for executing the script.
    '''
    filename = "map_features.py"
    if not os.path.exists(filename):
        url = "https://raw.githubusercontent.com/syedhamidali/test_scripts/master/map_features.py"
        urllib.request.urlretrieve(url, filename)
    import map_features as mf

if __name__ == "__main__":
    main()

