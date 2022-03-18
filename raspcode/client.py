from need.main import Model, infer
from typing import List

def char_list_from_file() -> List[str]:
    with open('model/charList.txt') as f:
        return list(f.read())

model = Model(char_list_from_file())
ls = ['data/word.png', 'data/word1.png', 'data/word2.png']
infer(model, ls)