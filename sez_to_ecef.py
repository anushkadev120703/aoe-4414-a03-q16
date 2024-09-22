# sez_to_ecef.py
#
# Usage: python3 sez_to_ecef.py o_lat_deg o_lon_deg o_hae_km s_km e_km z_km
#  Converts SEZ vector components to ECEF
#  
# Parameters:
# o_lat_deg: latitude in degrees
# o_lon_deg:longitutde in degrees 
# o_hae_km: height above the elipsoid in km
# s_km: SEZ south-component in km
# e_km: SEZ east-component in km
# z_km: SEZ z-component in km

#
# Output:
#  Prints the ecef x, y and z vectors in km
#
# Written by Anushka Devarajan
# Other contributors: None
#
# This work is licensed under CC BY-SA 4.0

# import Python modules
import math # math module
import sys  # argv
import numpy as np


# "constants"
R_E_KM = 6378.137
E_E    = 0.081819221456

# helper functions

# initialize script arguments
o_lat_deg=float('nan') #latitude in degrees
o_lon_deg= float('nan') #longitude in degrees
o_hae_km= float('nan') #height above the ellipsoid in km
s_km = float('nan') # SEZ south-component in km
e_km = float('nan') # SEZ east-component in km
z_km = float('nan') # SEZ z-component in km


# parse script arguments
if len(sys.argv)==7:
  o_lat_deg = float(sys.argv[1])
  o_lon_deg= float(sys.argv[2])
  o_hae_km= float(sys.argv[3])
  s_km = float(sys.argv[4])
  e_km = float(sys.argv[5])
  z_km = float(sys.argv[6])
else:
  print(\
   'Usage: '\
   'python3 sez_to_ecef.py o_lat_deg o_lon_deg o_hae_km s_km e_km z_km'\
  )
  exit()

#calculating llh to ecef
lat_rad = o_lat_deg * math.pi/180
lon_rad = o_lon_deg *math.pi/180

c_E= R_E_KM/(math.sqrt(1-(E_E**2)*(math.sin(lat_rad))**2))
s_E= (R_E_KM*(1-E_E**2))/(math.sqrt(1-(E_E**2)*(math.sin(lat_rad))**2))
r_x_km = (c_E + o_hae_km)*math.cos(lat_rad)*math.cos(lon_rad)
r_y_km = (c_E + o_hae_km)*math.cos(lat_rad)*math.sin(lon_rad)
r_z_km = (s_E+ o_hae_km)*math.sin(lat_rad)

#calculating sez to ecef
lat_rad =o_lat_deg * math.pi/180
lon_rad= o_lon_deg * math.pi/180

sez=[[s_km],
     [e_km],
     [z_km]]
r_y_90=[[math.sin(lat_rad),0,math.cos(lat_rad)],
        [0,1,0],
        [-math.cos(lat_rad),0,math.sin(lat_rad)]]
r_z=[[math.cos(lon_rad), -math.sin(lon_rad),0],
     [math.sin(lon_rad), math.cos(lon_rad),0],
     [0,0,1]]

#calculate rotations 
first_rot=np.dot(r_y_90,sez) 
second_rot= np.dot(r_z, first_rot)

ecef_x_km=second_rot.item(0)+r_x_km
ecef_y_km=second_rot.item(1)+r_y_km
ecef_z_km=second_rot.item(2)+r_z_km

print(ecef_x_km)
print(ecef_y_km)
print(ecef_z_km)

