table = {
    "Pizza": {"Wasabi": 0.5, "Snowball": 1.45},
    "Wasabi": {"Pizza": 1.95, "Snowball": 3.1},
    "Snowball": {"Pizza": 0.67, "Wasabi": 0.31}
}

from_shell = {"Pizza": 1.34, "Wasabi": 0.64, "Snowball": 1.98}
to_shell = {"Pizza": 0.75, "Wasabi": 1.49, "Snowball": 0.48}

trade_log = {}
trades = ""

"""for item, ratio in from_shell.items():  
    for item1, ratio1 in table[item].items():
        for item2, ratio2 in table[item1].items():
            for item3, ratio3 in table[item2].items():
                trades = ""
                trades += item + item1 + item2 + item3
                trade_log[trades] = ratio*ratio1*ratio2*ratio3*to_shell[item3]"""

for item, ratio in from_shell.items():  
    for item1, ratio1 in table[item].items():
            trades = ""
            trades += item + item1 
            trade_log[trades] = ratio*ratio1*to_shell[item1]

print(trade_log)
print(max(trade_log, key=trade_log.get))
