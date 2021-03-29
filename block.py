# This class represents a single block for the folding structure
# A block is either UTR or CDS, Introns are not saved as blocks


class Block:

    def __init__(self, bezeichnung, start, end, direction):
        self.bezeichnung = bezeichnung
        self.start = start
        self.end = end
        self.direction = direction

    # checks if this block is a UTR block
    def is_utr(self):
        return "UTR" in self.bezeichnung

    # checks if this block is a CDS block
    def is_cds(self):
        return "CDS" in self.bezeichnung

    def is3(self):
        return self.is_utr() and self.direction == '3\''

    def is5(self):
        return not self.is3()


