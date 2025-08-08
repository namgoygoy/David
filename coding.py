def solution(name, yearning, photo):
    score_map = {}
    for i in range(len(name)):
        score_map[name[i]] = yearning[i]
    
    answer = []

    for photo_list in photo:
        total_score = 0
        for person in photo_list:
            total_score += score_map.get(person,0)
        answer.append(total_score)
    return answer