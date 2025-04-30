
from uncertainties import ufloat
from uncertainties.umath import *
import numpy as np
import statistics
class Spectroscopy():
    # Read index of refraction and angle from a file
    data = np.loadtxt("HydrogenGasSpectroscopyData.txt", unpack=True, skiprows=1)

    # Given an angle and an index of refraction, n, return wavelength in nm
    angle = []
    for i in data[1]:
        # Convert to radians
        angle.append(ufloat((i * np.pi / 180), (0.05 * np.pi / 180)))
    n = data[0]
    
    def calcWavelength(angle, n):
        # a is the distance between lines in the diffraction grating in meters
        a = 1.667 * 10 ** -6
        # Take the sin of the angle
        asin = sin(angle)
        return (a * asin / n)

    # Calculate the Rydberg constant for a given wavelength, element, and principle quantum number
    z = 1
    n2 = data[2]
    def calcRydberg(wavelength, z, n2):
        # For the Balmer series, n1 = 2
        n1 = 2
        return (1 / ((wavelength) * (z ** 2) * ((1 / n1 ** 2) - (1 / n2 ** 2))))

    # Executing methods
    # Calculate wavelengths
    wavelength = []
    count = 0
    for i in angle:
        wavelength.append(calcWavelength(angle[count], n[count]))
        count = count + 1
    # Print Wavelengths
    print("---Wavelengths---")
    for i in wavelength:
        print(f"{i * 10 ** 9:.3f}")
    print()

    # Calculate Rydberg constants
    rydberg = []
    count = 0
    for i in wavelength:
        rydberg.append(calcRydberg(wavelength[count], z, n2[count]))
        count = count + 1
    # Print Rydberg constants
    print("---Rydberg Constants---")
    for i in rydberg:
        print(f"{i:.1f}")
    print()

    # Error Analysis
    # We want to obtain a single value for the Rydberg constant of hydrogen
    # Take only the nominal value from each Rydberg constant to use with statistics library
    stdRydberg = []
    for i in rydberg:
        stdRydberg.append(i.nominal_value)
    
    # Mean
    mean = statistics.mean(stdRydberg)
    print("---Mean---")
    print(f"{mean:.1f}")
    print()
    
    # Standard Deviation
    std = statistics.stdev(stdRydberg)
    print("---Standard Deviation---")
    print(f"{std:.1f}")
    print()

    # Standard Error
    N = data[0].size
    se = std / np.sqrt(N)
    print("---Standard Error---")
    print(f"{se:.1f}")
    print()
    
