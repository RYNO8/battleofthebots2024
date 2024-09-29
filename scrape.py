import requests
from os import path
import os
import re
from collections import defaultdict
import argparse
import statistics

if not path.exists("logs/"):
    os.mkdir("logs")

def getStrat(filename):
    with open(f"logs/{filename}") as f:
        for line in f.readlines():
            match = re.match(r"Sounds Good: STRAT=(.*)\n", line)
            if match:
                return match.group(1)
    return None

def parseFile(filename):
    with open(f"logs/{filename}") as f:
        lines = [line.strip() for line in f.readlines()]
        players = eval(re.match(r"Engine: Match has begun with participants (.*)", lines[0]).group(1))
        wins = [0, 0, 0, 0]
        scores = [0, 0, 0, 0]
        for line in lines:
            winsMatch = re.match(r"Engine: (.*) won the game!", line)
            if winsMatch:
                player = winsMatch.group(1)
                wins[players.index(player)] += 1
            scoreMatch = re.match(r"Engine: (.*) finished with \d+ cards in hand. They are now on (-?\d+) points", line)
            if scoreMatch:
                player, score = scoreMatch.group(1), scoreMatch.group(2)
                scores[players.index(player)] = int(score)

        return players, wins, scores

def printWinrate(strategy):
    numMatches = defaultdict(int)
    gameWins = defaultdict(int)
    matchWins = defaultdict(int)

    for filename in os.listdir("logs"):
        if strategy == None or getStrat(filename) == strategy:
            players, wins, scores = parseFile(filename)
            for p, win, score in zip(players, wins, scores):
                numMatches[p] += 1
                gameWins[p] += win
                matchWins[p] += score == max(scores)

    def gameWinrate(p):
        return gameWins[p] / (numMatches[p] * 3)
    def matchWinrate(p):
        return matchWins[p] / numMatches[p]
    
    # ranking = sorted(numMatches.keys(), reverse=True, key=gameWinrate)
    ranking = sorted(numMatches.keys(), reverse=True, key=matchWinrate)
    print("NAME            gameW% matchW% #match")
    TABLE_FMT = "{:<15} {:.3f}  {:.3f}   {:<4}"
    for p in ranking:
        print(TABLE_FMT.format(p, gameWinrate(p), matchWinrate(p), numMatches[p]))
    # if ranking:
    #     trueGameWinRate = 1 - statistics.mean(gameWinrate(p) for p in ranking if p != "Sounds Good")
    #     trueMatchWinRate = 1 - statistics.mean(matchWinrate(p) for p in ranking if p != "Sounds Good")
    #     print(TABLE_FMT.format("--TRUE WINS--", trueGameWinRate, trueMatchWinRate, numMatches["Sounds Good"]))

def initSession():
    # change when expires
    REFRESH = {
        "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcyNjMxMzMzNiwiaWF0IjoxNzI2MjI2OTM2LCJqdGkiOiJmMjBlN2QxYjRiOWE0ZGVkYjk2MGQyNGNiZDQ2YzJlMCIsInVzZXJfaWQiOjE0fQ.WeBICEUkgCCoI4pdv0TWwaFRjyKn1q8HumGlKnquqlw",
    }

    HEADERS = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
        "dnt": "1",
        "origin": "https://botb.codersforcauses.org",
        "priority": "u=1, i",
        "referer": "https://botb.codersforcauses.org/",
        "sec-ch-ua-mobile": "?0",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    }

    response = requests.post("https://bigtwo.codersforcauses.org/api/refresh/", headers=HEADERS, json=REFRESH).json()
    if "code" in response and response["code"] == "token_not_valid":
        LOGIN = {
            "team_name": "Sounds Good",
            "password": "REDACTED"
        }
        response = requests.post("https://bigtwo.codersforcauses.org/api/token/", headers=HEADERS, json=LOGIN).json()
        REFRESH = response
        response = requests.post("https://bigtwo.codersforcauses.org/api/refresh/", headers=HEADERS, json=REFRESH).json()
    HEADERS["authorization"] = "Bearer " + response["access"]

    s = requests.Session()
    s.headers.update(**HEADERS)
    return s

def download(s, id, creation_time, place_achieved, status):
    filename = f"logs/logfile{id}.txt"
    if path.exists(filename):
        return

    print("DOWNLOADING", id, creation_time, place_achieved, status)
    response = s.get(f"https://bigtwo.codersforcauses.org/api/download_log/{id}/")
    data = response.text
    if data == '{"id":["Log not found."]}':
        print("\x1b[31m", "Log not found", "\x1b[0m", sep="\n")
        return
    
    # grep "Sounds Good's algorithm produced an invalid move" logs/* --after-context=10
    lines = data.split("\n")
    for i in range(len(lines)):
        if lines[i] == "Engine: Sounds Good's algorithm produced an invalid move":
            print("\x1b[31m", *lines[i-1:i+10], "\x1b[0m", sep="\n")

    open(filename, "w").write(data)

def downloadAll(s):
    response = s.get("https://bigtwo.codersforcauses.org/api/get_logs/").json()
    for log in response:
        id, creation_time, place_achieved, status = (
            log["id"],
            log["creation_time"],
            log["place_achieved"],
            log["status"]
        )
        download(s, id, creation_time, place_achieved, status)
        

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog='stats.py',
        description='looks at logs/logfile*.txt and displays data about win rate',
    )
    parser.add_argument("-s", "--strategy", help="e.g. grok_ryno, grok_haowen")
    parser.add_argument("-d", "--download", action="store_true")

    args = parser.parse_args()
    if args.download:
        s = initSession()
        downloadAll(s)

    printWinrate(args.strategy)
