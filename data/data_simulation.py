""" Module with that simulates the data from our assumed generative process to do inference.
"""
import pickle
from typing import Dict
from utils.utils import *

import stan


def main():
    """ 
    TODO: consider abstracting more the other elements of this function
    TODO: consider using argparse for this main
    """
    model_dir = "./STAN/data_generation.stan"
    data_dir = "./data/simulated_data.pkl"
    
    model_definition = load_model(model_dir)
    
    simulation_data = {"N": 500}
    posterior = stan.build(model_definition, data=simulation_data, random_seed=1)
    fit = posterior.fixed_param(num_samples=1)

    data_dictionary = {
        "y": fit["y"][:,0],
        "x_1": fit["x_1"][:,0],
        "x_2": fit["x_2"][:,0],
        "z": fit["z"][:,0],
        "u": fit["u"][:,0],
        "beta_0_y": fit["beta_0_y"][:,0],
        "beta_1_y": fit["beta_1_y"][:,0],
        "beta_2_y": fit["beta_2_y"][:,0],
        "beta_u_y": fit["beta_u_y"][:,0],
        "beta_z_y": fit["beta_z_y"][:,0],
        "sigma_y": fit["sigma_y"][:,0],
        "beta_0_u": fit["beta_0_u"][:,0],
        "beta_1_u": fit["beta_1_u"][:,0],
        "beta_2_u": fit["beta_2_u"][:,0], 
        "sigma_u": fit["sigma_u"][:,0],
    }

    data_saving(data_dictionary, data_dir)


if __name__ == "__main__":
    main()