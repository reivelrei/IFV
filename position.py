# This class represents a single position (= a row in the .bedgraph file)
# chromosome - the chromosome
# start -  the start value
# end - the end value
# mapped_reads - the mapped_reads of the file


class Position:
    def __init__(self, chromosome, start, end, mapped_reads):
        self.chromosome = chromosome
        self.start = start
        self.end = end
        self.mapped_reads = mapped_reads

    # compare two positions by their chromosome and start value
    def __eq__(self, other):
        return self.chromosome == other.chromosome and self.start == other.start
