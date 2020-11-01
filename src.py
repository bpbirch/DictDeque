#%%
# creating a dict-based deque structure that allows for O(1) addition and removal 
# from either end of the deque
#%%
import numpy as np
import time
import matplotlib.pyplot as plt 
from string import whitespace, punctuation
import urllib.request 
#%%
# Deque
# writing vanilla list-based deque
class Deque:
    def __init__(self):
        self.items = []
    def addFront(self, item):
        self.items.append(item)
    def addRear(self, item):
        self.items.insert(0, item)
    def removeFront(self):
        return self.items.pop()
    def removeRear(self):
        return self.items.pop(0)
    def isEmpty(self):
        return self.items == []
    def size(self):
        return len(self.items)
    def __repr__(self):
        return f'{self.items}'

if __name__ == '__main__':
    d = Deque()
    d.addFront(10)
    d.addRear(20)
    d.addRear(30)
    print(d)
    d.removeFront()
    print(d)
    d.removeRear()
    print(d)
    print(d.size())
#%%

class DictDeque:
    """
    The goal of creating this dict-based deque structure was to achieve
    O(1) performance on adding and removing from the front and back of a deque
    A normal list-based deque has to sacrifice performance on one end or the other of a deque,
    while a dict-based deque does not

    This structure begins by indexing the front of the queue to 0, and the rear to 1
    The value of self.items[0] is set to None so that we don't raise Key Errors down the road
    If an item is added to the front, the front is indexed to -1
    If an item is added to the back, then the rear is indexed to 2
    When an item is removed from the front, we increment the front's index by +1
    When an item is removed from the rear, we decrement the rear's index by -1
    Ultimately, this means that low numbers are at our 'front', and high numbers at our 'rear'
    """
    def __init__(self):
        self.items = {}
        self.high = 1
        self.low = 0 
    def addFront(self, item):
        self.items[self.low] = item
        self.low -= 1
    def addRear(self, item):
        self.items[self.high] = item
        self.high += 1
    def peekFront(self):
        return self.items[self.low+1]
        # since we increment after we assign keys, we have to use -1, +1 to access / manipulate keys
    def peekRear(self):
        return self.items[self.high-1]
    def removeFront(self):
        if not self.isEmpty():
            placeHolder = self.items[self.low+1] 
            del self.items[self.low+1] 
            # since we increment AFTER we assign a key:value pair in addFront/Rear, 
            # we have to delete based on previous index
            self.low += 1
            return placeHolder
    def removeRear(self):
        if not self.isEmpty():
            placeHolder = self.items[self.high-1]
            del self.items[self.high-1]
            self.high -= 1
            return placeHolder
    def isEmpty(self):
        return self.items == {}
    def size(self):
        return len(self.items)
    def __repr__(self):
        return f'{self.items}'

if __name__ == '__main__':
    dd = DictDeque()
    dd.addFront(11)
    print(dd.low)
    dd.addFront(22)
    print(dd.low)
    dd.addFront(33)
    print(dd.low)
    dd.addRear(44)
    print(dd.high)
    dd.addRear(55)
    print(dd.high)
    print(dd)
    dd.removeRear()
    dd.removeRear()
    print('dd.high:', dd.high)
    print(dd)
    print('dd.removeRear():', dd.removeRear())
    print(dd)
    print('dd.removeRear():', dd.removeRear())

# %%
def dequeTimer(d, n, addRemove, frontRear):
    """
    This function will return the time, in seconds, required to 
    remove or add items to the front or rear of a deque structure

    Args:
        d (deque-like structure): deque-like structure, whethere a DictDeque or Deque
        n (int): i through n will be removed or added
        addRemove (str): 
            if addRemove == 'remove', items i through n will first be added to 
            d, and then timing will be applied to the removal of those items from d
            if addRemove = 'add', timing will be applied as i through n are added to d
        frontRear (str):
            if frontRear == 'front', addRemove operation will be applied to front of d
            if frontRear == 'rear', addRemove operation will be applied to rear of d
    Returns:
        float: time in seconds to enqueue all of i through n to queue structure
    """
    if addRemove == 'add' and frontRear == 'front':
        start = time.time()
        for i in range(n):
            d.addFront(i)
        end = time.time()
        return end-start 
    if addRemove == 'add' and frontRear == 'rear':
        start = time.time()
        for i in range(n):
            d.addRear(i)
        end = time.time()
        return end-start 
    if addRemove == 'remove' and frontRear == 'front':
        for i in range(n):
            d.addRear(i)
        start = time.time()
        for i in range(n):
            d.removeFront()
        end = time.time()
        return end-start
    if addRemove == 'remove' and frontRear == 'rear':
        for i in range(n):
            d.addFront(i)
        start = time.time()
        for i in range(n):
            d.removeRear()
        end = time.time()
        return end-start
    
