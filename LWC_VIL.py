import numpy as np
import pyart
import matplotlib.pyplot as plt

# Load radar data
radar = pyart.io.read("../Git_Stuff/imd_temp_radar/out2/cfrad_GOA210516024101-IMD-B.nc")

def reflectivity_to_lwc(reflectivity, density_of_water=1000):
    """
    Convert reflectivity (dBZ) to liquid water content (LWC).
    Using empirical relationship: LW = 3.44 * 10^(-6) * (Z / rho_w)^(4/7)
    LWC is in kg/m^3
    """
    z_linear = 10 ** (reflectivity / 10)  # Linearize reflectivity
    lwc = 3.44e-6 * (z_linear / density_of_water) ** (4/7)
    return lwc

def calculate_vil(radar):
    """
    Calculate Vertically Integrated Liquid (VIL) from radar reflectivity data.
    VIL = sum(LWC * delta_height)
    """
    # Extract reflectivity field
    reflectivity = radar.fields['REF']['data']
    
    # Convert reflectivity to LWC
    lwc = reflectivity_to_lwc(reflectivity)
    
    # Calculate delta_height for integration (convert range_bins to height using elevation angle)
    range_bins = radar.range['data']
    delta_height = np.diff(range_bins, prepend=0)
    
    # Align delta_height shape with lwc shape for broadcasting
    delta_height = delta_height[:, np.newaxis, np.newaxis]
    
    # Integrate LWC vertically
    vil = (lwc * delta_height).sum(axis=0)
    
    return vil

# Calculate VIL
vil = calculate_vil(radar)

# Add VIL to radar object
vil_field = {
    'data': vil,
    'units': 'kg/m^2',
    'long_name': 'Vertically Integrated Liquid'
}
radar.add_field('vil', vil_field)

# Print VIL values
# print(vil)

# Plot the VIL field
display = pyart.graph.RadarDisplay(radar)
display.plot('vil', sweep=0, vmin=0, vmax=np.nanmax(vil), colorbar_label='VIL (kg/m^2)')

plt.show()
