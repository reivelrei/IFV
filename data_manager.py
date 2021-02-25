from folding import parse
from position import Position
from section import Section

from os import listdir, walk


class data_manager:
    def __init__(self, input_path, position_file, section_file,  folding_version):
        self.input_path = input_path
        self.position_file = position_file
        self.section_file = section_file
        self.folding_version = folding_version

    def update(self, input_path, position_file, section_file,  folding_version):
        self.input_path = input_path
        self.position_file = position_file
        self.section_file = section_file
        self.folding_version = folding_version

    def read_file(self, name, section, positions):
        data = []
        input_file = self.input_path + name

        with open(input_file, 'r') as input:
            lines = input.readlines()

        if self.folding_version == 1:
            data = self.read_folding(lines=lines, section=section, positions=positions)
        else:
            if self.folding_version == 2:
                data = self.read_folding_two(lines=lines, section=section, positions=positions)

        return data

    def read_section(self, transcript):
        input_file = self.input_path + self.section_file

        with open(input_file, 'r') as input:
            for line in input:
                if transcript in line:
                    values = line.split("\t")
                    return Section(transcript=values[3], chrom=values[0], start=values[1], end=values[2], sign=values[5], thickstart=values[6], thickend=values[7], block_size=values[10], block_start=values[11].strip())

    def read_positions(self, section):
        input_file = self.input_path + self.position_file
        positions = []
        start = int(section.start)
        end = int(section.end)
        with open(input_file, 'r') as input:
            targes = [line.strip() for line in input if section.chrom in line]
            for line in targes:
                value = line.strip().split("\t")
                if value[0] == section.chrom and int(value[1]) >= start and int(value[2]) <= end:
                    positions.append(Position(value[0], int(value[1]), int(value[2]), int(value[3])))
                else:
                    if value[0] == section.chrom and int(value[1]) > end:
                        break
        return positions

    def read_folding(self, lines, section, positions):
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
                foldings.append(parse(heading, sequence, folding, section, positions))
                heading = ''
                folding = ''

        if sequence != '' and heading != '' and folding != '':
            foldings.append(parse(heading, sequence, folding, section, positions))

        return foldings

    def read_folding_two(self, lines, section, positions):
        foldings = []
        sequence = ''
        heading = ''
        folding = ''
        count = 0
        for line in lines:

            if line.startswith('>'):
                if sequence != '' and heading != '' and folding != '':
                    heading = heading.replace('ENERGY:', 'ENERGY = ') + 'AT5G02120.1::Chr5:419090-419773(+)'
                    foldings.append(parse(heading, sequence, folding, section, positions))
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
            foldings.append(parse(heading, sequence, folding, section, positions))

        return foldings

    def list_files(self):
        files = {}

        files['position_files'] = []
        files['section_files'] = []
        files['folding_files'] = []
        files['unknown'] = []

        f = []
        for (dirpath, dirnames, filenames) in walk(self.input_path):
            for file in filenames:
                if '.BEDGRAPH' in file.upper():
                    files['position_files'].append(file)
                else:
                    if '.BED' in file.upper():
                        files['section_files'].append(file)
                    else:
                        if '.FA.DBR' in file.upper():
                            files['folding_files'].append(file)
                        else:
                            files['unknown'].append(file)

        return files
