import re, os
def create_path(path):
    if not os.path.exists(path):
        os.mkdir(path)
create_path("Data")
create_path("Output")
create_path("src")

NB_file = 'Data\\NetBackup81_RefGuide_StatusCodes'
os.system("pip install pdf2txt")
os.system(f"pdf2txt.py {NB_file}.pdf -o {NB_file}.txt")
counter=-1
codes = {}
error = 0
cond = False
with open(f'{NB_file}.txt', 'r', encoding='utf-8') as f:
    for line in f:
        if re.search("This chapter includes the following topics:", line) is not None:
            cond = True
        if cond == False:
            continue
        if counter == 1:
            if re.search("Message: ", line):
                codes[error] = "".join(line.split(': ')[1:])[0:-1]
                counter=2
                continue
            else:
                continue
        if counter == 2:
            if re.search("Explanation: ", line) or re.search("^\n", line):
                counter=-1
            else:
                codes[error] += " " + line[:-1]
        if re.search('NetBackup status code: ', line):
            counter=1
            error = line.split(': ')[1]
            error = error[0:-1]
            continue

with open("Output/Error_codes.py", "w", encoding='utf-8') as f:
    f.write("codes = {")
    for code,meaning in codes.items():
        f.write(code + ': "' + meaning + '",\n')
    f.seek(f.tell() - 3, os.SEEK_SET)
    f.write("}")
