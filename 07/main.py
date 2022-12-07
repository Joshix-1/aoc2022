#!/usr/bin/env python3
import sys
from dataclasses import dataclass

@dataclass
class Dir:
    children: "dict[str, Dir | int]"
    parent: "Dir | None"
    name: str

    _size = None

    def get_size(self):
        if self._size is not None:
            return self._size
        size = 0
        for child in self.children.values():
            if isinstance(child, int):
                size += child
            else:
                size += child.get_size()
        self._size = size
        return size

    def __str__(self):
        return self.name

def solve(input_: str) -> tuple[int | str, int | str]:
    lines: list[str] = list(filter(None, input_.split("\n")))

    res1, res2 = 0, 0

    dirs = []
    root_dir = Dir({}, None, "/")
    current_dir = None
    last_command_was_ls = False
    for line in lines:
        print(f"{res1=}, {res2=}, {line=}")
        if line.startswith("$ cd"):
            dir = line.removeprefix("$ cd ")
            if ".." in dir:
                assert dir == ".."
                assert current_dir
                current_dir = current_dir.parent
            elif not current_dir or dir == "/":
                assert dir == "/"
                current_dir = root_dir
            else:
                current_dir = current_dir.children[dir]
            last_command_was_ls = False
        elif line == "$ ls":
            last_command_was_ls = True
        else:
            assert last_command_was_ls
            size, file_name = line.split(" ")
            if size == "dir":
                if file_name not in current_dir.children:
                    dir_ = Dir({}, current_dir, file_name)
                    dirs.append(dir_)
                    current_dir.children[file_name] = dir_
                continue
            size = int(size)
            current_dir.children[file_name] = size

    root_dir.get_size()
    for dir in dirs:
        size = dir.get_size()
        print(f"{dir=}, {size=}")
        if size <= 100000:
            res1 += size

    return res1, res2

def main() -> None:
    stdout, sys.stdout = sys.stdout, sys.stderr
    try:
        res1, res2 = solve(sys.stdin.read())
    finally:
        sys.stdout = stdout
    print(f"1: {res1}\n2: {res2}")

if __name__ == "__main__":
    sys.exit(main())
