""" Data exploration and preprocessing for the electric dataset

TODO: maybe abstract the read_table for electric to a "load_electric_data function in utils"
"""
import pandas as pd

from utils.utils import *
from utils.plot_utils import *


def main():
    """
    """
    # Electric data
    data_dir = "./data/electric_wide.txt"
    
    data = pd.read_table(data_dir, header=0, sep="\s+", names=["city", "grade",  "treated_pretest", "treated_posttest", "control_pretest",  "control_posttest", "supplement"])

    # Computing the correlation for every grade and plotting as in figure 18.2
    correlations = {}
    correlations["treated_correlation"] = data.groupby("grade")[["treated_pretest","treated_posttest"]].corr().iloc[0::2]["treated_posttest"].values
    correlations["control_correlation"] = data.groupby("grade")[["control_pretest","control_posttest"]].corr().iloc[0::2]["control_posttest"].values
    
    electric_line_plot(correlations, "./results/plots/fig_18_2.png")

    # Setting the variables for input in STAN
    stan_data = {
        "N": data.shape[0],
        "treated_pretest": data.treated_pretest.values,
        "treated_posttest": data.treated_posttest.values,
        "control_pretest": data.control_pretest.values,
        "control_posttest": data.control_posttest.values,
        "city": pd.factorize(data.city)[0]+1,
        "supplement": pd.factorize(data.supplement)[0]+1,
        "grade": data.grade.values,
    }

    # Saving
    data_saving(stan_data, "./data/electric_stan_data.pkl")


if __name__ == "__main__":
    main()