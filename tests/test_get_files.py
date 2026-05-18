from functions.get_files_info import getFilesInfo

print(getFilesInfo("calculator", "."))
print(getFilesInfo("calculator", "pkg"))
print(getFilesInfo("calculator", "/bin"))
print(getFilesInfo("calculator", "../"))
