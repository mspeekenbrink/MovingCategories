dataFolder <- "~/Documents/GitHub/MovingCategories/Data/"

readDat <- function(files) {
  alldata <- vector()
  for(f in files) {
    tmp <- strsplit(readLines(f,1),"; ")
    id <- strsplit(tmp[[1]][1]," = ")[[1]][2]
    sex <- strsplit(tmp[[1]][2]," = ")[[1]][2]
    age <- strsplit(tmp[[1]][3]," = ")[[1]][2]
    condition <- strsplit(tmp[[1]][4]," = ")[[1]][2]
    responseOrder <- strsplit(tmp[[1]][5]," = ")[[1]][2]
    featureOrder <- strsplit(tmp[[1]][6]," = ")[[1]][2]
    fname <- strsplit(f,"//")[[1]][2]
    fname <- strsplit(fname,".csv")[[1]]
    date <- substring(fname,nchar(id)+1)
    dat <- read.csv(f,skip=1,header=TRUE)
    dat$id <- id
    dat$condition <- condition
    dat$date <- date
    dat$sex <- sex
    dat$age <- age
    dat$responseOrder <- responseOrder
    dat$featureOrder <- featureOrder
    alldata <- rbind(alldata,dat)
  }
  alldata <- alldata[,c(8:14,1:7)]
  alldata$time <- alldata$time * 1000
  alldata$id <- factor(as.numeric(alldata$id))
  alldata$condition <- factor(alldata$condition,labels=c("StartWithRule","StartWithII"))
  alldata$sex <- factor(alldata$sex)
  alldata$age <- as.numeric(alldata$age)
  alldata <- alldata[order(as.numeric(as.character(alldata$id)),alldata$trial),]
  return(alldata)
}
files <- list.files(path=dataFolder,pattern="*.csv",full.names=TRUE)
MovingCat <- readDat(files)
#write.csv(MovingCat,file="~/Documents/GitHub/MovingCategories/MovingCat.csv",row.names=FALSE)
