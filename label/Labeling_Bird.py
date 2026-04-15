import re, yaml
import numpy as np

def get_total_listt1(dict_list):
    total_list=[]
    for image_num in range(len(dict_list)):
        image_list=[]
        for name in dict_list[image_num]['object_detect']:
            if dict_list[image_num]['object_detect'][name]!="0":
                has=name+"(image"+str(dict_list[image_num]['imageId'])+","+dict_list[image_num]['object_detect'][name]+")"
                image_list.append(has)
            else:
                for new_image_num in range(len(dict_list)):
                    if dict_list[new_image_num]['object_detect'][name]!="0":
                        not_has="¬"+name+"(image"+str(dict_list[image_num]['imageId'])+","+dict_list[new_image_num]['object_detect'][name]+")"
                        image_list.append(not_has)
        total_list.append(image_list)
    return total_list

def unique_list(A):
    res = []
    for i in range(len(A)):
        res.append([A[i][0]])
        seen = set()
        seen.add(A[i][0])
        res[i].extend([predicate for predicate in A[i][1::] if not (predicate in seen or seen.add(predicate))] )
    return res

def get_total_listt(total_list1):
    total_list=[]
    for image in total_list1:
        list=[]
        for clauses in image:
            a=re.split(r'[(|,|)]',clauses)
            if a[0]!='overlap' and a[0]!='num' and a[0]!='area':
                sub=a[1]
                break
        for clauses in image:
            a=re.split(r'[¬|(|,|)]',clauses)
            if a[1]==sub:
                a[1]="X"
                if len(a)==3:
                    result=a[0]+"("+a[1]+")"+a[2]
                else:
                    result=a[0]+"("+a[1]+","+a[2]+")"+a[3]
                list.append(result)
            elif a[2]==sub:
                a[2]="X"
                result="¬"+a[1]+"("+a[2]+","+a[3]+")"+a[4]
                list.append(result)
            else:
                result=a[0]+"("+a[1]+","+a[2]+")"+a[3]
                list.append(result)
        total_list.append(list)
        total_list = unique_list(total_list)
    return total_list

def labeling(total_list,rules):
    labels=[]
    possible_labels=[]
    label_list_with_hit_rules_list=[]
    for possible_label in rules.keys():
        possible_labels.append(possible_label)
    for image in total_list:
        label_list=[]
        label_list_with_hit_rules=dict()
        find=False
        for possible_label in possible_labels:
            rule_list=rules[possible_label]
            satisfy=["False" for i in range(len(rule_list))]
            for rule_num,rule in enumerate(rule_list):
                satisfy_list=["False" for i in range(len(rule))]
                for position,clauses in enumerate(rule):
                    for predicate in image:
                        if predicate == clauses:
                            satisfy_list[position]="True"
                            break
                if "False" not in satisfy_list:
                    satisfy[rule_num]="True"
            if "True" in satisfy:
                label_list.append(possible_label)
                satisfy_array = np.array(satisfy)
                satisfy_index = np.where(satisfy_array=="True")
                satisfy_index = satisfy_index[0].tolist()
                label_list_with_hit_rules[possible_label]={"satisfy_rules":satisfy_index,"count":len(satisfy_index)}
                find=True
        if find==False:
            label_list.append("None")
            label_list_with_hit_rules = {}
        labels.append(label_list)
        label_list_with_hit_rules_list.append(label_list_with_hit_rules)
    return labels,label_list_with_hit_rules_list

def get_ground_truth(total_list):
    ground_truth_list = list()
    for image_num in range(len(total_list)):
        ground_truth_list.append(total_list[image_num][0])
    return ground_truth_list

def label(total_list,rules):
    labels,label_list_with_hit_rules_list=labeling(total_list, rules)
    return labels,label_list_with_hit_rules_list

def predition(testset:list,rules:dict,match_result:str):

    ground_truth_list = get_ground_truth(testset)
    labels,label_list_with_hit_rules_list = label(testset,rules)
    
    test = list(zip(ground_truth_list,labels,label_list_with_hit_rules_list))

    instance_match = dict()
    for idx,pred in enumerate(test):
        possible_class = pred[2]
        instance_match[idx]={"class_id":pred[0],"possible_class":possible_class}
    with open(match_result,'w') as f:
        yaml.dump(instance_match, f, sort_keys=False)
        f.close()


