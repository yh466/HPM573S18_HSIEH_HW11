from enum import Enum
import numpy as np
import scipy.stats as stat
import math as math
import InputData as Data
import scr.MarkovClasses as MarkovCls
import scr.RandomVariantGenerators as Random


class HealthStats(Enum):
    """ health states of patients with HIV """
    WELL = 0
    STROKE = 1
    POST_STROKE = 2
    STROKE_DEATH = 3
    BACKGROUND_DEATH = 4


class Therapies(Enum):
    """ mono vs. combination therapy """
    NONE = 0
    ANTICOAG = 1


class ParametersFixed():
    def __init__(self, therapy):

        # selected therapy
        self._therapy = therapy

        # simulation time step
        self._delta_t = Data.DELTA_T

        # calculate the adjusted discount rate
        self._adjDiscountRate = Data.DISCOUNT*Data.DELTA_T

        # initial health state
        self._initialHealthState = HealthStats.WELL

        # annual treatment cost
        if self._therapy == Therapies.NONE:
            self._annualTreatmentCost = 0
        else:
            self._annualTreatmentCost = Data.Anticoagulant_COST

        # transition rate matrix of the selected therapy
        self._rate_matrix = []
        self._prob_matrix = []
        # treatment relative risk
        self._treatmentRR = 0

        # calculate transition probabilities depending of which therapy options is in use
        if therapy == Therapies.NONE:
            self._rate_matrix = Data.TRANS_MATRIX
            # convert rate to probability
            self._prob_matrix[:], p = MarkovCls.continuous_to_discrete(self._rate_matrix, Data.DELTA_T)
           # print('Upper bound on the probability of two transitions within delta_t:', p)
        else:
            self._rate_matrix = Data.TRANS_MATRIX_ANTICOAG
            self._prob_matrix[:], p = MarkovCls.continuous_to_discrete(self._rate_matrix, Data.DELTA_T)
           # print('Upper bound on the probability of two transitions within delta_t:', p)

        # annual state costs and utilities
        self._annualStateCosts = Data.ANNUAL_STATE_COST
        self._annualStateUtilities = Data.ANNUAL_STATE_UTILITY

    def get_initial_health_state(self):
        return self._initialHealthState

    def get_delta_t(self):
        return self._delta_t

    def get_adj_discount_rate(self):
        return self._adjDiscountRate

    def get_transition_prob(self, state):
        return self._prob_matrix[state.value]

    def get_annual_state_cost(self,state):
        if state == HealthStats.STROKE_DEATH or state == HealthStats.BACKGROUND_DEATH:
            return 0
        else:
            return  self._annualStateCosts[state.value]

    def get_annual_state_utility(self,state):
        if state == HealthStats.STROKE_DEATH or state == HealthStats.BACKGROUND_DEATH:
            return 0
        else:
            return self._annualStateUtilities[state.value]

    def get_annual_treatment_cost(self):
        return self._annualTreatmentCost


#def calculate_rate_matrix_anticoag():
#    """ :returns transition rate matrix under anticoagulation use"""
#
#    # create an empty matrix populated with zeroes
#    rate_matrix = []
#    for l in Data.TRANS_MATRIX:
#        rate_matrix.append([0] * len(l))
#
#        # for all health states
#        for s in HealthStats:
#            # if the current state is post-stroke
#            if s == HealthStats.POST_STROKE:
#                # post-stoke to stroke
#                rate_matrix[s.value][HealthStats.STROKE.value] \
#                    = Data.RR_STROKE * Data.TRANS_MATRIX[s.value][HealthStats.STROKE.value]
#                # post-stroke to non-stroke death
#                rate_matrix[s.value][HealthStats.BACKGROUND_DEATH.value] \
#                    = Data.RR_BLEEDING * Data.TRANS_MATRIX[s.value][HealthStats.BACKGROUND_DEATH.value]
#                rate_matrix[s.value][HealthStats.WELL.value]\
#                    = Data.TRANS_MATRIX[s.value][HealthStats.WELL.value]
#                rate_matrix[s.value][HealthStats.POST_STROKE.value]\
#                    = Data.TRANS_MATRIX[s.value][HealthStats.POST_STROKE.value]
#                rate_matrix[s.value][HealthStats.STROKE_DEATH.value] \
#                    = Data.TRANS_MATRIX[s.value][HealthStats.STROKE_DEATH.value]
#            else:
#                rate_matrix[s.value] = Data.TRANS_MATRIX[s.value]
#
#        return rate_matrix
