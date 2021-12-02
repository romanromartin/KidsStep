from typing import List
import re

n =3



def countPrimes( n: int) -> int:
    if n ==0 or n ==1 or n ==2 :
        return 0
    lst = [2]
    for i in range(3, n, 2):
        if (i > 10) and (i % 10 == 5):
            continue
        for j in lst:
            if j * j - 1 > i:
                lst.append(i)
                break
            if (i % j == 0):
                break
        else:
            lst.append(i)
    return len(lst)



    # res =[]
    #
    # for i in range(2, n ):
    #     if i ==2:
    #         res.append(i)
    #     if i % 2 == 0:
    #         continue
    #     if i ==3:
    #         res.append(i)
    #     if i % 3 == 0:
    #         continue
    #     if i ==5:
    #         res.append(i)
    #     if i % 5 == 0:
    #         continue
    #     if i ==7:
    #         res.append(i)
    #     if i % 7 == 0:
    #         continue
    #     res.append(i)





    # t = res
    # for char in t:
    #     if char * char in t:
    #         print(char, char * char)
    #         res.remove(char * char)
    #
    # print(res)
    # return len(res)


print(countPrimes(n))


#
# n =15
#
# def fizzBuzz( n: int) -> List[str]:
#     i =1
#     res =[]
#     while i <= n:
#         if i % 3 == 0 and i % 5 == 0:
#             res.append("FizzBuzz")
#         elif i % 5 == 0:
#             res.append("Buzz")
#         elif i % 3 == 0:
#             res.append("Fizz")
#         else:
#             res.append(str(i))
#         i +=1
#     return res
#
# print(fizzBuzz(n))
#
#




# head = [-3,5,-99]
# node = -3
# def deleteNode(node):
#     if node in head:
#         head.remove(node)
#
#
#
# deleteNode(node)
#
# print(head)

# n = 40
#
#
# def countAndSay( n: int) -> str:
#     result = '1'
#     i =1
#     while i < n:
#         temp = ''
#         total = ''
#         for char in result :
#             if temp == '':
#                 temp +=char
#             elif char == temp[-1]:
#                 temp +=char
#             else:
#                 total += str(len(temp)) + temp[0]
#                 temp =char
#         result = total + str(len(temp)) + temp[0]
#         i+=1
#     return result
#
#
#
#
# print(countAndSay(n))


#--------------------------------------------------------------------------------------------
# strs = []
#
# def longestCommonPrefix( strs: List[str]) -> str:
#     if not strs:
#         return ''
#     i ='-----------------------------------------------------------------------------------------------------'
#     for n in strs:
#         if len(n) < len(i):
#             i = n
#     t =''
#     l =0
#     while l < len(i):
#         for w in strs:
#             if w[l] != i[l]:
#                 return t
#         t+=i[l]
#         l +=1
#     return t
#
#
#
# print(longestCommonPrefix(strs))






#--------------------------------------------------------------------------------------------------

# haystack = "aaaaa"
# needle = ""
#
# def strStr( haystack: str, needle: str) -> int:
#     if needle == '':
#         return 0
#     i = haystack.find(needle)
#     return i
#
# print(strStr(haystack, needle))




#_------------------------------------------------------------
# s = "+"
#
# def myAtoi( s: str) -> int:
#     # s = s.replace(' ', '')
#     # if len(s) < 1:
#     #     return 0
#     ar = ['a', 'b', 'c', 'd', 'e', 'f',
#               'g', 'h', 'i', 'j', 'k', 'l',
#               'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
#               'w', 'x', 'y', 'z', '.']
#     dig_ar = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9',]
#     op =0
#     negative = False
#     fin = ''
#     a = False
#     for char in s:
#         if op > 0:
#             if not char in dig_ar and a ==False:
#                 return 0
#         if a:
#             if not char in dig_ar:
#                 break
#         if char.lower() in ar:
#             return 0
#         if char =='-':
#             op +=1
#             negative = True
#         if char == '+':
#             op += 1
#             negative = False
#         if op > 1:
#             return 0
#         if char in dig_ar:
#             a =True
#             fin += char
#     try:
#         if negative:
#             fin = int(fin) * -1
#         else:
#             fin = int(fin)
#         if fin < -2**31:
#             return -2**31
#         if fin > 2**31 - 1:
#             return 2**31 - 1
#     except:
#         return 0
#     return fin
#
#
#
#




    # match = re.search(r'[a-zA-Z.]', s)
    # ind =100
    # if match:
    #     ind = s.find(str(match[0]))
    #     # print(ind)
    #     # print('match', match[0])
    # t = re.findall(r'[-+]?\d+', s)
    # # print(ind, s.find(t[0][0]))
    # if ind < s.find(t[0][0]):
    #     return 0
    # if int(t[0]) < -2**31:
    #     return -2**31
    # if int(t[0]) > 2**31 - 1:
    #     return 2**31 - 1
    # return int(t[0])







