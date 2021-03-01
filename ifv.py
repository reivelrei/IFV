# -*- coding: utf-8 -*-
import argparse
import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

from dash.dependencies import Input, Output
from ColorScale import ColorScale
from FORNAPlotter import FORNAPlotter
from data_manager import data_manager
from pca_plot import PCAPlotter
sample_files = ['AT5G02120.1.fa.dbr', 'insilico_AT5G02120.1.dbr']
version = 1


class Ifv:
    def __init__(self):
        self.prs = None
        self.working_path = None
        self.data_provider = None
        self.file_lists = None
        self.section = None
        self.positions = None
        self.folding = None
        self.app = None
        self.selected_bed = 'Araport11_protein_coding.201606.bed'
        self.selected_graph = 'xlsite.bedgraph'
        self.selected_transcript = sample_files[version - 1]
        self.selected_folding = 0
        self.selected_color_mode = ColorScale.ABSOLUTE
        self.graph = None
        self.plot = None
        self.menu = None
        self.wrapper = None

        self.parse_parameters()
        self.read_data()
        self.create()

    def parse_parameters(self):
        self.prs = argparse.ArgumentParser(
            description='Interactive Folding Visualizer')
        self.prs.add_argument('-i', '--input', required=False,
                              help='Working Directory')
        self.prs.parse_args()
        # TODO Path args?
        self.working_path = 'C:/Users/Marco/IFV/data/'

    def read_data(self):
        if self.data_provider is None:
            self.data_provider = data_manager(input_path=self.working_path, position_file=self.selected_graph,
                                              section_file=self.selected_bed, folding_version=version)
            self.file_lists = self.data_provider.list_files()
        else:
            self.data_provider.update(input_path=self.working_path, position_file=self.selected_graph,
                                      section_file=self.selected_bed, folding_version=version)

        if self.must_read_new():
            self.read_file(self.selected_transcript)

    def read_file(self, name):
        self.section = self.data_provider.read_section(name.replace('.fa.dbr', ''))
        self.positions = self.data_provider.read_positions(self.section)
        self.folding = self.data_provider.read_file(name, self.section, self.positions)

    def create(self):
        self.app = dash.Dash(name=__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
        self.init_layout()
        self.define_callbacks()

    def plot_graphs(self, plot_pca, plot_forna):
        graphs = {}

        if plot_pca:
            plotter = PCAPlotter()
            fig = plotter.plot(self.folding)
            graphs['pca'] = dcc.Graph(figure=fig)

        if plot_forna:
            plotter_forna = FORNAPlotter()
            forna = plotter_forna.plot(folding=self.folding[self.selected_folding], color_scale=self.selected_color_mode)
            graphs['forna'] = html.Div(forna)

        return graphs

    def init_layout(self):

        self.graph = html.Div(children=['Graph'], id='graph', className='col-md-7 column')
        self.plot = html.Div(children=['Plot'], id='plot', className='col-md-3 column')
        self.menu = html.Div(children=['Menu'], id='menu', className='col-md-2 column')

        self.wrapper = html.Div(children=[
                        self.menu,
                        self.graph,
                        self.plot
                        ], id='wrapper')

        self.menu.children = [
            dbc.Label('Bed-File (.bed)'),
            dcc.Dropdown(
                id="bed_select",
                options=[
                ]),
            dbc.Label('Bedgraph-File (.bedgraph)'),
            dcc.Dropdown(
                id="graph_select",
                options=[
                ]),
            dbc.Label('Transcript (.fa.dbr)'),
            dcc.Dropdown(
                id="transcript_select",
                options=[
            ]),
            dbc.Label('Faltung'),
            dcc.Dropdown(
                id="folding_select",
                options=[
            ]),
            dbc.FormGroup(
                [
                    dbc.Label("Färbung"),
                    dbc.Checklist(
                        options=[
                            {"label": "Blockfärbung", "value": ColorScale.REGION},
                            {"label": "Logarithmisch", "value": ColorScale.LOG},
                        ],
                        value=[],
                        id="color_select",
                        inline=True,
                        switch=True,
                    ),
                ]
            ),
            dbc.Button("Download", color="info", className="mr-1", id='download_button'),
        ]

        graph_select = self.find_menu_child(id='graph_select')
        for file in self.file_lists['position_files']:
            graph_select.options.append({'label': file, 'value': file})

        bed_select = self.find_menu_child(id='bed_select')
        for file in self.file_lists['section_files']:
            bed_select.options.append({'label': file, 'value': file})

        transcript_select = self.find_menu_child(id='transcript_select')
        for file in self.file_lists['folding_files']:
            transcript_select.options.append({'label': file, 'value': file})

        self.app.layout = self.wrapper

    def define_callbacks(self):
        @self.app.callback(
            Output(component_id='plot', component_property='children'),
            Output(component_id='graph', component_property='children'),
            Output(component_id='folding_select', component_property='options'),
            Input(component_id='bed_select', component_property='value'),
            Input(component_id='graph_select', component_property='value'),
            Input(component_id='folding_select', component_property='value'),
            Input(component_id='transcript_select', component_property='value'),
            Input(component_id='color_select', component_property='value')
        )
        def bed_selected(bed_select, graph_select, folding_select, transcript_select, color_select):
            ifv.selected_bed = bed_select
            ifv.selected_graph = graph_select
            ifv.selected_folding = folding_select
            ifv.selected_transcript = transcript_select

            if ColorScale.REGION in color_select:
                ifv.selected_color_mode = ColorScale.REGION
            else:
                if ColorScale.LOG in color_select:
                    ifv.selected_color_mode = ColorScale.LOG
                else:
                    ifv.selected_color_mode = ColorScale.ABSOLUTE

            graph = ifv.check_new_load()
            new_foldings = ifv.update_values()
            return graph['pca'], graph['forna'], new_foldings

    def find_menu_child(self, id):
        child = []

        for ch in self.menu.children:
            try:
                if ch.id is id:
                    child = ch
                    break
            except AttributeError:
                # when the child has no id
                pass

        return child

    def start(self):
        self.app.run_server(debug=True)

    def check_new_load(self):
        graphs = {}
        if self.selected_graph is not None \
                and self.selected_bed is not None \
                and self.selected_transcript is not None:
            self.read_data()
            if self.selected_folding is not None:
                graphs = self.plot_graphs(plot_pca=True, plot_forna=True)
            else:
                graphs = self.plot_graphs(plot_pca=True, plot_forna=False)
                graphs['forna'] = dbc.Label('NO_DATA_FOUND')
        else:
            graphs['pca'] = dbc.Label('NO_DATA_FOUND')
            graphs['forna'] = dbc.Label('NO_DATA_FOUND')
        return graphs

    def must_read_new(self):
        read_new = False

        if self.folding is None:
            read_new = True
        else:
            if self.folding[0].section is None:
                read_new = True
            else:
                read_new = self.folding[0].section.transcript is not self.selected_transcript
        return read_new

    def update_values(self):
        options = []
        if self.selected_transcript is not None:
            index = 0
            for f in self.folding:
                options.append({'label': f.label, 'value': index})
                index += 1
        return options


if __name__ == '__main__':
    ifv = Ifv()
    ifv.start()

