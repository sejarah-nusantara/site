import import_hartakarun_category
import import_hartakarun_item


import import_resolutioninstance


def import_small_dataset():
    limit = 100 #no table has more than 100 records
    import_all_data(limit=100)

def import_all_data(limit=None):
    import_resolutioninstance.ResolutionImporter().load_items(limit=limit)


if __name__ == "__main__":
    import_small_dataset() 