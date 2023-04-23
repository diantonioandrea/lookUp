# Inspired from CLIbrary.interface.optionParses
def parser(instructions: list) -> dict: # Parses the options contained in a list of strings.
	# OPTIONS: SINGLE DASH [{(-)key1: value1}, ...] AND DOUBLE DASH [(--)key1, ...]

	sdOpts = dict()
	ddOpts = list()

	for inst in instructions:
		if inst[0] + inst[1] == "--":
			ddOpts.append(inst.replace("--", ""))
		
		elif inst[0] == "-" and instructions.index(inst) < len(instructions) - 1:
			try:
				if type(float(inst)) == float:
					pass

			except(ValueError):
				sdOpts[inst.replace("-", "")] = instructions[instructions.index(inst) + 1]

	return sdOpts, ddOpts