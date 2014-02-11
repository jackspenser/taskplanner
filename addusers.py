#!/usr/bin/env python
from taskplanner import model
import csv

theRole = model.Role.query.filter_by(name='reader').one()

def add_user(record=[], role=theRole):
    theUser = model.User(record[2], u'password')
    theUser.fname = record[0]
    theUser.lname = record[1]
    theUser.email = record[3]
    theUser.roles.append(role)
    return theUser


with open('users.csv', 'rb') as inFile:
    reader = csv.reader(inFile)
    for row in reader:
        newUser = add_user(row, theRole)
        print newUser
        model.db.session.add(newUser)
    model.db.session.commit()
