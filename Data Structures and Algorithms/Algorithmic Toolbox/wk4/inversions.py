# Uses python3
import sys

def MergeAndCount(lst):
    
    lstlen=len(lst)

    if lstlen > 1:
         lst1,cnt1 = MergeAndCount(lst[:lstlen//2])
         lst2,cnt2 = MergeAndCount(lst[lstlen//2:])
         cnt = cnt1+cnt2
    else:
        return lst,0

    i, j = 0, 0
    lst1len, lst2len = len(lst1), len(lst2)
    lst=[]
    while i<lst1len and j<lst2len:
        if lst1[i] <= lst2[j]:
            lst.append(lst1[i])
            i+=1
        else:
            lst.append(lst2[j])
            j+=1
            cnt += lst1len - i
    if i < lst1len:
        lst += lst1[i:]
    elif j < lst2len:
        lst += lst2[j:]

    return lst,cnt

def get_number_of_inversions(a, b, left, right):
    number_of_inversions = 0
    if right - left <= 1:
        return number_of_inversions
    ave = (left + right) // 2
    number_of_inversions += get_number_of_inversions(a, b, left, ave)
    number_of_inversions += get_number_of_inversions(a, b, ave, right)
    #write your code here
    return number_of_inversions

def get_number_of_inversions(a):
    return(MergeAndCount(a)[1])

if __name__ == '__main__':
    input = sys.stdin.read()
    n, *a = list(map(int, input.split()))
    #b = n * [0]
    #print(get_number_of_inversions(a, b, 0, len(a)))
    print(get_number_of_inversions(a))
