dane=read.table("E:/data.csv",header=T,sep=",")
head(dane)
attach(dane)
mean(Price)
mean(Longitude)
mean(Latitude)
sd(Price)
sd(Longitude)
sd(Latitude)
quantile(Price)
quantile(Longitude)
quantile(Latitude)

shapiro.test(Price)
shapiro.test(Longitude)
shapiro.test(Latitude)

chisq.test(Price)
chisq.test(Longitude)
chisq.test(Latitude)

cor.test(Latitude, Longitude, method="spearman")
cor.test(Price, Latitude, method="spearman")
cor.test(Price, Longitude, method="spearman")

#ANOVA - kryteria są niemożliwe do sprawdzenia w R

t.test(Latitude, Longitude)
t.test(Price, Latitude)
t.test(Price, Longitude)

cor.test(Latitude, Longitude, method="pearson")
cor.test(Price, Latitude, method="pearson")
cor.test(Price, Longitude, method="pearson")

#Kruskal - kryteria są niemożliwe do sprawdzenia w R