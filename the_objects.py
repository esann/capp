from the_object import  create_empty_object

def get_the_objects():
    db_objects = [create_empty_object("a"), create_empty_object("b"), create_empty_object("c"), create_empty_object("d")]
    for o in db_objects:
        yield o

    return