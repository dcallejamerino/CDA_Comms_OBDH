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
Gr_S = 40         # Gr - receive antenna gain  (dBi) 35.4
B_S =  3.6e6      # B - transmit bandwidth (bps) QPSK, RS(255, 2223)  +  C(7, 1/2) for a BER 1E-5 -> MAX 4.3Mbps
Tnoise_S = 1000   # Tnoise - noise temperature (K)
eta_t_S = 0       # eta_t - transmit feeder gain (dB)
eta_r_S = 1       # eta_r - receive feeder gain (dB)
Lt_S = 1          # Lt - transmiter feeder loss (dB)
Lr_S = 1          # Lr - receiver feeder loss (dB) 
Ladd_S = 2        # Ladd - additional losses (dB)
gamma_S = 1.002   # gamma - receiver noise bandwith constant

        #QPSK, RS(255, 2223)  +  C(7, 1/2) for a BER 1E5 requires SNR 10

## DOWNLINK TTC  ## UHF-BAND ALEN SPACE TRISKEL OBC+TTC+OBSW
f0_U = 400e6      # f0 - carrier frequency (Hz)
Pt_U = 1          # Pt - transmitted power (Watts)
Gt_U = 0          # Gt - transmit antenna gain (dBi) 
Gr_U = 16.3       # Gr - receive antenna gain  (dBi) 
B_U =  9600      # B - transmit bandwidth (bps) GFSK modulation (GMSK)
Tnoise_U = 1000   # Tnoise - noise temperature (K)
eta_t_U = 0       # eta_t - transmitt feeder gain (dB)
eta_r_U = 0       # eta_r - receive feeder gain (dB)
Lt_U = 1          # Lt - transmiter feeder loss (dB)
Lr_U = 1          # Lr - receiver feeder loss (dB) 
Ladd_U = 2        # Ladd - additional losses (dB)
gamma_U = 1.002   # gamma - receiver noise bandwith constant

        #GFSK modulation (GMSK) for a BER 1E5 requires SNR 20


## UPLINK TTC  ## UHF-BAND ALEN SPACE TRISKEL OBC+TTC+OBSW
f0_U_up = 400e6      # f0 - carrier frequency (Hz)
Pt_U_up = 10         # Pt - transmitted power (Watts)
Gt_U_up = 16.3       # Gt - transmit antenna gain (dBi) 
Gr_U_up = 0          # Gr - receive antenna gain  (dBi) 
B_U_up =  19200      # B - transmit bandwidth (bps) GFSK modulation (GMSK)
Tnoise_U_up = 1000   # Tnoise - noise temperature (K)
eta_t_U_up = 0       # eta_t - transmitt feeder gain (dB)
eta_r_U_up = 0       # eta_r - receive feeder gain (dB)
Lt_U_up = 1          # Lt - transmiter feeder loss (dB)
Lr_U_up = 1          # Lr - receiver feeder loss (dB) 
Ladd_U_up = 2        # Ladd - additional losses (dB)
gamma_U_up = 1.57    # gamma - receiver noise bandwith constant

        #GFSK modulation (GMSK) for a BER 1E5 requires SNR 20

#Outputs:
     # snr - expected SNR (dB)
     # EIRP - equivalent isolated radiated power (dBm)

snr_S, EIRP_S = l_d.expected_snr(f0_S, Pt_S, Gt_S, Gr_S, B_S, Tnoise_S,eta_t_S,eta_r_S, Lt_S, Lr_S, Ladd_S, gamma_S)
snr_U, EIRP_U = l_d.expected_snr(f0_U, Pt_U, Gt_U, Gr_U, B_U, Tnoise_U,eta_t_U,eta_r_U, Lt_U, Lr_U, Ladd_U, gamma_U)
snr_U_up, EIRP_U_up = l_d.expected_snr(f0_U_up, Pt_U_up, Gt_U_up, Gr_U_up, B_U_up, Tnoise_U_up,eta_t_U_up,eta_r_U_up, Lt_U_up, Lr_U_up, Ladd_U_up, gamma_U_up)

###### RESULTS AND PLOTS ######

MaxSNR_S = max(snr_S)
print(f"SNR S-BAND SCIENCE DOWNLINK (dB): {MaxSNR_S}") # a higher signal-to-noise ratio is generally preferred in most applications as it indicates a stronger and more reliable signal relative to the background noise.
print(f"EIRP S-BAND SCIENCE DOWNLINK  (dBm): {EIRP_S}")
print(f"BIT RATE S-BAND SCIENCE DOWNLINK  (bps): {B_S}")

