from need.main import Model, infer
from typing import List
import os

def char_list_from_file() -> List[str]:
    with open('./model/charList.txt') as f:
        return list(f.read())

model = Model(char_list_from_file())
ls = []
for i in os.listdir('cropped'):
    ls.append(os.path.join('cropped', i))
print(ls)
a = infer(model, ls)
print(a)
