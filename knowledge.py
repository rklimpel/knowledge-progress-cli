#!/usr/bin/env python3

from tinydb import TinyDB, Query
import os
import time
import json

def main():
	subject = open_subject()
	while(True):
		print("="*60)
		print("you are in subject \"" + subject + "\". what do you want to do?")
		print("  (show)  show current progress for the subject")
		print(" (track)  track progress of a topic")
		print("(switch)  change the subject")
		print("  (exit)  close the application")
		arg = input(" => ")
		if arg == "show":
			print("="*60)
			show_progress(subject)
		elif arg == "track":
			print("="*60)
			track_progress(subject)
		elif arg == "switch":
			print("="*60)
			subject = change_subject()
		elif arg == "exit":
			print("="*60)
			exit()
		else:
			print("error: please use one of the specified commands")

def open_subject():
	print("="*60)
	print("hello user.")
	if not os.path.exists('./data/'):
		os.makedirs('./data/')
	db = TinyDB("./data/database.json", indent=4)
	available_tables = db.tables()
	i = 0
	subject_order = {}
	print("choose one of your subjects:")
	for subject in available_tables:
		if subject != "_default" and subject != "":
			print("("+str(i)+") " + subject)
			subject_order[subject] = i
			i += 1
	subject_number = input(" => ")
	for sub in subject_order:
		if subject_order[sub] == int(subject_number):
			subject = sub
	table = db.table(subject.lower()).all()
	db.close()
	return subject

def add_topic(subject):
	topic = input("Give me the name of the new topic you want to add to " + subject + "\n => ")
	db = TinyDB('./data/database.json', indent=4)
	timestamp = int(round(time.time() * 1000))
	table = db.table(subject.lower())
	table.insert({
			"topic" : topic,
			"timestamp" : timestamp, 
			"progress" : 0,
	})
	db.close()

def show_progress(subject):
	db = TinyDB('./data/database.json', indent=4)
	table = db.table(subject).all()
	print("your knowledge progress for all topics in " + subject + ":")
	for entry in table:
		name_filler = " "*(30-len(entry["topic"]))
		progress_pipes = u"\u2586"*(entry["progress"]-2)
		progress_spaces = " "*(100-2-entry["progress"])
		print(entry["topic"] + ": " + name_filler + "|" + progress_pipes + progress_spaces + "|")

def track_progress(subject):
	db = TinyDB('./data/database.json', indent=4)
	table = db.table(subject)
	topic = input("Which topic do you want to update?\n => ")

	if not table.search(Query().topic==topic):
		create_answer = input("This topic does not exists, do you want to create it?\n => ")
		if create_answer=="y" or create_answer=="yes":
			progress = input("Whats your progress?\n => ")
			timestamp = int(round(time.time() * 1000))
			table.insert({"progress": int(progress),"topic": topic,"timestamp": timestamp})
			print("topic created and progress tracked.")
	else:
		progress = input("Whats your progress?\n => ")
		timestamp = int(round(time.time() * 1000))
		table.update({"progress": int(progress),"topic": topic,"timestamp": timestamp},Query().topic==topic)
		print("progress updated.")

if __name__== "__main__":
	main()