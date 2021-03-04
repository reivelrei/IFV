# This class caches folding data for reuse if the user
# selects a previously rendered folding to speed up calculations


class Cache:

    def __init__(self):
        self.map = {}

    # invalidates the cache
    def invalidate(self):
        self.map = {}

    # adds the folding to the cache
    # folding - the folding which should be cached
    def add_to_cache(self, folding):
        key = self.generate_id_for_cache(folding)
        self.map[key] = folding
        print("Add_To_Cache: " + str(key) + str(folding))

    # removes the folding from the cache
    # folding - the folding which should be removed from cache
    def get_from_cache(self, folding):
        obj = None
        key = self.generate_id_for_cache(folding)
        try:
            obj = self.map[key]
        except KeyError:
            obj = None
        print("Get_From_Cache: " + str(key) + str(folding) + "-> " + str(obj))
        return obj

    # generates an id for caching by using input files and transcript name
    # folding - a folding for which the id should be generated
    def generate_id_for_cache(self, folding):
        return hash((str(folding.position_file)
                     + str(folding.section_file)
                     + str(folding.section.transcript) + str(folding.foldings)))
