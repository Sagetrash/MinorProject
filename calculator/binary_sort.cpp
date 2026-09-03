#include <iostream>
#include <vector>

// Function to find the position where it should be inserted in sorted array
int binarySearch(int a[], int item, int low, int high) {
    while (low <= high) {
        int mid = low + (high - low) / 2;
        if (item == a[mid])
            return mid + 1;
        if (item > a[mid])
            low = mid + 1;
        else
            high = mid - 1;
    }
    return low;
}

// Function to sort array using Binary Insertion Sort
void binaryInsertionSort(int a[], int n) {
    for (int i = 1; i < n; i++) {
        int selected = a[i];
        int j = i - 1;

        // Find location to insert using binary search
        int loc = binarySearch(a, selected, 0, j);

        // Move all elements after location to create space
        while (j >= loc) {
            a[j + 1] = a[j];
            j--;
        }
        a[loc] = selected;
    }
}

void printArray(int a[], int n) {
    for (int i = 0; i < n; i++)
        std::cout << a[i] << " ";
    std::cout << std::endl;
}

int main() {
    int arr[] = {37, 23, 0, 17, 12, 72, 31, 46, 100, 88, 54};
    int n = sizeof(arr) / sizeof(arr[0]);

    std::cout << "Original array: ";
    printArray(arr, n);

    binaryInsertionSort(arr, n);

    std::cout << "Sorted array: ";
    printArray(arr, n);

    return 0;
}
