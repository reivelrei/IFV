# -*- coding: utf-8 -*-
import argparse
import time
import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

from dash.dependencies import Input, Output
import visdcc

from block import Block
from color import Color
from folding import Folding
from forna import Forna
from cache import Cache
from datamanager import DataManager
from pca import PCAPlotter
from position import Position
from section import Section

version = 1


# [MAIN]
# IFV is a tool for visualizing RNA secondary structures and protein binding sites.
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
        self.selected_bed = None
        self.selected_graph = None
        self.selected_transcript = None
        self.selected_folding_index = 0
        self.selected_folding = None
        self.selected_color_mode = Color.ABSOLUTE
        self.graph = None
        self.plot = None
        self.menu = None
        self.blocklegende = None
        self.loader = None
        self.output = None
        self.wrapper = None
        self.forna = None
        self.use_cache = False
        self.cache = Cache()

        self.parse_parameters()
        self.read_data()
        self.create()

    # parse all input parameters
    # -i path -> the path of the folder with all the data.
    # if -i is not provided, the data folder of the project is used as default
    def parse_parameters(self):
        self.prs = argparse.ArgumentParser(
            description='Interactive Folding Visualizer')
        self.prs.add_argument('-i', '--input', required=False,
                              help='Working Directory')
        args = self.prs.parse_args()

        if args.input is not None:
            self.working_path = args.input
        else:
            self.working_path = 'data/'

    # reads the data for the all the selected_x properties
    def read_data(self):
        if self.data_provider is None:
            self.data_provider = DataManager(input_path=self.working_path, position_file=self.selected_graph,
                                             section_file=self.selected_bed, folding_version=version)
            self.file_lists = self.data_provider.list_files()
        else:
            self.data_provider.update(input_path=self.working_path, position_file=self.selected_graph,
                                      section_file=self.selected_bed, folding_version=version)
            if self.must_read_new():
                self.read_file(self.selected_transcript)

    # reads the data for the given transcript file (.fa.dbr)
    def read_file(self, name):
        self.section = self.data_provider.read_section(name.replace('.fa.dbr', ''))
        self.positions = self.data_provider.read_positions(self.section)
        self.folding = self.data_provider.read_file(name, self.section, self.positions)

    # checks cache with must_read_new.
    # if a new read is necessary the method reads the new data and plots it
    def check_new_load(self):
        graphs = {}

        if self.selected_graph is not None \
                and self.selected_bed is not None \
                and self.selected_transcript is not None:
            self.read_data()
            if self.selected_folding_index is None:
                self.selected_folding_index = 0

            self.selected_folding = self.folding[self.selected_folding_index]
            cached_folding = self.find_cached()

            if cached_folding is None:
                graphs = self.plot_graphs(plot_pca=True, plot_forna=True)
                self.cache_graph(graphs)
            else:
                graphs = cached_folding.graph

        else:
            graphs['pca'] = dbc.Label('NO_DATA_FOUND')
            graphs['forna'] = dbc.Label('NO_DATA_FOUND')
        return graphs

    # checks if the app has to read a new file or could use previous data
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

    # fills the dropdown for all possible foldings after reading the .fa.dbr file
    def update_values(self):
        options = []
        if self.selected_transcript is not None:
            index = 0
            for f in self.folding:
                options.append({'label': f.label, 'value': index})
                index += 1
        return options

    # finds a cached folding if present, else returns None
    def find_cached(self):
        if self.use_cache:
            return self.cache.get_from_cache(self.selected_folding)
        else:
            return None

    # caches the given graph with the current selected folding
    # graph - a graph dict with plotted graphs
    def cache_graph(self, graph):
        if self.use_cache:
            if self.selected_folding is not None:
                self.selected_folding.graph = graph
                self.cache.add_to_cache(self.selected_folding)

    # creates the app
    def create(self):
        self.app = dash.Dash(name=__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)
        self.init_layout()
        self.define_callbacks()

    # plots the selected data
    # plot_pca - the transcript file which should be plotted as pca scatterplot
    # plot_forna - the folding structure which should be plotted using forna container
    def plot_graphs(self, plot_pca, plot_forna):
        graphs = {}

        if plot_pca:
            plotter = PCAPlotter()
            fig = plotter.plot(self.folding)
            graphs['pca'] = dcc.Graph(figure=fig, id="pca")

        if plot_forna:
            forna = Forna()
            forna = forna.plot(folding=self.selected_folding, color_scale=self.selected_color_mode)
            self.forna = forna.id
            graphs['forna'] = html.Div(children=[forna], id='fornaWrapper')

        return graphs

    # creates the layout for the app
    def init_layout(self):

        self.graph = html.Div(children=[''], id='graph', className='col-md-7 column')
        self.plot = html.Div(children=[''], id='plot', className='col-md-3 column')

        self.loader = html.Div(children=[html.Div(children=[html.Div(), html.Div(), html.Div(), html.Div()], className='lds-ring')],
                                id='loader',  className='loader')

        self.menu = html.Div(children=['Menu'], id='menu', className='col-md-2 column')
        self.output = html.Div(children=[], id='output')
        self.wrapper = html.Div(children=[
                        self.menu,
                        self.graph,
                        self.plot,
                        self.loader
                        ], id='wrapper')

        self.menu.children = [
            dbc.Label(Section.get_display_name()),
            dcc.Dropdown(
                id="bed_select",
                value=None,
                options=[
                ]),
            dbc.Label(Position.get_display_name()),
            dcc.Dropdown(
                id="graph_select",
                value=None,
                options=[
                ]),
            dbc.Label(Folding.get_display_name()),
            dcc.Dropdown(
                id="transcript_select",
                value=None,
                options=[
            ]),
            dbc.Label('folding'),
            dcc.Dropdown(
                id="folding_select",
                value=None,
                options=[
            ]),
            dbc.FormGroup(
                [
                    dbc.Label("coloring"),
                    dbc.Checklist(
                        options=[
                            {"label": "blocks", "value": Color.REGION},
                            {"label": "logarithmic", "value": Color.LOG},
                        ],
                        value=[],
                        id="color_select",
                        inline=True,
                        switch=True,
                    ),
                ]
            ),
            html.Div(children=[], id='legende', className='legende'),
            dbc.Button("Download", color="info", className="mr-1", id='download_button'),
            self.output,
            visdcc.Run_js(id='javascript'),
            visdcc.Run_js(id='loadingScript')

        ]

        graph_select = self.find_menu_child(key='graph_select')
        for file in self.file_lists['position_files']:
            if graph_select.value is None:
                graph_select.value = file
            graph_select.options.append({'label': file, 'value': file})

        bed_select = self.find_menu_child(key='bed_select')
        for file in self.file_lists['section_files']:
            if bed_select.value is None:
                bed_select.value = file
            bed_select.options.append({'label': file, 'value': file})

        transcript_select = self.find_menu_child(key='transcript_select')
        for file in self.file_lists['folding_files']:
            if transcript_select.value is None:
                transcript_select.value = file
            transcript_select.options.append({'label': file, 'value': file})

        self.app.layout = self.wrapper

    # defines all the callbacks for the GUI of the app
    def define_callbacks(self):
        @self.app.callback(
            Output(component_id='plot', component_property='children'),
            Output(component_id='graph', component_property='children'),
            Output(component_id='folding_select', component_property='options'),
            Output(component_id='legende', component_property='children'),
            Output(component_id='loadingScript', component_property='run'),
            Input(component_id='bed_select', component_property='value'),
            Input(component_id='graph_select', component_property='value'),
            Input(component_id='folding_select', component_property='value'),
            Input(component_id='transcript_select', component_property='value'),
            Input(component_id='color_select', component_property='value')
        )
        def bed_selected(bed_select, graph_select, folding_select, transcript_select, color_select):
            start_time = current_milli_time()
            ifv.selected_bed = bed_select
            ifv.selected_graph = graph_select
            ifv.selected_folding_index = folding_select
            ifv.selected_transcript = transcript_select
            legende = None

            if Color.REGION in color_select:
                ifv.selected_color_mode = Color.REGION
                legende = html.Div(children=[html.Div(children=[], style=
                                             {'backgroundColor':  Block.color_intron()}, className='legendBlock intronBlock'),
                                             html.Div(children=["= Intron"], className = "legendLabel"),
                                             html.Div(children=[], style=
                                             {'backgroundColor': Block.color_utr()}, className='legendBlock'),
                                             html.Div(children=["= UTR"], className="legendLabel"),
                                             html.Div(children=[], style=
                                             {'backgroundColor': Block.color_cds()}, className='legendBlock'),
                                             html.Div(children=["= CDS"], className="legendLabel"),
                                             ], id='legend_wrapper')
            else:
                if Color.LOG in color_select:
                    ifv.selected_color_mode = Color.LOG
                else:
                    ifv.selected_color_mode = Color.ABSOLUTE

            graph = ifv.check_new_load()
            new_foldings = ifv.update_values()
            end_time = current_milli_time()
            print("used time : " + str(end_time-start_time))
            return graph['pca'], graph['forna'], new_foldings, legende, 'hideLoader()'

        @self.app.callback(
            Output(component_id='folding_select', component_property='value'),
            Input('pca', 'clickData'))
        def on_data_clicked(click_data):
            if click_data is not None:
                index = click_data['points'][0]['pointIndex']
                folding = self.folding[index]
                return index
            else:
                return self.selected_folding_index

        @self.app.callback(
            Output('javascript', 'run'),
            Input('download_button', 'n_clicks'))
        def on_download(n_clicks):
            if n_clicks is not None:
                forna_id = self.forna
                return 'download(\"'+forna_id+'\")'

            return ''

    # convenience method for finding the menu layout element and its children
    # key - the id of the element
    def find_menu_child(self, key):
        child = []

        for ch in self.menu.children:
            try:
                if ch.id is key:
                    child = ch
                    break
            except AttributeError:
                # when the child has no id
                pass

        return child

    # starts the app
    def start(self):
        self.app.run_server(debug=True)


# gives the current time in millis
def current_milli_time():
    return round(time.time() * 1000)


if __name__ == '__main__':
    ifv = Ifv()
    ifv.start()

