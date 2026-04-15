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

def get_parameter_list_v2(result):
    parameter_list=[]
    for clause in result:
        a=re.split(r'[(|,|)]',clause)
        if a[0]!="overlap" and a[0]!="num" and a[0]!='area':
            parameter_list.append(a[0])
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

def get_new_total_list_cover(result_list,total_list):
    del_number_hd=[]
    new_total=copy.deepcopy(total_list)
    for i in range(len(result_list)):
        if i!=len(result_list)-1:
            for image_number,image in enumerate(total_list):
                del_result=True
                for obj in result_list[i]:
                    flag = False
                    for pred in image:
                        a = re.split(r'[(|,|)]',pred)
                        if obj == a[0]:
                            flag = True
                            break
                    if (flag==False):        
                        del_result=False
                        break
                if del_result==True:
                    del_number_hd.append(image_number)
        else:
            for image_number,image in enumerate(total_list):
                for obj in result_list[i]:
                    flag = False
                    for pred in image:
                        a = re.split(r'[(|,|)]',pred)
                        if obj == a[0]:
                            flag = True
                            break
                    if (flag==False):        
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
    
def get_total_list(total_list1):
    total_list=[]
    for image in total_list1:
        list=[]
        sub=re.split(r'[(|,|)]',image[0])[1]  
        for clauses in image:
            a=re.split(r'[(|,|)]',clauses)
            if a[1]==sub:
                a[1]="X"
                if len(a)==3:
                    result=a[0]+"("+a[1]+")"+a[2]
                else:
                    result=a[0]+"("+a[1]+","+a[2]+")"+a[3]
                list.append(result)
            else:
                result=a[0]+"("+a[1]+","+a[2]+")"+a[3]
                list.append(result)
        total_list.append(list)
    return total_list

def get_int(elem):
    return int(elem)
    
def get_result_list(target,result_list,total_list,variable1,variable2):
    new_result_list=[]
    number=[]
    character=[]
    for image in result_list:
        for clauses in image:
            a=re.split(r'[(|,|)]',clauses)
            if a[0]!="overlap" and a[0]!="num" and a[0]!="area":
                if a[2] not in number:
                    number.append(a[2])
            elif a[0]=="overlap":
                if a[2] not in number:
                    number.append(a[2])
                if a[1] not in number:
                    number.append(a[1])
            else:
                if a[1] not in number:
                    number.append(a[1])
    number.sort(key=get_int)
    for i in range(len(number)):
        if i<13:
            character.append(chr(i+65))
        elif 13<=i<23:
            character.append(chr(i+65+1))
        else:
            character.append(chr(i+65+2))
    for image in result_list:
        result=[]
        for clauses in image:
            a=re.split(r'[(|,|)]',clauses)
            if a[0]!="overlap" and a[0]!='num'and a[0]!='area':
                position=number.index(a[2])
                a[2]=character[position]
                clause=a[0]+"("+a[1]+","+a[2]+")"+a[3]
                result.append(clause)
            elif a[0]=="overlap":
                position1=number.index(a[1])
                position2=number.index(a[2])
                a[1]=character[position1]
                a[2]=character[position2]
                clause=a[0]+"("+a[1]+","+a[2]+")"+a[3]
                result.append(clause)
            else:
                position=number.index(a[1])
                a[1]=character[position]
                clause=a[0]+"("+a[1]+","+"N"+")"+a[3]
                result.append(clause)
                mini,maxi=threshold(target,clauses,total_list,variable1,variable2)
                if mini!=0:
                    threshold_clause="N>"+str(mini)
                else:
                    threshold_clause="N<"+str(maxi)
                result.append(threshold_clause)
        new_result_list.append(result)
    return new_result_list
    
