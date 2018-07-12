# python3
import fileinput


if __name__ == '__main__':

    total_value = int(fileinput.input()[0])
    coins = [10,5,1]
    change = 0
    result = 0

    for i in range(len(coins)):
        while change + coins[i] <= total_value:
            change = change + coins[i]
            result += 1
        if change == total_value: 
            break

    print(result)    
