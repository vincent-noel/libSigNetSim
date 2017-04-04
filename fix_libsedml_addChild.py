import libsedml, shutil, os


# Getting the filenames
original_file = libsedml.__file__
original_filepath = os.path.dirname(original_file)


original_file = os.path.join(original_filepath, "__init__.py")
backup_file = os.path.join(original_filepath, "__init__.backup")

# Making a backup
shutil.copy(original_file, backup_file)

# Deleting the original
os.remove(original_file)

original = open(os.path.join(original_filepath, "__init__.backup"), "r")
# Reading the backup
lines = []
for line in original:
	lines.append(line)

original.close()

# Writing the new file
print "> Modifying %s" % original_file
new = open(os.path.join(original_filepath, "__init__.py"), "w")
for i, line in enumerate(lines):
	
	if (		i < len(lines)-4
		and
			line.startswith("        if args[0] is not None: args[0].thisown = 0")
		and
			lines[i+3].startswith("        return _libsedml.ASTNode_addChild(self, disownedChild, inRead)")
	):
		print "> Found line to modify"
		new.write("        if disownedChild is not None: disownedChild.thisown = 0\n")
	else:
		new.write(line)

new.close()
print "> Done"
