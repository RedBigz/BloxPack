#!/usr/bin/python3

from os.path import join
from re import finditer
from argparse import ArgumentParser
from sys import argv

remExt = lambda x: x.replace(".lua", "")
addExt = lambda x: x + ".lua"

def rfind_all(x, p):
	a = finditer(p, x)
	return [x.end() for x in a]

def findImports(data: str = ""):
	search = "Import\(\""
	imports = rfind_all(data, search)
	foundImports = []

	for i in imports:
		_import = ""
		x = 0
		while data[i + x] != "\"":
			_import += data[i + x]
			x += 1
		
		foundImports.append(_import)

	return foundImports

def loadData(directory: str = "") -> dict:
	files = {}
	def wrap(fn: str = "init.lua") -> None:
		if not remExt(fn) in files:
			with open(join(directory, fn), "r") as file:
				data = file.read().replace("require(\"", "Import(\"")

				newData = []
				for l in data.split("\n"):
					if l.startswith("--@Export"):
						default = l.startswith("--@ExportDefault")
						startAt = 17 if default else 10
						name = "default" if default else l[startAt:]
						newData.append(f"Export({l[startAt:]}, \"{name}\")")
						continue
					newData.append(l)

				files[remExt(fn)] = "\n".join(newData)

				for i in findImports(data):
					wrap(addExt(i))
	
	wrap()

	return files

def genFile(files: dict) -> None:
	with open("out.lua", "w") as file:
		file.write("-- Generated by BloxPack\nlocal BloxPack = {\n")

		for name, data in files.items():
			fileData = data.replace("\n", "\n\t\t")
			file.write(f"\t{name} = function(Import, Export)\n\t\t{fileData}\n\tend,\n")

		file.write("}\n\nrequire(game:GetService(\"ReplicatedStorage\"):WaitForChild(\"BloxPack\"))(BloxPack)")

def parse_args():
	parser = ArgumentParser(description="Pack multiple lua files into a single script.")

	parser.add_argument("dir", metavar="DIRECTORY", help="Directory to pack. Must contain an 'init.lua' file.")
	parser.add_argument("--output", "--out", "-o", default="out.lua", dest="out")

	if len(argv) == 1:
		return parser.parse_args(["-h"])
	
	return parser.parse_args()

def main(args):
	data = loadData(directory = args.dir)
	genFile(files = data)

if __name__ == "__main__":
	args = parse_args()
	main(args)