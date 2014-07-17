#gender.py

A simple program to make use of genderize.io's gender recognising api.

##Usage

```shell
sands@firefly#gender.py|master⚡ ⇒ cat sample 
Mary
Anna
Emma
Elizabeth
sands@firefly#gender.py|master⚡ ⇒ ./gender.py sample 
Frau Elizabeth, 1.0
Frau Mary, 1.0
Frau Anna, 0.99
Frau Emma, 0.99
sands@firefly#gender.py|master⚡ ⇒ 
```

##Output

The actual output is a python shelf saved in `names_gender.db`, which is used more or less like memoization, so that no name needs to be queried more than once.

Once the program is run for a list of names, the data is available locally, and could be pretty-printed as you will/wish -- from the shelf.

##Requirements

Requires requests to function for HTTP requests.
