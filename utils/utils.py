import json, yaml, math

def copy_yaml(scr, des):
    data = read_yaml(scr)
    write_yaml(des, data)

def read_json_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        print(f"error: {file_path} not found")
    except json.JSONDecodeError:
        print(f"error:file {file_path} is invalid")
    except Exception as e:
        print(f"unknown error: {e}")
    return None

def write_json_file(data, file_path):
    try:
        with open(file_path, 'w') as file:
            json.dump(data, file)
        print(f"successfully write {file_path}")
    except Exception as e:
        print(f"error: {e}")


def read_yaml(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = yaml.safe_load(file)
            return data
    except FileNotFoundError:
        print(f"error:  {file_path} not found")
    except yaml.YAMLError as e:
        print(f"error: {e}")
    return None


def write_yaml(file_path, data):
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            yaml.dump(data, file, allow_unicode=True)
        print(f"successfully write {file_path}。")
    except Exception as e:
        print(f"error: {e}")

def sort_prob_class(match_result:str, rule_with_score_path:str, prob_class_sorted_path:str):
    with open(match_result,'r',encoding='utf-8') as f:
        instance_match = yaml.load(f,Loader=yaml.FullLoader)
        f.close()

    with open(rule_with_score_path,'r',encoding='utf-8') as f:
        rule_score = yaml.load(f,Loader=yaml.FullLoader)
        f.close()

    data = dict()

    for instance_id in instance_match.keys():
        class_id = instance_match[instance_id]["class_id"]
        prob_classes_score = list()
        for prob_class in instance_match[instance_id]["possible_class"].keys():
            prob_class_rule_score = list()
            for satisfy_rule_idx in instance_match[instance_id]["possible_class"][prob_class]["satisfy_rules"]:
                prob_class_rule_score.append((satisfy_rule_idx,rule_score[prob_class]['score'][satisfy_rule_idx]))
            prob_classes_score.append((prob_class,sum([i[1] for i in prob_class_rule_score])))
        prob_classes_score = sorted(prob_classes_score ,key = lambda x:x[1],reverse=True)
        if prob_classes_score  != []:
            max_pred = prob_classes_score[0][0]
        else:
            max_pred = None
        data[instance_id]={"class_id":class_id,
                            "prob_classes":[prob_classes_score[i][0] for i in range(len(prob_classes_score))],
                            "prob_score":[prob_classes_score[i][1] for i in range(len(prob_classes_score))],
                            "max_pred":max_pred}
    with open(prob_class_sorted_path,'w') as f:
        yaml.dump(data,f,sort_keys=False)
        f.close()

def test_accuracy(prob_class_sorted_path:str, test_accuracy_path:str):
    with open(prob_class_sorted_path,'r',encoding='utf-8') as f:
        prob_class_sorted = yaml.load(f,Loader=yaml.FullLoader)
    dict_class_correct_total = dict()
    for idx, instance_dict in prob_class_sorted.items():
        if dict_class_correct_total.get(instance_dict["class_id"]) == None:
            dict_class_correct_total[instance_dict["class_id"]] = [0,1]
        else:
            dict_class_correct_total[instance_dict["class_id"]][1] = dict_class_correct_total[instance_dict["class_id"]][1] + 1
        
        if instance_dict["class_id"] == instance_dict["max_pred"]:
            dict_class_correct_total[instance_dict["class_id"]][0] = dict_class_correct_total[instance_dict["class_id"]][0] + 1

    for class_id in dict_class_correct_total.keys():
        dict_class_correct_total[class_id] = float(dict_class_correct_total[class_id][0]/dict_class_correct_total[class_id][1])
    
    average_accuray = {"average_accuray":sum([i for i in dict_class_correct_total.values()])/len(dict_class_correct_total.values())}
    
    with open(test_accuracy_path,'w',encoding='utf-8') as f:
        yaml.dump(dict_class_correct_total,f,sort_keys=False)
        yaml.dump(average_accuray,f,sort_keys=False)

def integrate_rules_all_v2(Rule_list,save_path):
    with open(Rule_list[0],"r",encoding='utf-8') as file:
        base = yaml.load(file,Loader=yaml.FullLoader)
    file.close()
    for Rule in Rule_list:
        with open(Rule,"r",encoding='utf-8') as file:
            data = yaml.load(file,Loader=yaml.FullLoader)
            for key in data:
                for rule in data[key]:
                    rule = sorted(rule)
                    for base_rule in base[key]:
                        flag = False
                        base_rule = sorted(base_rule)
                        if base_rule == rule:
                            flag = True
                            break
                    if not flag:
                       base[key].append(rule) 
        file.close()
    write_yaml(save_path,base)
    file.close()

def integrate_rules_all(output_dir,iter_list,rules_path):
    with open(f"{output_dir}/rules_{iter_list[0]}.yaml","r",encoding='utf-8') as file:
        base = yaml.load(file,Loader=yaml.FullLoader)
    file.close()
    for iter in iter_list:
        with open(f"{output_dir}/rules_{iter}.yaml","r",encoding='utf-8') as file:
            data = yaml.load(file,Loader=yaml.FullLoader)
            for key in data:
                for rule in data[key]:
                    rule = sorted(rule)
                    for base_rule in base[key]:
                        flag = False
                        base_rule = sorted(base_rule)
                        if base_rule == rule:
                            flag = True
                            break
                    if not flag:
                       base[key].append(rule) 
        file.close()
    write_yaml(rules_path, base)
    file.close()

    rule_result = dict()
    for key in base:
        for idx, clause in enumerate(base[key]):
            if len(clause) > 1:
                base[key][idx] = ['∧'.join(clause)]
    for key in base:
        clause_list = list()
        for clause in base[key]:
            clause_list.append(clause[0])
        rule_result[key] = '∨'.join(clause_list)
    
    for key in rule_result:
        print(key,":",rule_result[key])
    return rule_result
        




def get_foil_label_fn(type):
    if type == 'Bird':
        from model.FOIL_Bird import FOIL, rules_score, prepare_has_list
        from label.Labeling_Bird import predition
        return FOIL, rules_score, predition, prepare_has_list
    elif type == 'Glaucoma':
        from model.FOIL_Glaucoma import FOIL, rules_score
        from label.Labeling_Glaucoma import predition
    elif type == 'Occupation' or 'Traffic':
        from model.FOIL_Common import FOIL, rules_score
        from label.Labeling_Common import predition
    else:
        raise Exception('Invalid type')
    return FOIL, rules_score, predition

def foil_gain_v1(pre_p,pre_n,now_p,now_n):
    if (pre_p==0 or now_p==0):
        return -99                        
    gain=now_p*(math.log2(now_p/(now_n+now_p))-math.log2(pre_p/(pre_p+pre_n))) 
    return gain

def foil_gain_v2(pre_p,pre_n,now_p,now_n):
    if (pre_p==0 or now_p==0):
        return 0
    tf = now_p/(now_n+now_p)
    return tf
    