# import pandas
import numpy

KITTENS = 'dataset/kittens.in'
ME_AT_THE_ZOO = 'dataset/me_at_the_zoo.in'

f = open(ME_AT_THE_ZOO, 'r')

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

print(endpoints)
print(requests)
