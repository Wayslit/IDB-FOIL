import re, json, yaml
import numpy as np

def get_ground_truth(dict_list):
    ground_truth_list = list()
    for image_num in range(len(dict_list)):
        ground_truth=dict_list[image_num]['type']+'(X)'
        ground_truth_list.append(ground_truth)
    return ground_truth_list

def get_total_listt1(input_list):
    total_object=["OC","OD","HCup","HDisc","VCup","VDisc"]
    total_object1=["ACDR","HCDR","VCDR"]
    total_list=[]
    for image_num in range(len(input_list)):
        image_list=[]
        # string=input_list[image_num]['type']+"(image"+str(input_list[image_num]['imageId'])+")"
        # image_list.append(string)
        position_list1=[0,1,2]
        for index,objects in enumerate(position_list1):
            has=total_object1[objects]+"(image"+str(input_list[image_num]['imageId'])+","+str(objects)+")"
            area1=float(input_list[image_num]['object_detect']['space'][total_object[objects*2]])
            area2=float(input_list[image_num]['object_detect']['space'][total_object[objects*2+1]])
            area="area"+"("+str(objects)+","+str(area1/area2)+")"
            image_list.append(has)
            image_list.append(area)
        total_list.append(image_list)
    return total_list

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
                object_in_rule=[]
                object_character=[]
                for position,clauses in enumerate(rule):
                    a=re.split(r'[¬|(|,|)]',clauses)
                    if len(a)==5:
                        for predicate in image:
                            b=re.split(r'[¬|(|,|)]',predicate)
                            if b[1]==a[1]:
                                satisfy_list[position]="True"
                                break
                    elif a[0]!='overlap' and a[0]!='num' and a[0]!='area' and len(a)==4:
                        object_in_rule.append(a[0])
                        object_character.append(a[2])
                        for predicate in image:
                            b=re.split(r'[(|,|)]',predicate)
                            if b[0]==a[0]:
                                satisfy_list[position]="True"
                                break
                    elif a[0]=='overlap':
                        object_in_image=[]
                        object_number=[]
                        object1_in_rule=object_in_rule[object_character.index(a[1])]
                        object2_in_rule=object_in_rule[object_character.index(a[2])]
                        for predicate in image:
                            b=re.split(r'[(|,|)]',predicate)
                            if b[0]!='overlap' and b[0]!='num' and b[0]!='area':
                                object_in_image.append(b[0])
                                object_number.append(b[2])
                            if b[0]==a[0]:
                                object1_in_image=object_in_image[object_number.index(b[1])]
                                object2_in_image=object_in_image[object_number.index(b[2])]
                                if object1_in_image==object1_in_rule and object2_in_image==object2_in_rule:
                                    satisfy_list[position]="True"
                                    break
                    elif a[0]=='num' or a[0]=='area':
                        object_in_image=[]
                        object_number=[]
                        object1_in_rule=object_in_rule[object_character.index(a[1])]
                        for predicate in image:
                            b=re.split(r'[(|,|)]',predicate)
                            #print(b)
                            if b[0]!='overlap' and b[0]!='num' and b[0]!='area':
                                object_in_image.append(b[0])
                                object_number.append(b[2])
                            if b[0]==a[0]:
                                object1_in_image=object_in_image[object_number.index(b[1])]
                                c=re.split(r'[(|,|)]',rule[position+1])
                                maxi=float(c[3])
                                mini=float(c[2])
                                if object1_in_image==object1_in_rule and mini<=float(b[2])<=maxi:
                                    satisfy_list[position]="True"
                                    satisfy_list[position+1]="True"
                                    break
                #print(satisfy_list)
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


def label(dict_list,rules):
    total_list1=get_total_listt1(dict_list)
    total_list=get_total_listt(total_list1)
    labels,label_list_with_hit_rules_list=labeling(total_list,rules)
    return labels,label_list_with_hit_rules_list

def read_json_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        print(f"错误：未找到文件 {file_path}。")
    except json.JSONDecodeError:
        print(f"错误：文件 {file_path} 不是有效的 JSON 格式。")
    except Exception as e:
        print(f"发生未知错误：{e}")
    return None

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
    




