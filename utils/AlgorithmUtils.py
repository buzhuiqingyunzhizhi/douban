# -*- coding: utf-8 -*-
# pro1  AlgorithmUtils
# uni
# author : huagnlei
# 2018/6/7 20:53
#
from utils import DBUtils
from math import sqrt


def findAllJson2():
    db = DBUtils.DBUtils("localhost", "python", "python", "movie", 3306)
    sql = 'SELECT DISTINCT h.uid,h.score,m.movieName from history h ,movie m where h.mid=m.id'
    result = db.query(sql)
    dic0 = {}
    for line in result:
        dic1 = {line[2]: line[1]}
        try:
            dic0[line[0]].update(dic1)
        except Exception as e:
            dic0[line[0]] = dic1
    return dic0


# Returns the Pearson correlation coefficient for p1 and p2
def sim_pearson(prefs, p1, p2):
    # Get the list of mutually rated items
    si = {}
    for item in prefs[p1]:
        if item in prefs[p2]:
            si[item] = 1

    # if they are no ratings in common, return 0
    if len(si) == 0:
        return 0

    # Sum calculations
    n = len(si)

    # Sums of all the preferences
    sum1 = sum([prefs[p1][it] for it in si])
    sum2 = sum([prefs[p2][it] for it in si])

    # Sums of the squares
    sum1Sq = sum([pow(prefs[p1][it], 2) for it in si])
    sum2Sq = sum([pow(prefs[p2][it], 2) for it in si])

    # Sum of the products
    pSum = sum([prefs[p1][it] * prefs[p2][it] for it in si])

    # Calculate r (Pearson score)
    num = pSum - (sum1 * sum2 / n)
    den = sqrt((sum1Sq - pow(sum1, 2) / n) * (sum2Sq - pow(sum2, 2) / n))
    if den == 0:
        return 0

    r = num / den
    return r


# Gets recommendations for a person by using a weighted average
# of every other user's rankings
def getRecommendations(prefs, person, similarity=sim_pearson):
    if person not in prefs:
        print('%s这个人不存在' % person)
        person = '2'
    totals = {}
    simSums = {}
    for other in prefs:
        # don't compare me to myself
        if other == person: continue
        sim = similarity(prefs, person, other)
        # print('sim 1 ', sim)
        # ignore scores of zero or lower
        # if sim <= 0: continue
        for item in prefs[other]:

            # only score movies I haven't seen yet
            if item not in prefs[person] or prefs[person][item] == 0:
                # Similarity * Score
                totals.setdefault(item, 0.001)
                totals[item] += prefs[other][item] * sim
                # Sum of similarities
                simSums.setdefault(item, 0.001)
                simSums[item] += sim

    # Create the normalized list

    rankings = [(total / simSums[item], item) for item, total in totals.items()]

    # Return the sorted list
    rankings.sort()
    rankings.reverse()
    return rankings
