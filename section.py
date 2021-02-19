class Section:
    def __init__(self, transcript, chrom, start, end, sign):
        self.transcript = transcript
        self.chrom = chrom
        self.start = int(start)
        self.end = int(end)
        self.sign = sign
