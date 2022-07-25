import sys, os
from re import finditer

proj = None
if len(sys.argv) > 1:
	proj = sys.argv[1]
else:
	proj = "test"

files = {}

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


def loadData(fn: str = "init.lua"):
	if not remExt(fn) in files:
		with open(os.path.join(proj, fn), "r") as file:
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
				loadData(addExt(i))

def genFile():
	with open("out.luau", "w") as file:
		file.write("local RPack = {\n")

		for name, data in files.items():
			fileData = data.replace("\n", "\n\t\t")
			file.write(f"\t{name} = function(Import, Export)\n\t\t{fileData}\n\tend,\n")

		file.write("}\n\nrequire(game:GetService(\"ReplicatedStorage\"):WaitForChild(\"RPack\"))(RPack)")

loadData()
genFile()