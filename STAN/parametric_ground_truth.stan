data{
    int<lower=1> N;
    vector[N] y;
    vector[N] x_1;
    vector[N] x_2;
    vector[N] z;
    array[1] real mu_b_0_u;
    array[1] real mu_b_1_u;
    array[1] real mu_b_2_u;
    array[1] real mu_b_0_y;
    array[1] real mu_b_1_y;
    array[1] real mu_b_2_y;
    array[1] real mu_b_u_y;
    array[1] real mu_b_z_y;
    array[1] real<lower=0> sd_priors;
}
parameters{
    real beta_0_y; 
    real beta_1_y;
    real beta_2_y;
    real beta_u_y;
    real beta_z_y;
    real<lower=0> sigma_y;
    
    real beta_0_u; 
    real beta_1_u;
    real beta_2_u; 
    real<lower=0> sigma_u;
    vector[N] u;
}
model { 
    beta_0_u ~ normal(mu_b_0_u, sd_priors);
    beta_1_u ~ normal(mu_b_1_u, sd_priors);
    beta_2_u ~ normal(mu_b_2_u, sd_priors);
    sigma_u ~ std_normal();

    beta_0_y ~ normal(mu_b_0_y, sd_priors);
    beta_1_y ~ normal(mu_b_1_y, sd_priors);
    beta_2_y ~ normal(mu_b_2_y, sd_priors);
    beta_u_y ~ normal(mu_b_u_y, sd_priors);
    beta_z_y ~ normal(mu_b_z_y, sd_priors);
    sigma_y ~ std_normal();
    
    for (n in 1:N){
        u[n] ~ normal(beta_0_u + beta_1_u*x_1[n] + beta_2_u*x_2[n], sigma_u);
        y[n] ~ normal(beta_0_y + beta_1_y*x_1[n] + beta_2_y*x_2[n] + beta_u_y*u[n] + beta_z_y*z[n], sigma_y); 
    }
} 
generated quantities { } 