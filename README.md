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

|Known Locations|Algorithm|Number Correct|Average Distance|Time (seconds)|Standard Deviation of Average Distances|
|     :---:    |     :---:      |     :---:     |     :---:     |     :---:     |     :---:     |
|0|Random|0.8667|2.2203|0.0047|0.0352|
|0|Greedy|1.0|1.9764|0.2905|0.0|
|0|Partitioning-Based|11.0|1.4853|395.897|0.0|
|0|Graph Drawing|1.3333|2.0509|7.5926|0.1776|
|3|Random|3.8667|2.1927|0.0047|0.0485|
|3|Greedy|5.2667|1.9103|0.1016|0.5144|
|3|Partitioning-Based|20.7333|1.3088|408.281|0.3281|
|3|Graph Drawing|5.0667|1.6324|8.1366|0.3606|
|68|Random|68.9667|1.9937|0.0051|0.0547|
|68|Greedy|70.6667|1.8556|0.1078|0.4058|
|68|Partitioning-Based|80.1667|1.5062|403.1903|0.4409|
|68|Graph Drawing|72.6|1.0994|7.4609|0.2018|
|206|Random|207.2667|1.551|0.0058|0.0378|
|206|Greedy|209.7333|1.3816|0.1059|0.3154|
|206|Partitioning-Based|215.7667|1.3659|407.0433|0.3927|
|206|Graph Drawing|214.4|0.4511|5.7416|0.0395|
|344|Random|345.1667|1.1163|0.0062|0.0425|
|344|Greedy|348.9333|0.9168|0.0975|0.2704|
|344|Partitioning-Based|352.6333|0.9387|397.8484|0.2807|
|344|Graph Drawing|354.6667|0.2836|4.2107|0.0176|
|481|Random|481.8667|0.6754|0.0065|0.0278|
|481|Greedy|495.0|0.3876|0.0824|0.1482|
|481|Partitioning-Based|486.6333|0.6401|392.5766|0.123|
|481|Graph Drawing|493.9|0.1602|2.6946|0.0103|

### Fairfax Mobility Network

This table shows the qualitative results for the Fairfax Mobility Data. The results for the Fairfax Mobility Data show similar patterns to that of the Facebook Location data. For the Partitioning Algorithm with 24 known locations, clusters can be seen where communities where matched correctly, but vertices within the community were matched incorrectly.

| Known Locations | Random Algorithm | Greedy Algorithm | Partitioning Algorithm | Graph Drawing Algorithm |
|     :---:    |     :---:      |     :---:     |     :---:     |     :---:     |
| 0 | <img src="ExperimentalResults/FairfaxImages/FairfaxCorrectDistanceRandomKnown0.png" width="250"> | <img src="ExperimentalResults/FairfaxImages/FairfaxCorrectDistanceGreedyKnown0.png" width="250"/> | <img src="ExperimentalResults/FairfaxImages/FairfaxCorrectDistancePartitioningKnown0.png" width="250"> | <img src="ExperimentalResults/FairfaxImages/FairfaxCorrectDistanceGraphDrawingKnown0.png" width="250"> |
| 3 | <img src="ExperimentalResults/FairfaxImages/FairfaxCorrectDistanceRandomKnown3.png" width="250"> | <img src="ExperimentalResults/FairfaxImages/FairfaxCorrectDistanceGreedyKnown3.png" width="250"/> | <img src="ExperimentalResults/FairfaxImages/FairfaxCorrectDistancePartitioningKnown3.png" width="250"> | <img src="ExperimentalResults/FairfaxImages/FairfaxCorrectDistanceGraphDrawingKnown3.png" width="250"> |
| 24 \(10%\) | <img src="ExperimentalResults/FairfaxImages/FairfaxCorrectDistanceRandomKnown24.png" width="250"> | <img src="ExperimentalResults/FairfaxImages/FairfaxCorrectDistanceGreedyKnown24.png" width="250"/> | <img src="ExperimentalResults/FairfaxImages/FairfaxCorrectDistancePartitioningKnown24.png" width="250"> | <img src="ExperimentalResults/FairfaxImages/FairfaxCorrectDistanceGraphDrawingKnown24.png" width="250"> |
| 121 \(50%\) | <img src="ExperimentalResults/FairfaxImages/FairfaxCorrectDistanceRandomKnown121.png" width="250"> | <img src="ExperimentalResults/FairfaxImages/FairfaxCorrectDistanceGreedyKnown121.png" width="250"/> | <img src="ExperimentalResults/FairfaxImages/FairfaxCorrectDistancePartitioningKnown121.png" width="250"> | <img src="ExperimentalResults/FairfaxImages/FairfaxCorrectDistanceGraphDrawingKnown121.png" width="250"> |

