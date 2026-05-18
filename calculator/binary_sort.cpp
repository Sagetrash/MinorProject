#include <iostream>
#include <vector>

// Function to find the position where the element should be inserted
int binarySearch(const std::vector<int>& arr, int item, int low, int high) {
    while (low <= high) {
        int mid = low + (high - low) / 2;
        if (item == arr[mid])
            return mid + 1;
        if (item > arr[mid])
            low = mid + 1;
        else
            high = mid - 1;
    }
    return low;
}

// Function to sort the array using Binary Insertion Sort
void binaryInsertionSort(std::vector<int>& arr) {
    int n = arr.size();
    for (int i = 1; i < n; ++i) {
        int key = arr[i];
        int j = i - 1;

        // Find the location of the element to be inserted
        int pos = binarySearch(arr, key, 0, j);

        // Move all elements after the position to the right
        while (j >= pos) {
            arr[j + 1] = arr[j];
            j--;
        }
        arr[pos] = key;
    }
}

void printArray(const std::vector<int>& arr) {
    for (int i : arr) {
        std::cout << i << " ";
    }
    std::cout << std::endl;
}

int main() {
    std::vector<int> arr = {37, 23, 0, 17, 12, 72, 31, 46, 100, 88, 54};
    
    std::cout << "Original array: ";
    printArray(arr);

    binaryInsertionSort(arr);

    std::cout << "Sorted array: ";
    printArray(arr);

    return 0;
}
