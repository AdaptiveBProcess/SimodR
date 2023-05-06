
#devtools::install_github("bergant/bpmn")

packages = c("xesreadR", "datastructures",
             "devtools","xml2")

## Now load or install&load all
package.check <- lapply(
  packages,
  FUN = function(x) {
    if (!require(x, character.only = TRUE)) {
      install.packages(x, repos = "http://cran.rstudio.com", dependencies = TRUE, INSTALL_opts = c('--no-lock'))
      library(x, character.only = TRUE)
    }
  }
)

#devtools::install_github("bergant/bpmn")
library(bpmn)

args = commandArgs(trailingOnly=TRUE)
logPath= args[1]
bpmnPath=paste(logPath,".bpmn",sep="")
xesPath=paste(logPath,".xes",sep="")

bpmnModel=file.choose()
logFile=read_xes(xesfile = file.choose(), validate = TRUE)

bpmnModel=bpmnPath
insertSource("modified_bpmn_get_elements.R", package = "bpmn", functions = "bpmn_get_elements")

elements <- bpmn_get_elements(read_xml(bpmnModel))
logFile=read_xes(xesfile = xesPath, validate = TRUE)

#Escanear BPMN
#Why isn't working? bpmn_file <- system.file("qr-code.bpmn", package = "bpmn")


#sourceRef=xml2::xml_attr(elements_xml, attr = "sourceRef"),
#targetRef=xml2::xml_attr(elements_xml, attr = "targetRef"),
#elements <- bpmn_get_elements(read_xml(bpmnModel))

listaArcosTaskFirst=data.frame()
listaArcosTaskLast=data.frame()
listaArcosEfectivos=list()



listaArcos <- subset(elements, type=='sequenceFlow',
                  select=c('id', 'sourceRef', 'targetRef'))
resourcesNumber=0
resourcesN=c()
for(resource in unique(logFile$resource_id)){
  
  if(resource != 'Start' && resource!='End'){
    resourcesNumber=resourcesNumber+1
    resourcesN[resourcesNumber]=resource
  }
  
}

resourcesN=as.list(resourcesN)
resourcesNames=c()
length(resourcesN)
for( i in 1:length(resourcesN)){
  resourcesNames=rbind(resourcesNames, as.character(resourcesN[i][[1]]))
}




#Dice si un nodo es un gateWay
isGateway<-function(idNodo){
  indiceNodo=which(elements$id==idNodo)

  if(elements[indiceNodo,'type']=='exclusiveGateway' || elements[indiceNodo,'type']=='parallelGateway'){
    return(TRUE)
  }
  else{
  return(FALSE)
  }
  
}
#Dice si un nodo es un start/end
isTerminal<-function(idNodo){
  indiceNodo=which(elements$id==idNodo)

  if(elements[indiceNodo,'type']=='startEvent' || elements[indiceNodo,'type']=='endEvent'){
    return(TRUE)
  }
  else{
    return(FALSE)
  }
  
}

#Dice si un nodo es task
isTask<-function(idNodo){
  indiceNodo=which(elements$id==idNodo)

  if(elements[indiceNodo,'type']=='task'){
    return(TRUE)
  }
  else{
    return(FALSE)
  }
  
}
#Retorna los vecinos para un nodo dado
getVecinos<-function(actual){
  
  listaVecinos=list()
  for(i in 1:length(listaArcosTaskLast[,1])){
    
    
    if(listaArcosTaskLast[i,'sourceRef']==actual){
      
      listaVecinos=rbind(listaVecinos,listaArcosTaskLast[i,'targetRef'])
      
    }
    
  }
  return(listaVecinos)
}




#Creaci�n de matriz de actividades
for(i in 1:length(listaArcos[,1])){
  if(isTask(listaArcos[i,'sourceRef']) && isTask(listaArcos[i,'targetRef']) ){
    
    #activities[listaArcos[i,'sourceRef'],listaArcos[i,'sourceRef']]=matrix(rep(0,(resurcesNumber*resourcesNumber)),ncol=resourcesNumber)
    
    matrizCooperacion=matrix(rep(0,(resourcesNumber*resourcesNumber)),ncol=resourcesNumber)
    colnames(matrizCooperacion)=resourcesNames
    rownames(matrizCooperacion)=resourcesNames
    
  
    if(!is.na(listaArcos[i,'sourceRef']) && !is.na(listaArcos[i,'targetRef']) && listaArcos[i,'sourceRef']!='NA' && listaArcos[i,'targetRef']!='NA' && listaArcos[i,'sourceRef']!='' && listaArcos[i,'targetRef']!=''){
     
      assign(paste(listaArcos[i,'sourceRef'],listaArcos[i,'targetRef'],sep='::'),matrizCooperacion) 
    
      listaArcosEfectivos=rbind(listaArcosEfectivos,paste(listaArcos[i,'sourceRef'],listaArcos[i,'targetRef'],sep='::'))
    
      }
    
    }
  else if(isTask(listaArcos[i,'sourceRef'])){
    
    listaArcosTaskFirst=rbind(listaArcosTaskFirst,listaArcos[i,])
    #listaArcosTaskFirst[listaArcos[i,'id'],]=listaArcos[i,]
    
  }
  else{
    listaArcosTaskLast=rbind(listaArcosTaskLast,listaArcos[i,])
   # listaArcosTaskLast[listaArcos[i,'id'],]=listaArcos[i,]
  }
}



