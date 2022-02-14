packages = c("xesreadR", "devtools",
             "xml2")

## Now load or install&load all
package.check <- lapply(
  packages,
  FUN = function(x) {
    if (!require(x, character.only = TRUE)) {
      install.packages(x,repos = "http://cran.us.r-project.org", dependencies = TRUE)
      library(x, character.only = TRUE)
    }
  }
)

devtools::install_github("bergant/bpmn")
library(bpmn)



args = commandArgs(trailingOnly=TRUE)
logPath= args[1]
bpmnPath=paste(logPath,".bpmn",sep="")
xesPath=paste(logPath,".xes",sep="")
print(bpmnPath)
print(xesPath)

#bpmnPath=file.choose()
#xesPath=file.choose()


bpmnModel=bpmnPath
elemen <- bpmn_get_elements(read_xml(bpmnModel))
print("hola")


logFile=read_xes(xesfile = xesPath, validate = TRUE)


df=as.data.frame(logFile)
activities=unique(logFile$activity_id)
activities=as.list(activities)
activitiesNames=c()

resourcesN=unique(logFile$resource_id)
resourcesN=resourcesN[]
resourcesN=as.list(resourcesN)
resourcesNames=c()

for( i in 1:length(resourcesN)){
  if( !(as.character(resourcesN[i][[1]])=='Start' && as.character(resourcesN[i][[1]])=='End') ){
  resourcesNames=rbind(resourcesNames, as.character(resourcesN[i][[1]]))
  }
   
}

for( i in 1:length(activities)){
  if( !(as.character(activities[i][[1]])=='Start' && as.character(activities[i][[1]])=='End') ){
  activitiesNames=rbind(activitiesNames, as.character(activities[i][[1]]))
  }
}

matrizProbabilidades=matrix(data=rep(0,length(resourcesNames)*length(activitiesNames)),ncol=length(resourcesNames), nrow = length(activitiesNames))
colnames(matrizProbabilidades)=resourcesNames
rownames(matrizProbabilidades)=activitiesNames
for(i in activitiesNames){
  for(j in resourcesNames){
    matrizProbabilidades[i,j]=length(subset(df,df$activity_id==i & df$lifecycle_id=='complete' & df$resource_id==j)[,1])
  }
}


write.csv(matrizProbabilidades, paste(logPath,"_incidenceMatrix.csv",sep=""))

