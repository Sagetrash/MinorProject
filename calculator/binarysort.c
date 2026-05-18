#include <stdio.h>

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
    int i, loc, j;

    for (i = 1; i < n; ++i) {
        loc = binarySearch(a, a[i], 0, i - 1);

        for (j = i - 1; j >= loc; --j)
            a[j + 1] = a[j];

        a[loc] = a[i];
    }
}

void printArray(int a[], int n) {
    for (int i = 0; i < n; ++i)
        printf("%d ", a[i]);
    printf("\n");
}

int main() {
    int a[] = {37, 23, 0, 17, 12, 72, 31, 46, 100, 88, 54};
    int n = sizeof(a) / sizeof(a[0]);

    printf("Original array: \n");
    printArray(a, n);

    binaryInsertionSort(a, n);

    printf("Sorted array: \n");
    printArray(a, n);

    return 0;
}
