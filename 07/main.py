#!/usr/bin/env python3
import sys
from dataclasses import dataclass

@dataclass
class File:
    name: str
    size: int

@dataclass
class Dir:
    children: "dict[str, Dir | File]"
    parent: "Dir | None"
    name: str

    _size = None

    def add_child(self, new_child: "Dir | File") -> None:
        self.children[new_child.name] = new_child
        self._size = None

    @property
    def size(self) -> int:
        if self._size is None:
            size = 0
            for child in self.children.values():
                size += child.size
            self._size = size
        return self._size

    def tree(self, indentation: int = 2) -> str:
        lines: list[str] = []
        for name, child in sorted(self.children.items()):
            if isinstance(child, File):
               lines.append(f"- {child.name} (file, size={child.size})")
            if isinstance(child, Dir):
                lines.extend(child.tree(indentation).split("\n"))
        lines = [(indentation * " " + line) for line in lines]
        lines.insert(
            0,
            f"- {self.name} (dir, size={self.size}, children={len(self.children)})",
        )
        return "\n".join(lines)


def solve(input_: str) -> tuple[int | str, int | str]:
    lines: list[str] = list(filter(None, input_.split("\n")))

    dirs = []
    root_dir = Dir({}, None, "/")
    current_dir = None
    last_command_was_ls = False
    for line in lines:
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
                assert "/" not in dir
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
                    current_dir.add_child(dir_)
                continue
            current_dir.add_child(File(file_name, int(size)))

    print(root_dir.tree())

    res1, res2 = 0, 0

    space = 70000000 - 30000000
    rd = root_dir.size

    dirs_to_free = []
    for dir in dirs:
        size = dir.size
        if size <= 100000:
            res1 += size
        if rd - size <= space:
            dirs_to_free.append(size)
    res2 = list(sorted(dirs_to_free))[0]
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
