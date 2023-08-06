# -*- coding:utf-8 -*-
# Author: hankcs
# Date: 2022-04-13 02:15
import io
from datetime import date
import pygraphviz as pgv

from perin_parser.thirdparty.mtool.graph import Graph


def to_dot(mrp: dict):
    mrp['time'] = str(date.today())
    g = Graph.decode(mrp)
    with io.StringIO() as out:
        g.dot(out)
        return out.getvalue()


def to_svg(dot):
    try:
        G = pgv.AGraph(dot)
        return G.draw(format='svg', prog='dot').decode("utf-8").strip()
    except Exception as e:
        return f'Failed due to {e}.'


def main():
    mrp = {
        "id": "0",
        "input": "The boy wants the girl to believe him .",
        "nodes": [
            {
                "id": 0,
                "label": "boy"
            },
            {
                "id": 1,
                "label": "want-01"
            },
            {
                "id": 2,
                "label": "girl"
            },
            {
                "id": 3,
                "label": "believe-01"
            }
        ],
        "edges": [
            {
                "source": 3,
                "target": 0,
                "label": "arg1"
            },
            {
                "source": 1,
                "target": 3,
                "label": "arg1"
            },
            {
                "source": 3,
                "target": 2,
                "label": "arg0"
            },
            {
                "source": 1,
                "target": 0,
                "label": "arg0"
            }
        ],
        "tops": [
            1
        ],
        "framework": "amr"
    }
    dot = to_dot(mrp)
    svg = to_svg(dot)
    print(svg)


if __name__ == '__main__':
    main()
