library(networkD3)
library(igraph)
library(data.table)
library(data.tree)
library(treemap)
library(visNetwork)
library(data.tree)
library(stringi)
library(dplyr)
library(plotly)
# read in data
setwd('/Users/linzili1235/Desktop/graduate/503/project')
filenames <- list.files("proj_data", pattern = '*.csv', full.names = T)
ldf <- lapply(filenames, fread,select = c('Year','Trade Flow Code',
                                          'Partner', 'Commodity Code', 
                                          'Commodity', 'Trade Value (US$)'))
# Pick columns that will be used
for (i in c(1:length(ldf))){
  names(ldf[[i]]) = c('Year','Trade_Flow_Code',
                      'Partner', 'Commodity_Code', 
                      'Commodity', 'Trade_Value')
  ldf[[i]]$nchart = stri_length(ldf[[i]]$Commodity_Code)
  ldf[[i]] = ldf[[i]][ldf[[i]]$nchart == 2,]
  ldf[[i]] = ldf[[i]][!ldf[[i]]$Partner=='World',]}

# change trade flow code to more readable steps
for (i in c(1:5)){
  ldf[[i]]$Trade_Flow_Code = rep('export',dim(ldf[[i]])[1])
}
for (i in c(6:length(ldf))){
  ldf[[i]]$Trade_Flow_Code = rep('import', dim(ldf[[i]])[1])
}

# combine files of different years
DataF = ldf[[1]]
for (i in c(2:length(ldf))){
  DataF <- rbind(DataF,ldf[[i]])
}

#group data and find the top3 commodity of each country and trade flow
DataF <- subset(DataF, select = -c(nchart))
Grouped_data <- DataF%>%group_by(Partner,Trade_Flow_Code,Commodity)%>%
  summarise(Freq = sum(Trade_Value))
Grouped_data<-Grouped_data%>%arrange(desc(Freq))%>%
  group_by(Trade_Flow_Code, Partner)%>%slice(1:3)



# change the data type to list
Grouped_data$pathString = paste('USA',Grouped_data$Partner,
                              Grouped_data$Trade_Flow_Code,Group_data$Commodity,
                              sep = '/')
population = as.Node(Grouped_data)
population = as.list(population, mode = 'explicit', unname = T)

a = radialNetwork(List = population, fontSize =18, opacity = 0.9,
                   height = 3000, width = 3000,linkColour = 'seagreen',
              nodeColour = 'pink'
                 )%>%saveNetwork('radk.html', selfcontained = T)
















