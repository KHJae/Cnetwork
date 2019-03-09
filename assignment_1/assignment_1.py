# -*- coding:utf-8 -*-

def sortAD(item, left, right, reverse):
    low = left
    high = right + 1
    pivot = item[left]

    while low < high:
        low += 1
        high -=1
        if reverse == False: #오름차순 정렬
            while(low <= right and item[low] < pivot):
                low += 1
            while(high >= left and item[high] > pivot):
                high -= 1
        else: # 내림차순 정렬
            while(low <= right and item[low] > pivot):
                low += 1
            while(high >= left and item[high] < pivot):
                high -= 1
        if(low < high):
            swap(item, low, high)
    
    swap(item, left, high)
    return high

def swap(item, x, y):
    t = item[x]
    item[x] = item[y]
    item[y] = t

def quicksort(item, left, right, reverse):
    if left < right :
        index = sortAD(item, left, right, reverse)
        quicksort(item, left, index-1, reverse)
        quicksort(item, index + 1, right, reverse)

def sorting(item, reverse):
    quicksort(item, 0, len(item) -1, reverse) 
 

spliteditem = input().split()
sub = 0
if spliteditem[1] == 'A':
    reverse = False
elif spliteditem[1] == 'D':
    reverse = True

while sub < 3:
    del(spliteditem[0])
    sub += 1
for i in range(0, len(spliteditem)):
    spliteditem[i] = int(spliteditem[i])#문자열을 숫자로 변경후 재저장

sorting(spliteditem, reverse)
print(spliteditem)