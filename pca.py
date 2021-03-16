import plotly.express as px
import plotly.graph_objects as go
from sklearn.decomposition import PCA


# This class plots a folding file as a pca scatter plot.
class PCAPlotter:

    # plots the given folding
    # folding - the folding
    @staticmethod
    def plot(foldings):
        pca_vectors = []
        labels = []
        colors = []
        for val in foldings:
            pca_vectors.append(val.pca_vector)
            lbl = str(val.energy) + ' kcal/mol'
            val.label = lbl
            labels.append(lbl)
            colors.append(val.energy)

        return PCAPlotter.__create_figure(pca_vectors, labels, colors)

    # [PRIVATE] plots the given vectors with the given labels and colors
    @staticmethod
    def __create_figure(pca_vectors, point_labels, colors):
        pca = PCA(n_components=2)
        components = pca.fit_transform(pca_vectors)

        labels = {
            str(i): f"PC {i + 1} ({var:.1f}%)"
            for i, var in enumerate(pca.explained_variance_ratio_ * 100)
        }

        df = {'x': components[:, 0] * -1, 'y': components[:, 1]}
        fig = go.Figure(px.scatter(x=df['x'], y=df['y'], hover_name=point_labels,
                                   color=colors,
                                   color_continuous_scale=px.colors.sequential.Reds[::-1],
                                   labels=labels, height=900, width=900))

        fig.update_traces(customdata=point_labels, hovertemplate='<i>Energy</i>: %{customdata}',
                          selector=dict(type='scatter'), marker_line_width=0.5, marker_size=8)
        fig.update_xaxes(title_text='PC2', showline=True, linewidth=1, linecolor='black', showgrid=True, gridwidth=1,
                         gridcolor='#f0f0f0', zeroline=True, zerolinewidth=1, zerolinecolor='#f0f0f0')
        fig.update_yaxes(title_text='PC1', showline=True, linewidth=1, linecolor='black', showgrid=True, gridwidth=1,
                         gridcolor='#f0f0f0', zeroline=True, zerolinewidth=1, zerolinecolor='#f0f0f0')
        fig.update_layout(
            dragmode='select',
            width=450,
            height=450,
            hovermode='closest',
            plot_bgcolor='rgba(0, 0, 0, 0)',
            paper_bgcolor='rgba(0, 0, 0, 0)'
        )

        fig.update_layout(coloraxis_colorbar=dict(
            title="MFE",
        ))

        return fig
