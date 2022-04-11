# Radial Network

![screen shot](https://github.com/anly503/project-spring-2022-project-group-10/blob/main/network/screen_shot.png)


## Rationales

The radial network contains international trade data with USA from 2016 to 2020. Specifically, the graph contains: 

- countries that trade with USA
- trade flow
- commodity type

You could move the mouse on the nodes, and then check the specific countries, their corresponding trade flows and commodity types. You can see that there are only three commodity types for each trade flow. This is because that they are calculated based on the sum of trade values from 2016 and 2020. For each country and each trade flow, commodity types with top 3 trade values will be selected. The nodes are colored pink and links are colored green so that nodes will be easily seen. I tried to set different colors for different links and nodes but R will stuck in the middle and terminate. 
## Data

[original data](https://comtrade.un.org/data/)

## Data Preprocessing

- Choose column Year, Partner, Trade_Flow, Trade_Value, Commodity, Commodity_Code
- Group data by Partner Trade_value,Trade_Flow and Commodity and sum the trade_value of all years
- Choose top 3 commodities based on trade_value for each country and Trade_Flow

## Goals changed

The original goal of the radial network is to give an innovative view of the original data. From the radial network, people should be able to zoom in and hover over the specific country. Moreover, there should be a control bar that will show the year change of the network.  

However, the problem is that for radial network function in networkD3, there is no way of zooming and hover. According to the source code of [radialNetwork](https://rdrr.io/cran/networkD3/man/radialNetwork.html) function, there is no 'zoom' option. Moreover, this vis type cannot be combined with igraph or other libraries. I tried to use other libraries like igraph to do network viz, but they all are not as tidy as the radialNetwork does in networkD3. Moreover, the radialNetwork cannot be combined with plot_ly, which leads to the result that i couldn't put two radialNetworks in one graph and I couldn't set a control bar.

Therefore, I finally chose to draw one graph that represent the overall situation of five years. As there are a lot of information, I set bigger font size for the nodes. The viewers can still find the information that they want. From the graph, viewers can choose the countries that they want to study, then lead to the top commodity types the country traded with USA. Then the viewers can reach to the conclusion that which industry that the country developed well and which industry got bad performance from 2016 to 2020. 


