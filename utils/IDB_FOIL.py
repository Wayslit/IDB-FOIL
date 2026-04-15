from utils.utils import*

import os,yaml

 
def IDB_FOIL_main(config):

    output_dir= config.output_dir
    middle_dir = config.middle_dir
    decay_dir = config.middle_dir
    trainset_path = config.trainset_path
    testset_path = config.testset_path
    train_flag = True
    train_set = read_json_file(trainset_path)
    test_set = read_json_file(testset_path)
    iter_times = config.iter_times
    task_type = config.task_type

    if config.task_type == "Bird":
        FOIL, rules_score, predition, prepare_has_list = get_foil_label_fn(task_type)
        train_set, test_set = prepare_has_list(train_set,test_set)
    else:
        FOIL, rules_score, predition = get_foil_label_fn(task_type)
    
    while(train_flag):
        i=1
        Rule_base = []
        while(True):
            if os.path.isfile(f"{middle_dir}/rules_{i}.yaml"):
                Rule_base.append(f"{middle_dir}/rules_{i}.yaml")
                i+=1
            else:
                break

        Rule_list = []

        ######## v1 ########
        foil_gain = foil_gain_v1
        rules_path = f"{middle_dir}/rules_v1_{i}.yaml"
        Rule_list.append(rules_path)
        rules_score_path = f"{middle_dir}/rules_score_v1_{i}.yaml"
        match_result_path = f"{middle_dir}/match_reslut_v1_{i}.yaml"
        prob_class_sorted_path = f"{middle_dir}/prob_class_sorted_v1_{i}.yaml"
        test_accuracy_path = f'{middle_dir}/accuracy_v1_{i}.yaml'
        rules,_,_=FOIL(input_list=train_set,rule_save_path=rules_path,rule_base=Rule_base,decay_dir=decay_dir, foil_gain=foil_gain)
        rules_score(input_list=train_set,rule_list=rules,save_path=rules_score_path)
        predition(testset=test_set,rules=rules,match_result=match_result_path)
        sort_prob_class(match_result=match_result_path, rule_with_score_path=rules_score_path, prob_class_sorted_path=prob_class_sorted_path)
        test_accuracy(prob_class_sorted_path=prob_class_sorted_path, test_accuracy_path=test_accuracy_path)

        ######## v2 ########
        foil_gain = foil_gain_v2
        rules_path = f"{middle_dir}/rules_v2_{i}.yaml"
        Rule_list.append(rules_path)
        rules_score_path = f"{middle_dir}/rules_score_v2_{i}.yaml"
        match_result_path = f"{middle_dir}/match_reslut_v2_{i}.yaml"
        prob_class_sorted_path = f"{middle_dir}/prob_class_sorted_v2_{i}.yaml"
        test_accuracy_path = f'{middle_dir}/accuracy_v2_{i}.yaml'
        rules,_,_=FOIL(input_list=train_set,rule_save_path=rules_path,rule_base=Rule_base, decay_dir=decay_dir, foil_gain=foil_gain)
        rules_score(input_list=train_set,rule_list=rules,save_path=rules_score_path)
        predition(testset=test_set,rules=rules,match_result=match_result_path)
        sort_prob_class(match_result=match_result_path, rule_with_score_path=rules_score_path, prob_class_sorted_path=prob_class_sorted_path)
        test_accuracy(prob_class_sorted_path=prob_class_sorted_path, test_accuracy_path=test_accuracy_path)

        ######## v1v4 aggregation ########
        save_path = f"{middle_dir}/rules_{i}.yaml"
        integrate_rules_all_v2(Rule_list,save_path)
        rules_path = save_path
        rules_score_path = f"{middle_dir}/rules_score_{i}.yaml"
        match_result_path = f"{middle_dir}/match_reslut_{i}.yaml"
        prob_class_sorted_path = f"{middle_dir}/prob_class_sorted_{i}.yaml"
        test_accuracy_path = f'{middle_dir}/acc_dual_aggregation_{i}.yaml'
        rules = read_yaml(rules_path)
        rules_score(input_list=train_set,rule_list=rules,save_path=rules_score_path)
        predition(testset=test_set,rules=rules,match_result=match_result_path)
        sort_prob_class(match_result=match_result_path, rule_with_score_path=rules_score_path, prob_class_sorted_path=prob_class_sorted_path)
        test_accuracy(prob_class_sorted_path=prob_class_sorted_path, test_accuracy_path=test_accuracy_path)

        ######## aggregation all ########
        iter_list = [iter for iter in range(1,i+1)]
        rules_path = f"{middle_dir}/rules_all_from_1_to_{len(iter_list)}.yaml"
        rule_result = integrate_rules_all(middle_dir,iter_list,rules_path)
        rules_score_path = f"{middle_dir}/iter_aggregation_rules_score_from_1_to_{len(iter_list)}.yaml"
        match_result_path = f"{middle_dir}/iter_aggregation_match_reslut_{i}.yaml"
        prob_class_sorted_path = f"{middle_dir}/iter_aggregation_prob_class_sorted_{i}.yaml"
        test_accuracy_path = f'{middle_dir}/Labeling_Accuracy_iter_{i}.yaml'
        rules = read_yaml(rules_path)
        rules_score(input_list=train_set,rule_list=rules,save_path=rules_score_path)
        predition(testset=test_set,rules=rules,match_result=match_result_path)
        sort_prob_class(match_result=match_result_path, rule_with_score_path=rules_score_path, prob_class_sorted_path=prob_class_sorted_path)
        test_accuracy(prob_class_sorted_path=prob_class_sorted_path, test_accuracy_path=test_accuracy_path) 

        if i >= iter_times:
            train_flag = False
            final_rules_path = f"{output_dir}/labeling_rules.yaml"
            final_rules_score_path = f"{output_dir}/rules_clause_score.yaml"
            final_match_result_path = f"{output_dir}/rules_clause_satisfaction_reslut_{i}.yaml"
            final_prob_class_sorted_path = f"{output_dir}/problable_prediction_label{i}.yaml"
            final_test_accuracy_path = f'{output_dir}/Labeling_Accuracy_for_{i}_iter.yaml'
            write_yaml(final_rules_path,rule_result)
            copy_yaml(rules_score_path, final_rules_score_path)
            copy_yaml(match_result_path, final_match_result_path)
            copy_yaml(prob_class_sorted_path, final_prob_class_sorted_path)
            copy_yaml(test_accuracy_path,final_test_accuracy_path)



