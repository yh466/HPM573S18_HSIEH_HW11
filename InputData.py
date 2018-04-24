import numpy as np

POP_SIZE = 2000     # cohort population size
SIM_LENGTH = 15     # length of simulation (years)
ALPHA = 0.05        # significance level for calculating confidence intervals
DISCOUNT = 0.03     # annual discount rate

DELTA_T = 1/52       # years (length of time step, how frequently you look at the patient)

# transition rate calculations
# Part 1: non-stroke associated annual mortality rate
mu = -np.log(1-(18*100 - 36.2)/100000)

# Part 2: annual rate of stroke events
stroke_rate = -np.log(1-15/1000)

# Part 3: annual rate of transition from 'Well' to 'Stroke'
lambda1 = stroke_rate*0.9
#         annual rate of transition from 'Well' to 'Stroke Death'
lambda2 = stroke_rate*0.1

# Part 4: annual rate of recurrent stroke events
recur_stroke_rate = -np.log(1-0.17)/5

# Part 5: annual rate of transition from 'Post-stroke' to 'Stroke'
sigma1= recur_stroke_rate*0.8
#         annual rate of transition from 'Post-stroke' to 'Stroke Death'
sigma2= recur_stroke_rate*0.2

# Part 6: annual rate of transition from 'Stroke' to 'Post-stroke'
rho = 1/(1/52)

# transition rate matrix
TRANS_MATRIX = [
    [None,  lambda1,    0.0,    lambda2,      mu],   # Well
    [0.0,     None,    rho,        0.0,       mu],   # Stroke
    [0.0,   sigma1,    None,     sigma2,      mu],   # Post-Stroke
    [0.0,     0.0,      0.0,       None,     0.0],   # Stroke Death
    [0.0,     0.0,       0.0,       0.0,    None],   # Background Death
    ]


# anticoagulation relative risk in reducing stroke incidence and stroke death while in “Post-Stroke”
RR_STROKE = 0.75
# anticoagulation relative risk in increasing mortality due to bleeding is 1.05.
RR_BLEEDING = 1.05

# transition rate matrix
TRANS_MATRIX_ANTICOAG = [
    [None,           lambda1,       0.0,    lambda2,                  mu],   # Well
    [0.0,               None,       rho,        0.0,                  mu],   # Stroke
    [0.0,   sigma1*RR_STROKE,      None,     sigma2,      mu*RR_BLEEDING],   # Post-Stroke
    [0.0,                0.0,       0.0,       None,                 0.0],
    [0.0,                0.0,       0.0,        0.0,                None],
    ]

# annual cost of each health state
ANNUAL_STATE_COST = [
    0,        # Well
    5000.0,   # Stroke
    200.0,     # Post-Stroke
    0,        # stroke death
    0         # background death
    ]

# annual health utility of each health state
ANNUAL_STATE_UTILITY = [
    1,        # Well
    0.8865,   # Stroke
    0.9,       # Post-Stroke
    0,         # stroke death
    0          # background death
    ]

# annual drug costs
Anticoagulant_COST = 2000.0


# annual probability of background mortality (number per 100,000 PY)
ANNUAL_PROB_BACKGROUND_MORT = (18*100-36.2)/100000


