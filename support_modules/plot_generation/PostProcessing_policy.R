#Post Processing
#install.packages('ggplot2')
library('ggplot2')

args = commandArgs(trailingOnly=TRUE)
path=args[1]
#path='output/dic5656/Production'

results_iteration<-read.csv(paste(path,"_scores.csv",sep=""),header=FALSE)
results_baseline=read.csv(paste(path,"_baseline_scores.csv",sep=""),header=FALSE)

baseline=t(results_baseline[1,])
best_optimal=t(abs(results_iteration[1,])/results_baseline[1,])
rownames(best_optimal)=NULL
baseline_standard=cbind(rep("Baseline",length(baseline[,1])),rep(1,length(baseline[,1])),c("Cost","Flow time", "Waiting time", "Workload","Policy"))
best_optimal=cbind(rep("Optimal",length(best_optimal[,1])),best_optimal,c("Cost","Flow time", "Waiting time", "Workload","Policy"))



results=rbind(baseline_standard,best_optimal)
colnames(results)=c("Scenario","Value","Type")
results_df=as.data.frame(results)


picture=ggplot(results_df, aes(factor(Type),Value, fill=Scenario)) +
  geom_bar(stat="identity", position = "dodge") +
  scale_fill_brewer(palette = "Set1")
png(paste(path,"_graph.png",sep=""))
print(picture)
dev.off()

