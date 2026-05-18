from functions.get_file_content import getFileContent

# print((getFileContent("calculator", "lorem.txt")))
print(getFileContent("calculator", "main.py"))
print(getFileContent("calculator", "pkg/calculator.py"))
print(getFileContent("calculator", "/bin/cat"))
print(getFileContent("calculator", "pkg/does_not_exist.py"))