MaxSNR_U = max(snr_U)
print(f"SNR UHF-BAND TTC DOWNLINK (dB): {MaxSNR_U}") # a higher signal-to-noise ratio is generally preferred in most applications as it indicates a stronger and more reliable signal relative to the background noise.
print(f"EIRP UHF-BAND TTC DOWNLINK  (dBm): {EIRP_U}")
print(f"BIT RATE UHF-BAND TTC DOWNLINK  (bps): {B_U}")

MaxSNR_U_up = max(snr_U_up)
print(f"SNR UHF-BAND TTC UPLINK (dB): {MaxSNR_U_up}") # a higher signal-to-noise ratio is generally preferred in most applications as it indicates a stronger and more reliable signal relative to the background noise.
print(f"EIRP UHF-BAND TTC UPLINK  (dBm): {EIRP_U_up}")
print(f"BIT RATE UHF-BAND TTC UPLINK  (bps): {B_U_up}")

# Calculate the link margin, the difference between the expected value of Eb/N0 calculated and the Eb/N0 required (including implementation loss).
# Add 1 to 2 dB to the theoretical value given in the last step for implementation losses
Implementation_losses = 0
S_DOWNLINK_MARGIN = MaxSNR_S-10-Implementation_losses
U_DOWNLINK_MARGIN = MaxSNR_U-20-Implementation_losses
U_UPLINK_MARGIN = MaxSNR_U_up-20-Implementation_losses
print(f"S-BAND DOWNLINK MARGIN (dB): {S_DOWNLINK_MARGIN}")
print(f"UHF-BAND DOWNLINK MARGIN (dB): {U_DOWNLINK_MARGIN}")
print(f"UHF-BAND UPLINK MARGIN (dB): {U_UPLINK_MARGIN}")

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
    
if U_UPLINK_MARGIN > 3:
    status_U = "U-BAND UPLINK MARGIN OK"
    print("U-BAND UPLINK MARGIN OK")
else:
    status_U = "U-BAND UPLINK MARGIN NOT OK"
    print("U-BAND UPLINK MARGIN NOT OK: Adjust imput parameters until the margin is at least 3 dB greater than the estimated value")

# PLOTS
phi = np.pi*np.array(range(0,181,5))/180
plt.plot(180 * phi / np.pi, snr_S, label=f'{f0_S/1e6} MHz S-BAND', color='orange')
plt.axhline(y=10, color='orange', linestyle='dashed', label='QPSK for a BER 1E5 requires SNR 10')
plt.axhline(y=10+Implementation_losses+3, color='red', linestyle='dashed', label='DOWNLINK MARGIN>3dB)')

plt.title('Expected SNRs SBAND DOWNLINK')
plt.xlabel('Elevation angles (degrees)')
plt.ylabel('SNR (dB)')
plt.legend()
plt.grid()
plt.show()

plt.plot(180 * phi / np.pi, snr_U, label=f'{f0_U/1e6} MHz UHF-BAND', color='blue')
plt.axhline(y=20, color='blue', linestyle='dashed', label='GMSK for a BER 1E5 requires SNR 20')
plt.axhline(y=20+Implementation_losses+3, color='red', linestyle='dashed', label='DOWNLINK MARGIN>3dB)')

plt.title('Expected SNRs UHF DOWNLINK')
plt.xlabel('Elevation angles (degrees)')
plt.ylabel('SNR (dB)')
plt.legend()
plt.grid()
plt.show()

plt.plot(180 * phi / np.pi, snr_U, label=f'{f0_U/1e6} MHz UHF-BAND', color='blue')
plt.axhline(y=20, color='blue', linestyle='dashed', label='GMSK for a BER 1E5 requires SNR 20')
plt.axhline(y=20+Implementation_losses+3, color='red', linestyle='dashed', label='UPLINK MARGIN>3dB)')

plt.title('Expected SNRs UHF UPLINK')
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
    ("BIT RATE DOWNLINK (bps)", B_S, B_U),
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



# ---------------------------- # PLOTS # ---------------------------- #

## DOWNLINK SCIENCE  ## S-BAND ISIS-TXS2-DSH-0001, version 2.2 
f0_S1 = 2.245e9    # f0 - carrier frequency (Hz)
Pt_S1 = 1          # Pt - transmitted power (Watts)   
Gt_S1 = 6.5        # Gt - transmit antenna gain (dBi) 
Gr_S1 = 40         # Gr - receive antenna gain  (dBi) 35.4
B_S1 =  4.0e6      # B - transmit bandwidth (bps) QPSK, RS(255, 2223)  +  C(7, 1/2) for a BER 1E-5 -> MAX 4.3Mbps
Tnoise_S1 = 1000   # Tnoise - noise temperature (K)
eta_t_S1 = 0       # eta_t - transmit feeder gain (dB)
eta_r_S1 = 1       # eta_r - receive feeder gain (dB)
Lt_S1 = 1          # Lt - transmiter feeder loss (dB)
Lr_S1 = 1          # Lr - receiver feeder loss (dB) 
Ladd_S1 = 2        # Ladd - additional losses (dB)
gamma_S1 = 1.002   # gamma - receiver noise bandwith constant

