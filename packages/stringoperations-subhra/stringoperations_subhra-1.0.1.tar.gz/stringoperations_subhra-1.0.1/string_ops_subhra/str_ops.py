def  length_str():
    '''

    It is used  to find the length of a string.

    '''
    str = input("\n Enter a string to find the length: ")
    length = len(str)
    print(f"\nLength of the string '{str}' is {length}" )

def reverse_str() :
    '''

    It is used  to reverse a string.

    '''

    str = input("\n Enter a string to reverse: ")
    n=len(str)
    print(f"\nReverse of the string '{str}' is ",end ="")
    while((n-1)>=0):
        print(str[n-1],end="")
        n=n-1
    print()

def find_str():
    '''

    It is used to find the first occurrence of a substring in a string.

    '''

    str1 = input("\n Enter a string : ")
    str2= input("\n Enter a substring to find in the main string: ")
    s=str1.find(str2) 
    if(s!=-1):
        print(f"\nThe substring '{str2}' is first occurring at {s} postion in '{str1}'")
    else :
        print(f"\nThe substring '{str2}' could not be found in '{str1}'")

def num_of_words():
    '''

    It is used to find the number of words in a string.

    '''

    str = input("\n Enter a string to find the number of words in it: ")
    words=str.split()
    num_words= len(words)
    print(f"\nThere are {num_words} words in the string '{str}' " )
        
def num_of_vowels():
    '''

    It is used to find the number of vowels in a string

    '''
    vowels = 'aeiou'
    str=input("\nEnter a string to find the number of vowels in it: ")
    str = str.casefold()
    count_vowels = {}.fromkeys(vowels,0)
    for i in str:
          if i in count_vowels:
                  count_vowels[i] += 1
    print(f"\nThe vowels in the string '{str}' are ")
    print(count_vowels)

