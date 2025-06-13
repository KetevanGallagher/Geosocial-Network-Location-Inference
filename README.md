# Geosocial Network Location Estimation
This is the code for the forthcoming paper *Your Friends Reveal Where You Are: Location Estimation based on Friends’ Locations in Geosocial Networks*.

## Abstract
Geosocial networks serve as a critical bridge between cyber and physical worlds by linking individuals to locations. In many real-world scenarios, both the structure of social networks and the spatial distribution of places are known—yet the connecting information that links people to locations is missing. This absence is often intentional to ensure user privacy. In this work, we investigate the feasibility of estimating locations based solely on network structure and a limited set of known user-location pairs.
We propose and evaluate three novel algorithms for linking social and spatial networks: (i) a greedy assignment algorithm, (ii) a hierarchical approach using graph partitioning, and (iii) a spatially-aware adaptation of force-directed graph drawing. Each method is further enhanced to incorporate a small number of known anchor vertex—users with known locations. Using anonymized social network data from the Virginia, USA region, our empirical evaluation shows that even a sparse set of anchor points can enable accurate estimation of users' home locations. These findings highlight both the potential analytical value and the privacy risks associated with linking social and spatial data.

## Algorithms
The three proposed algorithms are included in this repository. The Greedy algorithm matches vertices to locations that are close to locations of vertices they are connected to. Vertices are processed iteratively in order of degree. The Partitioning-Based algorithm utilizes METIS, a graph partitioning software, to match clusters of vertices to clusters of locations. Finally, the Graph Drawing algorithm utilizes the NetworkX Spring Layout function to generate locations for each vertex in the social network. Vertices are then matched to the closest available location.

Each algorithm requires an adjacency matrix to represent the social network, a list of coordinates that vertices are matched to, and a dictionary of known locations which maps the ID of a vertex in the adjacency matrix to a coordinate in the list of locations. If there are no known locations, this dictionary is empty. For each algorithm, a dictionary which maps vertices to locations is returned.

## Experimental Results
|![](ExperimentalResults/FacebookImages/FacebookGroundTruth.png)<br>Ground Truth Network for Facebook Location Data|![](ExperimentalResults/FairfaxImages/FairfaxGroundTruth.png)<br>Ground Truth Network for Fairfax Mobility Data|
|:-:|:-:|

