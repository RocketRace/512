import sys
import re

def parse(file: str):
	with open(file) as code:
		data = code.read()
	datas = re.findall("(?:^|\\n)[^\\n]+(?:\\n\\t[^\\n]+)*", data)

	match = re.match("\\[start\\]\n\tstate: *([^\\n]+)\n\tsymbol: *(\\w+)\n\tposition: *(\\w+)", datas[0])
	state = match.group(1).strip()
	symbol = match.group(2)
	position = match.group(3)

	matches = re.findall("\n\t(\\w+): *(\\d+)", datas[1])
	symbols = {}
	for match in matches:
		symbols[match[0]] = int(match[1])

	matches = re.findall("\n\t(\\d+): *([^\\n]+)", datas[2])
	actions = {}
	for match in matches:
		action = match[1]
		if action == "nothing":
			actions[match[0]] = ""
		else:
			actions[match[0]] = action + "\n"

	states = {}
	numbers = {}
	for data in datas[3:]:
		lines = data.split("\n")
		name = lines[1]
		match = re.match("(\\d+) *(.*)", name)
		name = match.group(2).strip()
		numbers[name] = int(match.group(1))
		inputs = {}
		possible = []
		chars = []
		to = ""
		do = 0
		for line in lines[2:]:
			if line.startswith("\t@"):
				possible = line[2:].replace(" ", "").split(",").copy()
				chars = []
				to = ""
				do = 0
			elif line.endswith("|"):
				char = line[1:-1].strip()
				if len(char) == 1:
					chars.append(ord(char))
				elif "~" in char:
					ranges = char.split("~")
					start = ranges[0]
					end = ranges[1]
					if start.startswith("\\"):
						start = eval("0x" + start[1:])
					else:
						start = ord(start)
					if end.startswith("\\"):
						end = eval("0x" + end[1:])
					else:
						end = ord(end)
					for c in range(start, end + 1):
						chars.append(c)
				elif char.startswith("\\"):
					chars.append(eval("0x" + char[1:]))
			else:
				row = line.split("=>")
				char = row[0].strip()
				if len(char) == 1:
					chars.append(ord(char))
				elif "~" in char:
					ranges = char.split("~")
					start = ranges[0]
					end = ranges[1]
					if start.startswith("\\"):
						start = eval("0x" + start[1:])
					else:
						start = ord(start)
					if end.startswith("\\"):
						end = eval("0x" + end[1:])
					else:
						end = ord(end)
					for c in range(start, end + 1):
						chars.append(c)
				elif char.startswith("\\"):
					chars.append(eval("0x" + char[1:]))
				string = row[1].strip()
				match = re.match("([^\\n\\[\\+\\~]+)(\\[action \\d+\\])?(\\~\\w+)?(\\+\\w+)?", string)
				to = match.group(1).strip()
				if match.group(2) != None:
					do = int(match.group(2).split()[-1][:-1])
				else:
					do = 0
				for pos in possible:
					outputs = [pos]
					if match.group(3) != None:
						outputs = []
					if match.group(4) != None:
						outputs.append(match.group(4)[1:])
					if inputs.get(pos) == None:
						inputs[pos] = {}
					for c in chars:
						inputs[pos][c] = [to, do, outputs.copy()]
				chars = []
				to = ""
				do = 0
		states[name] = inputs.copy()
	
	out = {}
	for name, data in states.items():
		inputs = {}
		for t, cs in data.items():
			characters = {}
			for c, row in cs.items():
				row[0] = numbers[row[0]]
				written = []
				for x in row[2]:
					written.append(symbols[x])
				row[2] = written.copy()
				characters[c] = row
			inputs[symbols[t]] = characters.copy()
		out[numbers[name]] = inputs.copy()
	
	table = []
	for i in range(len(states) * 4 * 256):
		table.append(0)

	for start, tops in out.items():
		for top, chars in tops.items():
			for char, row in chars.items():
				length = len(row[2])
				write = 0
				if length == 0:
					write = 0
				elif length == 1:
					write = row[2][0] << 2
				elif length == 2:
					write = (row[2][0] << 2) | row[2][1]
				table[(start << 10) | (top << 8) | char] = (row[0] << 10) | (length << 8) | (write << 4) | row[1]

	print("int entry (char *s) ")
	print("{")
	print("\tu_short a = " + str(numbers[state]) + ";")
	print("\tu_short t[4096] = {1, "+str(symbols[symbol.strip()])+"};")
	print("\tfor (int i = 0; i < strlen (s); i++)")
	print("\t\ta = input (a, s[i], t, i);")
	print("\treturn !!a;")
	print("}")
	print("u_short list[] = ")
	print("{")
	for i in range(0, len(table), 256):
		print("\t" + str(table[i:i+256]).replace("[", "").replace("]", "") + ",")
	print("};")
parse(sys.argv[len(sys.argv) - 1])