def get_total_list1(input_list):

    total_object=[]
    total_list=[]
    for image_num in range(len(input_list)):
        for objects_num in range(len(input_list[image_num]['object_detect']['object'])):
            name=input_list[image_num]['object_detect']['object'][str(objects_num)]['name']
            if name not in total_object:
                total_object.append(name)
        for objects_num in range(len(input_list[image_num]['panoptic_segmentation'])):
            name=input_list[image_num]['panoptic_segmentation'][str(objects_num)]['name']
            if name not in total_object:
                total_object.append(name)
    for image_num in range(len(input_list)):
        image_list=[]
        string=input_list[image_num]['type']+"(image"+str(input_list[image_num]['imageId'])+")"
        image_list.append(string)
        position_list=[]
        position_list1=[]
        for objects_num in range(len(input_list[image_num]['object_detect']['object'])):
            name=input_list[image_num]['object_detect']['object'][str(objects_num)]['name']
            position=total_object.index(name)
            if position not in position_list:
                position_list.append(position)
        for objects_num in range(len(input_list[image_num]['panoptic_segmentation'])):
            name=input_list[image_num]['panoptic_segmentation'][str(objects_num)]['name']
            position=total_object.index(name)
            if position not in position_list1:
                position_list1.append(position)
        object_numbers=[0 for i in range(len(position_list))]
        for objects_num in range(len(input_list[image_num]['object_detect']['object'])):
            name=input_list[image_num]['object_detect']['object'][str(objects_num)]['name']
            position=total_object.index(name)
            object_numbers[position_list.index(position)]+=1
        
        for index,objects in enumerate(position_list):
            has=total_object[objects]+"(image"+str(input_list[image_num]['imageId'])+","+str(objects)+")"

            num="num"+"("+str(objects)+","+str(object_numbers[index])+")"
            image_list.append(has)
            image_list.append(num)
        for index,objects in enumerate(position_list1):
            has=total_object[objects]+"(image"+str(input_list[image_num]['imageId'])+","+str(objects)+")"
            area="area"+"("+str(objects)+","+str(input_list[image_num]['panoptic_segmentation'][str(index)]['area'])+")"
            image_list.append(has)
            image_list.append(area)
        for objects_num in range(len(input_list[image_num]['object_detect']['overlap'])):
            object1_name=input_list[image_num]['object_detect']['object'][str(input_list[image_num]['object_detect']['overlap'][str(objects_num)]["idA"])]['name']
            object2_name=input_list[image_num]['object_detect']['object'][str(input_list[image_num]['object_detect']['overlap'][str(objects_num)]["idB"])]['name']
            position1=total_object.index(object1_name)
            position2=total_object.index(object2_name)
            if position1<position2:
                overlap="overlap("+str(position1)+","+str(position2)+")"
            else:
                overlap="overlap("+str(position2)+","+str(position1)+")"
            if overlap not in image_list:
                image_list.append(overlap)
        total_list.append(image_list)
    return total_list

def threshold(target,clause,total_list,variable1,variable2):
    a1=re.split(r'[(|,|)]',clause)
    if a1[0]=='num':
        positive_list=[]
        negative_list=[]
        positive_greater=negative_greater=0
        for image in total_list:
            for clauses in image:
                a=re.split(r'[(|,|)]',clauses)
                if a[0]=='num' and a[1]==a1[1]:
                    if image[0]==target:
                        positive_list.append(int(a[2]))
                    else:
                        negative_list.append(int(a[2]))
        for number in positive_list:
            if number>variable1:
                positive_greater+=1
        for number in negative_list:
            if number>variable1:
                negative_greater+=1
        if positive_greater>2/3*len(positive_list) and negative_greater<=1/3*len(negative_list):
            return variable1,10000
        elif positive_greater<=1/3*len(positive_list) and negative_greater>2/3*len(negative_list):
            return 0,variable1
        else:
            return False
    if a1[0]=='area':
        positive_list=[]
        negative_list=[]
        positive_greater=negative_greater=0
        for image in total_list:
            for clauses in image:
                a=re.split(r'[(|,|)]',clauses)
                if a[0]=='area' and a[1]==a1[1]:
                    if image[0]==target:
                        positive_list.append(float(a[2]))
                    else:
                        negative_list.append(float(a[2]))
        for number in positive_list:
            if number>variable2:
                positive_greater+=1
        for number in negative_list:
            if number>variable2:
                negative_greater+=1
        if positive_greater>2/3*len(positive_list) and negative_greater<=1/3*len(negative_list):
            return variable2,10000
        elif positive_greater<=1/3*len(positive_list) and negative_greater>2/3*len(negative_list):
            return 0,variable2
        else:
            return False

