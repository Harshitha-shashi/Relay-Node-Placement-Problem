#!/usr/bin/env python
# coding: utf-8

# In[7]:


'''The files can be directly executed with their filename.
The data file can be changed in the DataLoading function
by giving the appropriate filename in the function
at the start of the main function'''
import numpy as np

#Loading the data from the given input file
def Dataloading(name):
    with open(name, "r") as the_file:
        c = 0
        for line in the_file:
            c = c + 1
    with open(name, "r") as the_file:
        row = 0
        gr = []
        for line in the_file:
            lines = line.split(" ")
            if (row == 0):
                nodes = int(lines[0])
            if (row == 1):
                Range= int(lines[0])
            if (row == 2):
                Budget = int(lines[0])
            if (row >= 3):
                gr.append([int(lines[0]), int(lines[1]), int(lines[2])])
            row+=1
    return nodes, Range, Budget, gr


def prims(V, G):

  Vertex = 0
  M_S_T = []
  edgelist = []
  labeled = []

  #Iterating the Loop till all the nodes are Labelled
  while len(M_S_T) != V-1:
    min = float('inf')
    labeled.append(Vertex)

    #Taking all the Edges From the Graph to the List
    for e in G:
        if (e[1] == Vertex or e[0]== Vertex):
            edgelist.append(e)

    #Finding the Minimum edge to add to MST
    for e in edgelist:
      if e[2] < min and e[1] not in labeled:
          min = e[2]
          mEdge=e


    edgelist.remove(mEdge)
    M_S_T.append(mEdge)
    Vertex = mEdge[1]

  return M_S_T

'''The files can be directly executed with their filename.
The data file can be changed in the DataLoading function
by giving the appropriate filename in the function 
at the start of the main function'''
if __name__ == "__main__":
    nodes, R, B, gr = Dataloading('datafile.txt')

    #Calling Prims Algorithm to find Minimum Spanning Tree
    # print('MST:',prims(nodes, gr))
    mst=np.array(prims(nodes, gr))
    # print(mst.shape)

    #Reassigning the Weights of MST to the Format of No of relay Nodes Required
    mst[:,-1]=(np.ceil(mst[:,-1]/R))-1
    sum=int(np.sum(mst[:,-1],axis=0))
    # print('newM after Changing Edge Weights',mst)
    # print(sum)
    mst1=mst.tolist()
    #Finding the Edges with Maximum Relay Nodes and Removing it Until Budget is Satisified
    while sum>B:
        edge=max(mst[:,-1])
        #Finding the Edges that having MAXIMUM Edges(If they are More than one)
        maxi=list(np.where(mst[:,-1]==edge))
        # print(maxi[0][0])
        #Deleting the First Edge which is having Maximum Edge
        mst=np.delete(mst,maxi[0][0],axis=0)
        sum=int(np.sum(mst[:,-1],axis=0))
    # print(mst.shape)
    mstl=mst.tolist()
    print('Results of BCRP-MNCC',mstl)

