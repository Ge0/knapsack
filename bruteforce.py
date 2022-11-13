import math
import csv
import pprint
import sys #K systemes
from collections import namedtuple
import time
from typing import NamedTuple


class Share(NamedTuple):
    name: str
    price: float
    rate: float
    performance: float

    def __eq__(self, other):
        return self.name == other.name

def read_csv_file(csv_filename): #Recup des valeurs du fichier.csv indiqué en entrée et on calcul directement les performances au chargement(Car on ne peut acheter qu'une seule action de chaque)
    shares = []
    with open(csv_filename) as csvfile:
        reader = csv.reader(csvfile, delimiter=";")
        next(reader) # Skip header du csv
        for row in reader:
            name = row[0]
            price, rate = map(float, row[1:])
            share = Share(name, round(price * 100), rate, round(price * (rate / 100), 2)) # 2chiffres apres la virgule
            shares.append(share)
    return shares


def knapsack01(max_investment, shares):
    if max_investment == 0 or not shares:
        return 0
    if shares[-1].price > max_investment:
        return knapsack01(max_investment, shares[:-1])
    else:
        return max(shares[-1].performance + knapsack01(max_investment - shares[-1].price, shares[:-1]), knapsack01(max_investment, shares[:-1]))
    

def compute_standard_deviation(collection):
    count = len(collection)
    mean = sum(collection) / count
    variance = sum((element - mean)**2 for element in collection) / count
    return math.sqrt(variance)

# https://medium.com/swlh/dynamic-programming-0-1-knapsack-python-code-222e607a2e8
def knapsack02(max_investment, shares):
    max_investment_cts = max_investment * 100
    results = [[0 for _ in range(max_investment_cts + 1)] for _ in range(len(shares) + 1)]
    shares_list = [[list() for _ in  range(max_investment_cts + 1)] for _ in range(len(shares) + 1)]
    for i in range(len(shares) + 1):
        for investment in range(max_investment_cts + 1):
            price_cts = round(shares[i-1].price * 100)
            if price_cts <= 0:
                continue
            if i == 0 or investment == 0:
                results[i][investment] = 0
                shares_list[i][investment] = []
            elif price_cts <= investment:
                if shares[i-1].performance + results[i-1][investment - price_cts] > results[i-1][investment]:
                    results[i][investment] = shares[i-1].performance + results[i-1][investment - price_cts]
                    shares_list[i][investment] = [shares[i-1]] + shares_list[i-1][investment - price_cts]
                else:
                    results[i][investment] = results[i-1][investment]
                    shares_list[i][investment] = list(shares_list[i-1][investment])
            else:
                results[i][investment] = results[i-1][investment]
                shares_list[i][investment] = list(shares_list[i-1][investment])
    return results[len(shares)][max_investment_cts], shares_list[len(shares)][max_investment_cts]


def knapsack03(max_investment, shares):
    shares_count = len(shares)
    results = [[0] * (max_investment + 1)] * (shares_count + 1)
    results = [[0 for w in range(max_investment + 1)]
            for i in range(shares_count + 1)]
    for i in range(shares_count + 1):
        for investment in range(max_investment + 1):
            if i == 0 or investment == 0:
                results[i][investment] = 0
            elif shares[i - 1].price <= investment:
                results[i][investment] = max(
                    shares[i - 1].performance + results[i - 1][investment - shares[i - 1].price],
                    results[i - 1][investment]
                )
            else:
                results[i][investment] = results[i - 1][investment]
    result = results[shares_count][max_investment]
    print(results)
    print(f"Result is {result}")

    investment = max_investment
    for i in range(shares_count, 0, -1):
        if result <= 0:
            break
        if result == results[i - 1][investment]:
            continue
        else:
            print(shares[i - 1])

            result -= shares[i - 1].performance
            investment -= round(shares[i-1].price)


def printknapSack(capacity, weights, values, n):
    results = [[0 for w in range(capacity + 1)]
            for i in range(n + 1)]
    for i in range(n + 1):
        for w in range(capacity + 1):
            if i == 0 or w == 0:
                results[i][w] = 0
            elif weights[i - 1] <= w:
                results[i][w] = max(
                    values[i - 1] + results[i - 1][w - weights[i - 1]],
                    results[i - 1][w]
                )
            else:
                results[i][w] = results[i - 1][w]
 
    # stores the result of Knapsack
    res = results[n][capacity]
    print(results)
    print(f"Second result is {res}")
    
     
    w = capacity
    for i in range(n, 0, -1):
        if res <= 0:
            break
        # either the result comes from the
        # top (K[i-1][w]) or from (val[i-1]
        # + K[i-1] [w-wt[i-1]]) as in Knapsack
        # table. If it comes from the latter
        # one/ it means the item is included.
        if res == results[i - 1][w]:
            continue
        else:
 
            # This item is included.
            print(weights[i - 1])
             
            # Since this weight is included
            # its value is deducted
            res = res - values[i - 1]
            w = w - weights[i - 1]
 

def get_max_performance(shares, max_amount):
    start = time.time()
    # Ici on trie les actions de la plus performante à la moins performante selon leurs rendement

    std = compute_standard_deviation([*map(lambda share: share.performance, shares)])

    shares = list(filter(lambda share: share.performance > std, shares))
    sorted_shares = sorted(shares, key=lambda share: share.price)

    test_shares = [
        Share(name="Share-1", price=10, rate=0, performance=60),
        Share(name="Share-2", price=20, rate=0, performance=100),
        Share(name="Share-3", price=30, rate=0, performance=120),
    ]

    knapsack03(max_amount, test_shares)
    printknapSack(max_amount, [share.price for share in test_shares], [share.performance for share in test_shares], len(test_shares))
    raise SystemExit(1)
    max_performance, best_shares = knapsack02(max_amount, sorted_shares)
    print(f"Performance maximale {max_performance}")
    # on imprime les résultats
    print(f"\nAvec {max_amount} euros d'investissement, vous pouvez maximiser votre randement en achetant : \n" )
    for share in best_shares:
        print(f"> 1 action -{share.name}- à {share.price} euros à {share.rate} % sur 2 ans (Performance = {share.performance} euros)")
    print(f"\n> Performance totale : {round(max_performance, 2)} euros\n")
    # print(f"Total dépensé {max_amount - max_spent_amount} euros \n")
    
    end = time.time()
    print(f"> Temps d'éxecution du programme : {end-start} secondes \n")

# Lancement du programme avec nom du fichier.py choixdudataset.csv et montant choisi
def main(args):
    if len(args) < 3:
        print(f"usage : {args[0]} csv_file max_amount", file=sys.stderr)
        raise SystemExit(-1)   
    csv_filename, max_amount, *_ = args[1:]
    print()
    print(f"Calcul du rendement sur le dataset : {csv_filename} avec un montant investi de : {max_amount} euros")
    shares = read_csv_file(csv_filename)
    get_max_performance(shares, int(max_amount))

if __name__ == "__main__":
    main(sys.argv)
    

    
    