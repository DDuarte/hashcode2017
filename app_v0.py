# import pandas
import numpy

def read_file(file_name):
    f = open('dataset/' + file_name + '.in', 'r')

    first_line = f.readline().split()

    V = int(first_line[0]) # number of videos
    E = int(first_line[1]) # number of endpoints
    R = int(first_line[2]) # number of request descriptions
    C = int(first_line[3]) # number of cache servers
    X = int(first_line[4]) # capacity cache MB

    second_line = f.readline()

    Sn = numpy.fromstring(second_line, dtype=int, sep=' ') #  individual videos MB

    endpoints = []

    for e in range(E):
        line = f.readline().split()
        Ld = int(line[0]) # the latency of serving a video request from the data center to this D <= 4 endpoint, in milliseconds
        K = int(line[1]) #  the number of cache servers that this endpoint is connected to
        entry = (Ld, [])
        for k in range(K):
            another_line = f.readline().split()
            c = int(another_line[0])
            Lc = int(another_line[1])
            entry[1].append((c, Lc))
        endpoints.append(entry)

    requests = []

    for r in range(R):
        line = f.readline().split()
        Rv = int(line[0]) #  ID of the requested video
        Re = int(line[1]) # ID of the endpoint from which the requests are coming from  x
        Rn = int(line[2]) # the number of requests
        requests.append((Rv, Re, Rn))


    return (endpoints, requests, Sn, C, X)


def weight_solution(endpoints, requests, videos, cache_servers, capacity_cache):

    Weighted = []

    for i,s in enumerate(videos):
        totas = list(filter(lambda x: x[0] == i, requests))
        if totas != []:
            total = [sum(x) for x in zip(*totas)][2]
            #print(total)
            entry = (i, s, total)
            Weighted.append(entry)

    videos =  sorted(Weighted, key=lambda ent: ent[2], reverse=True)
    allocations = []

    #print(videos)

    video_i = 1

    for c in range(cache_servers):
        if video_i >= len(videos):
            break # no more videos

        added_to_cache = videos[0][1]
        entry = ((c, [videos[0][0]]))
        while (added_to_cache + videos[video_i][1]) < capacity_cache and video_i < len(videos):
            video = videos[video_i][1]
            if video > capacity_cache: # doesnt fit anywere, skip video
                video_i += 1
                continue

            added_to_cache += videos[video_i][1]
            entry[1].append(videos[video_i][0])
            video_i += 1
        allocations.append(entry)

    return allocations

def bad_solution(endpoints, requests, videos, cache_servers, capacity_cache):
    allocations = []

    video_i = 0

    for c in range(cache_servers):
        if video_i >= len(videos):
            break # no more videos

        added_to_cache = 0
        entry = ((c, []))
        while (added_to_cache + videos[video_i][1]) < capacity_cache and video_i < len(videos):
            video = videos[video_i]
            if video > capacity_cache: # doesnt fit anywere, skip video
                video_i += 1
                continue

            added_to_cache += video
            entry[1].append(videos[video_i])
            video_i += 1
        allocations.append(entry)

    return allocations

def score_solution(allocations = []):
    pass

def print_solution(file_name, allocations):
    with open('dataset/' + file_name + '.out', 'w') as outf:
        N = len(allocations)
        outf.write(str(N) + '\n')
        i = 0
        for alloc in allocations:
            outf.write(str(i))
            for alloc_c in alloc[1]:
                outf.write(' ' + str(alloc_c))
            outf.write('\n')
            i += 1

files = ['me_at_the_zoo', 'kittens', 'trending_today', 'videos_worth_spreading']

for f in files:
    (endpoints, requests, videos, cache_servers, capacity_cache) = read_file(f)
    allocations = weight_solution(endpoints, requests, videos, cache_servers, capacity_cache)
    print_solution(f, allocations)
