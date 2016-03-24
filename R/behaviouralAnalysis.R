source("~/Documents/GitHub/MovingCategories/R/readData.R")

MovingCat$sblock <- cut(MovingCat$trial,breaks=seq(0,701,by=50))
MovingCat$lblock <- cut(MovingCat$trial,breaks=seq(0,701,by=100))

ttime <- MovingCat$time
MovingCat$time[ttime > mean(ttime) + 3*sd(ttime) | ttime < mean(ttime) - 3*sd(ttime)] <- NA



require(ggplot2)
ggplot(MovingCat,aes(x=sblock,y=correct,colour=condition)) +  stat_summary(fun.y = mean, geom="point",size=3)

ggplot(MovingCat,aes(x=sblock,y=time,colour=condition)) +  stat_summary(fun.y = mean, geom="point",size=3)


require(car)
require(reshape2)
mdat <- melt(MovingCat,measure.vars=c("correct","time"))
wdat <- dcast(mdat,id + condition ~ variable + lblock,mean,na.rm=TRUE)
write.csv(wdat,file="~/Documents/GitHub/MovingCategories/ForSPSS.csv",row.names=FALSE)

### Correct responses
mdat <- melt(MovingCat,measure.vars="correct")
wdat <- dcast(mdat,id + condition ~ lblock + variable,mean)
idata <- data.frame(block = factor(levels(mdat$lblock)))
y <- as.matrix(wdat[,-c(1:2)])
mod.cor <- lm(y~wdat$condition)
aov.cor <- Anova(mod.cor,idata=idata,idesign=~block,type="III")
summary(aov.cor,multivariate=FALSE)

### Response time
mdat <- melt(MovingCat,measure.vars="time")
wdat <- dcast(mdat,id + condition ~ lblock + variable,mean)
idata <- data.frame(block = factor(levels(mdat$lblock)))
y <- as.matrix(wdat[,-c(1:2)])
mod.cor <- lm(y~wdat$condition)
aov.cor <- Anova(mod.cor,idata=idata,idesign=~block,type="III")
summary(aov.cor,multivariate=FALSE)


require(depmixS4)
Rdat <- subset(MovingCat,condition=="StartWithRule")
Idat <- subset(MovingCat,condition=="StartWithII")

Rdat$logtime <- log(Rdat$time)
Rmod <- depmix(list(response~x1+x2,time~x1+x2),data=Rdat,ntimes=rep(699,11),family=list(binomial(link="probit"),gaussian()),nstates=2)
fRmod <- fit(Rmod)


rModels <- list(
  list(
    GLMresponse(formula=correct~x2,data=Rdat,family=binomial()),
    GLMresponse(formula=logtime~1,data=Rdat,family=gaussian())
  ),
  list(
    GLMresponse(formula=correct~x1+x2,data=Rdat,family=binomial()),
    GLMresponse(formula=logtime~1,data=Rdat,family=gaussian())
  ),list(
    GLMresponse(formula=correct~x1+x2,data=Rdat,family=binomial()),
    GLMresponse(formula=logtime~1,data=Rdat,family=gaussian())
  )
)


trstart=c(0.9,0.05,0.05,0.05,0.90,.05,.05,.05,.9)
transition <- list()
transition[[1]] <- transInit(~1,nstates=3,data=data.frame(1),pstart=c(trstart[1:3]))
transition[[2]] <- transInit(~1,nstates=3,data=data.frame(1),pstart=c(trstart[4:6]))
transition[[3]] <- transInit(~1,nstates=3,data=data.frame(1),pstart=c(trstart[7:9]))
instart <- c(.05,.9,.05)
inMod <- transInit(~1,ns=3,data=data.frame(rep(1,11)),family=multinomial("identity"),ps=instart)
Rmod <- makeDepmix(response=rModels,transition=transition,prior=inMod,
                  ntimes=rep(699,11),homogeneous=TRUE)
fRmod <- fit(Rmod,emc=em.control(random=FALSE))