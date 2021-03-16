from copy import deepcopy
from os import walk

from folding import parse, Folding
from position import Position
from section import Section


# This class handles the reading and file operations for getting the necessary data from .bed, .bedgraph or .dbr files.


class DataManager:
    # input_path - base path in which all the files are present
    # position_file - name of the position file (.bedgraph)
    # section_file -  name of the section file (.bed)
    # folding_version - 1 or 2 - defines the version of the folding_files
    def __init__(self, input_path, position_file, section_file,  folding_version):
        self.input_path = input_path
        self.position_file = position_file
        self.section_file = section_file
        self.folding_version = folding_version

    # updates config properties for reading future data
    # input_path - base path in which all the files are present
    # position_file - name of the position file (.bedgraph)
    # section_file -  name of the section file (.bed)
    # folding_version - 1 or 2 - defines the version of the folding_files
    def update(self, input_path, position_file, section_file,  folding_version):
        self.input_path = input_path
        self.position_file = position_file
        self.section_file = section_file
        self.folding_version = folding_version

    # reads a folding file with the given name
    # name -  name of the folding file
    # section - read annotation for this folding file
    # positions -  read data for this folding file
    def read_file(self, name, section, positions):
        data = []
        input_file = self.input_path + Folding.get_display_name() + "/" + name

        with open(input_file, 'r') as input:
            lines = input.readlines()

        if self.folding_version == 1:
            data = self.read_folding(lines=lines, section=section, positions=positions, section_file=self.section_file,
                                     position_file=self.position_file)
        else:
            if self.folding_version == 2:
                data = self.read_folding_two(lines=lines, section=section, positions=positions,
                                             section_file=self.section_file,
                                             position_file=self.position_file)

        return data

    # reads the section for the given transcript
    # transcript - transcript/folding file name
    def read_section(self, transcript):
        input_file = self.input_path + Section.get_display_name() + "/" + self.section_file

        with open(input_file, 'r') as input:
            for line in input:
                if transcript in line:
                    values = line.split("\t")
                    return Section(transcript=values[3], chrom=values[0], start=values[1], end=values[2], sign=values[5],
                                   thickstart=values[6], thickend=values[7], block_size=values[10],
                                   block_start=values[11].strip())

    # reads the positions for the given section
    # section - section for which positions should be read
    def read_positions(self, section):
        input_file = self.input_path + Position.get_display_name() + "/" + self.position_file
        positions = []
        start = int(section.start)
        end = int(section.end)
        chromosome = section.chrom
        sign = section.sign
        with open(input_file, 'r') as input:
            targets = [line.strip() for line in input if section.chrom in line]
            short_version = True
            value = targets[0].strip().split("\t")
            if len(value) == 1:
                # the format is not split by \t.
                # trying " "
                value = targets[0].strip().split(" ")

            if len(value) == 4:
                short_version = True
            else:
                if len(value) == 6:
                    short_version = False
                else:
                    raise ValueError('Unknown format for position file')

            if short_version:
                self.read_positions_short_format(chromosome, start, end,sign, targets, positions)
            else:
                self.read_positions_long_format(chromosome, start, end,sign, targets, positions)

        return positions

    # reads the position for the short format (.bedgraph)
    def read_positions_short_format(self, chromosome, start, end, sign, targets, positions):
        for line in targets:
            value = line.strip().split("\t")
            if value[0] == chromosome and int(value[1]) >= start and int(value[2]) <= end:
                positions.append(Position(value[0], int(value[1]), int(value[2]), sign, int(value[3])))
            else:
                if value[0] == chromosome and int(value[1]) > end:
                    break

    # reads the position for the long format (.bed 6 column)
    def read_positions_long_format(self, chromosome, start, end, sign,  targets, positions):
        new_pos = None
        old_pos = None
        relevant = False

        for line in targets:
            relevant = False
            value = line.strip().split(" ")

            new_pos = Position(str(value[0]), int(value[1]), int(value[2]), value[5], 1)

            if value[0] == chromosome and int(value[1]) >= start and int(value[2]) <= end and value[5] == sign:
                relevant = True
                if old_pos is not None:
                    if old_pos.chromosome == new_pos.chromosome and old_pos.start == new_pos.start and old_pos.sign == new_pos.sign:
                        new_pos.mapped_reads = old_pos.mapped_reads + 1
                    else:
                        positions.append(old_pos)
            else:
                if old_pos is not None:
                    positions.append(old_pos)
                if new_pos.chromosome == chromosome and new_pos.start > end:
                    break

            if relevant:
                old_pos = deepcopy(new_pos)

    # reads all foldings for given parameters for version 1
    def read_folding(self, lines, section, positions, section_file, position_file):
        foldings = []
        sequence = ''
        heading = ''
        folding = ''

        for line in lines:
            if line.startswith('>'):
                heading = line.strip()
            if not line.startswith('>') and sequence != '':
                folding = line.strip()
            if not line.startswith('>') and sequence == '':
                sequence = line.strip()
            if sequence != '' and heading != '' and folding != '':
                foldings.append(parse(heading, sequence, folding, section, positions, section_file, position_file))
                heading = ''
                folding = ''

        if sequence != '' and heading != '' and folding != '':
            foldings.append(parse(heading, sequence, folding, section, positions, section_file, position_file))

        return foldings

    # reads all foldings for given parameters for version 2
    def read_folding_two(self, lines, section, positions, section_file, position_file):
        foldings = []
        sequence = ''
        heading = ''
        folding = ''
        count = 0
        for line in lines:

            if line.startswith('>'):
                if sequence != '' and heading != '' and folding != '':
                    heading = heading.replace('ENERGY:', 'ENERGY = ') + 'AT5G02120.1::Chr5:419090-419773(+)'
                    foldings.append(parse(heading, sequence, folding, section, positions, section_file, position_file))
                    heading = ''
                    folding = ''
                count += 1
                heading = line.strip()

            if not line.startswith('>') and count > 1:
                folding += line.strip()

            if not line.startswith('>') and count == 1:
                sequence += line.strip()

        if sequence != '' and heading != '' and folding != '':
            heading = heading.replace('ENERGY:', 'ENERGY = ') + 'AT5G02120.1::Chr5:419090-419773(+)'
            foldings.append(parse(heading, sequence, folding, section, positions, section_file, position_file))

        return foldings

    # generates a dict of all files sorted by their type (.bedgraph, .bed, .fa.dbr, unknown)
    def list_files(self):
        files = {'position_files': [], 'section_files': [], 'folding_files': [], 'unknown': []}

        f = []
        for (base_dirpath, base_dirnames, base_filenames) in walk(self.input_path):
            for directory in base_dirnames:
                for (dirpath, dirnames, filenames) in walk(self.input_path+directory):
                    for file in filenames:
                        if directory.upper() == Position.get_display_name().upper():
                            files['position_files'].append(file)
                        else:
                            if directory.upper() == Section.get_display_name().upper():
                                files['section_files'].append(file)
                            else:
                                if directory.upper() == Folding.get_display_name().upper():
                                    files['folding_files'].append(file)
                                else:
                                    files['unknown'].append(file)

        return files
