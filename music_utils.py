#!/usr/bin/env python3
from pathlib import Path

def get_musics(directory):
    path = Path(directory).glob("**/*")
    files = [x for x in path if x.is_file()]
    
    return files

if __name__ == "__main__":
    musics = get_musics("./musics")
    for i in musics:
        print(i)