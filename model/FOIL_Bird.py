import math,re,copy,json,time,random,yaml,os
import numpy as np
from utils.utils import write_json_file, write_yaml, read_json_file, read_yaml

def get_parameter_list(result):
    parameter_list=[]
    for clause in result:
        a=re.split(r'[(|,|)]',clause)
        if a[0]!="overlap" and a[0]!="num" and a[0]!='area':
            parameter_list.append(a[2])

    return parameter_list

def pos_neg_list(target,total_list):
    positive_list=[]
    negative_list=[]
    for image_number,image in enumerate(total_list):
        for i,clause in enumerate(image):
            if i==0:
                if clause==target:
                    positive_list.append(image_number)
                else:
                    negative_list.append(image_number)
    return positive_list,negative_list

def get_new_total_list(result_list,total_list):
    del_number_hd=[]
    new_total=copy.deepcopy(total_list)
    for i in range(len(result_list)):
        if i!=len(result_list)-1:
            for image_number,image in enumerate(total_list):
                del_result=True
                for clause in result_list[i]:
                    if (clause not in image):   
                        del_result=False
                        break
                if del_result==True:
                    del_number_hd.append(image_number)
        else:
            for image_number,image in enumerate(total_list):
                for clause in result_list[i]:
                    if (clause not in image):
                        del_number_hd.append(image_number)
                        break
    del_number=list(set(del_number_hd)) 
    del_number.sort()
    for i in range(len(del_number)):
        del new_total[del_number[len(del_number)-1-i]] 
    return new_total   

def get_new_total_list1(result_list,total_list):      
    del_number_hd=[]
    new_total=copy.deepcopy(total_list)           
    for clauses_list in result_list:
        for image_number,image in enumerate(total_list):
            del_result=True
            for clause in clauses_list:
                if (clause not in image):        
                    del_result=False
                    break
            if del_result==True:
                del_number_hd.append(image_number)
    del_number=list(set(del_number_hd))         
    del_number.sort()
    for i in range(len(del_number)):
        del new_total[del_number[len(del_number)-1-i]]               
    return new_total   

def get_possible_clause1(counting,total_list,result_list):
    if counting==0:
        new_total=get_new_total_list1(result_list,total_list)
        clause_total=[]
        for image in new_total:
            for i,clause in enumerate(image):
                if i!=0 and (clause not in clause_total):        
                    clause_total.append(clause)
    else:
        new_total=get_new_total_list(result_list,total_list)
        clause_total=[]
        for image in new_total:
            for i,clause in enumerate(image):
                if i!=0 and (clause not in result_list[len(result_list)-1]) and (clause not in clause_total):        
                    clause_total.append(clause)
    return clause_total
    
def unique_list(A):
    res = []
    for i in range(len(A)):
        res.append([A[i][0]])
        seen = set()
        res[i].extend([predicate for predicate in A[i][1::] if not (predicate in seen or seen.add(predicate))] )
    return res

def get_total_list(total_list1):
    total_list=[]
    for image in total_list1:
        list_=[]
        sub=re.split(r'[(|,|)]',image[0])[1]     
        for clauses in image:
            a=re.split(r'[¬|(|,|)]',clauses)
            if a[1]==sub:
                a[1]="X"
                if len(a)==3:
                    result=a[0]+"("+a[1]+")"+a[2]
                else:
                    result=a[0]+"("+a[1]+","+a[2]+")"+a[3]
                list_.append(result)
            elif a[2]==sub:
                a[2]="X"
                result="¬"+a[1]+"("+a[2]+","+a[3]+")"+a[4]
                list_.append(result)
            else:
                result=a[0]+"("+a[1]+","+a[2]+")"+a[3]
                list_.append(result)
        list_ = list_
        total_list.append(list_)
        total_list = unique_list(total_list)
    return total_list

def get_total_list_has(total_list1):
    total_list=[]
    for image in total_list1:
        list_=[]
        sub=re.split(r'[(|,|)]',image[0])[1]
        for clauses in image:
            a=re.split(r'[¬|(|,|)]',clauses)
            if a[1]==sub:
                a[1]="X"
                if len(a)==3:
                    result=a[0]+"("+a[1]+")"+a[2]
                else:
                    result=a[0]+"("+a[1]+","+a[2]+")"+a[3]
                list_.append(result)
            elif a[2]==sub:
                a[2]="X"
                result="¬"+a[1]+"("+a[2]+","+a[3]+")"+a[4]
                list_.append(result)
            else:
                result=a[0]+"("+a[1]+","+a[2]+")"+a[3]
                list_.append(result)
        list_has = list()
        for item in list_:
            if '¬' not in item:
                list_has.append(item)
        total_list.append(list_has)
        total_list = unique_list(total_list)
    return total_list
    
