import numpy as np
import matplotlib.pyplot as plt

def stress_profile(bases, gammas, k0, gw, gamma_w=9.81, q=0):
    """
    Calculate profile of vertical and horizontal stresses
    in a soil mass consisting of a number of horizontal layers.
    The ground surface is at depth 0, and the layers are
    defined by their bases' depths, gammas and k0 arrays.
    Input:
    bases: array of layer bases' depths in meters
    gammas: array of layer unit weights in kN/m3
    k0: effective coefficient of earth pressure at rest,
        input an array of zeros if no horizontal stress is required
    gw: groundwater level in meters
    gamma_w: unit weight of water, kN/m3
    q: surcharge load in kN/m2
    """
    
    # Check if the input arrays have the same length
    if len(bases) != len(gammas) or len(bases) != len(k0):
        print("Error: The input arrays must have the same length")
        return

    # Number of layers
    n = len(bases)
    
    # Initialize arrays
    sz_total = np.zeros(n+1) # total vertical stress
    u = np.zeros(n+1) # pore water pressure
    sz_eff = np.zeros(n+1) # effective vertical stress
    sx_eff = np.zeros(n+1) # effective horizontal stress
    sx_total = np.zeros(n+1) # total horizontal stress
    # Add surcharge to the top layer
    sz_total[0] = q
    sz_eff[0] = q
    if k0[0] > 0:
        sx_eff[0] = k0[0] * q
        sx_total[0] = k0[0] * q
    
    # insert 0 at start of bases since the ground surface is at depth 0
    bases = np.insert(bases, 0, 0)
    
    # Calculate stresses
    for i in range(n):
        # total vertical stress at the base of the layer
        sz_total[i+1] = sz_total[i] + gammas[i]*(bases[i+1] - bases[i])
        # pore water pressure at the base of the layer
        if bases[i+1] > gw:
            u[i+1] = gamma_w*(bases[i+1] - gw)
        # effective vertical stress at the base of the layer      
        sz_eff[i+1] = sz_total[i+1] - u[i+1]
        # if horizontal stress is required
        if k0[i] > 0:
            # effective horizontal stress at the base of the layer
            sx_eff[i+1] = k0[i] * sz_eff[i+1]
            # total horizontal stress at the base of the layer
            sx_total[i+1] = sx_eff[i+1] + u[i+1]

    # print results, with 2 decimal places
    if k0[0] > 0:
        print("Depth (m)  σ_z (kPa)  u (kPa)  σ_z' (kPa)  σ_x' (kPa)  σ_x (kPa)")
        print('------------------------------------------------------------------')
    else:
        print("Depth (m)  σ_z (kPa)  u (kPa)  σ_z' (kPa)")
        print('------------------------------------------')
    for i in range(n+1):
        if k0[0] > 0:
            print(f'{bases[i]:6.2f} {sz_total[i]:10.2f} {u[i]:10.2f} '
                  f'{sz_eff[i]:10.2f} {sx_eff[i]:10.2f} {sx_total[i]:10.2f}')
        else:
            print(f'{bases[i]:6.2f} {sz_total[i]:10.2f} {u[i]:10.2f} {sz_eff[i]:10.2f}')

    # curves to plot
    n_curves = 3
    curves = [sz_total, u, sz_eff]
    titles = ['Total vertical stress (kPa)', 'Pore water pressure (kPa)', 
              'Effective vertical stress (kPa)']
    if k0[0] > 0:
        n_curves = 5
        curves.extend([sx_eff, sx_total])
        titles.extend(['Effective horizontal stress (kPa)', 
                       'Total horizontal stress (kPa)'])
    
    # Make a figure the different curves side by side
    fig, ax = plt.subplots(1, n_curves, figsize=(12, 6))
    # round the maximum value of the curves to the nearest 10
    rounded_num = np.ceil(max(curves[0]) / 10) * 10
        
    for i in range(n_curves):
        ax[i].plot(curves[i], bases, 'b-', marker='o', 
                   markerfacecolor='red', markeredgecolor='red')
        ax[i].grid(True)
        ax[i].set_xlabel(titles[i])
        ax[i].xaxis.set_label_position('top')
        ax[i].xaxis.tick_top()
        ax[i].set_xlim([0, rounded_num])
        if i == 0:
            ax[i].set_ylabel('Depth (m)')
        ax[i].set_ylim([bases[-1]+1, bases[0]])
        
    # avoid overlap of the subplots
    fig.tight_layout()

    plt.show()