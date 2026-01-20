import numpy as np
import matplotlib.patches as patches

def grain_size_chart(fig, ax, English=False):
    """
    Draw grain size chart as in Aarhaug (1991), 
    Geoteknikk og fundamenteringslære 1
    INPUT:
        fig : matplotlib figure
        ax  : matplotlib axes
        English : bool, optional
            If True, use English labels
            If False, use Norwegian labels (default)
    OUTPUT:
        None (the function modifies the input axes)
    """
    # ---------------- LANGUAGE ----------------
    labels = {1:"Passert i %", 2:"Rest på i %", 3:"U.S. Standard sikt",
              4:"LEIR", 5:"SILT", 6:"SAND", 7:"GRUS", 8:"STEIN",
              9:"Fin", 10:"Middels", 11:"Grov"}
    if English:
        labels = {1:"% Passing", 2:"% Retained", 3:"U.S. Standard Sieve",
                  4:"CLAY", 5:"SILT", 6:"SAND", 7:"GRAVEL", 8:"COBBLES",
                  9:"Fine", 10:"Medium", 11:"Coarse"}

    # ---------------- AXES LIMITS ----------------
    ax.set_xscale("log")
    ax.set_xlim(0.0008, 120)
    ax.set_ylim(0, 100)

    # ---------------- Y-AXIS (%) ----------------
    por_ticks = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    por_labels = ["0", "10", "20", "30", "40", "50", 
                "60", "70", "80", "90", "100"]

    # Axis labels
    ax.set_ylabel(labels[1], fontsize=11)
    ax.set_yticks(por_ticks)
    ax.set_yticklabels(por_labels, fontsize=9)

    # Right-side axis (Retained %)
    ax2y = ax.twinx()
    ax2y.set_ylim(100, 0)
    ax2y.set_ylabel(labels[2], fontsize=11)
    ax2y.set_yticks(por_ticks)
    ax2y.set_yticklabels(por_labels, fontsize=9)

    # ---------------- MAIN X-AXIS (mm) ----------------
    mm_ticks = [0.001, 0.002, 0.006, 0.01, 0.02, 0.06,
                0.1, 0.2, 0.6, 1, 2, 6,
                10, 20, 60, 120]
    mm_labels = ["0.001", "0.002", "0.006", "0.01", "0.02", 
                "0.06", "0.1", "0.2", "0.6", "1", "2", "6",
                "10", "20", "60", "mm"]
    ax.set_xticks(mm_ticks)
    ax.set_xticklabels(mm_labels, fontsize=9)

    # Grid lines
    ax.grid(which='both', linestyle='-', linewidth=0.5, color='black')
    # add two vertical grid lines at x = 100 and 110
    ax.axvline(100, color='black', linestyle='-', linewidth=0.5)
    ax.axvline(110, color='black', linestyle='-', linewidth=0.5)

    # ---------------- TICK VERTICAL BLACK LINES AT SOIL DIVISIONS ----------------
    soil_divisions = [0.002, 0.06, 2, 60]
    for x in soil_divisions:
        ax.axvline(x, color="black", linewidth=1.5)

    # ---------------- DASHED VERTICAL LINES AT SIKT VALUES ----------------
    sieve_mm = [0.075, 0.15, 0.3, 0.6, 1.18, 2.36,
                4.75, 9.5, 19.0, 37.5, 75.0, 120]
    sieve_labels = ['0.074', '0.149', '0.297', '0.59', '1.19', 
                    '2.38', '4.76', '9.52', '19.04', '38.1', 
                    '76.2', 'mm']
    for x in sieve_mm:
        ax.axvline(x, color="black", linestyle="--", linewidth=0.8)
    # add another one for sieve 40 (0.425 mm)
    ax.axvline(0.425, color="black", linestyle="--", linewidth=0.8)

    # ---------------- BOTTOM ROW (U.S. sieve openings in mm) ----------------
    ax_bottom = ax.secondary_xaxis('bottom')
    ax_bottom.set_xscale('log')
    ax_bottom.set_xlim(ax.get_xlim())
    ax_bottom.set_xticks(sieve_mm)
    ax_bottom.set_xticklabels(sieve_labels, fontsize=9)
    ax_bottom.spines['bottom'].set_position(('outward', 20))
    # remove bottom axis and ticks
    ax_bottom.spines['bottom'].set_visible(False)
    ax_bottom.tick_params(axis='x', which='both', length=0)

    # ---------------- TOP AXIS: U.S. STANDARD SIEVE ----------------
    ax2 = ax.twiny()
    ax2.set_xscale("log")
    ax2.set_xlim(ax.get_xlim())
    sieve_mm = [0.006, 0.075, 0.15, 0.3, 0.425, 0.6, 1.18, 2.36,
                4.75, 9.5, 19.0, 37.5, 75.0]
    sieve_labels = [labels[3],"200", "100", "50", "40", 
                    "30", "16", "8", "4", '3/8"', '3/4"', '1.5"', 
                    '3"']
    ax2.set_xticks(sieve_mm)
    ax2.set_xticklabels(sieve_labels, fontsize=9)
    ax2.xaxis.set_label_coords(0.5, 1.08)

    # ---------------- HEADER BOXES ----------------
    bbox = ax.get_position()
    band_height = 0.18
    band_y = bbox.y1 - 0.03
    ax_band = fig.add_axes([bbox.x0, band_y, bbox.width, band_height], sharex=ax)
    ax_band.set_xlim((0.0008, 120))
    ax_band.set_ylim(0, 1)
    ax_band.axis("off")

    # Main soil classes (LEIR, SILT, SAND, GRUS, STEIN)
    classes = [
        (0.0008, 0.002, labels[4]),
        (0.002, 0.06,  labels[5]),
        (0.06,  2.0,   labels[6]),
        (2.0,   60.0,  labels[7]),
        (60.0,  120.0, labels[8]),
    ]
    # draw rectangles and text
    for x0, x1, label in classes:
        rect = patches.Rectangle((x0, 0.45), x1 - x0, 0.5, linewidth=1.2, 
                                fill=False, edgecolor="black")
        ax_band.add_patch(rect)
        if label == labels[4] or label == labels[8]:
            ax_band.text(np.sqrt(x0 * x1), 0.72, label, ha="center",
                    va="center", fontsize=9, fontweight="bold")
        else:
            ax_band.text(np.sqrt(x0 * x1), 0.82, label, ha="center",
                    va="center", fontsize=9, fontweight="bold")
    # trace a horizontal line at the middle of the band from 0.002 to 60
    ax_band.hlines(0.7, 0.002, 60, colors="black", linewidth=0.8)

    # Subdivisions (Fin, Middels, Grov)
    subdivs = [
        (0.002, 0.006,  labels[9]),
        (0.006,  0.02,  labels[10]),
        (0.02,  0.06,  labels[11]),
        (0.06,  0.2,   labels[9]),
        (0.2,   0.6,   labels[10]),
        (0.6,   2.0,   labels[11]),
        (2.0,   6.0,   labels[9]),
        (6.0,   20.0,  labels[10]),
        (20.0,  60.0,  labels[11]),
    ]
    # draw rectangles and text 
    for x0, x1, label in subdivs:
        rect = patches.Rectangle((x0, 0.45), x1 - x0, 0.25, linewidth=0.8, 
                                fill=False, edgecolor="black")
        ax_band.add_patch(rect)
        ax_band.text(np.sqrt(x0 * x1), 0.575, label, ha="center",
                    va="center", fontsize=9)
