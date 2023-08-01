"""
--------------------------------------------
Code for generating plots round 3: Mayberries
 
Author: Vincent Su
--------------------------------------------
"""


library(tidyverse)
library(fpp3)
library(zoo)

# load data
data_0 <- read_csv2('data/data-round-3/prices_round_3_day_0.csv')
data_1 <- read_csv2('data/data-round-3/prices_round_3_day_1.csv') %>% 
  mutate(timestamp = timestamp + 1000000)
data_2 <- read_csv2('data/data-round-3/prices_round_3_day_2.csv') %>% 
  mutate(timestamp = timestamp + 2000000)

data_berries <- data_0 %>% 
  rbind(data_1) %>% 
  rbind(data_2) %>% 
  filter(product == "BERRIES") %>% 
  mutate(mid_price = mid_price/10)


### STL Decomposition ======================
decomp <- data_berries %>% 
  filter(timestamp <= 3000000) %>%
  as_tsibble(index = timestamp) %>% 
  model(
    STL(mid_price ~ trend(window =2000) + season(period = 10000, window = 4))
  ) %>% 
  components() 

### Plot STL components =======================
decomp %>% 
  autoplot() +
   theme_bw()

### Plot the averaged season component =======================
decomp %>% 
  as_tibble() %>% 
  # average the seasonal component
  mutate(day = timestamp %/% 1000000) %>% 
  mutate(timestamp = timestamp %% 1000000) %>% 
  group_by(timestamp) %>% 
  summarise(mean_season = mean(season_10000)) %>% 
  # plot
  ggplot(aes(x=timestamp, y=mean_season)) +
    geom_line() +
    theme_bw() +
    labs(title = "Average Seasonal Component of Mayberries") +
    ylab("average price of seasonal component")