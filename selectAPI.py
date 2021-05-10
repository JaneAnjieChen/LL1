
#
# def follow(non_terminal, terminal, expression_dict, first_dict):
#     follow_dict = {}
#     # S 为文法的开始符号，把#加入follow_dict["S"]中
#     # 初始化
#     for i in non_terminal:
#         if i == 'S':
#             follow_dict[i] = ['#']
#         else:
#             follow_dict[i] = []
#
#      # 开始，令Follow(A)={}
#      # ① 若有 X→…Aa…, a∈VT, 则把a加入到Follow(A)中
#      # ② 若有 X→…ABβ, B ∈VN,则把First(Bβ)- {ε}加入到Follow(A)中
#      # ③ 若有 X→…A 或 X→…Aβ且ε∈ First(β)，则把Follow(X)加入到Follow(A)中
#
#     # 1
#     for key, value in follow_dict.items():
#         for k, v in expression_dict.items():
#
#             for element in v:
#                 if key in element:
#                     index = element.index(key)
#
#                     if index+1 < len(element):
#
#                         if element[index+1] in terminal:
#                             follow_dict[key].append(element[index+1])
#
#                         if element[index+1] in non_terminal:
#                             for i in first_dict[element[index+1]]:
#                                 if i is not '$' and i not in follow_dict[key]:
#                                     follow_dict[key].append(i)
#                     # 是最后一个
#                     else:
#                         for i in follow_dict[k]:
#                             if i not in follow_dict[key]:
#                                 follow_dict[key].append(i)
#
#     print(follow_dict)
#     # 2


def select(non_terminal, terminal, expression_dict, first_dict, follow_dict):
    select_dict = {}
    first_expression_dict = {}
    # 遍历每条语句
    max = 0
    for key, value in expression_dict.items():
        for v in value:
            if len(v) > max:
                max = len(v)

    for length in range(1, max+1):
        for key, value in expression_dict.items():
            for v in value:
                # 找出 first(v)
                first_v = []
                if len(v) == length:
                    # when length ==1
                    if v == "$":
                        first_v.append('$')
                    elif v in terminal:
                        first_v.append(v)
                    elif v in non_terminal:
                        first_v.append(i for i in list(first_dict[v]))

                    # when length > 1
                    elif v[0] in terminal:
                        first_v.append(v[0])
                    elif v[0] in non_terminal:
                        if '$' not in first_dict[v[0]]:
                            first_v.append(i for i in list(first_dict[v[0]]))
                        else:
                            rest = v[1:]
                            tmp_dict = dict(first_expression_dict, **first_dict)
                            # print(length, tmp_dict)
                            for skey, svalue in tmp_dict.items():
                                if rest == skey:
                                    x = svalue
                                    break
                                else:
                                    x = set('$')
                            first_v = x.union(first_dict[v[0]]-{'$'})

                if len(first_v) != 0:
                    first_expression_dict[v] = set(first_v)
        length += 1
    # print(first_expression_dict)

    for key, value in expression_dict.items():
        for v in value:
            select_key = (key, v)
            if '$' not in list(first_expression_dict[v]):
                select_dict[select_key] = first_expression_dict[v]
            else:
                select_dict[select_key] = follow_dict[key].union(first_expression_dict[v]-{'$'})
    # print(select_dict)

    keys = []
    for key, value in select_dict.items():
        if key[0] not in keys:
            keys.append(key[0])
    # print(keys)

    intersections = []
    for key in keys:
        # sets
        tmp_sets = []
        for k, v in select_dict.items():
            if k == key:
                tmp_sets.append(v)

        tmp_intersaction = set()
        for s in tmp_sets:
            tmp_intersaction = tmp_intersaction.intersection(s)
        intersections.append(tmp_intersaction)

    # print(intersections)

    # 判断是否都是空
    count = 0
    for i in intersections:
        if i == set():
            count += 1

    ll1_flag = False
    if count == len(non_terminal):
        ll1_flag = True
        print('Is LL(1).')
    else:
        print('Is not LL(1).')

    return select_dict, ll1_flag

# ('S', 'AB'): {'a', '#', 'b'} -> {('S','b'):{'AB'}, ('S','a'):{'AB'}, ('S','#'):{'AB'}}
def select_api(select_dict):
    new_select_dict = {}
    # print(select_dict)
    for key, value in select_dict.items():
        for v in value:
            tmp_key = (list(key)[0], v)
            new_select_dict[tmp_key] = list(key)[1]

    # print(new_select_dict)
    return new_select_dict


if __name__ == '__main__':
    non_terminal = ['S', 'A', 'B', 'C', 'D']
    terminal = ['c', 'b', 'a', '$']
    expression_dict = {'S':{'AB','bC'}, 'A':{'$','b'}, 'B':{'$','aD'}, 'C':{'AD','b'}, 'D':{'aS','c'}}
    first_dict = {'S':{'a', 'b','$'},'A':{'b','$'}, 'B':{'a','$'}, 'C':{'a','b','c'}, 'D':{'a','c'}}
    # follow(non_terminal, terminal, expression_dict, first_dict)
    follow_dict = {'S':{'#'},'A':{'a','c','#'},'B':{'#'},'C':{'#'},'D':{'#'}}
    select_dict,ll1_flag = select(non_terminal, terminal, expression_dict, first_dict, follow_dict)
    select_api(select_dict)









