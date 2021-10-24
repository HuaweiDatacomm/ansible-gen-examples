import os

a = os.system("ansible-gen -y ../yang -r ../api_desc -o ../apis -l ../logs")
print(a)