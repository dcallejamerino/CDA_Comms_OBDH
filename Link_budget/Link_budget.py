import numpy as np
import matplotlib.pyplot as plt
import warnings
import pandas as pd
import tkinter as tk
from tkinter import ttk
from Functions import *

## SOLUTION
print("--hello--")

# LINK BUDGET
#Inputs:

h = 780*1e3     # h - orbit height in meters
mode = 'draft'  # mode - 'draft' (w/o coordinates consideration) or 'precise' (w/ coordinates consideration)
L_node =  0     # L_node - instantaneous ascending node (degrees)
incl = 0        # incl - instantaneous orbit pole (degrees)
lat_gs = 0      # lat_gs - ground station latitude (degrees)
long_gs = 0     # long_gs - ground station logtitude (degrees)
eps_min = 0     # eps_min - minimum spacecraft elevation (degrees)
    
l_d = LinkBudget(h, mode,L_node,incl,lat_gs,long_gs,eps_min)

# SNR & EIRP
#Inputs:

## DOWNLINK SCIENCE  ## S-BAND ISIS-TXS2-DSH-0001, version 2.2 
f0_S = 2.245e9    # f0 - carrier frequency (Hz)
Pt_S = 1          # Pt - transmitted power (Watts)   
Gt_S = 6.5        # Gt - transmit antenna gain (dBi) 
Gr_S = 35.4       # Gr - receive antenna gain  (dBi) 
B_S =  1.0e6      # B - transmit bandwidth (Hz) QPSK, RS(255, 2223)  +  C(7, 1/2) for a BER 1E-5 
Tnoise_S = 1000   # Tnoise - noise temperature (K)
eta_t_S = 0       # eta_t - transmit feeder gain (dB)
eta_r_S = 0       # eta_r - receive feeder gain (dB)
Lt_S = 1          # Lt - transmiter feeder loss (dB)
Lr_S = 1          # Lr - receiver feeder loss (dB) 
Ladd_S = 1        # Ladd - additional losses (dB)
gamma_S = 1       # gamma - nose bandwith constant

        #QPSK, RS(255, 2223)  +  C(7, 1/2) for a BER 1E5 requires SNR 10

## DOWNLINK TTC  ## UHF-BAND ALEN SPACE TRISKEL OBC+TTC+OBSW
f0_U = 400e6      # f0 - carrier frequency (Hz)
Pt_U = 1          # Pt - transmitted power (Watts)
Gt_U = 0          # Gt - transmit antenna gain (dBi) 
Gr_U = 16.3       # Gr - receive antenna gain  (dBi) 
B_U =  9600      # B - transmit bandwidth (Hz) GFSK modulation (GMSK)
Tnoise_U = 1000   # Tnoise - noise temperature (K)
eta_t_U = 0       # eta_t - transmitt feeder gain (dB)
eta_r_U = 0       # eta_r - receive feeder gain (dB)
Lt_U = 1          # Lt - transmiter feeder loss (dB)
Lr_U = 1          # Lr - receiver feeder loss (dB) 
Ladd_U = 1        # Ladd - additional losses (dB)
gamma_U = 1       # gamma - nose bandwith constant

        #GFSK modulation (GMSK) for a BER 1E5 requires SNR 20

#Outputs:
     # snr - expected SNR (dB)
     # EIRP - equivalent isolated radiated power (dBm)

snr_S, EIRP_S = l_d.expected_snr(f0_S, Pt_S, Gt_S, Gr_S, B_S, Tnoise_S,eta_t_S,eta_r_S, Lt_S, Lr_S, Ladd_S, gamma_S)
snr_U, EIRP_U = l_d.expected_snr(f0_U, Pt_U, Gt_U, Gr_U, B_U, Tnoise_U,eta_t_U,eta_r_U, Lt_U, Lr_U, Ladd_U, gamma_U)

###### RESULTS AND PLOTS ######

MaxSNR_S = max(snr_S)
print(f"SNR S-BAND SCIENCE DOWNLINK (dB): {MaxSNR_S}") # a higher signal-to-noise ratio is generally preferred in most applications as it indicates a stronger and more reliable signal relative to the background noise.
print(f"EIRP S-BAND SCIENCE DOWNLINK  (dBm): {EIRP_S}")
print(f"BIT RATE S-BAND SCIENCE DOWNLINK  (Hz - bps): {B_S}")

MaxSNR_U = max(snr_U)
print(f"SNR UHF-BAND TTC DOWNLINK (dB): {MaxSNR_U}") # a higher signal-to-noise ratio is generally preferred in most applications as it indicates a stronger and more reliable signal relative to the background noise.
print(f"EIRP UHF-BAND TTC DOWNLINK  (dBm): {EIRP_U}")
print(f"BIT RATE U-BAND SCIENCE DOWNLINK  (Hz - bps): {B_U}")