The three proposed algorithms were tested on three datasets: Facebook Social Connectedness Data [[1]](#1), Fairfax Mobility Data [[2]](#2), and a Synthetic Geosocial Erdős-Rényi Network [[3]](#3). The social networks and locations for the first two datasets were generated using the code in the folder Datasets. For the Synthetic Geosocial Erdős-Rényi Network, random locations were used and the social network was generated using the code in the [Synthetic Geosocial Networks Repository](https://github.com/KetevanGallagher/Synthetic-Geosocial-Networks). The Ground Truth Networks for the Facebook and Fairfax data are shown in the figure above.

### Facebook Social Connectedness Network
The qualitative results for the Facebook Network are shown in the figure below. In each figure, the estimated location and true location for each vertex is connected. Vertices with known locations are colored red. As can be seen, the links in the Graph Drawing algorithm image become shorter and the graph becomes less dark when compared to the other algorithms as the number of known locations increase. In particular, the figure for the Graph Drawing algorithm with 481 known locations has very few long links even when compared to the other algorithms with 481 known locations. Although the Partitioning-Based algorithm does not have very many long links when only a few locations are known, as can be seen in the example with three known locations, it does not improve as known locations are added. All three algorithms have more whitespace than the random graph, which has very long links even with many known locations.

| Known Locations |Random Algorithm | Greedy Algorithm | Partitioning-Based Algorithm | Graph Drawing Algorithm | 
|     :---:    |     :---:      |     :---:     |     :---:     |     :---:     |
| 0 | <img src="ExperimentalResults/FacebookImages/FacebookCorrectDistanceRandomKnown0.png" width="250"> | <img src="ExperimentalResults/FacebookImages/FacebookCorrectDistanceGreedyKnown0.png" width="250"/> | <img src="ExperimentalResults/FacebookImages/FacebookCorrectDistancePartitioningKnown0.png" width="250"> | <img src="ExperimentalResults/FacebookImages/FacebookCorrectDistanceGraphDrawingKnown0.png" width="250"> |
| 3 | <img src="ExperimentalResults/FacebookImages/FacebookCorrectDistanceRandomKnown3.png" width="250"> | <img src="ExperimentalResults/FacebookImages/FacebookCorrectDistanceGreedyKnown3.png" width="250"/> | <img src="ExperimentalResults/FacebookImages/FacebookCorrectDistancePartitioningKnown3.png" width="250"> | <img src="ExperimentalResults/FacebookImages/FacebookCorrectDistanceGraphDrawingKnown3.png" width="250"> |
| 68 \(10%\) | <img src="ExperimentalResults/FacebookImages/FacebookCorrectDistanceRandomKnown68.png" width="250"> | <img src="ExperimentalResults/FacebookImages/FacebookCorrectDistanceGreedyKnown68.png" width="250"/> | <img src="ExperimentalResults/FacebookImages/FacebookCorrectDistancePartitioningKnown68.png" width="250"> | <img src="ExperimentalResults/FacebookImages/FacebookCorrectDistanceGraphDrawingKnown68.png" width="250"> |
| 344 \(50%\) | <img src="ExperimentalResults/FacebookImages/FacebookCorrectDistanceRandomKnown344.png" width="250"> | <img src="ExperimentalResults/FacebookImages/FacebookCorrectDistanceGreedyKnown344.png" width="250"/> | <img src="ExperimentalResults/FacebookImages/FacebookCorrectDistancePartitioningKnown344.png" width="250"> | <img src="ExperimentalResults/FacebookImages/FacebookCorrectDistanceGraphDrawingKnown344.png" width="250"> |

Detailed quanitative results for the Facebook Network are displayed below. The runtime of each algorithm is relatively similar, except for the Partitioning-Based algorithm, which must consider combinations of location and social network clusters. It can be observed that the Partitioning-Based algorithm is able to match many vertices to their correct location when compared to the other algorithms for a small number of known locations, but the number of additional vertices inferred correctly does not increase with a higher number of known locations. However, for the Graph Drawing algorithm, as the number of known locations increase, so does the number of vertices inferred correctly when compared to the other three algorithms. Additionally, the standard deviation of the average distances for the Greedy and Partitioning-Based algorithms is higher than that for the random baseline and the Graph Drawing algorithm for all trials with known locations. For the Greedy algorithm, if the starting vertex is inferred incorrectly, then the error increases as more vertices are inferred incorrectly. For the Partitioning-Based algorithm, if clusters are matched incorrectly, this can lead to large errors later one. The random baseline has the lowest standard deviation, which is to be expected. The standard deviation for the Graph Drawing algorithm decreases as the number of known locations increase. For example, for 344 known locations, the standard deviations of the Partitioning-Based and Greedy algorithms are over ten times that of the Graph Drawing algorithm.

|Known Locations|Algorithm|Number Correct|Average Distance|Runtime (seconds)|Standard Deviation of Average Distances|
|     :---:    |     :---:      |     :---:     |     :---:     |     :---:     |     :---:     |
|0|Random|1.0333|210.5632|0.0046|4.0744|
|0|Greedy|1.0|171.3947|0.2925|0.0|
|0|Partitioning-Based|11.0|107.2386|397.4918|0.0|
|0|Graph Drawing|1.4667|200.2531|7.5295|17.6145|
|3|Random|3.7333|211.3271|0.0047|3.9804|
|3|Greedy|5.5667|191.8009|0.1023|44.5949|
|3|Partitioning-Based|22.0333|121.382|419.185|54.6683|
|3|Graph Drawing|5.0|134.8171|8.3625|25.0135|
|68|Random|69.1|189.3965|0.0051|3.5319|
|68|Greedy|71.7333|161.813|0.1073|50.8007|
|68|Partitioning-Based|79.7|136.5924|405.4833|59.2571|
|68|Graph Drawing|72.0|92.6715|7.5383|24.8616|
|206|Random|206.9667|146.3208|0.0057|5.1359|
|206|Greedy|209.2333|133.4153|0.1072|34.683|
|206|Partitioning-Based|219.0667|112.5161|396.7046|47.8983|
|206|Graph Drawing|215.9667|39.0742|5.8469|3.2839|
|344|Random|345.0667|105.53|0.0062|4.2922|
|344|Greedy|348.4333|97.7457|0.0972|23.8029|
|344|Partitioning-Based|350.4667|86.9888|431.18|27.0903|
|344|Graph Drawing|353.8667|24.4707|4.1703|1.7799|
|481|Random|481.8667|63.4465|0.0065|3.6456|
|481|Greedy|494.5667|36.4627|0.0829|14.2442|
|481|Partitioning-Based|488.3667|59.2672|394.2475|15.6749|
|481|Graph Drawing|493.6|13.7765|2.6696|0.9123|

### Fairfax Mobility Network

This table shows the qualitative results for the Fairfax Mobility Data, averaged over thirty trials. The results for the Fairfax Mobility Data show similar patterns to that of the Facebook Location data. For the Partitioning-Based algorithm with 24 known locations, areas can be seen where clusters were matched correctly but individual vertices within the cluster were matched incorrectly. For the Graph Drawing figure with zero known locations, long links on the peripheries of the graph are observed due to the fact that there are no known locations that can be used to attract vertices to the correct location.

| Known Locations | Random Algorithm | Greedy Algorithm | Partitioning-Based Algorithm | Graph Drawing Algorithm |
|     :---:    |     :---:      |     :---:     |     :---:     |     :---:     |
| 0 | <img src="ExperimentalResults/FairfaxImages/FairfaxCorrectDistanceRandomKnown0.png" width="250"> | <img src="ExperimentalResults/FairfaxImages/FairfaxCorrectDistanceGreedyKnown0.png" width="250"/> | <img src="ExperimentalResults/FairfaxImages/FairfaxCorrectDistancePartitioningKnown0.png" width="250"> | <img src="ExperimentalResults/FairfaxImages/FairfaxCorrectDistanceGraphDrawingKnown0.png" width="250"> |
| 3 | <img src="ExperimentalResults/FairfaxImages/FairfaxCorrectDistanceRandomKnown3.png" width="250"> | <img src="ExperimentalResults/FairfaxImages/FairfaxCorrectDistanceGreedyKnown3.png" width="250"/> | <img src="ExperimentalResults/FairfaxImages/FairfaxCorrectDistancePartitioningKnown3.png" width="250"> | <img src="ExperimentalResults/FairfaxImages/FairfaxCorrectDistanceGraphDrawingKnown3.png" width="250"> |
| 24 \(10%\) | <img src="ExperimentalResults/FairfaxImages/FairfaxCorrectDistanceRandomKnown24.png" width="250"> | <img src="ExperimentalResults/FairfaxImages/FairfaxCorrectDistanceGreedyKnown24.png" width="250"/> | <img src="ExperimentalResults/FairfaxImages/FairfaxCorrectDistancePartitioningKnown24.png" width="250"> | <img src="ExperimentalResults/FairfaxImages/FairfaxCorrectDistanceGraphDrawingKnown24.png" width="250"> |
| 121 \(50%\) | <img src="ExperimentalResults/FairfaxImages/FairfaxCorrectDistanceRandomKnown121.png" width="250"> | <img src="ExperimentalResults/FairfaxImages/FairfaxCorrectDistanceGreedyKnown121.png" width="250"/> | <img src="ExperimentalResults/FairfaxImages/FairfaxCorrectDistancePartitioningKnown121.png" width="250"> | <img src="ExperimentalResults/FairfaxImages/FairfaxCorrectDistanceGraphDrawingKnown121.png" width="250"> |

The following table shows detailed quanitative results for Fairfax Mobility Network, averaged over thirty trials. Similar patterns to those in generated by the Facebook Dataset are observed in this table.

|Known Locations|Algorithm|Number Correct|Average Distance|Runtime (seconds)|Standard Deviation of Average Distances|
|     :---:    |     :---:      |     :---:     |     :---:     |     :---:     |     :---:     |
|0|Random|0.6|14.2815|0.0008|0.5016|
|0|Greedy|0.0|11.971|0.0324|0.0|
|0|Partitioning-Based|1.2333|14.0688|403.6501|5.1748|
|0|Graph Drawing|0.9|14.9034|0.2661|4.4204|
|3|Random|4.0667|14.029|0.0008|0.4557|
|3|Greedy|5.4333|11.1201|0.0102|3.3937|
|3|Partitioning-Based|5.1|12.9973|400.4093|6.1565|
|3|Graph Drawing|4.8|12.1459|0.2648|4.8716|
|24|Random|25.0333|12.8345|0.0009|0.5159|
|24|Greedy|26.7333|10.5143|0.0101|2.693|
|24|Partitioning-Based|27.7333|8.7394|414.2682|5.6241|
|24|Graph Drawing|25.1333|12.6441|0.2635|2.9283|
|72|Random|72.8333|9.9931|0.0009|0.4199|
|72|Greedy|74.3667|7.5181|0.0113|1.734|
|72|Partitioning-Based|74.8|8.0971|402.9873|3.7353|
|72|Graph Drawing|73.3333|8.3542|0.2476|1.3505|
|121|Random|122.0|7.0541|0.001|0.4822|
|121|Greedy|123.6|5.8137|0.0105|1.7397|
|121|Partitioning-Based|122.6667|6.378|417.6914|2.0634|
|121|Graph Drawing|122.9|5.5236|0.2367|0.8885|
|169|Random|170.0333|4.3409|0.001|0.3587|
|169|Greedy|172.0333|3.3329|0.009|1.1096|
|169|Partitioning-Based|170.3333|4.0672|391.0564|1.0173|
|169|Graph Drawing|170.8667|3.1458|0.2289|0.4035|

### Synthetic Geosocial Erdős-Rényi Network

The following table shows qualitative results for the Geosocial Erdős-Rényi Network with all algorithms. Each figure was generated using the same set of 1,000 random locations and the same Geosocial network, but different levels of known locations were used. Similarly to the real-world datasets, the Graph Drawing algorithm improves greatly as more known locations are added. In fact, the figure for the Graph Drawing algorithm with 50 known locations has the highest amount of whitespace out of any of the Erdős-Rényi figures. The random baseline is also observed to have many long links and uniform errors, as expected.

| Known Locations | Random Algorithm | Greedy Algorithm | Partitioning-Based Algorithm | Graph Drawing Algorithm |
|     :---:    |     :---:      |     :---:     |     :---:     |     :---:     |
| 0 | <img src="ExperimentalResults/ErdosReyniImages/ERCorrectDistanceRandomKnown0.png" width="250"/> | <img src="ExperimentalResults/ErdosReyniImages/ERCorrectDistanceGreedyKnown0.png" width="250"> | <img src="ExperimentalResults/ErdosReyniImages/ERCorrectDistancePartitioningKnown0.png" width="250"> | <img src="ExperimentalResults/ErdosReyniImages/ERCorrectDistanceGraphDrawingKnown0.png" width="250"> |
| 3 | <img src="ExperimentalResults/ErdosReyniImages/ERCorrectDistanceRandomKnown3.png" width="250"/> | <img src="ExperimentalResults/ErdosReyniImages/ERCorrectDistanceGreedyKnown3.png" width="250"> | <img src="ExperimentalResults/ErdosReyniImages/ERCorrectDistancePartitioningKnown3.png" width="250"> | <img src="ExperimentalResults/ErdosReyniImages/ERCorrectDistanceGraphDrawingKnown3.png" width="250"> |
| 10 | <img src="ExperimentalResults/ErdosReyniImages/ERCorrectDistanceRandomKnown3.png" width="250"/> | <img src="ExperimentalResults/ErdosReyniImages/ERCorrectDistanceGreedyKnown10.png" width="250"> | <img src="ExperimentalResults/ErdosReyniImages/ERCorrectDistancePartitioningKnown10.png" width="250"> | <img src="ExperimentalResults/ErdosReyniImages/ERCorrectDistanceGraphDrawingKnown10.png" width="250"> |
| 50 | <img src="ExperimentalResults/ErdosReyniImages/ERCorrectDistanceRandomKnown50.png" width="250"/> | <img src="ExperimentalResults/ErdosReyniImages/ERCorrectDistanceGreedyKnown50.png" width="250"> | <img src="ExperimentalResults/ErdosReyniImages/ERCorrectDistancePartitioningKnown50.png" width="250"> | <img src="ExperimentalResults/ErdosReyniImages/ERCorrectDistanceGraphDrawingKnown50.png" width="250"> |

Quanititative results, averaged over thirty trials, for the Geosocial Erdős-Rényi are shown below. For each trial, random locations were used and a new geosocial network was generated everytime. Additionally, new random known locations were used for each trial. We see that for each population, the Graph Drawing algorithm has the best average distance out of all the algorithms in trials with 10 or 50 known locations. For trials with 50 known locations, the average distance of the Graph Drawing algorithm is consistently less than half of the average distances of all other algorithms.

| Population | Known Locations|Algorithm|Number Correct|Average Distance|Runtime (seconds)|Standard Deviation of Average Distances|
|     :---:    |     :---:    |     :---:      |     :---:     |     :---:     |     :---:     |     :---:     |
|100|0|Random|1.1|0.5222|0.0003|0.0307|
|100|0|Greedy|1.6|0.4934|0.0057|0.0694|
|100|0|Partitioning-Based|1.6667|0.4632|415.9714|0.142|
|100|0|Graph Drawing|1.1333|0.5431|0.0593|0.0975|
|100|3|Random|4.5333|0.501|0.0004|0.0272|
|100|3|Greedy|5.8|0.4264|0.0027|0.0783|
|100|3|Partitioning-Based|4.1333|0.5031|423.1631|0.046|
|100|3|Graph Drawing|8.5333|0.3224|0.0587|0.1071|
|100|10|Random|11.5667|0.4629|0.0004|0.0234|
|100|10|Greedy|12.1667|0.4144|0.0028|0.0912|
|100|10|Partitioning-Based|12.4333|0.4162|414.2671|0.1102|
|100|10|Graph Drawing|25.1667|0.1551|0.059|0.0638|
|100|50|Random|51.1333|0.2528|0.0004|0.0201|
|100|50|Greedy|52.5333|0.2085|0.0025|0.0286|
|100|50|Partitioning-Based|51.2333|0.2228|401.6261|0.0496|
|100|50|Graph Drawing|66.5|0.0582|0.0543|0.0108|
|500|0|Random|0.9333|0.5195|0.0028|0.012|
|500|0|Greedy|1.1667|0.502|0.1408|0.0588|
|500|0|Partitioning-Based|5.0|0.3893|422.1444|0.166|
|500|0|Graph Drawing|1.6|0.5244|4.9275|0.1464|
|500|3|Random|4.1667|0.5185|0.0028|0.0145|
|500|3|Greedy|5.0667|0.4698|0.0457|0.0747|
|500|3|Partitioning-Based|8.8667|0.3608|393.7533|0.1843|
|500|3|Graph Drawing|5.6|0.4353|5.2905|0.1354|
|500|10|Random|10.9333|0.508|0.0029|0.0124|
|500|10|Greedy|12.3|0.4557|0.0462|0.0664|
|500|10|Partitioning-Based|13.7667|0.4086|395.2789|0.1798|
|500|10|Graph Drawing|17.2667|0.2357|5.3788|0.0889|
|500|50|Random|50.9|0.4697|0.003|0.0113|
|500|50|Greedy|51.9333|0.4527|0.0509|0.0652|
|500|50|Partitioning-Based|53.7667|0.3421|395.1362|0.1455|
|500|50|Graph Drawing|63.7|0.1309|4.8724|0.0059|
|1000|0|Random|1.0|0.5216|0.0095|0.0095|
|1000|0|Greedy|1.6333|0.5104|0.6366|0.0533|
|1000|0|Partitioning-Based|8.1|0.3301|406.0176|0.1802|
|1000|0|Graph Drawing|1.3333|0.5273|12.4259|0.122|
|1000|3|Random|4.1|0.5191|0.0098|0.0071|
|1000|3|Greedy|5.1|0.4823|0.1982|0.0709|
|1000|3|Partitioning-Based|10.2|0.3824|432.8506|0.1841|
|1000|3|Graph Drawing|5.1|0.4522|13.1301|0.1627|
|1000|10|Random|10.8333|0.5157|0.0097|0.0074|
|1000|10|Greedy|11.9|0.4812|0.1853|0.0621|
|1000|10|Partitioning-Based|15.4667|0.4125|401.1124|0.2068|
|1000|10|Graph Drawing|13.0|0.366|13.1802|0.1193|
|1000|50|Random|51.1|0.4965|0.0101|0.0093|
|1000|50|Greedy|52.8667|0.459|0.1964|0.0706|
|1000|50|Partitioning-Based|56.8667|0.3587|452.2197|0.1832|
|1000|50|Graph Drawing|59.3333|0.1617|12.7328|0.008|

## References
<a id="1">[1]</a> 
M. Bailey, R. Cao, T. Kuchler, J. Stroebel, and A. Wong. Social connectedness: Measurement, determinants, and effects. *Journal of Economic Perspectives*, 32(3):259–280, 2018.

<a id="2">[2]</a> 
Y. Kang, S. Gao, Y. Liang, M. Li, J. Rao, and J. Kruse. Multiscale dynamic human mobility flow dataset in the us during the covid-19 epidemic. *Scientific data*, 7(1):390, 2020.

<a id="3">[3]</a> 
K. Gallagher, T. Anderson, A. Crooks, and A. Züfle. Synthetic geosocial network generation. In *Proceedings of the 7th ACM SIGSPATIAL Workshop on Location-based Recommendations, Geosocial Networks and Geoadvertising*, pages 15–24, 2023.
