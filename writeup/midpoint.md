# Midpoint Writeup

## Link to the data
**Original Resource**
**Georgetown Box** 
https://georgetown.box.com/s/y0y066u564g7lgfqxowffoqb9eto3hub

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
