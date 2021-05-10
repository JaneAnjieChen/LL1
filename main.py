# -*- coding: utf-8 -*-
'''
To-do:
- 未经大量数据验证的first和follow集生成
- 缺少左递归判断
'''

# 外调函数简单说明：
# select(list non_terminal, list terminal, dict expression_dict, dict first_dict, dict follow_dict)
# return (dict select_dict)
#
# select_api(dict select_dict)
# return (dict needed_select_dict, BOOL ll1_flag)
# ll1_flag = True则表明是LL(1)文法


import re
from queue import Queue
from selectAPI import select, select_api

first = {}
follow = {}
expression = {}
terminators = set()
non_terminators = set()


def read(path):
    global first
    global expression
    global terminators
    global non_terminators
    with open(path) as f:
        lines = f.readlines()
        for line in lines:
            right_list = []
            line = line.replace('\n', '')
            terminators = terminators | set(re.findall("[a-z]", line))
            non_terminators = non_terminators | set(re.findall("[A-Z]", line))
            left_str, right_str = line.split("->")
            right_list.append(right_str)
            if left_str in expression.keys():
                expression[left_str] = right_list.extend(expression[left_str])
            expression[left_str] = right_list
    return 0


def findfirst(term) -> set():
    finded = set()
    right_strs = expression[term]
    for right_str in right_strs:
        if right_str == "$":
            finded |= set("$")
        elif right_str[0] in terminators:
            finded |= set(right_str[0])
        elif right_str[0] in non_terminators:
            finded |= findfirst(right_str[0])
            if len(right_str) > 1:
                finded.discard('$')
            i = 0
            while i <= len(right_str) - 1 and '$' in findfirst(right_str[i]):
                i += 1
                if i < len(right_str):
                    temp = findfirst(right_str[i])
                    temp.discard('$') if i!=len(right_str)-1 else temp
                    finded |= temp
        else:
            finded |= findfollow(right_str[0])
    return finded


def findfollow(term):
    finded = set("#")
    for right_strs in expression.values():
        for right_str in right_strs:
            if term in right_str and right_str[-1] != term:
                right_str = str(right_str)
                next_term = right_str[right_str.index(term) + 1]
                if next_term in terminators:
                    finded |= set(next_term)
                elif next_term in non_terminators:
                    temp = findfirst(next_term)
                    temp.discard('$')
                    finded |= temp
    return finded


def getfirstandfollow():
    global first
    global follow
    for i in non_terminators:
        first[i] = findfirst(i)
    for i in non_terminators:
        follow[i] = findfollow(i)


if __name__ == '__main__':
    path = 'in2.txt'
    read(path)
    print(expression)

    getfirstandfollow()
    print(first)
    print(follow)

    select_dict,ll1_flag = select(non_terminators, terminators, expression, first, follow)
    print(select_dict, ll1_flag)

    select_api_dict = select_api(select_dict)
    print(select_api_dict)


