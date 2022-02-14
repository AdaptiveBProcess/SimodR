
packages = c("ggplot2")

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

args = commandArgs(trailingOnly=TRUE)
path=args[1]
#path='output/dic5656/Production'
#path='ConsultaDataMining201618'
results_iteration<-read.csv(paste(path,"_scores.csv",sep=""),header=FALSE)
results_baseline=read.csv(paste(path,"_baseline_scores.csv",sep=""),header=FALSE)

baseline=t(results_baseline)[1,c(1:4)]
best_optimal=t(abs(results_iteration[1,c(1:4)])/baseline)


rownames(best_optimal)=NULL
baseline_standard=cbind(rep("Baseline",length(baseline)),rep(1,length(baseline)),c("Cost","Flow time", "Waiting time", "Workload"))
best_optimal=cbind(rep("Optimal",length(best_optimal[,1])),best_optimal,c("Cost","Flow time", "Waiting time", "Workload"))



results=rbind(baseline_standard,best_optimal)
colnames(results)=c("Scenario","Value","Type")
results_df=as.data.frame(results)


picture=ggplot(results_df, aes(factor(Type),Value, fill=Scenario)) +
  geom_bar(stat="identity", position = "dodge") +
  scale_fill_brewer(palette = "Set1")
png(paste(path,"_graph.png",sep=""))
print(picture)
dev.off()