def still_has(possible_clause,foil_gain_list):
    has=False
    for clause_num,clauses in enumerate(possible_clause):
        a=re.split(r'[(|,|)]',clauses)
        if a[1]=='X' and foil_gain_list[clause_num]!=-99:
            has=True
            break
    return has

def still_has_num(result):
    has=0
    for clause_num,clauses in enumerate(result):
        a=re.split(r'[(|,|)]',clauses)
        if a[1]=='X':
            has+=1
    return has

def get_object_list(total_list):
    object_list=[]
    for image in total_list:
        for clauses in image:
            a=re.split(r'[(|,|)]',clauses)
            if a[0]!='overlap' and a[0]!='num' and a[0]!='area' and len(a)==4 and (a[0] not in object_list):
                object_list.append(a[0])
    return object_list

def get_object_list_v2(total_list):
    object_list=[]
    for image in total_list:
        for idx,clauses in enumerate(image):
            if idx!=0:
                object_list.append(clauses)
    return object_list


def unique_list(A):
    res = []
    for i in range(len(A)):
        res.append([A[i][0]])
        seen = set()
        res[i].extend([predicate for predicate in A[i][1::] if not (predicate in seen or seen.add(predicate))] )
    return res

def covered_instance(new_predicate, total_list1, target, now_clause = [], rule_list = [], i=0, counting=0):
    new_now_clause=copy.deepcopy(now_clause)
    new_rule_list=copy.deepcopy(rule_list)
    new_now_clause.append(new_predicate) #子句添加谓语
    new_rule_list.append(new_now_clause)
    if counting!=0:          #Each time, because we add the updated version at the end of the list, so delete the old version
        del new_rule_list[i]  
    new_total_list=get_new_total_list_cover(new_rule_list,total_list1)
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
        with open(path,'r') as f:
            rule = yaml.load(f,Loader=yaml.FullLoader)
            p_list = [p for clause in rule[target] for p in clause]
            for p in p_list:
                p=re.split(r'[(|,|)]',p)
                p=p[0]
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

def foil(target_list,object_list,target,total_list,variable1,variable2,rule_base,decay_dir,foil_gain):         #target should be a string, such as "guitarist"
    
    result_list=[]     
    new_total_list = unique_list(total_list)
    object_list=get_object_list(new_total_list)
    total_list1=copy.deepcopy(new_total_list)

    print(f"updating daecay factor......")
    if os.path.isfile(f"{decay_dir}/{target}_decay.yaml"):
        with open(f"{decay_dir}/{target}_decay.yaml","r") as decay_f:
            p_decay_factor = yaml.load(decay_f,yaml.FullLoader)
            decay_f.close()
    else:
        p_decay_factor = decay_factor(total_list,object_list,target)
        with open(f"{decay_dir}/{target}_decay.yaml","w") as decay_f:
            yaml.dump(p_decay_factor,decay_f,sort_keys=False)
            decay_f.close()

    p_count = p_times_count(rule_base,target)

    positive_list,negative_list=pos_neg_list(target,new_total_list)   
    c=re.split(r'[(|,|)]',target)
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
            possible_clause=get_possible_clause1(counting,total_list1,result_list)
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

                obj = re.split(r'[(|,|)]',new_clause)
                obj = obj[0]
                if p_count.get(obj) == None or p_decay_factor.get(obj) == None:
                    score = foil_gain(pre_p,pre_n,now_p,now_n)
                    foil_gain_list.append(score)
                else:
                    score = foil_gain(pre_p,pre_n,now_p,now_n)
                    decay = p_decay_factor[obj]
                    times = p_count[obj]
                    score = score*(decay**times)
                    foil_gain_list.append(score)

            correct_clause=False             
            parameter_list=get_parameter_list(result)

            while correct_clause == False:
                for clause_number,clause_gain in enumerate(foil_gain_list):
                    if max(foil_gain_list)==min(foil_gain_list):
                        return None
                    if clause_gain==max(foil_gain_list):
                        a=re.split(r'[(|,|)]',possible_clause[clause_number])
                        if a[0]=="overlap":
                            if (a[1] in parameter_list) and (a[2] in parameter_list) and still_has_num(result)>=2:
                                new_result=copy.deepcopy(result)  
                                new_result.append(possible_clause[clause_number])      
                                result_list.append(new_result)
                                correct_clause=True
                                break
                            else:
                                foil_gain_list[clause_number]=-99
                                break
                        elif a[0]=="num" or a[0]=='area':
                            if a[1] in parameter_list and threshold(target,possible_clause[clause_number],total_list1,variable1,variable2)!=False and still_has_num(result)>=3:
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
            new_total_list=get_new_total_list(result_list,total_list1)

            positive_list,negative_list=pos_neg_list(target,new_total_list)   

            counting+=1           
        new_total_list=get_new_total_list1(result_list,total_list1)
        positive_list,negative_list=pos_neg_list(target,new_total_list)
        print(f"Iteration: {i}")
        print("Rule:",result_list)
        i+=1
        
    return result_list