|Known Locations|Algorithm|Number Correct|Average Distance|Time (seconds)|Standard Deviation of Average Distances|
|     :---:    |     :---:      |     :---:     |     :---:     |     :---:     |     :---:     |
|0|Random|0.9|0.1642|0.0008|0.0051|
|0|Greedy|0.0|0.1427|0.0321|0.0|
|0|Partitioning-Based|1.8|0.1607|429.5778|0.0471|
|0|Graph Drawing|0.5333|0.1748|0.2672|0.0319|
|3|Random|3.9|0.1627|0.0008|0.0052|
|3|Greedy|4.6667|0.1311|0.0102|0.0329|
|3|Partitioning-Based|6.4|0.1279|397.1876|0.0654|
|3|Graph Drawing|4.9667|0.136|0.2651|0.0408|
|24|Random|24.8333|0.1477|0.0009|0.005|
|24|Greedy|25.7333|0.1205|0.0103|0.0231|
|24|Partitioning-Based|27.1|0.1145|394.0292|0.0542|
|24|Graph Drawing|24.8|0.146|0.2602|0.0343|
|72|Random|73.1667|0.1158|0.001|0.0043|
|72|Greedy|74.4333|0.0944|0.0109|0.0188|
|72|Partitioning-Based|73.8667|0.1038|414.3915|0.0361|
|72|Graph Drawing|73.2333|0.1051|0.2468|0.0184|
|121|Random|121.9667|0.0822|0.001|0.0042|
|121|Greedy|123.6|0.0662|0.0105|0.0147|
|121|Partitioning-Based|121.9667|0.079|393.0506|0.0183|
|121|Graph Drawing|122.4333|0.0651|0.2379|0.0087|
|169|Random|169.9|0.0485|0.001|0.0043|
|169|Greedy|172.2|0.0344|0.0092|0.0088|
|169|Partitioning-Based|170.3333|0.0487|422.536|0.0108|
|169|Graph Drawing|170.7667|0.0393|0.2287|0.0058|

### Synthetic Geosocial Erdős-Rényi Network

| Known Locations | Random Algorithm | Greedy Algorithm | Partitioning Algorithm | Graph Drawing Algorithm |
|     :---:    |     :---:      |     :---:     |     :---:     |     :---:     |
| 0 | <img src="ExperimentalResults/ErdosReyniImages/ERCorrectDistanceRandomKnown0.png" width="250"/> | <img src="ExperimentalResults/ErdosReyniImages/ERCorrectDistanceGreedyKnown0.png" width="250"> | <img src="ExperimentalResults/ErdosReyniImages/ERCorrectDistancePartitioningKnown0.png" width="250"> | <img src="ExperimentalResults/ErdosReyniImages/ERCorrectDistanceGraphDrawingKnown0.png" width="250"> |
| 3 | <img src="ExperimentalResults/ErdosReyniImages/ERCorrectDistanceRandomKnown3.png" width="250"/> | <img src="ExperimentalResults/ErdosReyniImages/ERCorrectDistanceGreedyKnown3.png" width="250"> | <img src="ExperimentalResults/ErdosReyniImages/ERCorrectDistancePartitioningKnown3.png" width="250"> | <img src="ExperimentalResults/ErdosReyniImages/ERCorrectDistanceGraphDrawingKnown3.png" width="250"> |
| 10 | <img src="ExperimentalResults/ErdosReyniImages/ERCorrectDistanceRandomKnown3.png" width="250"/> | <img src="ExperimentalResults/ErdosReyniImages/ERCorrectDistanceGreedyKnown10.png" width="250"> | <img src="ExperimentalResults/ErdosReyniImages/ERCorrectDistancePartitioningKnown10.png" width="250"> | <img src="ExperimentalResults/ErdosReyniImages/ERCorrectDistanceGraphDrawingKnown10.png" width="250"> |
| 50 | <img src="ExperimentalResults/ErdosReyniImages/ERCorrectDistanceRandomKnown50.png" width="250"/> | <img src="ExperimentalResults/ErdosReyniImages/ERCorrectDistanceGreedyKnown50.png" width="250"> | <img src="ExperimentalResults/ErdosReyniImages/ERCorrectDistancePartitioningKnown50.png" width="250"> | <img src="ExperimentalResults/ErdosReyniImages/ERCorrectDistanceGraphDrawingKnown50.png" width="250"> |

