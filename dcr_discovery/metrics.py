"""This file contains modules to compute the metrics for a rule."""

import math


def get_categorical_OR(pairs_similar_instances,X,PATH_TREATMENT,PATH_OUTCOME,t0,t1):
    """
    For a categorical rule and associated treatment, returns distribution of its associated pairs.
    
    Here : a pair is having the treatment IF they have different values on the treatment path (one has t0, one has t1)
    """
    T_O,T_not_O,not_T_O,not_T_not_O = 0,0,0,0

    for pair_ in pairs_similar_instances:
        try:
            ti0,oi0 = get_treatment_and_outcome(X,pair_[0],PATH_TREATMENT,PATH_OUTCOME)
            ti1,oi1 = get_treatment_and_outcome(X,pair_[1],PATH_TREATMENT,PATH_OUTCOME)

            if ti0 == t0 and ti1 == t1:
                if oi0 > oi1:
                    T_O += 1
                else:
                    T_not_O += 1
            elif ti0 == t1 and ti1 == t0:
                if oi0 > oi1:
                    T_O += 1
                else:
                    T_not_O += 1
        except:
            pass
    return T_O,T_not_O,not_T_O,not_T_not_O


def get_categorical_values(pairs_similar_instances,X,PATH_TREATMENT,PATH_OUTCOME,t0,t1):
    """
    For a categorical rule and associated treatment, returns distribution of its associated pairs.
    """
    T_O,T_not_O,same_0 = 0,0,0

    for pair_ in pairs_similar_instances:
        try: # we already know that one instance has t0 and the other has t1
            ti0,oi0 = get_treatment_and_outcome(X,pair_[0],PATH_TREATMENT,PATH_OUTCOME)
            ti1,oi1 = get_treatment_and_outcome(X,pair_[1],PATH_TREATMENT,PATH_OUTCOME)

            if ti0 == t0 and ti1 == t1:
                if oi0 > oi1:
                    T_O += 1
                elif oi0 < oi1:
                    T_not_O += 1    
                else:
                    same_0 += 1
            elif ti0 == t1 and ti1 == t0:
                if oi0 < oi1:
                    T_O += 1
                elif oi0 > oi1:
                    T_not_O += 1
                else:
                    same_0 += 1
                
            else:    
                print('There is an error in the treatments values of the instances.')
        except:
            pass
    return T_O,T_not_O,same_0


def compute_metric(pairs_similar_instances,X,PATH_TREATMENT,PATH_OUTCOME,t0,t1,stat_param=1.96):
    """
    Computation of the metric.
    """
    T_O,T_not_O,same_0 = get_categorical_values(pairs_similar_instances,X,PATH_TREATMENT,PATH_OUTCOME,t0,t1)
    if T_O > 0 and T_not_O > 0:
        causal_metric = T_O/T_not_O
        log_s = math.log(causal_metric)
        interval_amp = stat_param*math.sqrt((1/T_O)+(1/T_not_O))
        return round(causal_metric,3), [round(math.exp(log_s - interval_amp),3),round(math.exp(log_s + interval_amp),3)]
    else:
        print('The metric can not be computed - check values')
        return None


def get_treatment_and_outcome(X,instance,PATH_TREATMENT,PATH_OUTCOME):
    """
    Returns the value on the treatment and outcomes paths for an instance.
    
    This function iterates for each path through all properties until obtaining the values.
    """
    subject_treatment = instance
    for property_treatment in PATH_TREATMENT:
        subject_treatment = [x[2] for x in X if x[0]==subject_treatment and x[1]==property_treatment][0]
        
    subject_outcome = instance
    for property_treatment in PATH_OUTCOME:
        subject_outcome = [x[2] for x in X if x[0]==subject_outcome and x[1]==property_treatment][0]
        
    return subject_treatment, subject_outcome
    

def get_distribution_numerical_rule(pairs_similar_instances,treatment_0,treatment_1,PATH_TREATMENT):
    """
    For a numerical rule, returns distribution of its associated pairs.
    """
    T_O,T_not_O,not_T_O,not_T_not_O = 0,0,0,0
    return T_O,T_not_O,not_T_O,not_T_not_O


def get_oddsratio_for_pairs(T_O,T_not_O,not_T_O,not_T_not_O,stat_param=1.96):
    """
    Given the distribution of the pairs of a rule, returns the oddsratio.
    """
    if T_O > 0 and not_T_not_O > 0 and T_not_O > 0 and not_T_O > 0:
        oddsratio = (T_O*not_T_not_O)/(T_not_O*not_T_O)
        log_oddsratio = math.log(oddsratio)
        interval_amp = stat_param*math.sqrt((1/T_O)+(1/not_T_not_O)+(1/T_not_O)+(1/not_T_O))
        return round(oddsratio,3), [round(math.exp(log_oddsratio - interval_amp),3),round(math.exp(log_oddsratio + interval_amp),3)]