library(tidyverse)
library(fpp3)
library(plotly)
library(zoo)
library(patchwork)


# load data
data_1 <- read_csv2('data/data-round-3/prices_round_3_day_1.csv') %>% 
  mutate(timestamp = timestamp + 1000000)
data_2 <- read_csv2('data/data-round-3/prices_round_3_day_2.csv') %>% 
  mutate(timestamp = timestamp + 2000000)

data <- data_1 %>% 
  rbind(data_2) %>% 
  filter(product %in% c("DIVING_GEAR", "DOLPHIN_SIGHTINGS")) %>% 
  mutate(mid_price = mid_price/10)

# Clean data and perform some computations
data_gear <- data %>%  
  filter(product == "DIVING_GEAR") %>% 
  mutate(ma100_gear = rollmean(mid_price, k = 100, align = "right", fill = NA)) %>% 
  select(day, timestamp, mid_price, ma100_gear)

data_dol <- data %>%  
  filter(product == "DOLPHIN_SIGHTINGS") %>% 
  mutate(
    delta_dol = mid_price - lag(mid_price, 200),
    dol = mid_price) %>% 
  select(day, timestamp, dol, delta_dol)

# Join
pair <- data_gear %>% 
  left_join(data_dol) %>% 
  filter(day == 2)


# VISUALISATION ===================================================

# Plot Diving Gears
plot_gears <- pair %>% 
  filter(timestamp <=2400000) %>% 
  ggplot(aes(x = timestamp, y=mid_price)) +
    geom_line(color = "#0C8BC2") +
    ylab("Price of Diving Gears") +
    labs(title = "Changes in Dolphins against Diving Gears Price Movement") +
    theme_bw()

# Plot Dolphins Changes
plot_dol <- pair %>% 
  filter(timestamp <=2400000) %>% 
  ggplot(aes(x = timestamp, y=delta_dol)) +
    geom_line(color = "#37D9AA") +
    geom_hline(yintercept = 10, linetype = "dashed") +
    annotate(
      "text", x = 2050000, y = 12, 
      label="Significance level", color = "gray30") +
    ylab("Change in Dolphins") +
    theme_bw()

# Combine plots with package patchwork
combined_plot <- wrap_plots(plot_gears, plot_dol, ncol = 1)

# Display the combined plot
print(combined_plot)
