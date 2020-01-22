#!/usr/bin/env python3

from tinydb import TinyDB, Query
import os
import time

print("hello user.")
subject = input("which subject?\n => ")
print("You choosed \"" + subject + ".\"")

if not os.path.exists('./data/'):
        os.makedirs('./data/')

db = TinyDB('./data/database.json', indent=4)
table = db.table(subject).all()

print(table)

topic = input("Give me the name of the new topic you want to add to " + subject + "\n => ")
timestamp = int(round(time.time() * 1000))
table = db.table(subject)
table.insert({
        "topic" : topic,
        "timestamp" : timestamp, 
        "progress" : 0,
})

db.close()