#%%
# testing performance of DictDeque
if __name__ == '__main__':
    # here we're goint to use matplotlib to pot differences in performance
    # interestingly, list-based queue actually seems to be O(n^2) performance,
    # while DictQueue is O(1)
    nums = list(range(1000, 100000, 10000))
    # add, front
    dTimes = []
    ddTimes = []
    d = Deque()
    dd = DictDeque()    
    for n in nums:
        dTimes.append(dequeTimer(d, n, 'add', 'front'))
        ddTimes.append(dequeTimer(dd, n, 'add', 'front'))
    fig = plt.figure()
    ax = plt.subplot(111, xlabel='n', ylabel='time to addFront')
    ax.plot(nums, dTimes, label='Deque')
    ax.plot(nums, ddTimes, label='DictDeque')
    plt.legend()
    plt.show() # as we would expect, there is no performance benefit for addFront, 
    # since the list-based deque uses .append(), which is O(1)

#%%
if __name__ == '__main__':
    # remove, front
    nums = list(range(1000, 100000, 10000))
    dTimes = []
    ddTimes = []
    d = Deque()
    dd = DictDeque()    
    for n in nums:
        dTimes.append(dequeTimer(d, n, 'remove', 'front'))
        ddTimes.append(dequeTimer(dd, n, 'remove', 'front'))
    fig = plt.figure()
    ax = plt.subplot(111, xlabel='n', ylabel='time to removeFront')
    ax.plot(nums, dTimes, label='Deque')
    ax.plot(nums, ddTimes, label='DictDeque')
    plt.legend()
    plt.show() # once again, no real performance benefit removing from front, since .pop() is O(1)
#%%
#%%
if __name__ == '__main__':
    # remove, front
    nums = list(range(1000, 100000, 10000))
    dTimes = []
    ddTimes = []
    d = Deque()
    dd = DictDeque()    
    for n in nums:
        dTimes.append(dequeTimer(d, n, 'add', 'rear'))
        ddTimes.append(dequeTimer(dd, n, 'add', 'rear'))
    fig = plt.figure()
    ax = plt.subplot(111, xlabel='n', ylabel='time to addRear')
    ax.plot(nums, dTimes, label='Deque')
    ax.plot(nums, ddTimes, label='DictDeque')
    plt.legend()
    plt.show() # the actual performance of our DictDeque comes when removing or adding to rear
#%%
if __name__ == '__main__':
    # remove, front
    nums = list(range(1000, 100000, 10000))
    dTimes = []
    ddTimes = []
    d = Deque()
    dd = DictDeque()    
    for n in nums:
        dTimes.append(dequeTimer(d, n, 'remove', 'rear'))
        ddTimes.append(dequeTimer(dd, n, 'remove', 'rear'))
    fig = plt.figure()
    ax = plt.subplot(111, xlabel='n', ylabel='time to removeRear')
    ax.plot(nums, dTimes, label='Deque')
    ax.plot(nums, ddTimes, label='DictDeque')
    plt.legend()
    plt.show() # the actual performance of our DictDeque comes when removing or adding to rear

#%%
# using a deque for palindrome checking
def palindromeDequeCheck(string):
    """
    Checks a string to determine whether it's a palindrome

    Args:
        string (str): string to be checked as palindrome

    Returns:
        stillOK (bool): bool specifying True for palindrome, False for not palindrome
    """
    dd = DictDeque()
    stillOK = True
    for c in string:
        dd.addRear(c)
    while dd.size() > 1 and stillOK:
        if dd.peekFront() == dd.peekRear():
            dd.removeFront()
            dd.removeRear()
        else:
            stillOK = False
    return stillOK

print(palindromeDequeCheck('racecar'))

#%%
# will use cleanse for palindrome checking
def cleanse(word):
    '''
    This function removes punctuation and whitespace from word,
    the string that we pass as an argument

    Args:
    word (str): string we want to strip whitespace and punctuation from

    Returns:
    cleaned (str): word with whitespace and punctuation stripped
    '''
    cleaned = '' # we will only include non whitespace, non punctuation characters
    for char in word:
        if ((char in whitespace) or (char in punctuation)):
            pass
        else:
            cleaned += char.lower()
    return cleaned

if __name__ == '__main__':
    word = 'hey  th!ere?'
    print(cleanse(word))

#%%
def gatherBook(url):
    with urllib.request.urlopen(url) as file_object:
        # *** demarcates actual text of book in gutenberg files
        words = file_object.read().decode('utf-8-sig').split('***')[2]
        words = words.split()
    return words

if __name__ =='__main__':
    url = 'http://www.gutenberg.org/cache/epub/63393/pg63393.txt'
    words = gatherBook(url)
    print(words[:20])
#%%
# Writing a program that takes in a file, analyzes each word, and keeps a list of all palindromes
def findPalindromes(url):
    """
    Analyzes a text book from project gutenberg, then returns a dictionary
    of key:value pairs of palindrome:count form

    Args:
        url (str): url of project gutenberg book

    Returns:
        palindromes (dict): dictionary of key:value pairs of palindrome:count form
    """
    words = gatherBook(url)
    words = [cleanse(word) for word in words]
    words = [word for word in words if len(word) > 1] # don't want single letter words
    palindromes = {}
    
    for word in words:
        if palindromeDequeCheck(word):
            if word not in palindromes:
                palindromes[word] = 1
            else:
                palindromes[word] += 1
    return palindromes

if __name__ == '__main__':
    pals = findPalindromes('http://www.gutenberg.org/cache/epub/63393/pg63393.txt')
    print(pals)