# print(myAtoi(s))



#--------------------------------------------------------------------------------------
# s = " "
#
# def isPalindrome( s: str) -> bool:
#
#     reg = re.compile('[^a-zA-Z0-9 ]')
#     t = reg.sub('', s).replace(' ', '').lower()
#     print(len(t))
#     for i in range(len(t)):
#
#         if t[i] != t[-(i+1)]:
#             return False
#     return True
#
#
# print(isPalindrome(s))
#
#



# import collections
# c = collections.Counter("anagram")
# p = collections.Counter("nagaram")
# print(c)
# print(p)
#


# s = "rat"
# t = "tarr"
#
#
# def isAnagram(s: str, t: str) -> bool:
#     if len(s) != len(t):
#         return False
#     m = list(s)
#     for i in list(t):
#         if i in m:
#             m.remove(i)
#         else:
#             return False
#     return True
#
# print(isAnagram(s, t))








#-----------------------------------------------------------------------------------------------------

s = "leetcode"


# def firstUniqChar(s: str) -> int:
#     ar = ['a', 'b', 'c', 'd', 'e', 'f',
#           'g', 'h', 'i', 'j', 'k', 'l',
#           'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
#           'w', 'x', 'y', 'z']
#     i = ''
#     t = 1000000000
#     for ch in ar:
#         if len(s) == len(s.replace(ch, '')) + 1:
#             if t > s.find(ch):
#                 t = s.find(ch)
#             i += ch
#     if i == '':
#         return -1
#     return t
#
#
# print(firstUniqChar(s))

# ------------------------------------------------------------
# x = 123
#
# def reverse( x: int) -> int:
#     res = ''
#     minus = False
#     for item in str(x):
#         if item == '-':
#             minus = True
#             continue
#         res = item + res
#     if minus:
#         res = '-' + res
#     if not -2**31 <= int(res) <= 2**31 - 1:
#         return 0
#     return int(res)
#
# print(reverse(x))
#
#
#


# -----------------------------------Rotate Image----------------------------
# matrix = [[1,2,3]
#          ,[4,5,6],
#           [7,8,9]]
#
# def rotate( matrix: List[List[int]]) -> None:
#     f =0
#     new_arr = []
#     while f < len(matrix):
#         new_arr.append([])
#         f += 1
#     n = 0
#     while n < len(matrix):
#         i = 0
#         while i < len(matrix):
#             res = matrix[n][i]
#             new_arr[i].append(res)
#             i += 1
#         n += 1
#     r =0
#     while r < len(matrix):
#         new_arr[r].reverse()
#         r +=1
#     n = 0
#     while n < len(matrix):
#         i = 0
#         while i < len(matrix):
#             matrix[n][i] =new_arr[n][i]
#             i += 1
#         n += 1
#
#
#
# rotate(matrix)
# print(matrix)
#
#
#
#


# -------------------------------------------------------------Valid Sudoku-------------------------------------------
# board = [["5","3",".",".","7",".",".",".","."]
#         ,["6",".",".","1","9","5",".",".","."]
#         ,[".","9","8",".",".",".",".","6","."]
#         ,["8",".",".",".","6",".",".",".","3"]
#         ,["4",".",".","8",".","3",".",".","1"]
#         ,["7",".",".",".","2",".",".",".","6"]
#         ,[".","6",".",".",".",".","2","8","."]
#         ,[".",".",".","4","1","9",".",".","5"]
#         ,[".",".",".",".","8",".",".","7","9"]]
#
# def isValidSudoku( board: List[List[str]]) -> bool:
#
#     n = 0
#     col_arr = [[],[],[],[],[],[],[],[],[]]
#     square_arr = [[],[],[],[],[],[],[],[],[]]
#     while n < 9:
#         new_arr = []
#         i =0
#         while i < 9:
#             res = board[n][i]
#             if res == '.':
#                 i += 1
#                 continue
#             if res in new_arr:
#                 return False
#             else:
#                 new_arr.append(res)
#
#             if res in col_arr[i]:
#                 return False
#             else:
#                 col_arr[i].append(res)
#             if i < 3 and n < 3 :
#                 if res in square_arr[0]:
#                     return False
#                 else:
#                     square_arr[0].append(res)
#             elif i >= 3 and i < 6 and n < 3 :
#                 if res in square_arr[1]:
#                     return False
#                 else:
#                     square_arr[1].append(res)
#             elif i >= 6  and n < 3 :
#                 if res in square_arr[2]:
#                     return False
#                 else:
#                     square_arr[2].append(res)
#             elif i < 3 and n >= 3 and n < 6 :
#                 if res in square_arr[3]:
#                     return False
#                 else:
#                     square_arr[3].append(res)
#             elif i >= 3 and i < 6 and n >= 3 and n < 6 :
#                 if res in square_arr[4]:
#                     return False
#                 else:
#                     square_arr[4].append(res)
#             elif i >= 6 and n >= 3 and n < 6 :
#                 if res in square_arr[5]:
#                     return False
#                 else:
#                     square_arr[5].append(res)
#
#             elif i < 3 and n >= 6:
#                 if res in square_arr[6]:
#                     return False
#                 else:
#                     square_arr[6].append(res)
#             elif i >= 3 and i < 6 and n >= 6:
#                 if res in square_arr[7]:
#                     return False
#                 else:
#                     square_arr[7].append(res)
#             elif i >= 6 and n >= 6:
#                 if res in square_arr[8]:
#                     return False
#                 else:
#                     square_arr[8].append(res)
#
#
#
#
#             i += 1
#
#         n +=1
#     print(col_arr)
#     return True
#
#
#
#
#
# print(isValidSudoku(board))
#


