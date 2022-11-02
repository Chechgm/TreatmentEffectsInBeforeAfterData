""" This module contains the pipeline to fit the models to the data.
"""
import numpy as np

import arviz as az
import stan

from utils.utils import *


def main():
    """ 
    TODO: consider abstracting more the other elements of this function
    TODO: consider using argparse for this main
    TODO: Consider taking the model as argument to this function and making a directory for each model
    """
    model = "additive_treatment_error"
    model_dir = f"./STAN/{model}.stan"
    data_dir = "./data/electric_stan_data.pkl"
    #results_dir = f"./results/{model}_posterior.pkl"

    electric_data = pkl_loading(data_dir)
    model_definition = load_model(model_dir)
    
    posterior = stan.build(model_definition, data=electric_data, random_seed=2)
    fit = posterior.sample(num_chains=4, num_samples=500)

    # data_dictionary = {
    #     "u": fit["u"],
    #     "beta_0_y": fit["beta_0_y"],
    #     "beta_1_y": fit["beta_1_y"],
    #     "beta_2_y": fit["beta_2_y"],
    #     "beta_u_y": fit["beta_u_y"],
    #     "beta_z_y": fit["beta_z_y"],
    #     "sigma_y": fit["sigma_y"],
    #     "beta_0_u": fit["beta_0_u"],
    #     "beta_1_u": fit["beta_1_u"],
    #     "beta_2_u": fit["beta_2_u"],
    #     "sigma_u": fit["sigma_u"],
    # }

    # We want these variables in the summary: mean median sd rhat ess_bulk ess_tail [["mean", "sd", "ess_bulk", "ess_tail", "r_hat"]]
    # az.summary(fit, var_names=["alpha_mu", "alpha_sigma", "theta", "gamma_one_mean", "gamma_one_sigma"])[["mean", "sd", "ess_bulk", "ess_tail", "r_hat"]]
    
    #data_saving(data_dictionary, results_dir)

    # # Saving the posterior table TODO: consider packaging this into a function.
    # parameter_summary = az.summary(fit).head(10)
    # parameter_summary["true"] = 0
    # for i in parameter_summary.index:
    #     parameter_summary.loc[i, "true"] = np.round(simulated_data[i], 3)
    
    # with open(f"./results/table_{model}.txt", "w") as f:
    #     f.write(parameter_summary.to_latex())

    print("hi")


if __name__ == "__main__":
    main()
