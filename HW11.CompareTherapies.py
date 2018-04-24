import ParameterClasses as P
import MarkovModelClasses as MarkovCls
import SupportMarkovModel as SupportMarkov


# NO ANTICOAGULANT
# create a cohort
cohort_none = MarkovCls.Cohort(
    id=0,
    therapy=P.Therapies.NONE)
# simulate the cohort
simOutputs_none = cohort_none.simulate()

# ANTICOAGULANT
# create a cohort
cohort_anticoag = MarkovCls.Cohort(
    id=1,
    therapy=P.Therapies.ANTICOAG)
# simulate the cohort
simOutputs_anticoag = cohort_anticoag.simulate()

## draw survival curves and histograms
SupportMarkov.draw_survival_curves_and_histograms(simOutputs_none, simOutputs_anticoag)

## print the estimates
SupportMarkov.print_outcomes(simOutputs_none, "No Anticoagulant:")
SupportMarkov.print_outcomes(simOutputs_anticoag, "Anticoagulant:")
print('   ')

## print comparative outcomes
SupportMarkov.print_comparative_outcomes(simOutputs_none, simOutputs_anticoag)
print('  ')

## report the CEA results
SupportMarkov.report_CEA_CBA(simOutputs_none, simOutputs_anticoag)
print('When the estimates of cost and utility are based on 2000 simulated patietns,'
      'the confidence interval of the net monetary benefit curve is too wide to make a recommendation.'
      'Increasing the number of simulated patients to 20,000 or larger would provide sufficient confidence'
      'to recommend adopting anticoagulant if the decision makers willingness to pay is at least #23 000 per QALY gained.')