# ----------------------------------Two Sum----------------------------


# i = 0
# new_arr = []
# while i < len(nums):
#     n = i+1
#     while n < len(nums):
#         if nums[i] + nums[n] == target:
#             new_arr.append(i)
#             new_arr.append(n)
#         n += 1
#     i += 1
# return new_arr

#
#
# print(twoSum(nums, target))
#
#
#


# -------------------------------------------Move Zeroes------------------------------------

# nums = [0,1,0,3,12]
#
# def moveZeroes( nums: List[int]) -> None:
#     n = 0
#     i =0
#     while i < len(nums):
#         if nums[i] == 0:
#             nums.pop(i)
#             i -= 1
#             n += 1
#         i += 1
#     while n > 0:
#         nums.append(0)
#         n -=1
#
#
# moveZeroes(nums)
#
# print(nums)


# --------------------------------------------Plus One--------------------------------------
#
# digits = [4,3,2,1]
#
# def plusOne( digits: List[int]) -> List[int]:
#     m = ''
#     new_arr =[]
#     for i in digits:
#         m += str(i)
#     m = str(int(m)+1)
#     for t in m:
#         new_arr.append(int(t))
#     return new_arr
#
#
#
#
#
# print(plusOne(digits))


# -----------------------------Intersection of Two Arrays II---------------------------------------------------------

# nums1 = [4,7,9,7,6,7]
#
# nums2 = [5,0,0,6,1,6,2,2,4]
#
# def intersect( nums1: List[int], nums2: List[int]) -> List[int]:
#
#     i = 0
#     new =[]
#     while i < len(nums1):
#         print(nums1, nums2)
#         if nums1[i] in nums2:
#             nums2.remove(nums1[i])
#             new.append(nums1[i])
#         i += 1
#     return new
#
#
# print(intersect(nums1, nums2))


# ---------------------------------- Single Number--------------------------------

# nums = [2,2,1]
#
#
# def singleNumber( nums: List[int]) -> int:
#     nums.sort()
#     i = 0
#     while i < len(nums) - 1:
#         if nums[i] != nums[i + 1]:
#             return nums[i]
#         i += 2
#     return nums[-1]
#
#
# print(singleNumber(nums))


# ------------------------Contains Duplicate----------------------------


# nums = [1,1,1,3,3,4,3,2,4,2]
# def containsDuplicate( nums: List[int]) -> bool:

# nums.sort()
# i = 0
# while i < len(nums)-1:
#     if nums[i] == nums[i+1]:
#         return True
#     i += 1
# return False

# for i in nums:
#     m = nums.count(i)
#     print(m)
#     if m > 1:
#         return True
# return False


# new =[]
# for i in nums:
#     if i in new:
#         return True
#     else:
#         new.append(i)


# print(containsDuplicate(nums))


# -----------------------------Rotate Array----------------
# nums = [1,2,3,4,5,6,7]
# k = 3
#
# def rotate( arr, k):
#     k = k % len(nums)
#
#     m = arr[-k:] + arr[:-k]
#     arr.clear()
#     arr += m
#
#
#
# rotate(nums, k)
# print(nums)


# ----------------------------------------------------------------------------------------------------------

# class Solution(object):
#
#     def maxProfit(self, prices):
#         if len(prices) == 0:
#            return 0
#         save = 0
#         pres = False
#         add = 0
#         i =0
#         while i < len(prices) - 1:
#             prof = prices[i + 1] - prices[i]
#
#             if prof > 0:
#                 if not pres:
#                     save = prices[i]
#                     print('save', save, pres)
#                     pres = True
#             else:
#                 if pres:
#                     add += prices[i] - save
#                     print('add', add, '=', prices[i], '-', save, pres)
#                     pres = False
#             i += 1
#         if pres:
#             add += prices[len(prices) - 1] - save
#         return add
#
#
#
#
#
#
# egg = Solution()
#
#
# print('total', egg.maxProfit([7,1,5, 12,3,6,4]))
#
#
#
