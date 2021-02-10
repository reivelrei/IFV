import plotly.express as px
from sklearn.decomposition import PCA


def plot(pca_vectors, pointLabels, colors):
    pca = PCA()
    components = pca.fit_transform(pca_vectors)

    labels = {
         str(i): f"PC {i + 1} ({var:.1f}%)"
        for i, var in enumerate(pca.explained_variance_ratio_ * 100)
    }

    fig = px.scatter_matrix(
        components,
        hover_name=pointLabels,
        color=colors,
        color_continuous_scale=px.colors.sequential.Viridis,
        labels=labels,
        height=900,
        width=900,
        dimensions=range(2),

    )

    fig['layout']['xaxis']['autorange'] = "reversed"
    fig.update_traces(diagonal_visible=False)

    fig.show()
