library(tidyverse)
library(fpp3)
library(plotly)
library(zoo)
library(patchwork)


mean_diff <- data_picnic %>% summarise(mean(diff))

# ==================================

plot_diff <- data_picnic %>% 
  mutate(ma100 = rollmean(diff, k = 100, align = "right", fill = NA))%>%
  filter(timestamp >= 3200000 & timestamp <= 3600000) %>%
  ggplot(aes(timestamp)) +
    geom_line(aes(y = diff), color = '#D39615') +
    geom_hline(yintercept = 367, linetype = "dashed")


plot_picnic <- data_picnic %>% 
  mutate(
    ma100 = rollmean(diff, k = 100, align = "right", fill = NA)
  )%>%
  filter(timestamp >= 3200000 & timestamp <= 3600000) %>% 
  ggplot(aes(timestamp)) +
    geom_line(aes(y = PICNIC_BASKET), color = "#1B8292")


# Combine plots with package patchwork
combined_plot <- wrap_plots(plot_diff, plot_picnic, ncol = 1)

# Display the combined plot
print(combined_plot)




# ==================================

plot_diff_2 <- data_picnic %>% 
  mutate(diff = diff - 375.7248) %>%
  mutate(ma100 = rollmean(diff, k = 100, align = "right", fill = NA))%>%
  filter(timestamp >= 3200000 & timestamp <= 3600000) %>%
  ggplot(aes(timestamp)) +
  geom_line(aes(y = diff), color = '#D39615') +
  geom_hline(yintercept = 367, linetype = "dashed")


plot_picnic_2 <- data_picnic %>% 
  mutate(
    ma100 = rollmean(diff, k = 100, align = "right", fill = NA)
  )%>%
  filter(timestamp >= 3200000 & timestamp <= 3600000) %>% 
  ggplot(aes(timestamp)) +
  geom_line(aes(y = PICNIC_BASKET), color = "#1B8292")


# scale back the diff by demean
# plot ma100
# highlight periods that satisfy gap > 100 and trend reached peak/trough
# for buying and selling points