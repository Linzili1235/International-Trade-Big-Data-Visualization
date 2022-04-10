import plotly.express as px
import seaborn as sns
import pandas as pd
import numpy as np
import re
pd.set_option("display.max_rows", None)

# Load data
dat_exp16 = pd.read_csv("./data/USA_ALL_export_2016_allproduct.csv")

############## Data munging ##############

# Change column names to snake case
col_names = dat_exp16.head()
pattern = re.compile(r"[( -.)]")
new_names = []
for name in col_names:
    new_names.append(pattern.sub("_", name).lower())
# print(new_names)
dat_exp16.columns = new_names

# Drop unwanted columns
dat_exp16 = dat_exp16.drop([
    "classification",
    "period",
    "period_desc_",
    "aggregate_level",
    "is_leaf_code",
    "trade_flow",
    "reporter_iso",
    "2nd_partner_code",
    "2nd_partner",
    "2nd_partner_iso",
    "customs_proc__code",
    "customs",
    "mode_of_transport_code",
    "mode_of_transport",
    "alt_qty_unit_code",
    "alt_qty_unit",
    "alt_qty",
    "gross_weight__kg_",
    "cif_trade_value__us__",
    "flag",
    "netweight__kg_",
    "qty_unit_code"
],axis=1)
# print(dat_exp16.head(10))

dat_exp16_lit = dat_exp16.drop(dat_exp16.columns[[1,2,3,4,6]], axis = 1)
# print(dat_exp16_lit.head(10))

# World data
dat_exp16_world = dat_exp16_lit.loc[dat_exp16_lit['partner'] == 'World']
# Drop last row (Total)
dat_exp16_world.drop(dat_exp16_world.tail(1).index,inplace=True)
# Convert object to int
dat_exp16_world["commodity_code"] = dat_exp16_world.commodity_code.astype(np.int64)
dat_exp16_world["qty"] = dat_exp16_world.qty.astype(np.float64)

# Compute the sum of commodity quantity for all root categories
dat_exp16_w_temp = dat_exp16_world.loc[dat_exp16_world['commodity_code'] > 10000]
dat_exp16_w_temp["commodity_code"] = dat_exp16_w_temp["commodity_code"]/10000
dat_exp16_w_temp.commodity_code = dat_exp16_w_temp.commodity_code.round()
# print(dat_exp16_w_temp.head(10))
# print(dat_exp16_w_temp.commodity_code.unique())
qty_sum = dat_exp16_w_temp.groupby(['commodity_code',"year"])['qty','trade_value__us__','fob_trade_value__us__'].sum()
qty_sum = qty_sum.reset_index()

# Sub sum into World dataset
dat_exp16_w  = dat_exp16_world.loc[dat_exp16_world['commodity_code'] < 100]
dat_exp16_w = dat_exp16_w.reset_index()
dat_exp16_w.drop(["qty"],axis=1,inplace=True)

# Drop all rows with either 0 qty or trade value
dat_exp16_w["qty"]=qty_sum["qty"]
dat_exp16_w = dat_exp16_w[(dat_exp16_w[['trade_value__us__','qty']] != 0).all(axis=1)]

# Rescale column quantity
dat_exp16_w["qty"]=np.log(dat_exp16_w["qty"])

# print(len(qty_sum), len(dat_exp16_w))


# print(dat_exp16_w.tail())
# print(dat_exp16_w.dtypes)

# Sort
dat_exp16_w.sort_values(by=['trade_value__us__'], ascending=False, inplace=True)
dat_exp16_w=dat_exp16_w.reset_index()
print(dat_exp16_w)

# exit()

# Plot the treemap
# df = dat_exp16_w
dat_exp16_w["world"] = "Commodity Categories"  # in order to have a single root node
fig = px.treemap(
    dat_exp16_w,
    path=["world", "commodity"],  # << sets hierarchy
    values="trade_value__us__",
    color="qty",
    # hover_data=["year"],
    color_continuous_scale="RdBu",
    color_continuous_midpoint=np.average(dat_exp16_w["qty"]),
    labels={"qty":"Log(quantity"},
)
year = dat_exp16_w.year.tolist()
quantity = dat_exp16_w.qty.tolist()
fig.data[0].customdata = np.column_stack([year, quantity])
fig.data[0].hovertemplate = 'Category = %{label}<br>Year = %{customdata[0]}<br>Trade value(US$) = %{value}<br>Quantity = %{customdata[1]}'
fig.show()
