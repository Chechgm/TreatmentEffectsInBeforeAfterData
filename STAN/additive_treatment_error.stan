data{
    int<lower=1> N; // Number of individuals
    array[N] real treated_pretest;
    array[N] real treated_posttest;
    array[N] real control_pretest;
    array[N] real control_posttest;
    array[N] int city;
    array[N] int supplement;
    array[N] int grade;
}
parameters{
    real theta; // Treatment effect 
    
    array[N] real alpha; // alpha_{j} in the paper, per unit Constant
    real alpha_mu; // Constant hyperprior
    real<lower=0> alpha_sigma; // Constant hyperprior
    
    // The following are beta_{0} in the paper
    array[2] real b_city_zero;
    array[4] real b_grade_zero;
    array[2] real b_supplement_zero;
    
    // The following are beta_{1} in the paper
    array[2] real b_city_one;
    array[4] real b_grade_one;
    array[2] real b_supplement_one;

    real gamma_one_mean;
    real<lower=0> gamma_one_sigma;
    array[N] real gamma_one; // per unit Extra component after, here we have hyperprior
    
    real<lower=0> sigma_zero; // Variance before
    real<lower=0> sigma_one; // Variance after
}
model { 
    theta ~ std_normal();

    alpha_mu ~ normal(0, 1);
    alpha_sigma ~ normal(0, 1);
    alpha ~ normal(alpha_mu, alpha_sigma);
    
    b_city_zero ~ std_normal();
    b_grade_zero ~ std_normal();
    b_supplement_zero ~ std_normal();

    b_city_one ~ std_normal();
    b_grade_one ~ std_normal();
    b_supplement_one ~ std_normal();
    
    gamma_one_mean ~ std_normal();
    gamma_one_sigma ~ std_normal();
    gamma_one ~ normal(gamma_one_mean, gamma_one_sigma);
    
    sigma_zero ~ std_normal();
    sigma_one ~ std_normal();

    for(n in 1:N) {
        target += normal_lpdf(treated_pretest[n] | 
                    alpha[n] + b_city_zero[city[n]] + b_grade_zero[grade[n]] + b_supplement_zero[supplement[n]], 
                    sigma_zero);
        target += normal_lpdf(treated_posttest[n] | 
                    alpha[n] + theta + gamma_one[n] + b_city_one[city[n]] + b_grade_one[grade[n]] + b_supplement_one[supplement[n]], 
                    sigma_one);
        target += normal_lpdf(control_pretest[n] | 
                    alpha[n] + b_city_zero[city[n]] + b_grade_zero[grade[n]] + b_supplement_zero[supplement[n]], 
                    sigma_zero);
        target += normal_lpdf(control_posttest[n] | 
                    alpha[n] + b_city_one[city[n]] + b_grade_one[grade[n]] + b_supplement_one[supplement[n]],
                    sigma_one);
    }
} 
generated quantities {} 