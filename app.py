# import pandas
import numpy
from operator import itemgetter, attrgetter, methodcaller

class Video():
    def __init__(self, id, size):
        self.id = id
        self.size = size

    def __str__(self):
        return str((self.id, self.size))

class Cache():
    def __init__(self, id, max_capacity):
        self.id = id
        self.max_capacity = max_capacity
        self.videos = []

    def get_capacity(self):
        return sum(map(lambda video: video.size, self.videos))

    def add_video(self, video):
        if (self.get_capacity() + video.size) > self.max_capacity:
            return False
    
        for v in self.videos:
            if v.id == video.id:
                return False

        self.videos.append(video)
        return True

    def __str__(self):
        return str((self.id, self.max_capacity, self.videos))

class Request():
    def __init__(self, id, video, endpoint, count):
        self.id = id
        self.video = video
        self.endpoint = endpoint
        self.count = count

    def __str__(self):
        return str((self.id, self.video, self.endpoint, self.count))

class Connection():
    def __init__(self, endpoint, cache, latency):
        self.endpoint = endpoint
        self.cache = cache
        self.latency = latency

    def __str__(self):
        return str((self.cache, self.latency))

class Endpoint():
    def __init__(self, id, latency_dc, connections):
        self.id = id
        self.latency_dc = latency_dc
        self.connections = connections

    def __str__(self):
        return str((self.id, self.latency_dc, self.connections))

def get_thing_by_id(id, things):
    for thing in things:
        if thing.id == id:
            return thing
    return None

def read_file(file_name):
    f = open('dataset/' + file_name + '.in', 'r')

    first_line = f.readline().split()

    V = int(first_line[0]) # number of videos
    E = int(first_line[1]) # number of endpoints
    R = int(first_line[2]) # number of request descriptions
    C = int(first_line[3]) # number of cache servers
    X = int(first_line[4]) # capacity cache MB

    caches = []
    for c in range(C):
        caches.append(Cache(c, X))

    second_line = f.readline()

    Sn = numpy.fromstring(second_line, dtype=int, sep=' ') #  individual videos MB

    videos = []
    for idx, sn in enumerate(Sn):
        videos.append(Video(idx, sn))

    endpoints = []

    for e in range(E):
        line = f.readline().split()
        Ld = int(line[0]) # the latency of serving a video request from the data center to this D <= 4 endpoint, in milliseconds
        K = int(line[1]) #  the number of cache servers that this endpoint is connected to
        
        endpoint = Endpoint(e, Ld, [])

        connections = []
        entry = (Ld, [])
        for k in range(K):
            another_line = f.readline().split()
            c = int(another_line[0])
            Lc = int(another_line[1])
            connections.append(Connection(endpoint, get_thing_by_id(c, caches), Lc))
        endpoint.connections = connections
        endpoints.append(endpoint)

    requests = []

    for r in range(R):
        line = f.readline().split()
        Rv = int(line[0]) #  ID of the requested video
        Re = int(line[1]) # ID of the endpoint from which the requests are coming from  x
        Rn = int(line[2]) # the number of requests
        requests.append(Request(r, get_thing_by_id(Rv, videos), get_thing_by_id(Re, endpoints), Rn))

    return (endpoints, requests, videos, caches)

def bad_solution(endpoints, requests, videos, cache_servers, capacity_cache):
    allocations = []

    video_i = 0

    for c in range(cache_servers):
        if video_i >= len(videos):
            break # no more videos

        added_to_cache = 0
        entry = ((c, []))
        while (added_to_cache + videos[video_i]) < capacity_cache and video_i < len(videos):
            video = videos[video_i]
            if video > capacity_cache: # doesnt fit anywere, skip video
                video_i += 1
                continue

            added_to_cache += video
            entry[1].append(video_i)
            video_i += 1
        allocations.append(entry)

    return allocations

def bad_solution2(endpoints, requests, videos, cache_servers, capacity_cache):
    allocations = []

    video_i = 0
    
    def request_for_i(video_idx, requests):
        for r in requests:
            if r[0] == video_idx:
                return r[2]

    videos_full = map(lambda (idx, val): (idx, val, request_for_i(idx, requests)), enumerate(videos))

    videos_sorted = sorted(videos_full, key=itemgetter(2), reverse=True)

    # print videos_sorted

    for c in range(cache_servers):
        if video_i >= len(videos_sorted):
            break # no more videos

        added_to_cache = 0
        entry = ((c, []))
        while (added_to_cache + videos_sorted[video_i][1]) < capacity_cache and video_i < len(videos_sorted):
            video = videos_sorted[video_i]
            if video[1] > capacity_cache: # doesnt fit anywere, skip video
                video_i += 1
                continue

            added_to_cache += video[1]
            entry[1].append(video[0])
            video_i += 1
        allocations.append(entry)

    return allocations

def score_solution(allocations = []):
    pass

def print_solution(file_name, caches):
    with open('dataset/' + file_name + '.out', 'w') as outf:
        outf.write(str(len(caches)) + '\n')
        for cache in caches:
            outf.write(str(cache.id))
            for video in cache.videos:
                outf.write(' ' + str(video.id))
            outf.write('\n')

def lol_solution(endpoints, requests, videos, caches):
    requests_sorted = sorted(requests, key=attrgetter('count'), reverse=True)

    for req in requests_sorted:
        for connection in req.endpoint.connections:
            connection.cache.add_video(req.video)


files = ['videos_worth_spreading']

for f in files:
    (endpoints, requests, videos, caches) = read_file(f)
    lol_solution(endpoints, requests, videos, caches)
    print_solution(f, caches)