for(j in 1:length(listaArcosTaskFirst[,1])){
  nodeStack=stack()
  #for(k in 1:length(listaArcosTaskFirst[,'targetRef'])){
    nodeStack<-insert(nodeStack,listaArcosTaskFirst[j,'targetRef'])
  
  
  while (size(nodeStack)>0) {
 
    actual=pop(nodeStack)
    
    
    if(isTask(actual)){
      #activities[listaArcosTaskFirst[j,'sourceRef'],actual]=matrix(rep(0,(resurcesNumber*resourcesNumber)),ncol=resourcesNumber)
      matrizCooperacion=matrix(rep(0,(resourcesNumber*resourcesNumber)),ncol=resourcesNumber)
      colnames(matrizCooperacion)=resourcesNames
      rownames(matrizCooperacion)=resourcesNames
      
      if(listaArcosTaskFirst[j,'sourceRef']!="NA" && actual!="NA" && listaArcosTaskFirst[j,'sourceRef']!="" && actual!="" && !is.na(actual) && !is.na(listaArcosTaskFirst[j,'sourceRef'])){
          assign(paste(listaArcosTaskFirst[j,'sourceRef'],actual,sep='::'),matrizCooperacion) 
          listaArcosEfectivos=rbind(listaArcosEfectivos,paste(listaArcosTaskFirst[j,'sourceRef'],actual,sep='::'))
        }
      }
    else{
      vecinos=getVecinos(actual)
      for(k in vecinos){
        nodeStack<-insert(nodeStack,k)
      }
    }
    
  }
}


#Hasta aqu� todo va bien

#PROM

#Extraer martriz de cooperaci�n
namesDictionary=data.frame()
for(i in 1:length(elements[,1])){
  actual=elements[i,]
  if(isTask(actual$id)){
    namesDictionary=rbind(namesDictionary,elements[i,c('id','name')])
    
  }
}
#ARRIBA TA EL LIO

#REVISAR POR QU� EL PRIMERO DA MAL
#listaArcosEfectivos=listaArcosEfectivos[-c(1:11)]
df=as.data.frame(logFile)

casos=unique(df$CASE_concept_name)

#Hasta aqui excelentemente

for(actual in casos){
  casoActual=subset(df,CASE_concept_name==actual)
  
  for(i in 1:length(listaArcosEfectivos)){
    source=strsplit(listaArcosEfectivos[i][[1]],"::")[[1]][1]
    target=strsplit(listaArcosEfectivos[i][[1]],"::")[[1]][2]
    foundSource=FALSE
    foundTarget=FALSE
    foundBoth=FALSE
    dictionaryIndexSource=which(namesDictionary$id==source)
    
    dictionaryIndexTarget=which(namesDictionary$id==target)
    # print(namesDictionary[dictionaryIndexSource,2])
    #print(namesDictionary[dictionaryIndexTarget,2])
    for(j in 1:length(casoActual[,1])){
      
      if(casoActual[j,'activity_id']==namesDictionary[dictionaryIndexSource,2] && !foundSource){
        foundSource=TRUE
        indexSource=j
        #Break
      }
      if(casoActual[j,'activity_id']==namesDictionary[dictionaryIndexTarget,2] && foundSource && !foundTarget){
        foundTarget=TRUE
        indexTarget=j
        foundBoth=TRUE
        #break
      }
      if(foundBoth){
        
        sourceResource=as.character(casoActual[indexSource,'resource_id'])
        targetResource=as.character(casoActual[indexTarget,'resource_id'])
        if(!(sourceResource=='Start' || sourceResource=='End' || targetResource=='Start' || targetResource=='End')){
          
          
          matrizActual=get(paste(source,target,sep="::"))
          
          matrizActual[sourceResource,targetResource]=matrizActual[sourceResource,targetResource]+1
          assign(paste(source,target,sep="::"),matrizActual)
          break
        }
        
      }
      
    }
    
    
    
    
    
  }
  
}


#Probabilidades

#listaArcosEfectivos=listaArcosEfectivos[-1]