def get_total_list1(input_list):
    total_list=[]
    for image_num in range(len(input_list)):
        image_list=[]
        string=input_list[image_num]['type']+"(image"+str(input_list[image_num]['imageId'])+")"
        image_list.append(string)
        for name in input_list[image_num]['object_detect']:
            a=copy.deepcopy(name)
            new_name=re.split(r'[_]',a)
            #if name!='has_wing_color':
            if input_list[image_num]['object_detect'][name]!="0":
                    has=name+"(image"+str(input_list[image_num]['imageId'])+","+input_list[image_num]['object_detect'][name]+")"
                    image_list.append(has)
            else:
                for new_image_num in range(len(input_list)):
                    if input_list[new_image_num]['object_detect'][name]!="0":
                        not_has="¬"+name+"(image"+str(input_list[image_num]['imageId'])+","+input_list[new_image_num]['object_detect'][name]+")"
                        image_list.append(not_has)
        total_list.append(image_list)
    return total_list

def get_object_list(total_list):
    object_list=[]
    for image in total_list:
        for clauses in image:
            a=re.split(r'[¬(|,|)]',clauses)
            if a[0]!='overlap' and a[0]!='num' and a[0]!='area' and len(a)==4 and (a[0] not in object_list):
                object_list.append(a[0])
    return object_list

def get_object_list_cover(total_list):
    flat_list = [item for sublist in total_list for item in sublist[1::]]
    unique_list = list(set(flat_list))
    return unique_list


def covered_instance(new_predicate, total_list1, target, now_clause = [], rule_list = [], i=0, counting=0):
    new_now_clause=copy.deepcopy(now_clause)
    new_rule_list=copy.deepcopy(rule_list)
    new_now_clause.append(new_predicate) #子句添加谓语
    new_rule_list.append(new_now_clause)
    if counting!=0:          #Each time, because we add the updated version at the end of the list, so delete the old version
        del new_rule_list[i]  
    new_total_list=get_new_total_list(new_rule_list,total_list1)
    positive_list,negative_list=pos_neg_list(target,new_total_list)
    return new_total_list, positive_list, negative_list

def Jaccard(x,y):
    x = [object for object in x if "not" not in object]
    del x[0]
    y = [object for object in y if "not" not in object]
    del y[0]
    p = 0
    for object in x:
        if object in y:
            p+=1
    q = len(x)-p
    r = len(y)-p
    return p/(p+q+r)

def Cohesion(T,new_total_list):
    J = 0
    for i in T:
        for j in T:
            if i == j:
                continue
            else:
                J+=Jaccard(new_total_list[i],new_total_list[j])
    if len(T)<=1:
        return 1
    return J/((len(T))*(len(T)-1))

def p_times_count(Rule_base,target):
    # p:i
    p_count = dict()
    for path in Rule_base:
        with open(path,'r',encoding='utf-8') as f:
            rule = yaml.load(f,Loader=yaml.FullLoader)
            p_list = [p for clause in rule[target] for p in clause]
            for p in p_list:
                if p_count.get(p) == None:
                    p_count[p]=1
                else:
                    p_count[p]+=1
            f.close()
    return p_count

def decay_factor(total_list, object_list, target, theta = 0.95, epsilon = 1e-5):
    p_decay_factor = dict()
    for o in object_list:
        new_total_list, positive_list, negative_list = covered_instance(o, total_list, target)
        cohesion = Cohesion(positive_list,new_total_list)
        p_decay_factor[o] = theta**(cohesion+epsilon)
    return p_decay_factor

