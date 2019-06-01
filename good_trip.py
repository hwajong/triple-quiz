#!/usr/bin/env python3
import sys
import os

# return places, m
# - places : dict(no : [장소명, 소요시간, 만족도])
# - m      : 여행시간
def parse_input_file():
    argc = len(sys.argv)
    if argc != 2:
        progname = os.path.basename(sys.argv[0])
        print('* Usage: %s INPUT_FILE' % progname)
        exit(1)

    infile = sys.argv[1]
    with open(infile) as f:
        firstline = f.readline().strip()
        firstline_tokens = firstline.split(',')
        if len(firstline_tokens) != 2:
            print('Error: invalid input file - firstline [%s]' % firstline)
            exit(1)

        n = int(firstline_tokens[0])  # 장소들의 개수
        m = int(firstline_tokens[1])  # 여행 시간

        places = {}

        place_no = 0
        for line in f:
            place = line.strip()
            place_tokens = place.split(',')
            if len(place_tokens) != 3:
                print('Error: invalid input file - place [%s]' % place)
                exit(1)

            name = place_tokens[0]
            need_time = int(place_tokens[1])
            rating = int(place_tokens[2])

            places[place_no] = list((name, need_time, rating))
            place_no += 1

        if len(places) != n:
            print('Error: invalid input file - number of places')
            exit(1)

    return places, m


# 장소들을 여행하는데 필요한 시간의 합 리턴
def cal_visits_need_times(visit):
    return sum([t for no, t, s in visit.values()])


# 장소들을 여행애 얻는 만족도의 합 리턴
def cal_visits_ratings(visit):
    return sum([s for no, t, s in visit.values()])


# 방문한 장소들의 해시값 리턴 - 중복체크 제거를 위해
def make_visited_places_hash(visit):
    return ','.join(sorted([str(no) for no in visit.keys()]))

# places  : 입력 받은 장소 정보
# m       : 여행시간
# visit   : 테스트 중인 장소들의 Dict
# results : 결과를 저장할 Dict
def dfs(places, m, visits, results):
    visit_need_times = cal_visits_need_times(visits)
    visit_ratings = cal_visits_ratings(visits)

    added = False
    for place_no in places.keys():
        if place_no not in visits:
            if visit_need_times + places[place_no][1] > m:
                if not added and visit_ratings >= results['max_ratings']:
                    added = True
                    results['max_ratings'] = visit_ratings
                    # print(visit_need_times, visit_ratings, visit)

                    if results['max_ratings'] > results['ratings']:
                        results['ratings'] = results['max_ratings']
                        results['best_places'].clear()

                    results['best_places'].append(visits.copy())

                continue

            visits[place_no] = places[place_no]
            visited_places_hash = make_visited_places_hash(visits)
            if visited_places_hash not in results['visited_set']:
                results['visited_set'].add(visited_places_hash)
                dfs(places, m, visits, results)

            del visits[place_no]

def main():
    places, m = parse_input_file()

    results = {
        'max_ratings': 0,
        'visited_set': set(),
        'ratings': 0,
        'best_places': []
    }

    dfs(places, m, {}, results)

    print(results['ratings'])

    # for place in results['best_places']:
    #     print(place)


if __name__ == '__main__':
    main()