## DOWNLINK SCIENCE  ## S-BAND ISIS-TXS2-DSH-0001, version 2.2 
f0_S2 = 2.245e9    # f0 - carrier frequency (Hz)
Pt_S2 = 1          # Pt - transmitted power (Watts)   
Gt_S2 = 6.5        # Gt - transmit antenna gain (dBi) 
Gr_S2 = 40         # Gr - receive antenna gain  (dBi) 35.4
B_S2 =  3.0e6      # B - transmit bandwidth (bps) QPSK, RS(255, 2223)  +  C(7, 1/2) for a BER 1E-5 -> MAX 4.3Mbps
Tnoise_S2 = 1000   # Tnoise - noise temperature (K)
eta_t_S2 = 0       # eta_t - transmit feeder gain (dB)
eta_r_S2 = 1       # eta_r - receive feeder gain (dB)
Lt_S2 = 1          # Lt - transmiter feeder loss (dB)
Lr_S2 = 1          # Lr - receiver feeder loss (dB) 
Ladd_S2 = 2        # Ladd - additional losses (dB)
gamma_S2 = 1.002   # gamma - receiver noise bandwith constant

## DOWNLINK SCIENCE  ## S-BAND ISIS-TXS2-DSH-0001, version 2.2 
f0_S3 = 2.245e9    # f0 - carrier frequency (Hz)
Pt_S3 = 1          # Pt - transmitted power (Watts)   
Gt_S3 = 6.5        # Gt - transmit antenna gain (dBi) 
Gr_S3 = 40         # Gr - receive antenna gain  (dBi) 35.4
B_S3 =  2.0e6      # B - transmit bandwidth (bps) QPSK, RS(255, 2223)  +  C(7, 1/2) for a BER 1E-5 -> MAX 4.3Mbps
Tnoise_S3 = 1000   # Tnoise - noise temperature (K)
eta_t_S3 = 0       # eta_t - transmit feeder gain (dB)
eta_r_S3 = 1       # eta_r - receive feeder gain (dB)
Lt_S3 = 1          # Lt - transmiter feeder loss (dB)
Lr_S3 = 1          # Lr - receiver feeder loss (dB) 
Ladd_S3 = 2        # Ladd - additional losses (dB)
gamma_S3 = 1.002   # gamma - receiver noise bandwith constant


snr_S1, EIRP_S1 = l_d.expected_snr(f0_S1, Pt_S1, Gt_S1, Gr_S1, B_S1, Tnoise_S1,eta_t_S1,eta_r_S1, Lt_S1, Lr_S1, Ladd_S1, gamma_S1)
snr_S2, EIRP_S2 = l_d.expected_snr(f0_S2, Pt_S2, Gt_S2, Gr_S2, B_S2, Tnoise_S2,eta_t_S2,eta_r_S2, Lt_S2, Lr_S2, Ladd_S2, gamma_S2)
snr_S3, EIRP_S3 = l_d.expected_snr(f0_S3, Pt_S3, Gt_S3, Gr_S3, B_S3, Tnoise_S3,eta_t_S3,eta_r_S3, Lt_S3, Lr_S3, Ladd_S3, gamma_S3)


phi = np.pi*np.array(range(0,181,5))/180
plt.plot(180 * phi / np.pi, snr_S1, label=f'{B_S1/1e6} Mbps - 2.245GHz S-BAND', color='orange')
plt.plot(180 * phi / np.pi, snr_S2, label=f'{B_S2/1e6} Mbps - 2.245GHz S-BAND', color='blue')
plt.plot(180 * phi / np.pi, snr_S3, label=f'{B_S3/1e6} Mbps - 2.245GHz S-BAND', color='yellow')
plt.axhline(y=10, color='pink', linestyle='dashed', label='QPSK for a BER 1E5 requires SNR 10')
plt.axhline(y=10+Implementation_losses+3, color='red', linestyle='dashed', label='DOWNLINK MARGIN>3dB)')

plt.title('Expected SNRs SBAND DOWNLINK')
plt.xlabel('Elevation angles (degrees)')
plt.ylabel('SNR (dB)')
plt.legend()
plt.grid()
plt.show()