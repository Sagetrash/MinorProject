from functions.write_file import writeToFile

print(writeToFile("calculator", "lorem.txt", "wait, this isn't lorem ipsum"))
print(writeToFile("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"))
print(writeToFile("calculator", "/tmp/temp.txt", "this should not be allowed"))
