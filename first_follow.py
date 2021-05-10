# -*- coding: utf-8 -*-
'''
To-do:
- 未经大量数据验证的first和follow集生成
- 缺少左递归判断
'''


import re
from queue import Queue


def read(file):
    expression = {}
    terminators = set()
    non_terminators = set()
    with open(file) as f:
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
    return expression, terminators, non_terminators


# def generatefirst():
#     first = {}
#     expression = {}
#     terminators = set()
#     non_terminators = set()
#     non_terminators, terminators, expression = read(non_terminators, terminators, expression)
#
#     for key, value in expression.items():
#         for left_str in value:
#             id = 0
#             while id < len(left_str):
#                 # 终结符
#                 if left_str[id] in terminators or left_str == "$":
#                     if key in first.keys():
#                         first[key] = first[key] | set(left_str[0])
#                     else:
#                         first[key] = set(left_str[0])
#                 # 非终结符
#
#                 # 空
#                 if "$" in expression[left_str[id]]:
#                     id += 1
#                 else:
#                     break
#
#             # 非终结符
#             # q = Queue()
#             # vis = {}
#             # q.put(left_str[0])
#             # vis[left_str[0]] = 1
#             # while q.not_empty:
#             #     t = q.get()
#             #     for i in expression[t]:
#     print(first)
#
#     return non_terminators, terminators, expression


def findfirst(term, expression, terminators, non_terminators) :
    finded = set()
    if term in terminators:
        return set(term)
    right_strs = expression[term]
    for right_str in right_strs:
        if right_str == "$":
            finded |= set("$")
        elif right_str[0] in terminators:
            finded |= set(right_str[0])
        elif right_str[0] in non_terminators:
            finded |= findfirst(right_str[0], expression, terminators, non_terminators)
            if len(right_str) > 1:
                finded.discard('$')
            i = 0
            while i <= len(right_str) - 1 and '$' in findfirst(right_str[i], expression, terminators, non_terminators):
                i += 1
                if i < len(right_str):
                    temp = findfirst(right_str[i], expression, terminators, non_terminators)
                    temp.discard('$') if i!=len(right_str)-1 else temp
                    finded |= temp
        else:
            finded |= findfollow(right_str[0], expression, terminators, non_terminators)
    return finded


def findfollow(term, expression, terminators, non_terminators):
    finded = set("#")
    for right_strs in expression.values():
        for right_str in right_strs:
            if term in right_str and right_str[-1] != term:
                right_str = str(right_str)
                next_term = right_str[right_str.index(term) + 1]
                if next_term in terminators:
                    finded |= set(next_term)
                elif next_term in non_terminators:
                    temp = findfirst(next_term, expression, terminators, non_terminators)
                    temp.discard('$')
                    finded |= temp
    return finded


def getfirstandfollow():
    first = {}
    follow = {}
    file = "in.txt"
    expression, terminators, non_terminators = read(file)
    for i in non_terminators:
        first[i] = findfirst(i, expression, terminators, non_terminators)
    for i in non_terminators:
        follow[i] = findfollow(i, expression, terminators, non_terminators)
    return expression, terminators, non_terminators, first, follow


if __name__ == '__main__':
    expression, terminators, non_terminators, first, follow = getfirstandfollow()
    print(first, follow)



