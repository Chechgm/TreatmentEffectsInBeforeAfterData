""" This module contains the required functions to explore the data.

Available functions:
- scatter
- density
- posterior_vs_true

sns.plotting_context("paper", rc={"font.size": 15, "axes.titlesize": 15,
                                           "axes.labelsize": 15, "legend.fontsize": 12,
                                           "lines.markersize": 8, "xtick.labelsize": 10,
                                           "ytick.labelsize": 10}):
"""
from typing import Dict
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np


def electric_line_plot(data: Dict, save_directory: str):
    """ Reproduces Figure 18.2 of the paper
    """
    x = np.arange(1, 5)

    with plt.style.context('ggplot'):
        fig, ax = plt.subplots()
        ax.plot(x, data["treated_correlation"], linestyle="-")
        ax.plot(x, data["control_correlation"], linestyle="--")

        ax.text(3.65, 0.8, "treated")
        ax.text(3.65, 1, "controls")

        ax.set_ylim(bottom=0.78, top=1.01)
        ax.set_xlabel("grade")
        ax.set_ylabel("correlation")

        ax.set_xticks(x)
        ax.set_yticks([0.8, 0.9, 1])

        plt.savefig(save_directory, bbox_inches="tight", dpi=300)
        plt.close()
