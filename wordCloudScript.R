library(readr)
library(ggwordcloud)
library(dplyr)
library(tidyr)
library(tidyverse)

DeptData <- read_csv("C:/Users/llsch/Box Sync/Data Vis/Client Project/WordCloudDeptandInstitutions.csv")
#View(DeptData)

DeptDatawFreq <- DeptData%>%
  group_by(Dept, Institution)%>%
  summarise(Freq = n())
DeptDataFiltered <- subset(DeptDatawFreq, !(Freq==1))
DeptDataAngled90 <- DeptDatawFreq %>%
  mutate(angle = 90 * sample(c(0, 1), n(), replace = TRUE, prob = c(60, 40))) %>%
  rename(Scale_of_Dept_Members = Freq)

WordCloud <- ggplot(DeptDataAngled90, aes(label = Dept, size = Scale_of_Dept_Members, color = Institution, angle = angle)) + geom_text_wordcloud(area_corr = TRUE, rm_outside = TRUE, show.legend = TRUE) + scale_size_area(max_size = 10) + theme_minimal() + scale_color_manual(values = c("Bloomington High School South" = "#800080", "Bloomington Montessori School" = "#de8cc5", "City of Bloomington" = "#2d22a8", "Harvard University" = "#A51C30", "Indiana University" = "#990000", "Indiana University Purdue University Indianapolis" = "#191919", "Michigan State University" = "#18453B", "Other" = "#0e8787", "Purdue University" = "#F1BE48", "St. Charles School" = "#969696", "Texas Tech University" = "#CC0000", "Tulane University" = "#005837", "University of Maryland" = "#FFCD23", "University of Minnesota" = "#862334", "University of North Florida" = "#00246B", "University of Wisconsin-Stevens Point" = "#492F92")) + theme(legend.position = "right", legend.title = element_text(size = 5), legend.text = element_text(size = 5))

ggsave("UpdatedWordCloud.png")
