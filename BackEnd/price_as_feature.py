import sys

def apart_price(feature_string):
    prices = []
    splitted = feature_string.split(" ")
    i = 0
    while i < len(splitted):
        prices.append({
            splitted[i] : splitted[i+1]
        })
        i+=2
    return prices

if __name__ == "__main__":
    if sys.argv[1] == "-test":
        print("showing result for string '1 $2,100 2 $2,750+'")
        test_result = apart_price("1 $2,100 2 $2,750+")
        print("converting result is: ")
        for r in test_result:
            print(r)
    else:
        print("this is for converting the wired feature column to regular apartment prices, for testing, use -test")