def foil(target_list,target,total_list,rule_base,decay_dir,foil_gain):

    result_list=[]
    object_list_cover = get_object_list_cover(total_list)
    new_total_list=copy.deepcopy(total_list)

    print(f"updating decay factors......")
    if os.path.isfile(f"{decay_dir}/{target}_decay.yaml"):
        with open(f"{decay_dir}/{target}_decay.yaml","r",encoding='utf-8') as decay_f:
            p_decay_factor = yaml.load(decay_f,yaml.FullLoader)
            decay_f.close()
    else:
        p_decay_factor = decay_factor(total_list,object_list_cover,target)
        write_yaml(f"{decay_dir}/{target}_decay.yaml",p_decay_factor)

    p_count = p_times_count(rule_base,target)

    positive_list,negative_list=pos_neg_list(target,new_total_list)
    initial_neg_length = len(negative_list)
    initial_pos_length = len(positive_list)
    i=0 
    while (len(positive_list)> 0*initial_pos_length):
        counting=0
        while (len(negative_list)> 0.15*initial_neg_length):
            if len(result_list)==i:               
                result=[]
            else:
                result=result_list[i]
            pre_p=len(positive_list)
            pre_n=len(negative_list)
            foil_gain_list=[]
            possible_clause=get_possible_clause1(counting,total_list,result_list)
            for new_clause in possible_clause:           
                now_p=now_n=0
                for image_number,image in enumerate(new_total_list):
                    for clause in image:
                        if clause==new_clause:
                            for positive_image_number in positive_list:
                                if image_number==positive_image_number:
                                    now_p+=1  
                            for negative_image_number in negative_list:
                                if image_number==negative_image_number:
                                    now_n+=1

                if p_count.get(new_clause) == None:
                    score = foil_gain(pre_p,pre_n,now_p,now_n)
                    foil_gain_list.append(score)
                else:
                    score = foil_gain(pre_p,pre_n,now_p,now_n)
                    decay = p_decay_factor[new_clause]
                    times = p_count[new_clause]
                    score = score*(decay**times)
                    foil_gain_list.append(score)

            correct_clause=False            
            parameter_list=[]

            max_value = max(foil_gain_list)
            min_value = min(foil_gain_list)
            max_clause_number_list = [i for i in range(len(foil_gain_list)) if foil_gain_list[i] == max_value]
            select_clause_number = max_clause_number_list[0]

            if foil_gain_list==[]:
                return None
            while correct_clause == False:
                for clause_number,clause_gain in enumerate(foil_gain_list):
                    if max_value==min_value:
                        return result_list
                    if clause_number==select_clause_number:
                        a=re.split(r'[(|,|)]',possible_clause[clause_number])
                        if a[0]=="overlap":
                            if (a[1] in parameter_list) and (a[2] in parameter_list):
                                new_result=copy.deepcopy(result)    
                                new_result.append(possible_clause[clause_number])       
                                result_list.append(new_result)
                                correct_clause=True
                                break
                            else:
                                foil_gain_list[clause_number]=-99
                                break
                        elif a[0]=="num" or a[0]=='area':
                            if a[1] in parameter_list:
                                new_result=copy.deepcopy(result)
                                new_result.append(possible_clause[clause_number])
                                result_list.append(new_result)
                                correct_clause=True
                                break
                            else:
                                foil_gain_list[clause_number]=-99
                                break 
                        else:
                            new_result=copy.deepcopy(result)
                            new_result.append(possible_clause[clause_number]) 
                            result_list.append(new_result) 
                            correct_clause=True
                            break
            if counting!=0: 
                del result_list[i]

            new_total_list=get_new_total_list(result_list,total_list)

            positive_list,negative_list=pos_neg_list(target,new_total_list)   

            counting+=1           
        
        new_total_list=get_new_total_list1(result_list,total_list)

        positive_list,negative_list=pos_neg_list(target,new_total_list)
        print(f"Iteration: {i}")
        print("Rule:",result_list)
        i+=1
    return result_list


def prepare_has_list(train_set,test_set):
    train_set = get_total_list1(train_set)
    train_set_has = get_total_list_has(train_set)
    test_set = get_total_list1(test_set)
    test_set_has = get_total_list_has(test_set)
    whole_set_has = train_set_has
    has_list = [item for image in whole_set_has for item in image[1::]]
    has_list = list(set(has_list))

    for idx,image in enumerate(train_set_has):
        for has_attr in has_list:
            if has_attr not in image:
                train_set_has[idx].append("¬"+has_attr)

    for idx,image in enumerate(test_set_has):
        for has_attr in has_list:
            if has_attr not in image:
                test_set_has[idx].append("¬"+has_attr)
    final_train_set = get_total_list(train_set_has)
    final_test_set = get_total_list(test_set_has)
    return final_train_set, final_test_set

def FOIL(input_list,rule_save_path, rule_base, decay_dir, foil_gain):
    dict_math={}
    total_list=input_list
    object_list=get_object_list(total_list)
    target_list=[]
    for images in total_list:
        if images[0] not in target_list:
            target_list.append(images[0])
    for target in target_list:
        result_list=foil(target_list,target,total_list,rule_base,decay_dir,foil_gain = foil_gain)
        if result_list==None:
            dict_math[target]=[['none']]
        else:
            math_format=result_list
            dict_math[target]=math_format
    write_yaml(rule_save_path, dict_math)
    return dict_math,[],object_list

def scores(total_list,clause,target):
    
    pos_list = []
    neg_list = []
    clause_predicate_scores = []

    for image in total_list:
        type=image[0]
        if type == target:
            pos_list.append(image)
        else:
            neg_list.append(image)

    #对子句中的谓词计算得分
    for position,predicate in enumerate(clause):
        T_pos_with_A = 0
        T_neg_with_A = 0
        for image in pos_list:
            for predicate_img in image:
                if predicate_img == predicate:
                    T_pos_with_A+=1
                    break
        for image in neg_list:
            for predicate_img in image:
                if predicate_img == predicate:
                    T_neg_with_A+=1
                    break
            
    
        tf = T_pos_with_A/len(pos_list)
        idf = np.log(len(neg_list)/(1e-5+T_neg_with_A))

        clause_predicate_scores.append(tf*idf)
        

    return float(min(clause_predicate_scores))       


def rules_score(input_list:list,rule_list:dict,save_path:str,score_func=scores): 
    # total_list1=get_total_list1(input_list)
    # total_list=get_total_list(total_list1)
    total_list= input_list
    rules_score_dict = dict()
    for target in rule_list.keys():
        score=list()
        for clause in rule_list[target]:
            score.append(float(score_func(total_list,clause,target)))
        rules_score_dict[target]={"rule":rule_list[target],"score":score}
        write_yaml(save_path,rules_score_dict)





