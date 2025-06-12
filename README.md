# Geosocial Network Location Estimation
This is the code for the forthcoming paper *Your Friends Reveal Where You Are: Location Estimation based on Friends’ Locations in Geosocial Networks*.

## Abstract
Geosocial networks serve as a critical bridge between cyber and physical worlds by linking individuals to locations. In many real-world scenarios, both the structure of social networks and the spatial distribution of places are known—yet the connecting information that links people to locations is missing. This absence is often intentional to ensure user privacy. In this work, we investigate the feasibility of estimating locations based solely on network structure and a limited set of known user-location pairs.
We propose and evaluate three novel algorithms for linking social and spatial networks: (i) a greedy assignment algorithm, (ii) a hierarchical approach using graph partitioning, and (iii) a spatially-aware adaptation of force-directed graph drawing. Each method is further enhanced to incorporate a small number of known anchor vertex—users with known locations. Using anonymized social network data from the Virginia, USA region, our empirical evaluation shows that even a sparse set of anchor points can enable accurate estimation of users' home locations. These findings highlight both the potential analytical value and the privacy risks associated with linking social and spatial data.

## Algorithms
The three proposed algorithms are included in this repository. The Greedy Algorithm matches vertices to locations that are close to locations of vertices they are connected to. Vertices are processed iteratively in order of degree. The Partitioning Algorithm utilizes METIS, a graph partitioning software, to match communities of vertices to communities of locations. Finally, the Graph Drawing Algorithm utilizes the NetworkX Spring Layout function to generate locations for each vertex in the social network. Vertices are then matched to the closest available location.

Each algorithm requires an adjacency matrix to represent the social network, a list of coordinates that vertices are matched to, and a dictionary of known locations which maps the ID of a vertex in the adjacency matrix to a coordinate in the list of locations. If there are no known locations, this dictionary is empty. For each algorithm, a dictionary which maps vertices to locations is returned.

## Experimental Results
|![](ExperimentalResults/FacebookImages/FacebookGroundTruth.png)<br>Ground Truth Network for Facebook Location Data|![](ExperimentalResults/FairfaxImages/FairfaxGroundTruth.png)<br>Ground Truth Network for Fairfax Mobility Data|
|:-:|:-:|

