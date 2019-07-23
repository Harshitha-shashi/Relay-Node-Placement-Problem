#!/usr/bin/env python
# coding: utf-8

# In[14]:

'''The files can be directly executed with their filename.
The data file can be changed in the DataLoading function
by giving the appropriate filename in the function
at the start of the main function'''
import os
import sys  # Library for INT_MAX
import math        
    

def Dataloading(name):
    with open(name, "r") as the_file:
        row = 0
        for line in the_file:
            lines = line.replace("\n"," ").split(" ")
            if (row == 0):
                nodes = int(lines[0])
                graph = Graph(nodes)
            if (row == 1):
                Range = int(lines[0])
            if (row == 2):
                Budget = int(lines[0])
            if (row >= 3):
                graph.addEdge(int(lines[0]), int(lines[1]), int(lines[2]))
            row+=1
    return  Range, Budget, graph


class Graph():

    def __init__(self, vertices):
        self.V = vertices
        self.graph = [[0 for column in range(vertices)]
                      for row in range(vertices)]
        self.count = [0] * self.V
        self.upperBound = sys.maxsize

    def addEdge(self, u, v, weight):
#         print("came here")
        self.graph[u][v] = weight
        self.graph[v][u] = weight

    '''These are the functions for edges for checking Circle present or not. Adding included edges to the vertices'''
    #adding count to the edge to the vertice when a new edge is added during kmst
    def add(self, vertex):
        self.count[vertex] += 1

    #decreasing count to the edge excluding to the vertice when an edge is removed from the Kmst
    def remove(self, vertex):
        if self.count[vertex] > 0:
            self.count[vertex] -= 1

    #Total number of vertices which are included in the mst till now
    def numVerticesIncluded(self):
        size = 0
        for i in range(self.V):
            if self.count[i] > 0:
                size += 1
        return size

    #To check if there is a circle or not by adding this edge to the K-MST
    def isCircle(self, u, v):
        return self.count[u] > 0 and self.count[v] > 0


    '''Function to find a vertex with minimum distance value, from the set of vertices
    which has not been included in MST'''
    def minVertex(self, vertex, mstSet):
        # Initilaize min value
        min_index = -1
        min = sys.maxsize
        for v in range(self.V):
            if vertex[v] < min and mstSet[v] == False:
                min = vertex[v]
                min_index = v
        return min_index
    
    # Function to construct an MST 
    def primMST(self):
        # Vertex is used to pick minimum weight edge in cut
        vertex = [sys.maxsize] * self.V
        # Array to store constructed MST Make key 0 so that this vertex is picked as first vertex
        parent = [-1] * self.V 
        vertex[0] = 0
        mstSet = [False] * self.V
        # To represent it as a root
        parent[0] = -1
        for cout in range(self.V):
            # Pick the minimum distance vertex not processed
            u = self.minVertex(vertex, mstSet)
            mstSet[u] = True
            for v in range(self.V):
                if self.graph[u][v] > 0 and mstSet[v] == False and vertex[v] > self.graph[u][v]:
                    vertex[v] = self.graph[u][v]
                    parent[v] = u
        result = []
        for i in range(1, self.V):
            result.append([parent[i], i, vertex[i]])
        return result


##recursive function using branch and bound to calculate the K_MST function using 
def calculate_Kmst(mst, k, i, count, currentCost, threshold, graph, included):
    
    if count == k - 1 and graph.numVerticesIncluded() == k and currentCost < graph.upperBound:
        graph.upperBound = currentCost
        for j in range(len(included)):
            graph.included[j] = included[j]
        return
    
    #stop the program when currentCost is greater than threshold or UpperBound or included vertices is greater than k-1
    if i >= len(mst) or count >= k - 1 or currentCost > graph.upperBound:
        return
    #Getting the next shortest nodes required one 
    u, v, weight = mst[i]
    backtrack = False
    if not graph.isCircle(u, v):
        graph.add(u)
        graph.add(v)
        included[i] = True
        backtrack = True
        calculate_Kmst(mst, k, i + 1, count + 1, currentCost + weight, threshold, graph, included)
    #BackTracking until we have to remove the edges which forming circles
    if backtrack:
        graph.remove(u)
        graph.remove(v)
        included[i] = False
    calculate_Kmst(mst, k, i + 1, count, currentCost, threshold, graph, included)




if __name__ == "__main__":
    R, threshold, graph = Dataloading('datafile.txt')
    mst = graph.primMST()
    for k in range((graph.V)-1, 1, -1) :
        graph.count = [0] * graph.V
        graph.included = [False] * len(mst)
        included = [False] * len(mst)
        graph.upperBound = sys.maxsize
        calculate_Kmst(mst, k=k, i=0, count=0, currentCost = 0, threshold = threshold, graph = graph, included=included)
        relaysNeeded = 0
        for i in range(len(graph.included)):
            if graph.included[i]:
                relaysNeeded += math.ceil(mst[i][2] / R) - 1
#                 print(mst[i])
        if relaysNeeded!=0 and relaysNeeded <= threshold:
            print("The longest connected component is at k = ", k, " and the cost is ", relaysNeeded, "which is less than threshold")
            print("The connected components are as follows")
            for i in range(len(graph.included)):
                if graph.included[i]:
                    print("[", mst[i][0]," ", mst[i][1]," ", math.ceil(mst[i][2] / R) - 1 ," ]")
            break


