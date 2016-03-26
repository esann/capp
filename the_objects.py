from the_object import  create_empty_object, links_exists

# def get_the_objects():
#     db_objects = [create_empty_object("a"), create_empty_object("b"), create_empty_object("c"), create_empty_object("d")]
#     for o in db_objects:
#         yield o
#
#     return


def get_the_objects(objects_list, include_links, exclude_links) -> {}:
    with_link = [o for o in objects_list if links_exists(o, include_links)]
    if not exclude_links == []:
        without_links = [o for o in with_link if not links_exists(o, exclude_links)]
    else:
        without_links = with_link

    return without_links




