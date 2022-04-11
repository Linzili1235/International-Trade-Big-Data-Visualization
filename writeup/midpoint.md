## Treemap
* **Data preprocessing pipeline**
    1. Change column names to snake case
    2. Drop unwanted columns
    3. Filter desired rows: partner=world and only root categories (Commodity code in [1,99]) in this case
    4. Convert object type columns to numeric
    5. Aggregation: compute the sum of commodity quantity for all root categories based on quantities of sub-categories
    6. Rescale quantity and trade value variables
    7. DONE