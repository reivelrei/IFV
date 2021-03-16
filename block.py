# This class represents a single block for the folding structure
# A block is either UTR or CDS, Introns are not saved as blocks


class Block:

    def __init__(self, bezeichnung, start, end):
        self.bezeichnung = bezeichnung
        self.start = start
        self.end = end

    # checks if this block is a UTR block
    def is_utr(self):
        return "UTR" in self.bezeichnung

    # checks if this block is a CDS block
    def is_cds(self):
        return "CDS" in self.bezeichnung

    @staticmethod
    def color_utr():
        return '#5FADFC'

    @staticmethod
    def color_cds():
        return '#023E7D'

    @staticmethod
    def color_intron():
        return 'white'
