# StellarTools

StellarTools is a small python package that contains some functions and classes I've implemented through the years in the field of my reasearch in stellar physics.

Here is the comprehensive list of modules 

## binary 

A small module to compute binary orbits: in 3D, 2D-projected on the sky plane and radial velocities

## blackbody 

Blackbody functions for stellar fluxes including distance and stellar radius. Note that nowdays I use astropy module instead

## Colortemperature 

This modules contains two functions and two matplotlib colormaps that reprents the stellar colors as a function of its temperature.
* temperatureColor & temperatureColorMap : "real" colors
* temperatureColorFake & temperatureColorMapFake : "fake" saturated colors
 
## FluxConverter

Flux conversion from  photometric bands

## Geneva

Geneva stellar evolution tracks with interpolation

## hlines

Hydrogen spectral series

## Kurucz

Kurukz stellar atmosphere models synthetic Spectral Energy distribution for stellar from 3000 to 50000K

## lightColor

A function and a matplotlib colormap based on the color of the light as a function of the wavelength

## reto2mas & mas2reto

Simple function to perform conversion between milli-arcseconds and stellar (or solar radii) with distance in parsec

## mist

Simple class to plot interpolated MIST (MESA Isochrones & Stellar Tracks) models.

## reddening

Compute interstellar reddening based on Cardelli 1989 law

## sed

Retrieve and convert SED (Spectral Energy Distribution) from Vizier using astroquery and astropy

## TypicalStar

This module contains the class typicalStar that return "standard" stellar para-
meters for a given spectral class. The Teff, Radius, and Mass are taken from
Allen's Astrophysical Quantities.The Luminosity is computed from the Radius and
Teff and the critical velocity from using the Radius and the Mass

## udisk

Simple function that compute interferometric visibility for a uniform disk.
With three out of this 4 parameters : wavelength (micron), angular diameter (mas), baseline length (meters), and visibility return the 4th one.

## vonZeipel
Von Zeipel model of flatened star








