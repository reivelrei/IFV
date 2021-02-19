class Position:
    def __init__(self, chromosome, start, end, mapped_reads):
        self.chromosome = chromosome
        self.start = start
        self.end = end
        self.mapped_reads = mapped_reads

    def __eq__(self, other):
        return self.chromosome == other.chromosome and self.start == other.start
