import math
import csv
import pprint
import sys #K systemes
from collections import namedtuple
import time

Share = namedtuple("Share", ["name", "price", "rate", "performance"]) # Creation d'un namedtuple(Attributs)

def read_csv_file(csv_filename): #Recup des valeurs du fichier.csv indiqué en entrée et on calcul directement les performances au chargement(Car on ne peut acheter qu'une seule action de chaque)
    shares = []
    with open(csv_filename) as csvfile:
        reader = csv.reader(csvfile, delimiter=";")
        next(reader) # Skip header du csv
        for row in reader:
            name = row[0]
            price, rate = map(float, row[1:])
            share = Share(name, price, rate, round(price * (rate / 100), 2)) # 2chiffres apres la virgule
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


def greedy_algorithm(investment, shares):
    value = 0
    buylist = list()
    for share in shares:
        if share.price <= investment:
            investment -= share.price
            value += share.performance
            buylist.append(share)
    return value, buylist
        


def get_max_performance(shares, max_amount):
    start = time.time()

    # Écarte les mauvaises lignes
    shares = list(filter(lambda share: share.price > 0, shares))

    # Ici on trie les actions de la moins performante à la moins performante.
    sorted_shares = sorted(shares, key=lambda share: share.performance/share.price, reverse=True)
    max_performance, best_shares = greedy_algorithm(max_amount, sorted_shares)
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
    

    
    