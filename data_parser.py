from __future__ import annotations
import json
import subprocess
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

class Datafile:
    def __init__(self, datafile):
        self.datafile = datafile
        
        self.operator_id = 0
        self.operators = {}
    
    def get_new_id(self):
        self.operator_id += 1
        return f"op{self.operator_id}"
    
    def register(self, node):
        operator_name = node.operator_id
        self.operators[operator_name] = node.to_dict()
        
    def read(self):
        return Timeline("JSONReader", "json", [], [], "JSONReader", self)
    
    def build(self, sink_node):
        opname = sink_node.operator_id
        self.operators["result"] = self.operators[opname]
        #del self.operators[opname]
        self.operators["sink"] = ["result"]
        return json.dumps(self.operators, indent=2)
    
    
class Timeline:
    def __init__(self, operation, result_type, upstream_ops, parameters, operator_id, parser:NewParser):
        self.operation = operation
        self.result_type = result_type
        self.upstream_ops = upstream_ops
        self.parameters = parameters
        self.operator_id = operator_id
        self.parent = parser
        self.parent.register(self)

    def to_dict(self):
        return {
            "operation": self.operation,
            "result_type": self.result_type,
            "upstream_ops": self.upstream_ops,
            "parameters": self.parameters,
        }

    def _to_true(self) -> Timeline:
        return Timeline("ToTrue", "boolean", [self.operator_id], [], self.parent.get_new_id(), self.parent)
    
    def _had_true_within(self, window) -> Timeline:
        return Timeline("HadTrueEventWithin", "boolean", [self.operator_id], [float(window)], self.parent.get_new_id(), self.parent)
    
    def get(self, field, value_type) -> Timeline:
        return Timeline("JSONGet", value_type, [self.operator_id], [field], self.parent.get_new_id(), self.parent)
    
    def averageWithin(self, window_len) -> Timeline:
        return Timeline("AverageWithin", self.result_type, [self.operator_id], [float(window_len)], self.parent.get_new_id(), self.parent)
    
    def add(self, other:Timeline) -> Timeline:
        return Timeline("Add", self.result_type, 
                        upstream_ops=[self.operator_id, other.operator_id], 
                        parameters=[], operator_id = self.parent.get_new_id(), parser = self.parent)

    def addConst(self, value) -> Timeline:
        return Timeline("AddConst", self.result_type, 
                        upstream_ops=[self.operator_id], 
                        parameters=[float(value)], operator_id = self.parent.get_new_id(), parser = self.parent)

    def multiply(self, other:Timeline) -> Timeline:
        return Timeline("Multiply", self.result_type, 
                        upstream_ops=[self.operator_id, other.operator_id], 
                        parameters=[], operator_id = self.parent.get_new_id(), parser = self.parent)

    def multiplyConst(self, value) -> Timeline:
        return Timeline("MultiplyConst", self.result_type, 
                        upstream_ops=[self.operator_id], 
                        parameters=[float(value)], operator_id = self.parent.get_new_id(), parser = self.parent)

    def divide(self, other:Timeline) -> Timeline:
        return Timeline("Divide", self.result_type, 
                        [self.operator_id, other.operator_id], [], self.parent.get_new_id(), self.parent)
    
    def hasDataWithin(self, window_len) -> Timeline:
        tmp1 = self._to_true()
        return tmp1._had_true_within(window_len)

    
    def shift(self, left) -> Timeline:
        return Timeline("Lookahead", self.result_type, [self.operator_id], [float(left)], self.parent.get_new_id(), self.parent)

    def latestEventToState(self) -> Timeline:
        return Timeline("LatestEventToState", self.result_type, [self.operator_id], [], self.parent.get_new_id(), self.parent)
     
    def calculate(self):
        dag_json = self.parent.build(self)
        with open("library/compiled.json", "w") as fout:
            print(dag_json, file = fout)
        with open("library/config_simple.json", "r") as fin:
            cfg = json.load(fin)
        cfg["data_file"] = self.parent.datafile
        with open("library/config_simple.json", "w") as fout:
            print(json.dumps(cfg, indent = 2), file=fout)
        #with open(os.devnull, 'wb') as devnull:
        #    subprocess.check_call(["scala", "library/timeline_prototype.jar", "library/config_simple.json"], stdout=subprocess.STDOUT, stderr=subprocess.STDOUT)
        os.system("scala library/timeline_prototype.jar library/config_simple.json")
    
    
def read_df(filename):
    df = pd.read_csv(filename, header=None, sep=',', skiprows=1)
    df.columns = ["start", "end", "value"]
    return df

def timeline_to_dataframe(timeline: Timeline):
    timeline.calculate()
    with open("library/compiled.json") as fin:
        cfg = json.load(fin)
    name = cfg["sink"][0]
    return read_df(f"library/output/{name}.timeline")


def plot_timeline(timeline: Timeline):
    timeline.calculate()
    with open("library/compiled.json") as fin:
        cfg = json.load(fin)
    dfs = {name: read_df(f"library/output/{name}.timeline") for name in cfg['sink']}
    for name in dfs.keys():
        df = dfs[name]
        plt.plot(df["end"], df["value"])
        plt.xlabel("time")
        plt.ylabel(name)
        plt.grid()
        plt.show()

def plot_multiple_timeline(timelines, labels=None):
    if labels is None:
        labels = list(range(len(timelines)))

    for timeline, label in zip(timelines, labels):
        df = timeline_to_dataframe(timeline)
        plt.plot(df["end"], df["value"], label=label)
    plt.xlabel("time")
    plt.ylabel("values")
    plt.grid()
    plt.legend()
    plt.show()


def calculate_rmse(groundtruth: Timeline, prediction: Timeline, show=False):
    preddf = timeline_to_dataframe(prediction)
    realdf = timeline_to_dataframe(groundtruth)
    final_df = realdf.merge(preddf, on="end", how="left").fillna(0)
    if show:
        plt.plot(final_df["end"], final_df["value_x"], label="ground truth")
        plt.plot(final_df["end"], final_df["value_y"], label="predicted value")
        plt.grid()
        plt.legend()
        plt.show()
    return np.sqrt(np.mean((final_df["value_x"] - final_df["value_y"]) ** 2))

