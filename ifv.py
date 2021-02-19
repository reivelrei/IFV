# -*- coding: utf-8 -*-
import argparse
import dash
import dash_html_components as html
import dash_core_components as dcc

from FORNAPlotter import FORNAPlotter
from data_manager import data_manager
from pca_plot import PCAPlotter

sample_files = ['AT2G02130.1.fa.dbr', 'insilico_AT5G02120.1.dbr']


class Ifv:
    def __init__(self):
        self.__parse_parameters()
        self.__read_data()
        self.__create()
        self.__plot()

    def __parse_parameters(self):
        self.prs = argparse.ArgumentParser(
            description='Interactive Folding Visualizer')
        self.prs.add_argument('-i', '--input', required=False,
                         help='Working Directory')
        self.prs.parse_args()

    def __read_data(self):
        version = 1
        # self, input_path, position_file, section_file,  folding_version
        self.data_provider = data_manager(input_path='C:/Users/Marco/IFV/data/', position_file='xlsite',
                                          section_file='Araport11_protein_coding.201606', folding_version=version)
        self.__read_file(sample_files[version - 1])
        print(self)

    def __read_file(self, name):
        self.section = self.data_provider.read_section(name.replace('.fa.dbr', ''))
        self.positions = self.data_provider.read_positions(self.section)
        self.folding = self.data_provider.read_file(name, self.section, self.positions)

    def __create(self):
        self.app = dash.Dash(__name__)
        self.__initLayout()

    def __plot(self):
        plotter = PCAPlotter()
        plotter_forna = FORNAPlotter()
        fig = plotter.plot(self.folding)
        forna = plotter_forna.plot(folding=self.folding[0])

        self.plot.children = [dcc.Graph(
            figure=fig
        )]

        self.graph.children = [html.Div(forna)]


    def __initLayout(self):

        #self.heading = html.H1(children=['Interactive Folding Visualizer'])
        self.graph = html.Div(children=['Graph'], id='graph', className='col-md-7 column')
        self.plot = html.Div(children=['Plot'], id='plot', className='col-md-3 column')
        #self.menu = html.Div(children=[self.heading], id='menu', className='col-md-2 column')
        self.menu = html.Div(id='menu', className='col-md-2 column')

        self.wrapper = html.Div(children=[
                        self.menu,
                        self.graph,
                        self.plot
                        ], id='wrapper')

        self.app.layout = self.wrapper

    def start(self):
        self.app.run_server(debug=True)


if __name__ == '__main__':
    ifv = Ifv()
    ifv.start()
