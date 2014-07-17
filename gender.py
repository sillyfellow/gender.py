#!/usr/bin/python

import requests
import json
import sys
import shelve

def fill_gender_db(names, db):
    """ call the genderize.io api and then fill in the details
        to a local db, a shelf """
    url = ""
    cnt = 0
    for name in names:
        print name
        if url == "":
            url = "name[0]=" + name
        else:
            url = url + "&name[" + str(cnt) + "]=" + name
        cnt += 1
    req = requests.get("http://api.genderize.io?" + url)
    parse_json_to_db(json.loads(req.text), db)


def parse_json_to_db(data, db):
    for item in data:
        parse_json_item_to_db(item, db)


def parse_json_item_to_db(item, db):
    """ shelves cannot have unicode keys, so keep the latinized version """
    name = item["name"]
    values = []
    if item["gender"] is not None:
        values = [name, item["gender"],
                  float(item["probability"]), int(item["count"])]
    else:
        values = [name, u'None', u'0.0', 0.0]
        db[name.encode('latin_1')] = values


def chunks(l, n):
    for i in xrange(0, len(l), n):
        yield l[i:i + n]


def create_gender_db(names_file, database="names_gender.db", chunk_size=20):
    """
    read names from the file, call the api, fill the db (shelf)
    """
    fd = open(names_file, "r")
    db = shelve.open(database)

    # If the name is already in the db, then don't check for it
    names = [name.strip() for name in fd.readlines()
             if name.strip().encode('latin_1') not in db]

    for name_chunk in chunks(names, chunk_size):
        fill_gender_db(name_chunk, db)

    fd.close()
    db.close()


def salute(gender):
    if gender == u'female':
        return u'Frau '
    return u'Herr '


def read_gender_db(database="names_gender.db"):
    """
    read the database (only the values)
    sort them based on the probability of being correct
    and print them out with the salutation
    """
    db = shelve.open(database)
    result = []
    for value in db.itervalues():
        result.append(value)

    result = sorted(result, key=lambda x: x[2], reverse=True)
    output = [salute(x[1]) + x[0] + ', ' + unicode(x[2])
              for x in result]
    for person in output:
        print person
    db.close()


if __name__ == '__main__':
    args = sys.argv

    if len(args) == 2:
        create_gender_db(args[1])
        read_gender_db()
    else:
        print "Usage: ", args[0], " <file-with-names>"
