import matplotlib.pyplot as plt
import pandas as pd
from config import *
import numpy as np

# Load data from text files, skipping the appropriate number of header rows
def load_data(file_path, usecols, skiprows):
    return pd.read_csv(file_path, sep='\t', usecols=usecols, skiprows=skiprows)

# Load all chromatogram and mass spectrum data
chromatograms = [load_data(f'chromatogram{i+1}.txt', [0, 2], skiprows=43) for i in range(3)]
mass_spectra = [load_data(f'mass_spectrum{i+1}.txt', None, skiprows=35) for i in range(3)]

# Create the plot
fig, axes = plt.subplots(nrows=4, ncols=1, figsize=SIZE, gridspec_kw={'height_ratios': [1, 1, 1, 1]})

# Plot chromatograms on the first subplot
for i, chromatogram in enumerate(chromatograms):
    time_values = chromatogram.iloc[:, 0]
    intensity_values = chromatogram.iloc[:, 1]
    axes[0].plot(time_values, intensity_values, color=COLORS[i], linewidth=CHROMATOGRAM_LW)

axes[0].set_xlabel('Time (min)')
axes[0].set_ylabel('Intensity (mAU)')
axes[0].set_xlim(0, 3)
axes[0].set_ylim(-20)

# Plot mass spectra on the subsequent subplots
for i, mass_spectrum in enumerate(mass_spectra):
    mz_values = pd.to_numeric(mass_spectrum.iloc[:, 0], errors='coerce').dropna()
    intensity_values = pd.to_numeric(mass_spectrum.iloc[:, 1], errors='coerce').dropna()

    # Normalize intensity values to percentage
    max_intensity = intensity_values.max()
    intensity_values = (intensity_values / max_intensity) * 100

    axes[i+1].bar(mz_values, intensity_values, color=COLORS[i], width=MS_LW)

    # Label all peaks larger than threshold
    for mz, intensity in zip(mz_values, intensity_values):
        if intensity > MS_PEAK_THRESHOLD and mz > 200:
            axes[i+1].annotate(f'{mz:.2f}', xy=(mz, intensity), xytext=(mz, intensity + 5), fontsize=8, color=COLORS[i], ha='center')
    
    # Add dead space
    dead_space_factor = 1.2  # Increase the y-axis limit by 20% to add dead space
    axes[i+1].set_ylim(0, 100 * dead_space_factor)
    axes[i+1].set_xlim(0, 1200)

    axes[i+1].set_xlabel('M/Z')
    axes[i+1].set_ylabel('Intensity (%)')

# Adjust layout
plt.tight_layout()
plt.show()
