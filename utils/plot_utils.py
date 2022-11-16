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

    with plt.style.context('seaborn-v0_8-paper'):
        fig, ax = plt.subplots()
        ax.plot(x, data["treated_correlation"], linestyle="-", color="#AFC840")
        ax.plot(x, data["control_correlation"], linestyle="--", color="#123C52")

        ax.text(3.65, 0.8, "treated", color="#AFC840")
        ax.text(3.65, 1, "controls", color="#123C52")

        ax.set_ylim(bottom=0.78, top=1.01)
        ax.set_xlabel("grade")
        ax.set_ylabel("correlation")

        ax.set_xticks(x)
        ax.set_yticks([0.8, 0.9, 1])

        plt.savefig(save_directory, bbox_inches="tight", dpi=300)
        plt.close()


def electric_posterior_line_plot(treatment_dict: Dict, control_dict: Dict, save_directory: str):
    """ Reproduces Figure 18.2 of the paper for the posterior of inference
    """
    x = np.arange(1, 5)

    with plt.style.context('seaborn-v0_8-paper'):
        fig, ax = plt.subplots()
        ax.text(3.5, 0.4, "treated", color="#AFC840")
        ax.text(3.5, 0.6, "controls", color="#B6DCF0")

        ax.plot(x, treatment_dict["median"], linestyle="-", color="#AFC840")
        ax.fill_between(x, treatment_dict["lower"], treatment_dict["upper"], color="#DAEB91", alpha=.4)

        ax.plot(x, control_dict["median"], linestyle="-", color="#8DBDD6")
        ax.fill_between(x, control_dict["lower"], control_dict["upper"], color="#CFECFA", alpha=.4)

        ax.set_ylim(bottom=0, top=0.8)
        ax.set_xlabel("grade")
        ax.set_ylabel("correlation")

        ax.set_xticks(x)

        plt.savefig(save_directory, bbox_inches="tight", dpi=300)
        plt.close()
