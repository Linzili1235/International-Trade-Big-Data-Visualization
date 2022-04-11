# Midpoint Writeup

## Link to the data
[Original Resource](https://comtrade.un.org/data/)

[Georgetown Box](https://georgetown.box.com/s/y0y066u564g7lgfqxowffoqb9eto3hub)

## Treemap
### Rationale
The treemap is designed to showcase trade value and quantity rankings for all US export commodity categories. The area of each category in the treemap is proportional to its trade value. The color of each category reflects quantity. Since trade value and quantity are both numeric data types, area and color are intuitive ways to encode such continuous variables. 

The quantity for each commodity category is a derived variable. In the original data, there are thousands of sub-categories under 99 root categories, which are featured in the treemap, and only sub-catogories have given quantities. Since the treemap would be uninterpretable if all sub-categories were plotted, only root categories are selected and their quantities are obtained from aggregation of sub-category quantities. In addition, as the quantity variable has a huge range, the resulting treemap would have categories so small that could be hardly seen if plotted directly. To resolve the issue, the quantity is plotted on a logarithmic scale. 

Moreover, tooltip is used to display details about each category when the cursor hovers on it, which contains addition information includes trading year, trading value in US $MM, and log(quantity). Instead of displaying all the information in category boxes directly, showing in a hovering tooltip makes the visualizaiton more concise. 

In terms of visual encoding choices, diverging color encoding is used for the quantity variable, which emphasizes values on both ends of the scale. 

### Vision and goals
My original goal was to showcase how trade values are distributed across different commodity catogories using percentage values to represent share in the economy. However, during the making of the prototype, I felt it is better to use absolute trade values because it gives a better sense in terms of the scale of a commodity category. Apart from this, I sticked to my original plan. The current treemap is effective in showing the top commodity categories for US export. 

### Data preprocessing pipeline
1. Change column names to snake case
2. Drop unwanted columns
3. Filter desired rows: partner=world and only root categories (commodity code in [1,99]) in this case
4. Convert object type columns to numeric
5. Aggregation: compute the sum of commodity quantity for all root categories based on quantities of sub-categories
6. Rescale quantity and trade value variables
7. DONE

### Prototype illustration
![Screenshot 1](/treemap/proto1.jpg)

![Screenshot 2](/treemap/proto2.jpg)



## Radial Network

![screen shot](https://github.com/anly503/project-spring-2022-project-group-10/blob/main/network/screen_shot.png)


### Rationales

The radial network contains international trade data with USA from 2016 to 2020. Specifically, the graph contains: 

- countries that trade with USA
- trade flow
- commodity type

You could move the mouse on the nodes, and then check the specific countries, their corresponding trade flows and commodity types. You can see that there are only three commodity types for each trade flow. This is because that they are calculated based on the sum of trade values from 2016 and 2020. For each country and each trade flow, commodity types with top 3 trade values will be selected. The nodes are colored pink and links are colored green so that nodes will be easily seen. I tried to set different colors for different links and nodes but R will stuck in the middle and terminate. 

### Data Preprocessing

- Choose column Year, Partner, Trade_Flow, Trade_Value, Commodity, Commodity_Code
- Group data by Partner Trade_value,Trade_Flow and Commodity and sum the trade_value of all years
- Choose top 3 commodities based on trade_value for each country and Trade_Flow

### Goals changed

The original goal of the radial network is to give an innovative view of the original data. From the radial network, people should be able to zoom in and hover over the specific country. Moreover, there should be a control bar that will show the year change of the network.  

However, the problem is that for radial network function in networkD3, there is no way of zooming and hover. According to the source code of [radialNetwork](https://rdrr.io/cran/networkD3/man/radialNetwork.html) function, there is no 'zoom' option. Moreover, this vis type cannot be combined with igraph or other libraries. I tried to use other libraries like igraph to do network viz, but they all are not as tidy as the radialNetwork does in networkD3. Moreover, the radialNetwork cannot be combined with plot_ly, which leads to the result that i couldn't put two radialNetworks in one graph and I couldn't set a control bar.

Therefore, I finally chose to draw one graph that represent the overall situation of five years. As there are a lot of information, I set bigger font size for the nodes. The viewers can still find the information that they want. From the graph, viewers can choose the countries that they want to study, then lead to the top commodity types the country traded with USA. Then the viewers can reach to the conclusion that which industry that the country developed well and which industry got bad performance from 2016 to 2020. 



## Slope Chart

![screen shot](https://github.com/anly503/project-spring-2022-project-group-10/blob/main/`slope chart`/slope_chart.png)


### Rationales

The slope chart contains international trade data with USA from 2016 to 2020. Specifically, the graph contains: 

- countries that trade with USA
- trade flow
- commodity type

You could move the mouse on the nodes, and then check the specific countries, their corresponding trade flows and commodity types. You can see that there are only three commodity types for each trade flow. This is because that they are calculated based on the sum of trade values from 2016 and 2020. For each country and each trade flow, commodity types with top 3 trade values will be selected. The nodes are colored pink and links are colored green so that nodes will be easily seen. I tried to set different colors for different links and nodes but R will stuck in the middle and terminate. 

### Data Preprocessing

- Choose column Year, Partner, Trade_Flow, Trade_Value, Commodity, Commodity_Code
- Group data by Partner Trade_value,Trade_Flow and Commodity and sum the trade_value of all years
- Choose top 3 commodities based on trade_value for each country and Trade_Flow

### Goals changed

The original goal of the radial network is to give an innovative view of the original data. From the radial network, people should be able to zoom in and hover over the specific country. Moreover, there should be a control bar that will show the year change of the network.  

However, the problem is that for radial network function in networkD3, there is no way of zooming and hover. According to the source code of [radialNetwork](https://rdrr.io/cran/networkD3/man/radialNetwork.html) function, there is no 'zoom' option. Moreover, this vis type cannot be combined with igraph or other libraries. I tried to use other libraries like igraph to do network viz, but they all are not as tidy as the radialNetwork does in networkD3. Moreover, the radialNetwork cannot be combined with plot_ly, which leads to the result that i couldn't put two radialNetworks in one graph and I couldn't set a control bar.

Therefore, I finally chose to draw one graph that represent the overall situation of five years. As there are a lot of information, I set bigger font size for the nodes. The viewers can still find the information that they want. From the graph, viewers can choose the countries that they want to study, then lead to the top commodity types the country traded with USA. Then the viewers can reach to the conclusion that which industry that the country developed well and which industry got bad performance from 2016 to 2020. 



