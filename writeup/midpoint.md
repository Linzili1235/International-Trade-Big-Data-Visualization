# Midpoint Writeup

## Link to the data
[Original Resource](https://comtrade.un.org/data/)

[Georgetown Box](https://georgetown.box.com/s/y0y066u564g7lgfqxowffoqb9eto3hub)


## World Heat Map

### Import:
![screen shot](/map/import.png)

### Export:
![screen shot](/map/export.png)


### Rationale

The interactive world heatmap shows the magnitude of both import and export trades between USA and the other countries from year 2016 to year 2020 in a form of world map with the color intensity of the country indicating the quantity of import or export. By selecting a speed on the speed slider, it shows the trading pattern in this specific speed. As the time changes, it is clear to see the variance of trading patterns over these years. From the world heatmap, it clearly shows the country having the largest total trade values with USA in each year. China has the largest total trades value with respect to import, and Canada has the largest total trades value with respect to export, since they have center points of the biggest area.

### Data Preprocessing

- Remove rows with `Partner` as `World`
- Convert all country names to 2 digit code and remove the countries with unknown codes
- Collect the location of center point for each country.
- Group data by country, and calculate the sum of trade values.

### Goals Changed

The original goal of this world heatmap is to show the condition of import and export data in one map by using the inward and outward arrows, where outward arrows represent export, and inward arrows stand for import. However, because the countries involve in the international trade with USA is much more than our original imagination. If the map is filled with both inward and outward arrows for each country, then the map will look like a huge mess. Therefore, the final version of the world heatmap splits the import and export, and performs the visualizaiton respectively for better visualization display.


## Treemap

![Screenshot 1](/treemap/proto1.jpg)

![Screenshot 2](/treemap/proto2.jpg)

### Rationale
The treemap is designed to showcase trade value and quantity rankings for all US export commodity categories. The area of each category in the treemap is proportional to its trade value. The color of each category reflects quantity. Since trade value and quantity are both numeric data types, area and color are intuitive ways to encode such continuous variables. 

The quantity for each commodity category is a derived variable. In the original data, there are thousands of sub-categories under 99 root categories, which are featured in the treemap, and only sub-catogories have given quantities. Since the treemap would be uninterpretable if all sub-categories were plotted, only root categories are selected and their quantities are obtained from aggregation of sub-category quantities. In addition, as the quantity variable has a huge range with extreme values, if plotted directly, the resulting treemap would have a majority of categories with similar colors. Then, tt would be difficult to see the difference in quantity. To resolve the issue, the quantity is plotted on a logarithmic scale, which brings all values closer to each other. 

Moreover, tooltip is used to display details about each category when the cursor hovers on it, which contains addition information includes trading year, trading value in US $MM, and log(quantity). Instead of displaying all the information in category boxes directly, showing in a hovering tooltip makes the visualizaiton more concise. 

In terms of visual encoding choices, diverging color encoding is used for the quantity variable, which emphasizes values on both ends of the scale. 

### Data Preprocessing
- Change column names to snake case
- Drop unwanted columns
- Filter desired rows: partner=world and only root categories (commodity code in [1,99]) in this case
- Convert object type columns to numeric
- Aggregation: compute the sum of commodity quantity for all root categories based on quantities of sub-categories
- Rescale quantity and trade value variables
- DONE

### Goals Changed
My original goal was to showcase how trade values are distributed across different commodity catogories using percentage values to represent share in the economy. However, during the making of the prototype, I felt it is better to use absolute trade values because it gives a better sense in terms of the scale of a commodity category. Apart from this, I sticked to my original plan. The current treemap is effective in showing the top commodity categories for US export. 


## Race Bar Chart
![Screenshot](/racebarchart/export.png)

### Rationale
This is a race bar chart with regard to the trade value of different commodity types. The goal of this visualization is to intuitively show the changes of top10 largest categories of commodities, both imported and exported, of the US. Different colors have been assigned to each category to make the trend clearer visually. The names of the commodities shown in the chart have also been simplified from the categories given by original dataset to avoid wordy text. The scale of the trade value is in billions to ensure that there are not too many zeros and enhance visibility.

Matplotlib.animation is utilized in the animation process of the race bar chart. There are three interactive options for this visual: once, loop and reflect. Users can choose flexibly according to their needs. Also there are several play options that can let users either watch the whole animation or view the graphs one by one.

### Data Preprocessing
- Select variables `Commodity Code`, `Commodity` and `Trade Value (US$)` from the huge dataset.
- Change the type of `Commodity Code` from string to int. Note that `Commodity Code` has a value “total”, which refers to the sum trade value of all categories of commodities. Since the focus of the race bar chart is the rank of commodity types, we delete “total” from the dataset and convert it to int.
- Choose the main categories whose `Commodity Code` is from 1 to 99.
- Delete the values "Commodities not specified according to kind" from the `Commodity` column.
- Make abbreviation for the commodity names.

### Goals Changed
The goal of the race bar chart visualization does not change. It communicates the data story in the big picture. However, it does change a little in the way we demonstrate the commodity type. Initially we tried to add small icons to show the categories more vividly, but it turned out that icons could not convey the exact information of the product types. Conveying throught text is a more professional method. Also we add the trade values on the right of the bars to make the visual more scientific.



## Slope Chart

![screen shot](/slopechart/slope_chart.png)


### Rationale

In order to figure out the impact of COVID-19 on international trade, a slope chart is plotted to compare the difference in total amounts of trade value between year 2016 and year 2020 with respect to different kinds of commodity categories. Since both import and export trades are our focus, two slope charts are plotted respectively and put together to compare the tendency for these two types of trades. The Race Bar Chart plotted before also focuses on the change of total amounts of trade value but is more likely to concentrate on the dynamic change year by year, aiming at finding the top 10 popular categories. This slope chart is plotted to help catch the audience's eyes immediately on the change between the beginning and the end year by the slope of each line. Moreover, the color of the slope clearly shows whether the change is positive or negative. Since there are over 90 categories, it is not realistic to plot changes in all categories. Moreover, the most popular categories of commodities are our primary interests. Therefore, we only select the top 8 categories based on the plotting result of the Race Bar Chart and perform the visualization in this slope chart. 

### Data Preprocessing

- Choose a subset of columns including `Year`, `Partner`, `Commodity.Code`, `Commodity`, `Trade.Value..US..`
- Filter the data to keep only the trades between USA and World
- Choose the trades with commodities belonging to the top 8 popular categories found by Race Bar Chart
- Drop missing values

### Goals Changed

The original goal of the slope chart is to plot the slope line for the top 10 categories in one figure. However, because text plays a significant role in this kind of plot and there occurred some overlapping problems among texts for different categories, two categories that tend to be steady from 2016 to 2020 without any obvious change are removed from the original plot for better visualization display. Therefore, the final version of the slope chart only contains the change of 8 categories.


## Radial Network

![screen shot](https://github.com/anly503/project-spring-2022-project-group-10/blob/main/network/screen_shot.png)


### Rationale

The goal of the radial network is to show the top 3 commodity types that each country have for each trade flow with USA from 2016 to 2020. The radial network contains international trade data with USA from 2016 to 2020. Specifically, the graph contains: 

- countries that trade with USA
- trade flow
- commodity type

You could move the mouse on the nodes, and then check the specific countries, their corresponding trade flows and commodity types. You can see that there are only three commodity types for each trade flow. This is because that they are calculated based on the sum of trade values from 2016 and 2020. For each country and each trade flow, commodity types with top 3 trade values will be selected. The nodes are colored pink and links are colored green so that nodes will be easily seen. I tried to set different colors for different links and nodes but R will stuck in the middle and terminate. 

### Data Preprocessing

- Choose column `Year`, `Partner`, `Trade_Flow`, `Trade_Value`, `Commodity`, `Commodity_Code`
- Group data by Partner `Trade_value`, `Trade_Flow` and `Commodity` and sum the `Trade_Value` of all years
- Choose top 3 commodities based on `Trade_Value` for each country and `Trade_Flow`

### Goals Changed

The original goal of the radial network is to give an innovative view of the original data. From the radial network, people should be able to zoom in and hover over the specific country. Moreover, there should be a control bar that will show the year change of the network.  

However, the problem is that for radial network function in networkD3, there is no way of zooming and hover. According to the source code of [radialNetwork](https://rdrr.io/cran/networkD3/man/radialNetwork.html) function, there is no 'zoom' option. Moreover, this vis type cannot be combined with igraph or other libraries. I tried to use other libraries like igraph to do network viz, but they all are not as tidy as the radialNetwork does in networkD3. Moreover, the radialNetwork cannot be combined with plot_ly, which leads to the result that i couldn't put two radialNetworks in one graph and I couldn't set a control bar.

Therefore, I finally chose to draw one graph that represent the overall situation of five years. As there are a lot of information, I set bigger font size for the nodes. The viewers can still find the information that they want. From the graph, viewers can choose the countries that they want to study, then lead to the top commodity types the country traded with USA. Then the viewers can reach to the conclusion that which industry that the country developed well and which industry got bad performance from 2016 to 2020. 

