"""
--------------------------------------------
Code for generating plots round 4: Arbitrage
 
Author: Vincent Su
--------------------------------------------
"""

library(tidyverse)
library(fpp3)
library(plotly)
library(zoo)
library(patchwork)


# Load data
data_1 <- read_csv2('data/data-round-4/prices_round_4_day_1.csv') %>% 
  mutate(timestamp = timestamp)
data_2 <- read_csv2('data/data-round-4/prices_round_4_day_2.csv') %>% 
  mutate(timestamp = timestamp + 1000000)
data_3 <- read_csv2('data/data-round-4/prices_round_4_day_3.csv') %>% 
  mutate(timestamp = timestamp + 2000000)
data_4 <- read_csv2('data/data-round-4/day-4-result.csv') %>% 
  mutate(timestamp = timestamp + 3000000)

# Clean and some computation
data_picnic <- data_1 %>% 
  rbind(data_2) %>% 
  rbind(data_3) %>% 
  rbind(data_4) %>%
  filter(product %in% c("DIP", "BAGUETTE", "UKULELE", "PICNIC_BASKET") 
  ) %>% 
  mutate(mid_price = mid_price/10)

data_picnic <- data_picnic %>% 
  select(day, timestamp, product, mid_price) %>% 
  pivot_wider(
    names_from = product,
    values_from = mid_price
  ) %>% 
  mutate(sum = 4*DIP + 2*BAGUETTE + UKULELE) %>% 
  mutate(diff = PICNIC_BASKET - sum)


# Average of the difference
data_picnic %>% summarise(mean(diff))

# Plotting Diff against Picnic Basket==================================

plot_diff <- data_picnic %>% 
  filter(timestamp >= 3200000 & timestamp <= 3600000) %>%
  ggplot(aes(timestamp)) +
    geom_line(aes(y = diff), color = '#9540EF', linewidth = 0.8) +
    geom_hline(yintercept = 367, linetype = "dashed") +
    annotate(
      "text", x = 3270000, y = 400, 
      label="Mean", color = "gray40") +
    ylab("Difference") +
    labs(title = "Plotting the Difference against Picnic Basket's Price") +
    theme_bw()


plot_picnic <- data_picnic %>% 
  mutate(ma100 = rollmean(diff, k = 100, align = "right", fill = NA))%>%
  filter(timestamp >= 3200000 & timestamp <= 3600000) %>% 
  ggplot(aes(timestamp)) +
    geom_line(aes(y = PICNIC_BASKET), color = "#D39615", linewidth = 0.8) +
    ylab("Actual Picnic Basket Price") +
    theme_bw()


# Combine plots with package patchwork
combined_plot <- wrap_plots(plot_diff, plot_picnic, ncol = 1)

# Display the combined plot
print(combined_plot)




# Additional Visualisation ==================================

# scale back the diff by demean
# plot ma100
# highlight periods that satisfy gap > 100 and trend reached peak/trough
# for buying and selling points


# plot_diff_2 <- data_picnic %>% 
#   mutate(diff = diff - 375.7248) %>%
#   mutate(ma100 = rollmean(diff, k = 100, align = "right", fill = NA)) %>%
#   filter(timestamp >= 3300000 & timestamp <= 3630000) %>%
#   ggplot(aes(timestamp)) +
#     geom_line(aes(y = diff), color = '#D39615') +
#     geom_line(aes(y = ma100), color = '#6E4D08') +
#     geom_hline(yintercept = 0, linetype = "dashed")
# 
# plot_picnic_2 <- data_picnic %>% 
#   mutate(
#     ma100 = rollmean(diff, k = 100, align = "right", fill = NA)
#   )%>%
#   filter(timestamp >= 3300000 & timestamp <= 3630000) %>% 
#   ggplot(aes(timestamp)) +
#     geom_line(aes(y = PICNIC_BASKET), color = "#1B8292")
# 
# # Combine plots with package patchwork
# combined_plot <- wrap_plots(plot_diff_2, plot_picnic_2, ncol = 1)
# 
# # Display the combined plot
# print(combined_plot)


