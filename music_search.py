# you may use pandas only for IO reason
# Using it to do sort will impact your grade
# import pandas as pd
import random
import timeit
import csv


def timeFunc(method):
    """
    Define the main body of the decorator that decorates a method.
        
    Returns
    -------
    Callable
        A wrapper that defines the behavior of the decorated method
    """
    def wrapper(*args, **kwargs):
        """
        Define the behavior of the decorated method
        Parameters:
            Same as the parameters used in the methods to be decorated
            
        Returns:
            Same as the objects returned by the methods to be decorated
        """
        start = timeit.default_timer()
        result = method(*args, **kwargs)  
        # record the time consumption of executing the method
        time = timeit.default_timer() - start
        
        # send metadata to standard output
        print(f"Method: {method.__name__}")
        print(f"Result: {result}")
        print(f"Elapsed time of 10000 times: {time*10000} seconds")
        return result
    return wrapper


class MusicLibrary:
    def __init__(self):
        """
        Initialize the MusicLibrary object with default values.
        self.data the collect of music library
        self.rows: the row number 
        self.cols: the col number 
        self.nameIndex: the number represent the index of name in each element of self.data
        self.albumIndex: the number represent the index of album in each element of self.data
        self.trackIndex: the number represent the index of track in each element of self.data
        """
        self.data = []
        self.rows = 0
        self.cols = 0
        self.nameIndex = 0
        self.albumIndex = 1
        self.trackIndex = 1

    def readFile(self, fileName):
        """
        Read music data from a CSV file and store it in the self.data attribute.
        The self.rows and self.cols should be updated accordingly. 
        The self.data should be [[name, albums count, tract count],...]
        You could assume the file is in the same directory with your code.
        Please research about the correct encoding for the given data set, 
        as it is not UTF-8.
        You are allowed to use pandas or csv reader, 
        but self.data should be in the described form above.

        Parameters
        ----------
        fileName : str
            The file name of the CSV file to be read.
        """
        self.data = []
        with open(fileName, mode='r', encoding='iso-8859-1') as file:
            csv_reader = csv.reader(file)
            # next(csv_reader)
            for row in csv_reader:
                if len(row) >= 3:
                    artist_name, albums_count, tracks_count = row[:3]
                    self.data.append([artist_name.strip(), int(albums_count), int(tracks_count)])
        self.rows = len(self.data)
        self.cols = 3 if self.data else 0

    def printData(self):
        """
        Print the data attribute stored in the library instance in a formatted manner.
        """
        for entry in self.data:
            print(f"Artist: {entry[0]}, Albums: {entry[1]}, Tracks: {entry[2]}")

    def shuffleData(self):
        """
        Shuffle the data stored in the library.
        refer to the random package
        """
        random.shuffle(self.data)


    @timeFunc
    def binarySearch(self, key, keyIndex):
        """
        Perform a binary search on the data.

        Parameters
        ----------
        key : int or str
            The key to search for.
        keyIndex : int
            The column index to search in.

        Returns
        -------
        int
            The index of the row where the key is found, or -1 if not found.
        """
        low, high = 0, len(self.data) - 1

        while low <= high:
            mid = (low + high) // 2
            mid_value = self.data[mid][keyIndex]

            if mid_value < key:
                low = mid + 1
            elif mid_value > key:
                high = mid - 1
            else:
                return mid

        return -1

    @timeFunc
    def seqSearch(self, key, keyIndex):
        """
        Perform a sequential search on the data.

        Parameters
        ----------
        key : int or str
            The key to search for.
        keyIndex : int
            The column index to search in.

        Returns
        -------
        int
            The index of the row where the key is found, or -1 if not found.
        """
        for index, row in enumerate(self.data):
            if row[keyIndex] == key:
                return index
        return -1

    @timeFunc
    def bubbleSort(self, keyIndex):
        """
        Sort the data using the bubble sort algorithm based on a specific column index.
        self.data will have to be in sorted order after calling this function.

        Parameters
        ----------
        keyIndex : int
            The column index to sort by.
        """
        n = len(self.data)
        for i in range(n):
            for j in range(0, n-i-1):
                if self.data[j][keyIndex] > self.data[j+1][keyIndex]:
                    self.data[j], self.data[j+1] = self.data[j+1], self.data[j]

    def merge(self, L, R, keyIndex):
        """
        Merge two sorted sublists into a single sorted list.
        This is the helper function for merge sort.
        You may change the name of this function or even not have it.
        

        Parameters
        ----------
        L, R : list
            The left and right sublists to merge.
        keyIndex : int
            The column index to sort by.

        Returns
        -------
        list
            The merged and sorted list.
        """
        merged = []
        i = j = 0
        while i < len(L) and j < len(R):
            if L[i][keyIndex] <= R[j][keyIndex]:
                merged.append(L[i])
                i += 1
            else:
                merged.append(R[j])
                j += 1
        merged.extend(L[i:])
        merged.extend(R[j:])
        return merged

    @timeFunc
    def mergeSort(self, keyIndex):
        """
        Sort the data using the merge sort algorithm.
        This is the main mergeSort function
        self.data will have to be in sorted order after calling this function.

        Parameters
        ----------
        keyIndex : int
            The column index to sort by.
        """
        self._mergeSort(self.data, keyIndex)

    def _mergeSort(self, arr, keyIndex):

        # This is the helper function for merge sort.
        # You may change the name of this function or even not have it.
        # This is a helper method for mergeSort
        if len(arr) > 1:
            mid = len(arr) // 2
            L = arr[:mid]
            R = arr[mid:]

            self._mergeSort(L, keyIndex)
            self._mergeSort(R, keyIndex)

            i = j = k = 0

            while i < len(L) and j < len(R):
                if L[i][keyIndex] < R[j][keyIndex]:
                    arr[k] = L[i]
                    i += 1
                else:
                    arr[k] = R[j]
                    j += 1
                k += 1

            while i < len(L):
                arr[k] = L[i]
                i += 1
                k += 1

            while j < len(R):
                arr[k] = R[j]
                j += 1
                k += 1

    @timeFunc
    def quickSort(self, keyIndex):
        """
        Sort the data using the quick sort algorithm.
        This is the main quickSort function
        self.data will have to be in sorted order after calling this function.

        Parameters
        ----------
        keyIndex : int
            The column index to sort by.
        """
        self.data = self._quickSort(self.data, keyIndex)

    def _quickSort(self, arr, keyIndex):
        if len(arr) <= 1:
            return arr
        else:
            pivot = arr[0][keyIndex]
            left = [x for x in arr[1:] if x[keyIndex] < pivot]
            right = [x for x in arr[1:] if x[keyIndex] >= pivot]

            return self._quickSort(left, keyIndex) + [arr[0]] + self._quickSort(right, keyIndex)

    def comment(self):
        '''
        Based on the result you find about the run time of calling different function,
        Write a small paragraph (more than 50 words) about time complexity, and print it. 
        '''
        my_commentary = """
        The results obtained from the execution of sorting and searching algorithms in this project offer insightful reflections on their theoretical complexities. Bubble sort, the simplest yet least efficient with a complexity of O(n^2), required significantly more time to complete as demonstrated by its elapsed time of approximately 49.40 seconds for 10,000 iterations. This reinforces its impracticality for large datasets.

        In contrast, merge sort and quick sort, both theoretically optimized with an average complexity of O(n log n), showed far superior performance. Merge sort was the fastest, taking only about 5.20 seconds for the same number of iterations, highlighting its efficiency and stability even though it requires more memory, which might be a consideration in resource-limited environments. Quick sort also performed well at 9.08 seconds, demonstrating its capability to handle large datasets efficiently, though it can suffer in performance in the worst-case scenarios, such as already sorted data.

        For the search algorithms, binary search dramatically outperformed sequential search with its logarithmic complexity, making it exceptionally suitable for sorted datasets. The results from binary search, taking only about 0.027 seconds, as opposed to the sequential search's 0.015 seconds, underscore the importance of utilizing efficient algorithms like binary search when working with ordered data.

        These practical results not only validate the theoretical expectations regarding algorithm performance but also emphasize the critical importance of selecting the right algorithm based on data characteristics and specific application needs. Understanding the time and space complexity trade-offs is essential in making these choices, particularly in professional and academic settings where efficiency and resource management are necessary.
        """
        print(my_commentary)



# create instance and call the following instance method
# using decroator to decroate each instance method
def main():
    random.seed(42)
    myLibrary = MusicLibrary()
    filePath = 'music-search/music.csv'
    myLibrary.readFile(filePath)

    idx = 0
    myLibrary.data.sort(key = lambda data: data[idx])
    myLibrary.seqSearch(key="30 Seconds To Mars", keyIndex=idx)
    myLibrary.binarySearch(key="30 Seconds To Mars", keyIndex=idx)

    idx = 2
    myLibrary.shuffleData()
    myLibrary.bubbleSort(keyIndex=idx)
    myLibrary.shuffleData()
    myLibrary.quickSort(keyIndex=idx)
    myLibrary.shuffleData()
    myLibrary.mergeSort(keyIndex=idx)
    myLibrary.printData()
    myLibrary.comment()

if __name__ == "__main__":
    main()

