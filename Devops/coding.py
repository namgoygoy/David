def solution(t, p):
    answer = 0
    p_num = int(p)
    p_len = len(p)
    
    for i in range(len(t) - p_len + 1):
        num += t[i: i + p_len]
        if num [i] <= p_num:
            answer += 1
    return answer