| Population | Known Locations|Algorithm|Number Correct|Average Distance|Time (seconds)|Standard Deviation of Average Distances|
|     :---:    |     :---:    |     :---:      |     :---:     |     :---:     |     :---:     |     :---:     |
|100|0|Greedy|1.6|0.4934|0.0057|0.0694|
|100|0|Partitioning-Based|1.6667|0.4632|415.9714|0.142|
|100|0|Graph Drawing|1.1333|0.5431|0.0593|0.0975|
|100|0|Random|1.1|0.5222|0.0003|0.0307|
|100|3|Greedy|5.8|0.4264|0.0027|0.0783|
|100|3|Partitioning-Based|4.1333|0.5031|423.1631|0.046|
|100|3|Graph Drawing|8.5333|0.3224|0.0587|0.1071|
|100|3|Random|4.5333|0.501|0.0004|0.0272|
|100|10|Greedy|12.1667|0.4144|0.0028|0.0912|
|100|10|Partitioning-Based|12.4333|0.4162|414.2671|0.1102|
|100|10|Graph Drawing|25.1667|0.1551|0.059|0.0638|
|100|10|Random|11.5667|0.4629|0.0004|0.0234|
|100|50|Greedy|52.5333|0.2085|0.0025|0.0286|
|100|50|Partitioning-Based|51.2333|0.2228|401.6261|0.0496|
|100|50|Graph Drawing|66.5|0.0582|0.0543|0.0108|
|100|50|Random|51.1333|0.2528|0.0004|0.0201|
|500|0|Greedy|1.1667|0.502|0.1408|0.0588|
|500|0|Partitioning-Based|5.0|0.3893|422.1444|0.166|
|500|0|Graph Drawing|1.6|0.5244|4.9275|0.1464|
|500|0|Random|0.9333|0.5195|0.0028|0.012|
|500|3|Greedy|5.0667|0.4698|0.0457|0.0747|
|500|3|Partitioning-Based|8.8667|0.3608|393.7533|0.1843|
|500|3|Graph Drawing|5.6|0.4353|5.2905|0.1354|
|500|3|Random|4.1667|0.5185|0.0028|0.0145|
|500|10|Greedy|12.3|0.4557|0.0462|0.0664|
|500|10|Partitioning-Based|13.7667|0.4086|395.2789|0.1798|
|500|10|Graph Drawing|17.2667|0.2357|5.3788|0.0889|
|500|10|Random|10.9333|0.508|0.0029|0.0124|
|500|50|Greedy|51.9333|0.4527|0.0509|0.0652|
|500|50|Partitioning-Based|53.7667|0.3421|395.1362|0.1455|
|500|50|Graph Drawing|63.7|0.1309|4.8724|0.0059|
|500|50|Random|50.9|0.4697|0.003|0.0113|
|1000|0|Greedy|1.6333|0.5104|0.6366|0.0533|
|1000|0|Partitioning-Based|8.1|0.3301|406.0176|0.1802|
|1000|0|Graph Drawing|1.3333|0.5273|12.4259|0.122|
|1000|0|Random|1.0|0.5216|0.0095|0.0095|
|1000|3|Greedy|5.1|0.4823|0.1982|0.0709|
|1000|3|Partitioning-Based|10.2|0.3824|432.8506|0.1841|
|1000|3|Graph Drawing|5.1|0.4522|13.1301|0.1627|
|1000|3|Random|4.1|0.5191|0.0098|0.0071|
|1000|10|Greedy|11.9|0.4812|0.1853|0.0621|
|1000|10|Partitioning-Based|15.4667|0.4125|401.1124|0.2068|
|1000|10|Graph Drawing|13.0|0.366|13.1802|0.1193|
|1000|10|Random|10.8333|0.5157|0.0097|0.0074|
|1000|50|Greedy|52.8667|0.459|0.1964|0.0706|
|1000|50|Partitioning-Based|56.8667|0.3587|452.2197|0.1832|
|1000|50|Graph Drawing|59.3333|0.1617|12.7328|0.008|
|1000|50|Random|51.1|0.4965|0.0101|0.0093|

## References
<a id="1">[1]</a> 
M. Bailey, R. Cao, T. Kuchler, J. Stroebel, and A. Wong. Social connectedness: Measurement, determinants, and effects. *Journal of Economic Perspectives*, 32(3):259–280, 2018.

<a id="2">[2]</a> 
Y. Kang, S. Gao, Y. Liang, M. Li, J. Rao, and J. Kruse. Multiscale dynamic human mobility flow dataset in the us during the covid-19 epidemic. *Scientific data*, 7(1):390, 2020.

<a id="3">[3]</a> 
K. Gallagher, T. Anderson, A. Crooks, and A. Züfle. Synthetic geosocial network generation. In *Proceedings of the 7th ACM SIGSPATIAL Workshop on Location-based Recommendations, Geosocial Networks and Geoadvertising*, pages 15–24, 2023.