# Calculate the link margin, the difference between the expected value of Eb/N0 calculated and the Eb/N0 required (including implementation loss).
# Add 1 to 2 dB to the theoretical value given in the last step for implementation losses
Implementation_losses = 1
S_DOWNLINK_MARGIN = MaxSNR_S-10-Implementation_losses
U_DOWNLINK_MARGIN = MaxSNR_U-20-Implementation_losses
print(f"S-BAND DOWNLINK MARGIN (dB): {S_DOWNLINK_MARGIN}")
print(f"UHF-BAND DOWNLINK MARGIN (dB): {U_DOWNLINK_MARGIN}")

if S_DOWNLINK_MARGIN > 3:
    status_S = "S-BAND DOWNLINK MARGIN OK"
    print("S-BAND DOWNLINK MARGIN OK")
else:
    status_S = "S-BAND DOWNLINK MARGIN NOT OK"
    print("S-BAND DOWNLINK MARGIN NOT OK: Adjust imput parameters until the margin is at least 3 dB greater than the estimated value")

if U_DOWNLINK_MARGIN > 3:
    status_U = "U-BAND DOWNLINK MARGIN OK"
    print("U-BAND DOWNLINK MARGIN OK")
else:
    status_U = "U-BAND DOWNLINK MARGIN NOT OK"
    print("U-BAND DOWNLINK MARGIN NOT OK: Adjust imput parameters until the margin is at least 3 dB greater than the estimated value")

# PLOTS
phi = np.pi*np.array(range(0,181,5))/180
plt.plot(180 * phi / np.pi, snr_S, label=f'{f0_S/1e6} MHz S-BAND', color='orange')
plt.axhline(y=10, color='orange', linestyle='dashed', label='QPSK for a BER 1E5 requires SNR 10')
plt.axhline(y=10+Implementation_losses+3, color='red', linestyle='dashed', label='DOWNLINK MARGIN>3dB)')

plt.title('Expected SNRs')
plt.xlabel('Elevation angles (degrees)')
plt.ylabel('SNR (dB)')
plt.legend()
plt.grid()
plt.show()

plt.plot(180 * phi / np.pi, snr_U, label=f'{f0_U/1e6} MHz UHF-BAND', color='blue')
plt.axhline(y=20, color='blue', linestyle='dashed', label='GMSK for a BER 1E5 requires SNR 20')
plt.axhline(y=20+Implementation_losses+3, color='red', linestyle='dashed', label='DOWNLINK MARGIN>3dB)')

plt.title('Expected SNRs')
plt.xlabel('Elevation angles (degrees)')
plt.ylabel('SNR (dB)')
plt.legend()
plt.grid()
plt.show()


def create_info_table(master, data, row):
    frame = ttk.Frame(master)
    frame.grid(row=row, column=0, padx=10, pady=10)

    columns = ("Parameter", "S-Band Value - SCIENCE", "UHF-Band Value - TTC")

    tree = ttk.Treeview(frame, columns=columns, show="headings",height=len(data) + 2)
    
    tree.column("Parameter", width=400)
    tree.column("S-Band Value - SCIENCE", width=400)
    tree.column("UHF-Band Value - TTC", width=400)


    for col in columns:
        tree.heading(col, text=col)

    for item in data:
        tree.insert("", "end", values=item)

    
    tree.pack()

# Main window
main_window = tk.Tk()
main_window.title("Downlink Analysis")

# Data for the table
table_data = [
    ("SNR DOWNLINK (dB)", round(MaxSNR_S, 2), round(MaxSNR_U, 2)),
    ("EIRP DOWNLINK (dBm)", EIRP_S, EIRP_U),
    ("BIT RATE DOWNLINK (Hz - bps)", B_S, B_U),
    ("DOWNLINK MARGIN (dB)", round(S_DOWNLINK_MARGIN, 2), round(U_DOWNLINK_MARGIN, 2)),
    ("STATUS", status_S, status_U),
]

# Create and display the information table
create_info_table(main_window, table_data, row=0)

# Run the main loop
main_window.mainloop()

print("--bye--")





# path_loss = l_d.path_loss(f0_S)
# phi = np.pi*np.array(range(0,181,5))/180
# plt.plot(180*phi/np.pi, path_loss, '-o')
# plt.title('Path_loss')
# plt.xlabel('Elevation angles (degrees)')
# plt.ylabel('Path_loss (dB)')
# plt.grid()
# plt.show()
