from utils import (
    read_graph_entities_json,
    read_json,
    catch_single_val,
    Graph
)
import networkx as nx
from pyvis.network import Network

def visualise_all_graph_types(graph):
    G = nx.DiGraph()

    graph_types = set([x["@type"] for x in graph.entities])
    color_map = dict(zip(graph_types, colors[:len(graph_types)]))

    for entity in graph.entities:
        G.add_node(entity["@id"], color=color_map[entity["@type"]], title=entity["@type"])
        for item in entity.items():
            if item[0] not in ["@id", "@type"]:
                for value in catch_single_val(item[1]):
                    value_strf = f"{(value[:75] + '..') if len(value) > 75 else value}"
                    G.add_edge(entity["@id"], value_strf, label=item[0])

    net = Network(height='100%', width='100%', directed =True)
    net.set_edge_smooth('dynamic')
    net.from_nx(G)
    net.show("./output/visualise_all_graph_types.html")


def main():
    entities = read_graph_entities_json("./graph/*.json")
    schema = read_json("./graph/meta/schema.jsonx")
    graph = Graph(entities=entities)

    visualise_all_graph_types(graph)

if __name__ == "__main__":

    colors = [
        "#000000",
        "#00FF00",
        "#0000FF",
        "#FF0000",
        "#01FFFE",
        "#FFA6FE",
        "#FFDB66",
        "#006401",
        "#010067",
        "#95003A",
        "#007DB5",
        "#FF00F6",
        "#FFEEE8",
        "#774D00",
        "#90FB92",
        "#0076FF",
        "#D5FF00",
        "#FF937E",
        "#6A826C",
        "#FF029D",
        "#FE8900",
        "#7A4782",
        "#7E2DD2",
        "#85A900",
        "#FF0056",
        "#A42400",
        "#00AE7E",
        "#683D3B",
        "#BDC6FF",
        "#263400",
        "#BDD393",
        "#00B917",
        "#9E008E",
        "#001544",
        "#C28C9F",
        "#FF74A3",
        "#01D0FF",
        "#004754",
        "#E56FFE",
        "#788231",
        "#0E4CA1",
        "#91D0CB",
        "#BE9970",
        "#968AE8",
        "#BB8800",
        "#43002C",
        "#DEFF74",
        "#00FFC6",
        "#FFE502",
        "#620E00",
        "#008F9C",
        "#98FF52",
        "#7544B1",
        "#B500FF",
        "#00FF78",
        "#FF6E41",
        "#005F39",
        "#6B6882",
        "#5FAD4E",
        "#A75740",
        "#A5FFD2",
        "#FFB167",
        "#009BFF",
        "#E85EBE"]

    main()
