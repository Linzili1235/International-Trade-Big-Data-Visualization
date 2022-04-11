# Midpoint Writeup

## Treemap
### Rationale
The treemap is designed to showcase trade value and quantity rankings for all US export commodity categories. The area of each category in the treemap is proportional to its trade value. The color of each category reflects quantity. Since trade value and quantity are both numeric data types, area and color are intuitive ways to encode such continuous variables. 

The quantity for each commodity category is a derived variable. In the original data, there are thousands of sub-categories under 99 root categories, which are featured in the treemap, and only sub-catogories have given quantities. Since the treemap would be uninterpretable if all sub-categories were plotted, only root categories are selected and their quantities are obtained from aggregation of sub-category quantities. 

The 

### Data preprocessing pipeline
1. Change column names to snake case
2. Drop unwanted columns
3. Filter desired rows: partner=world and only root categories (Commodity code in [1,99]) in this case
4. Convert object type columns to numeric
5. Aggregation: compute the sum of commodity quantity for all root categories based on quantities of sub-categories
6. Rescale quantity and trade value variables
7. DONE

### Prototype illustration
![Screenshot 1](treemap/proto1.jpg)

![Screenshot 2](treemap/proto2.jpg)