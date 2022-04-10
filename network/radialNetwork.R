library(networkD3)
library(igraph)
library(data.table)
library(data.tree)
library(treemap)
library(visNetwork)
library(data.tr)
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

#commoDity = unique(Grouped_data$Commodity_Code)
#tradetop <- read.csv('tradetop10.csv')
#CommodiTy = unique(tradetop$Commodity.Code)
#intersect(commoDity,CommodiTy)

# vis code
Grouped_data$pathString = paste('USA',Grouped_data$Partner,
                              Grouped_data$Trade_Flow_Code,Group_data$Commodity,
                              sep = '/')
population = as.Node(Grouped_data)
population = as.list(population, mode = 'explicit', unname = T)

#network_vector <- lapply(list(nodeVector,linkVector,textVector), function(j) {
#  JS(paste0('function(d, i) { return ',paste0('["', 
#                                              paste(j, 
#                                                    collapse = '", "'),
#                                              '"]'), '[i]; }'))
#})

a = radialNetwork(List = population, fontSize =18, opacity = 0.9,
                   height = 3000, width = 3000,linkColour = 'seagreen',
              nodeColour = 'pink'
                 )%>%saveNetwork('radk.html', selfcontained = T)

#dt1 = DataF_2016[1:2]
#dt2 = distinct(DataF_2016[2:3])
#dt3 = DataF_2016[3:4]
#names(dt1) = c('source','target')
#names(dt2) = c('source','target')
#names(dt3) = c('source', 'target')
#EXP = rbind(dt1,dt2,dt3)

#simpleNetwork(EXP,zoom = T,height = 1000,width = 1000)%>%saveNetwork('what.html', selfcontained = T)%>%saveNetwork('afk.html', selfcontained = T)

#dt1 = unique(DataF_2016[1])
#dt2 = unique(DataF_2016[2])
#dt3 = unique(DataF_2016[3])
#dt4 = unique(DataF_2016[4])
#names(dt1) = c('source')
#names(dt2) = c('source')
#names(dt3) = c('source')
#names(dt4) = c('source')

#Nodes = rbind(dt1,dt2,dt3,dt4) 
#nodes <- data.frame(id = Nodes$source)
#edges <- data.frame(from = EXP$source, to = EXP$target)
#visNetwork(nodes,edges,height = 1000,width = 1000)%>%
#  visOptions(highlightNearest = T,nodesIdSelection = T)%>%saveNetwork('what.html', selfcontained = T)



#rsplit <- function(x) {
#  x <- x[!is.na(x[,1]),,drop=FALSE]
#  if(ncol(x)==1) return(lapply(x[,1], function(v) list(name=v)))
#  s <- split(x[,-1, drop=FALSE], x[,1])
# unname(mapply(function(v,n) {if(!is.null(v)) list(name=n, children=v) else list(name=n)}, lapply(s, rsplit), names(s), SIMPLIFY=FALSE))
#}








#nodeVector <- c('black', rep('green',length(unique(DataF_2016$Partner))),
#                rep('blue',length(dim(DataF_2016)[1]/3)),
#                rep('yellow',length(dim(DataF_2016)[1]))
#)
#linkVector <- c(rep("seagreen", length(unique(DataF_2016$Partner))), 
#                rep("blue", length(dim(DataF_2016)[1]/3)),
#                rep("#66bd63", length(dim(DataF_2016)[1]))
#)
#textVector <- c("black", 
#                rep("#01665e", ,length(unique(DataF_2016$Partner))),
#                rep("#66bd63", length(dim(DataF_2016)[1]/3)),
#                rep('seagreen',length(dim(DataF_2016)[1])))

#dd<-structure(list(Country = c("Canada", "Canada", "Canada", "Canada", 
#                               "Canada", "Canada", "Canada", "Canada", "Canada", "Canada"), 
#                   Provinces = c("Newfondland", "PEI", "Nova Scotia", "New Brunswick", 
#                                "Quebec", "Quebec", "Ontario", "Ontario", "Manitoba", "Saskatchewan"
#                   ), City = c("St Johns", "Charlottetown", "Halifax", "Fredericton", 
#                               NA, "Quebec City", "Toronto", "Ottawa", "Winnipeg", "Regina"
#                   ), Zone = c("A", "B", "C", "D", NA, NA, "A", "B", "C", 
#                               "D")), class = "data.frame", row.names = c(NA, -10L), .Names = c("Country", 
#                                                                                                "Provinces", "City", "Zone"))
#dd
#k = rsplit(dd)
#radialNetwork(List = k[[1]],fontSize = 5, opacity = 0.9)
#k[[1]]


#Grouped_data <- DataF%>% group_by(Year, Trade_Flow_Code, Partner)
#Group_Data <- DataF %>% arrange(desc(Trade_Value)) %>%
#  group_by(Year, Trade_Flow_Code, Partner)%>%slice(1:3)

#DataF_2016 = Group_Data[Group_Data$Year=='2016',]
#DataF_2016 = subset(DataF_2016, select = -c(Trade_Value,Year,Commodity_Code))
#DataF_2016$Root = rep('USA',dim(DataF_2016)[1])
#DataF_2016 = DataF_2016[,c(4,2,1,3)]
#DataF_2016 = DataF_2016%>%arrange(Partner)