def set_rules(dict_math):
    res = dict()
    for target in dict_math:
        res[target] = [dict_math[target][0]]
    for target in dict_math:
        for idx in range(1,len(dict_math[target])):
            for idx_ in range(len(res[target])):
                r1 = sorted(dict_math[target][idx])
                r2 = sorted(res[target][idx_])
                flag = False
                if r1==r2:
                    flag = True
                    break
            if not flag:
                res[target].append(r1) 
    return res


def FOIL(input_list, rule_save_path, rule_base, decay_dir, foil_gain):
    global_variable1=10
    global_variable2=30

    dict_math={}
    dict_nl={}

    total_list1=get_total_list1(input_list)
    total_list=get_total_list(total_list1)

    object_list=get_object_list(total_list)
    target_list=[]
    for images in total_list:
        if images[0] not in target_list:
            target_list.append(images[0])

    for target in target_list:
        result_list=foil(target_list,object_list,target,total_list,global_variable1,global_variable2,rule_base,decay_dir,foil_gain=foil_gain)
        if result_list==None:
            dict_math[target]=[['none']]

        else:
            math_format=get_result_list(target,result_list,total_list,global_variable1,global_variable2)
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

    #记录子句中的谓词索引
    object_in_rule=[]
    object_character=[]
    #计算谓词得分
    for position,predicate in enumerate(clause):
            a=re.split(r'[(|,|)]',predicate)
            if a[0]!='overlap' and a[0]!='num' and a[0]!='area' and len(a)==4:
                object_in_rule.append(a[0])
                object_character.append(a[2])
    #对子句中的谓词计算得分

    for position,predicate in enumerate(clause):
        T_pos_with_A = 0
        T_neg_with_A = 0
        a=re.split(r'[(|,|)]',predicate)
        if a[0]!='overlap' and a[0]!='num' and a[0]!='area' and len(a)==4:
            #存在性判断
            for image in pos_list:
                for predicate_img in image:
                    b=re.split(r'[(|,|)]',predicate_img)
                    if b[0]==a[0]:
                        T_pos_with_A+=1
                        break
            for image in neg_list:
                for predicate_img in image:
                    b=re.split(r'[(|,|)]',predicate_img)
                    if b[0]==a[0]:
                        T_neg_with_A+=1
                        break
        elif a[0]=='overlap':
            #确定规则谓词所含目标的索引
            object1_in_rule=object_in_rule[object_character.index(a[1])]
            object2_in_rule=object_in_rule[object_character.index(a[2])]
            for image in pos_list:
                #确定每张图的目标索引
                object_in_image=[]
                object_number=[]
                for predicate_img in image:
                    b=re.split(r'[(|,|)]',predicate_img)
                    if b[0]!='overlap' and b[0]!='num' and b[0]!='area':
                        object_in_image.append(b[0])
                        object_number.append(b[2])
                for predicate_img in image:
                    b=re.split(r'[(|,|)]',predicate_img)
                    if b[0]==a[0]:
                        object1_in_image=object_in_image[object_number.index(b[1])]
                        object2_in_image=object_in_image[object_number.index(b[2])]
                        if object1_in_image==object1_in_rule and object2_in_image==object2_in_rule:
                            T_pos_with_A+=1
                            break
            for image in neg_list:
                #确定每张图的目标索引
                object_in_image=[]
                object_number=[]
                for predicate_img in image:
                    b=re.split(r'[(|,|)]',predicate_img)
                    if b[0]!='overlap' and b[0]!='num' and b[0]!='area':
                        object_in_image.append(b[0])
                        object_number.append(b[2])
                for predicate_img in image:
                    b=re.split(r'[(|,|)]',predicate_img)
                    if b[0]==a[0]:
                        object1_in_image=object_in_image[object_number.index(b[1])]
                        object2_in_image=object_in_image[object_number.index(b[2])]
                        if object1_in_image==object1_in_rule and object2_in_image==object2_in_rule:
                            T_neg_with_A+=1
                            break
        elif a[0]=='num' or a[0]=='area':
            #确定规则谓词所含目标的索引
            object1_in_rule=object_in_rule[object_character.index(a[1])]
            for image in pos_list:
                #确定每张图的目标索引
                object_in_image=[]
                object_number=[]
                for predicate_img in image:
                    b=re.split(r'[(|,|)]',predicate_img)
                    if b[0]!='overlap' and b[0]!='num' and b[0]!='area':
                        object_in_image.append(b[0])
                        object_number.append(b[2])
                for predicate_img in image:
                    b=re.split(r'[(|,|)]',predicate_img)
                    if b[0]==a[0]:
                        object1_in_image=object_in_image[object_number.index(b[1])]
                        c=re.split(r'[<]',clause[position+1]) #阈值
                        if len(c)!=1:
                            maxi=float(c[1])
                            if object1_in_image==object1_in_rule and float(b[2])<=maxi:
                                T_pos_with_A+=1
                                break
                        else:
                            c=re.split(r'[>]',clause[position+1])
                            mini=float(c[1])
                            if object1_in_image==object1_in_rule and mini<float(b[2]):
                                T_pos_with_A+=1
                                break
            for image in neg_list:
                #确定每张图的目标索引
                object_in_image=[]
                object_number=[]
                for predicate_img in image:
                    b=re.split(r'[(|,|)]',predicate_img)
                    if b[0]!='overlap' and b[0]!='num' and b[0]!='area':
                        object_in_image.append(b[0])
                        object_number.append(b[2])
                for predicate_img in image:
                    b=re.split(r'[(|,|)]',predicate_img)
                    if b[0]==a[0]:
                        object1_in_image=object_in_image[object_number.index(b[1])]
                        c=re.split(r'[<]',clause[position+1]) #阈值
                        if len(c)!=1:
                            maxi=float(c[1])
                            if object1_in_image==object1_in_rule and float(b[2])<=maxi:
                                T_neg_with_A+=1
                                break
                        else:
                            c=re.split(r'[>]',clause[position+1])
                            mini=float(c[1])
                            if object1_in_image==object1_in_rule and mini<float(b[2]):
                                T_neg_with_A+=1
                                break
    
        tf = T_pos_with_A/len(pos_list)
        idf = np.log(len(neg_list)/(1e-5+T_neg_with_A))

        clause_predicate_scores.append(tf*idf)
        

    return float(min(clause_predicate_scores))       


def rules_score(input_list:list,rule_list:dict,save_path:str,score_func=scores): 
    total_list1=get_total_list1(input_list)
    total_list=get_total_list(total_list1)
    rules_score_dict = dict()
    for target in rule_list.keys():
        score=list()
        for clause in rule_list[target]:
            score.append(float(score_func(total_list,clause,target)))
        rules_score_dict[target]={"rule":rule_list[target],"score":score}
    with open(save_path,'w') as f:
        yaml.dump(rules_score_dict,f,sort_keys=False)