df=as.data.frame(logFile)
activities=unique(logFile$activity_id)

activities=as.list(activities)
activitiesNames=c()

for( i in 1:length(activities)){
  activitiesNames=rbind(activitiesNames, as.character(activities[i][[1]]))
}

matrizProbabilidades=matrix(data=rep(0,length(resourcesNames)*length(activitiesNames)),ncol=length(resourcesNames), nrow = length(activitiesNames))
colnames(matrizProbabilidades)=resourcesNames
rownames(matrizProbabilidades)=activitiesNames
for(i in activitiesNames){
  for(j in resourcesNames){
    matrizProbabilidades[i,j]=length(subset(df,df$activity_id==i & df$lifecycle_id=='complete' & df$resource_id==j)[,1])
  }
}




for(i in 1:length(listaArcosEfectivos)){
  source=strsplit(listaArcosEfectivos[i][[1]],"::")[[1]][1]
  target=strsplit(listaArcosEfectivos[i][[1]],"::")[[1]][2]
  matrizActual=get(paste(source,target,sep="::"))
  matrizResultado=matrizActual
  sumaTotal=sum(matrizActual)
  for(j in resourcesNames){
    for(k in resourcesNames){
      #HAY UN ERROR, LA PROBABILIDAD POR RECURSO EST� MAL CALCULADA (?), SER� NECESARIO LEERLA DEL LOG
      
      
      dictionaryIndexSource=which(namesDictionary$id==source)
      dictionaryIndexTarget=which(namesDictionary$id==target)
  
      sourceResource=namesDictionary[dictionaryIndexSource,2]
      targetResource=namesDictionary[dictionaryIndexTarget,2]
      if(!(sourceResource=='Start' || sourceResource=='End' || targetResource=='Start' || targetResource=='End')){
        
        denom=((matrizProbabilidades[namesDictionary[dictionaryIndexSource,2],j]/sum(matrizProbabilidades[namesDictionary[dictionaryIndexSource,2],])) *(matrizProbabilidades[namesDictionary[dictionaryIndexTarget,2],k]/sum(matrizProbabilidades[namesDictionary[dictionaryIndexTarget,2],])))
        if(denom==0){
          correlation=0
        }
        else{
          correlation=(matrizActual[j,k]/sumaTotal)/((matrizProbabilidades[namesDictionary[dictionaryIndexSource,2],j]/sum(matrizProbabilidades[namesDictionary[dictionaryIndexSource,2],])) *(matrizProbabilidades[namesDictionary[dictionaryIndexTarget,2],k]/sum(matrizProbabilidades[namesDictionary[dictionaryIndexTarget,2],])))
        }
        
        if(correlation>1){
          matrizResultado[j,k]=((matrizActual[j,k]/sumaTotal)-((matrizProbabilidades[namesDictionary[dictionaryIndexSource,2],j]/sum(matrizProbabilidades[namesDictionary[dictionaryIndexSource,2],])) *(matrizProbabilidades[namesDictionary[dictionaryIndexTarget,2],k]/sum(matrizProbabilidades[namesDictionary[dictionaryIndexTarget,2],]))))/((matrizProbabilidades[namesDictionary[dictionaryIndexSource,2],j]/sum(matrizProbabilidades[namesDictionary[dictionaryIndexSource,2],]))*(1-(matrizProbabilidades[namesDictionary[dictionaryIndexTarget,2],k]/sum(matrizProbabilidades[namesDictionary[dictionaryIndexTarget,2],]))))
        }
        else{
          matrizResultado[j,k]=0
        }
      }
      
      
    }
  }
  #Esto pa qu� era?
 # matrizActual[sourceResource,targetResource]=matrizActual[sourceResource,targetResource]+1
  assign(paste(source,target,sep="::"),matrizActual)
  
}

#C�lculo correlaciones
matrizCooperaciones=matrizResultado
for(i in 1:length(matrizCooperaciones[,1])){
  for(j in 1:length(matrizCooperaciones[1,])){
    matrizCooperaciones[i,j]=0
  }
}
for(i in 1:length(listaArcosEfectivos)){
  source=strsplit(listaArcosEfectivos[i][[1]],"::")[[1]][1]
  target=strsplit(listaArcosEfectivos[i][[1]],"::")[[1]][2]
  matrizActual=get(paste(source,target,sep="::"))
  matrizCooperaciones=matrizActual+matrizCooperaciones
  assign(paste(source,target,sep="::"),matrizActual)
  
}

write.csv(matrizCooperaciones,paste(logPath,"_cooperationMatrix.csv",sep=""))

#Dashboard a nivel de procesos. Muestra resultados cada vez que se cambie una pol�tica. Preferiblemente cargar datos guardados. FO, POLITICA, CLUSTERING

