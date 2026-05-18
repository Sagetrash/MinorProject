public class BinarySort {

    /**
     * Sorts an array using Binary Insertion Sort.
     * Binary Insertion Sort improves upon Insertion Sort by using binary search 
     * to find the correct position to insert the current element.
     * 
     * @param array The array to be sorted.
     */
    public static void binaryInsertionSort(int[] array) {
        for (int i = 1; i < array.length; i++) {
            int key = array[i];
            int low = 0;
            int high = i - 1;

            // Binary search to find the position where key should be inserted
            while (low <= high) {
                int mid = low + (high - low) / 2;
                if (key < array[mid]) {
                    high = mid - 1;
                } else {
                    low = mid + 1;
                }
            }

            // Move all elements after the found position one position to the right
            for (int j = i - 1; j >= low; j--) {
                array[j + 1] = array[j];
            }
            array[low] = key;
        }
    }

    public static void main(String[] args) {
        int[] data = {37, 23, 0, 17, 12, 72, 31, 46, 100, 88, 54};
        System.out.println("Original array:");
        printArray(data);

        binaryInsertionSort(data);

        System.out.println("Sorted array:");
        printArray(data);
    }

    private static void printArray(int[] array) {
        for (int i : array) {
            System.out.print(i + " ");
        }
        System.out.println();
    }
}