The three proposed algorithms were tested on three datasets: Facebook Social Connectedness Data [[1]](#1), Fairfax Mobility Data [[2]](#2), and a Synthetic Geosocial Erdős-Rényi Network [[3]](#3). The social networks and locations for the first two datasets were generated using the code in the folder Datasets. For the Synthetic Geosocial Erdős-Rényi Network, random locations were used and the social network was generated using the code in the [Synthetic Geosocial Networks Repository](https://github.com/KetevanGallagher/Synthetic-Geosocial-Networks). The Ground Truth Networks for the Facebook and Fairfax data are shown in the figure above.

### Facebook Social Connectedness Network
The qualitative results for the Facebook Network are shown in the figure below. In each figure, the estimated location and true location for each vertex is connected. Vertices with known locations are colored red. As can be seen, the links in the Graph Drawing Algorithm image become shorter and the graph becomes less dark when compared to the other algorithms as the number of known locations increase. Although the Partitioning Algorithm does not have very many long links when only a few locations are known, as can be seen in the example with three known locations, it does not improve as known locations are added. All three algorithms have more whitespace than the Random graph, which has very long links even with many known locations.

| Known Locations |Random Algorithm | Greedy Algorithm | Partitioning Algorithm | Graph Drawing Algorithm | 
|     :---:    |     :---:      |     :---:     |     :---:     |     :---:     |
| 0 | <img src="ExperimentalResults/FacebookImages/FacebookCorrectDistanceRandomKnown0.png" width="250"> | <img src="ExperimentalResults/FacebookImages/FacebookCorrectDistanceGreedyKnown0.png" width="250"/> | <img src="ExperimentalResults/FacebookImages/FacebookCorrectDistancePartitioningKnown0.png" width="250"> | <img src="ExperimentalResults/FacebookImages/FacebookCorrectDistanceGraphDrawingKnown0.png" width="250"> |
| 3 | <img src="ExperimentalResults/FacebookImages/FacebookCorrectDistanceRandomKnown3.png" width="250"> | <img src="ExperimentalResults/FacebookImages/FacebookCorrectDistanceGreedyKnown3.png" width="250"/> | <img src="ExperimentalResults/FacebookImages/FacebookCorrectDistancePartitioningKnown3.png" width="250"> | <img src="ExperimentalResults/FacebookImages/FacebookCorrectDistanceGraphDrawingKnown3.png" width="250"> |
| 68 \(10%\) | <img src="ExperimentalResults/FacebookImages/FacebookCorrectDistanceRandomKnown68.png" width="250"> | <img src="ExperimentalResults/FacebookImages/FacebookCorrectDistanceGreedyKnown68.png" width="250"/> | <img src="ExperimentalResults/FacebookImages/FacebookCorrectDistancePartitioningKnown68.png" width="250"> | <img src="ExperimentalResults/FacebookImages/FacebookCorrectDistanceGraphDrawingKnown68.png" width="250"> |
| 344 \(50%\) | <img src="ExperimentalResults/FacebookImages/FacebookCorrectDistanceRandomKnown344.png" width="250"> | <img src="ExperimentalResults/FacebookImages/FacebookCorrectDistanceGreedyKnown344.png" width="250"/> | <img src="ExperimentalResults/FacebookImages/FacebookCorrectDistancePartitioningKnown344.png" width="250"> | <img src="ExperimentalResults/FacebookImages/FacebookCorrectDistanceGraphDrawingKnown344.png" width="250"> |

### Fairfax Mobility Network

This table shows the qualitative results for the Fairfax Mobility Data. The results for the Fairfax Mobility Data show similar patterns to that of the Facebook Location data. For the Partitioning Algorithm with 24 known locations, clusters can be seen where communities where matched correctly, but vertices within the community were matched incorrectly.

| Known Locations | Random Algorithm | Greedy Algorithm | Partitioning Algorithm | Graph Drawing Algorithm |
|     :---:    |     :---:      |     :---:     |     :---:     |     :---:     |
| 0 | <img src="ExperimentalResults/FairfaxImages/FairfaxCorrectDistanceRandomKnown0.png" width="250"> | <img src="ExperimentalResults/FairfaxImages/FairfaxCorrectDistanceGreedyKnown0.png" width="250"/> | <img src="ExperimentalResults/FairfaxImages/FairfaxCorrectDistancePartitioningKnown0.png" width="250"> | <img src="ExperimentalResults/FairfaxImages/FairfaxCorrectDistanceGraphDrawingKnown0.png" width="250"> |
| 3 | <img src="ExperimentalResults/FairfaxImages/FairfaxCorrectDistanceRandomKnown3.png" width="250"> | <img src="ExperimentalResults/FairfaxImages/FairfaxCorrectDistanceGreedyKnown3.png" width="250"/> | <img src="ExperimentalResults/FairfaxImages/FairfaxCorrectDistancePartitioningKnown3.png" width="250"> | <img src="ExperimentalResults/FairfaxImages/FairfaxCorrectDistanceGraphDrawingKnown3.png" width="250"> |
| 24 \(10%\) | <img src="ExperimentalResults/FairfaxImages/FairfaxCorrectDistanceRandomKnown24.png" width="250"> | <img src="ExperimentalResults/FairfaxImages/FairfaxCorrectDistanceGreedyKnown24.png" width="250"/> | <img src="ExperimentalResults/FairfaxImages/FairfaxCorrectDistancePartitioningKnown24.png" width="250"> | <img src="ExperimentalResults/FairfaxImages/FairfaxCorrectDistanceGraphDrawingKnown24.png" width="250"> |
| 121 \(50%\) | <img src="ExperimentalResults/FairfaxImages/FairfaxCorrectDistanceRandomKnown121.png" width="250"> | <img src="ExperimentalResults/FairfaxImages/FairfaxCorrectDistanceGreedyKnown121.png" width="250"/> | <img src="ExperimentalResults/FairfaxImages/FairfaxCorrectDistancePartitioningKnown121.png" width="250"> | <img src="ExperimentalResults/FairfaxImages/FairfaxCorrectDistanceGraphDrawingKnown121.png" width="250"> |

### Synthetic Geosocial Erdős-Rényi Network

| Known Locations | Random Algorithm | Greedy Algorithm | Partitioning Algorithm | Graph Drawing Algorithm |
|     :---:    |     :---:      |     :---:     |     :---:     |     :---:     |
| 0 | <img src="ExperimentalResults/ErdosReyniImages/ERCorrectDistanceRandomKnown0.png" width="250"/> | <img src="ExperimentalResults/ErdosReyniImages/ERCorrectDistanceGreedyKnown0.png" width="250"> | <img src="ExperimentalResults/ErdosReyniImages/ERCorrectDistancePartitioningKnown0.png" width="250"> | <img src="ExperimentalResults/ErdosReyniImages/ERCorrectDistanceGraphDrawingKnown0.png" width="250"> |
| 3 | <img src="ExperimentalResults/ErdosReyniImages/ERCorrectDistanceRandomKnown3.png" width="250"/> | <img src="ExperimentalResults/ErdosReyniImages/ERCorrectDistanceGreedyKnown3.png" width="250"> | <img src="ExperimentalResults/ErdosReyniImages/ERCorrectDistancePartitioningKnown3.png" width="250"> | <img src="ExperimentalResults/ErdosReyniImages/ERCorrectDistanceGraphDrawingKnown3.png" width="250"> |
| 10 | <img src="ExperimentalResults/ErdosReyniImages/ERCorrectDistanceRandomKnown3.png" width="250"/> | <img src="ExperimentalResults/ErdosReyniImages/ERCorrectDistanceGreedyKnown10.png" width="250"> | <img src="ExperimentalResults/ErdosReyniImages/ERCorrectDistancePartitioningKnown10.png" width="250"> | <img src="ExperimentalResults/ErdosReyniImages/ERCorrectDistanceGraphDrawingKnown10.png" width="250"> |
| 50 | <img src="ExperimentalResults/ErdosReyniImages/ERCorrectDistanceRandomKnown50.png" width="250"/> | <img src="ExperimentalResults/ErdosReyniImages/ERCorrectDistanceGreedyKnown50.png" width="250"> | <img src="ExperimentalResults/ErdosReyniImages/ERCorrectDistancePartitioningKnown50.png" width="250"> | <img src="ExperimentalResults/ErdosReyniImages/ERCorrectDistanceGraphDrawingKnown50.png" width="250"> |

## References
<a id="1">[1]</a> 
M. Bailey, R. Cao, T. Kuchler, J. Stroebel, and A. Wong. Social connectedness: Measurement, determinants, and effects. *Journal of Economic Perspectives*, 32(3):259–280, 2018.

<a id="2">[2]</a> 
Y. Kang, S. Gao, Y. Liang, M. Li, J. Rao, and J. Kruse. Multiscale dynamic human mobility flow dataset in the us during the covid-19 epidemic. *Scientific data*, 7(1):390, 2020.

<a id="3">[3]</a> 
K. Gallagher, T. Anderson, A. Crooks, and A. Züfle. Synthetic geosocial network generation. In *Proceedings of the 7th ACM SIGSPATIAL Workshop on Location-based Recommendations, Geosocial Networks and Geoadvertising*, pages 15–24, 2023.
