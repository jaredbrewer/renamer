#!/usr/bin/python3

import os, csv, string, random, sys
from os import path

def blindrename(folder):

	# Root = bad
	if os.geteuid() == 0:
		exit("For safety reasons, you must NOT be root when running renamer.py.  Please become a non-root user, make sure that user has permissions to write to all files in " + folder + ", and try again.")

	# Needs a folder, if none is provided, die
	if folder == None:
		exit("You must supply a folder name. I will randomly rename all files in that folder, and create a key file in .CSV format in that folder.")

	# The folder needs to already exist.
	if not path.isdir(folder):
		exit(folder + "is not a valid, existing folder.  Try again - typo maybe?")

	# And it presumably needs to have some number of non-hidden files in it. Seems harmless if it is empty, but not expected behavior.

	contents = os.listdir(folder)
	if ".DS_Store" in contents:
		contents.remove(".DS_Store")
	if len(contents) == 0:
		exit("Looks like that folder is empty?")

	# Avoid double renaming.
	if path.exists(os.path.join(folder, "keyfile.csv")):
		exit("Keyfile already exists. Have you already randomized that folder?")

	csvfile = open(path.join(folder, "keyfile.csv"), "w")
	writer = csv.writer(csvfile)
	writer.writerow(["original", "file.path"])

	chars = str(string.ascii_letters + string.digits)

	print("Renaming: ")

	for file in os.listdir(folder):
		old_name = path.join(folder, file)
		if file == "keyfile.csv":
			pass
		elif file.startswith("."):
			pass
		else:
			base = file.split(os.extsep, 1)
			cloaked_name = "".join(random.choices(chars, k = 5))
			new_name = path.join(folder, cloaked_name + "." + base[1])
			print(old_name, " to ", new_name)
			writer.writerow([old_name, new_name])
			os.rename(old_name, new_name)

	print("Finished!")

def unblind(folder):

	if os.geteuid() == 0:
		exit("For safety reasons, you must NOT be root when running renamer.py.  Please become a non-root user, make sure that user has permissions to write to all files in " + folder + ", and try again.")

	# Needs a folder, if none is provided, die
	if folder == None:
		exit("You must supply a folder name. I will randomly rename all files in that folder, and create a key file in .CSV format in that folder.")

	# The folder needs to already exist.
	if not path.isdir(folder):
		exit(folder + "is not a valid, existing folder.  Try again - typo maybe?")

	# And it presumably needs to have some number of non-hidden files in it. Seems harmless if it is empty, but not expected behavior.

	contents = os.listdir(folder)
	if ".DS_Store" in contents:
		contents.remove(".DS_Store")
	if len(contents) == 0:
		exit("Looks like that folder is empty?")

	# Avoid double renaming.
	if not path.exists(os.path.join(folder, "keyfile.csv")):
		exit("No keyfile?")

	csvfile = open(path.join(folder, "keyfile.csv"), "r")
	reader = csv.reader(csvfile)

	print("Renaming: ")

	for file in reader:
		masked = file[1]
		original = file[0]
		if path.exists(masked):
			print(masked + " to " + original)
			os.rename(masked, original)

	print("Finished!")

if __name__ == '__main__':
	globals()[sys.argv[1]](sys.argv[2])
