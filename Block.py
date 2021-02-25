class Block:

    def __init__(self, bezeichnung, start, end):
        self.bezeichnung = bezeichnung
        self.start = start
        self.end = end

    def is_utr(self):
        return "UTR" in self.bezeichnung

    def is_cds(self):
        return "CDS" in self.bezeichnung

