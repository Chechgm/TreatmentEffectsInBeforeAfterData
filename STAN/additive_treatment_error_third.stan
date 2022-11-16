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
    
    array[N] real alpha_treated; // alpha_{j} in the paper, per unit Constant
    array[N] real alpha_control;
    
    // We can either have a common hyperprior for the alpha treated and the alpha control
    // or a hyper prior that depends on the treatment status:
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

    //real gamma_one_mean;
    //real<lower=0> gamma_one_sigma;
    //array[N] real gamma_one; // per unit Extra component after, here we have hyperprior
    // An option is to constraint gamma_one to be positive, since this is our hypothesis
    //array[N] real<lower=0> gamma_one; // per unit Extra component after, here we have hyperprior
    
    real<lower=0> sigma_zero; // Variance before
    real<lower=0> sigma_one; // Variance after
    real<lower=0> sigma_treated; // Additional variance for treated units
}
model { 
    theta ~ std_normal();

    alpha_mu ~ normal(0, 1);
    alpha_sigma ~ normal(0, 1);
    alpha_treated ~ normal(alpha_mu, alpha_sigma);
    alpha_control ~ normal(alpha_mu, alpha_sigma);
    
    b_city_zero ~ std_normal();
    b_grade_zero ~ std_normal();
    b_supplement_zero ~ std_normal();

    b_city_one ~ std_normal();
    b_grade_one ~ std_normal();
    b_supplement_one ~ std_normal();
    
    //gamma_one_mean ~ std_normal();
    //gamma_one_sigma ~ std_normal();
    //gamma_one ~ normal(gamma_one_mean, gamma_one_sigma);
    
    sigma_zero ~ std_normal();
    sigma_one ~ std_normal();
    sigma_treated ~ std_normal();

    for(n in 1:N) {
        target += normal_lpdf(treated_pretest[n] | 
                    alpha_treated[n] + b_city_zero[city[n]] + b_grade_zero[grade[n]] + b_supplement_zero[supplement[n]], 
                    sigma_zero);
        target += normal_lpdf(treated_posttest[n] | 
                    alpha_treated[n] + theta + b_city_one[city[n]] + b_grade_one[grade[n]] + b_supplement_one[supplement[n]], 
                    sigma_one+sigma_treated);
        target += normal_lpdf(control_pretest[n] | 
                    alpha_control[n] + b_city_zero[city[n]] + b_grade_zero[grade[n]] + b_supplement_zero[supplement[n]], 
                    sigma_zero);
        target += normal_lpdf(control_posttest[n] | 
                    alpha_control[n] + b_city_one[city[n]] + b_grade_one[grade[n]] + b_supplement_one[supplement[n]],
                    sigma_one);
    }
} 
generated quantities {
    array[N] real control_pre;
    array[N] real control_post;
    array[N] real treatment_pre;
    array[N] real treatment_post;

    for(n in 1:N) {
        treatment_pre[n] = normal_rng(alpha_treated[n] + b_city_zero[city[n]] + b_grade_zero[grade[n]] + b_supplement_zero[supplement[n]], 
                    sigma_zero);
        treatment_post[n] = normal_rng(alpha_treated[n] + theta + b_city_one[city[n]] + b_grade_one[grade[n]] + b_supplement_one[supplement[n]],
                    sigma_one+sigma_treated);
        control_pre[n] = normal_rng(alpha_control[n] + b_city_zero[city[n]] + b_grade_zero[grade[n]] + b_supplement_zero[supplement[n]], 
                    sigma_zero);
        control_post[n] = normal_rng(alpha_control[n] + b_city_one[city[n]] + b_grade_one[grade[n]] + b_supplement_one[supplement[n]],
                    sigma_one);
    }
} 