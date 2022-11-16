""" This module contains the pipeline to fit the models to the data.
"""
import numpy as np

import arviz as az
import stan

from utils.utils import *
from utils.plot_utils import *


def vectorized_correlation(x, y):
    """ Computes the correlation between the two vectors
    
    The input is of shape (individual vector length, number of repetitions)
    The output is of shape (number of repetitions)
    """
    n = x.shape[0]
    deviations_x = x - (np.einsum('ij->j',x) / n)
    deviations_y = y - (np.einsum('ij->j',y) / n)
    squared_deviations_x = np.einsum('ij,ij->j', deviations_x, deviations_x)
    squared_deviations_y = np.einsum('ij,ij->j', deviations_y, deviations_y)
    
    return np.einsum('ij,ij->j', deviations_x, deviations_y) / np.sqrt(np.einsum('j,j->j', squared_deviations_x, squared_deviations_y))


def electric_correlation(x, y, grade):
    """ Estimate the posterior correlation per grade for the electric company data
    """
    grades = np.unique(grade)
    correlation_dict = {}
    correlation_dict["lower"] = []
    correlation_dict["median"] = []
    correlation_dict["upper"] = []
    
    for g in grades:
        idx = np.where(grade==g)[0]
        x_tmp = x[idx, :]
        y_tmp = y[idx, :]
        correlation_dict[g] = vectorized_correlation(x_tmp, y_tmp)
        low, median, upper = np.quantile(correlation_dict[g], [0.1, 0.5, 0.9])
        correlation_dict["lower"].append(low)
        correlation_dict["median"].append(median)
        correlation_dict["upper"].append(upper)

    return correlation_dict


def main():
    """ 
    TODO: consider abstracting more the other elements of this function
    TODO: consider using argparse for this main
    TODO: Consider taking the model as argument to this function and making a directory for each model
    """
    #model = "additive_treatment_error"
    model = "additive_treatment_error_third"
    model_dir = f"./STAN/{model}.stan"
    data_dir = "./data/electric_stan_data.pkl"
    results_dir = f"./results/{model}_posterior.pkl"

    electric_data = pkl_loading(data_dir)
    model_definition = load_model(model_dir)
    
    posterior = stan.build(model_definition, data=electric_data, random_seed=2)
    fit = posterior.sample(num_chains=4, num_samples=500)

    data_dictionary = {
        "control_pre": fit["control_pre"],
        "control_post": fit["control_post"],
        "treatment_pre": fit["treatment_pre"],
        "treatment_post": fit["treatment_post"],
    }

    control_posterior_correlation = electric_correlation(data_dictionary["control_pre"], 
                                                        data_dictionary["control_post"], 
                                                        electric_data["grade"])
    treatment_posterior_correlation = electric_correlation(data_dictionary["treatment_pre"], 
                                                        data_dictionary["treatment_post"], 
                                                        electric_data["grade"])
    
    data_saving(data_dictionary, results_dir)

    # Saving the posterior table
    # Full list of variables of interest. Use as needed
    # var_names = ["alpha_treated_mu", "alpha_treated_sigma",
    #             "alpha_control_mu", "alpha_control_sigma", 
    #             "alpha_mu", "alpha_sigma", "theta", 
    #             "gamma_one_mean", "gamma_one_sigma",
    #             "b_city_zero", "b_grade_zero", "b_supplement_zero",
    #             "b_city_one", "b_grade_one", "b_supplement_one",
    #             "sigma_zero", "sigma_one", "sigma_treated"]
    var_names = ["alpha_mu", "alpha_sigma", "theta",
                "b_city_zero", "b_grade_zero", "b_supplement_zero",
                "b_city_one", "b_grade_one", "b_supplement_one",
                "sigma_zero", "sigma_one", "sigma_treated"]
    parameter_summary = az.summary(fit, var_names=var_names)[["mean", "sd", "ess_bulk", "ess_tail", "r_hat"]]
    with open(f"./results/table_{model}.txt", "w") as f:
        f.write(parameter_summary.to_latex())

    # Plotting the correlation between control pre and posttest
    electric_posterior_line_plot(treatment_posterior_correlation, 
                                control_posterior_correlation,
                                f"./results/plots/posterior_line_plot_{model}.png")
    
    print("hi")


if __name__ == "__main__":
    main()
