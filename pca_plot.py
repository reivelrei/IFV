import plotly.express as px
import plotly.graph_objects as go
from sklearn.decomposition import PCA


class PCAPlotter:
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
                                   color_continuous_scale=px.colors.sequential.Viridis,
                                   labels=labels, height=900, width=900, template="plotly_dark"))

        fig.update_traces(customdata=point_labels, hovertemplate='<i>Energy</i>: %{customdata}', selector=dict(type='scatter'))
        fig.update_xaxes(title_text='PC2')
        fig.update_yaxes(title_text='PC1')
        fig.update_layout(
            title='PCA',
            dragmode='select',
            width=450,
            height=450,
            hovermode='closest'
        )

        return fig