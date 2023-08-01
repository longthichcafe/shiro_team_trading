"""
--------------------------------------------
Code for generating plots round 2: Coconuts and Pina Coladas
 
Author: Vincent Su
--------------------------------------------
"""


library(tidyverse)
library(plotly)
library(zoo)

# load data
data_2 <- read_csv2('data/data-round-4/prices_round_4_day_2.csv') %>% 
  mutate(timestamp = timestamp + 2000000)
data_3 <- read_csv2('data/data-round-4/prices_round_4_day_3.csv') %>% 
  mutate(timestamp = timestamp + 3000000)

data <- data_2 %>% 
  rbind(data_3) %>% 
  filter(product %in% c("COCONUTS", "PINA_COLADAS")) %>% 
  mutate(mid_price = mid_price/10)

# Scaling the data
scaled_data <- data %>% 
  select(timestamp, product, mid_price) %>% 
  pivot_wider(names_from = product,
              values_from = mid_price) %>% 
  mutate(COCONUTS = (COCONUTS - 7926.957)/12.5475,
         PINA_COLADAS = (PINA_COLADAS - 14885.35)/29.1494)


### Visual Strategies (figure 1) =======================================
p1 <- scaled_data %>% 
    mutate(
      ma20_coco = rollmean(COCONUTS, k = 20, align = "right", fill = NA),
      ma20_pina = rollmean(PINA_COLADAS, k = 20, align = "right", fill = NA),
      ma200_avg = rollmean(COCONUTS + PINA_COLADAS, k = 200, align = "right", fill = NA)/2
    ) %>%
    filter(timestamp >= 3290000 & timestamp <= 3325000) %>% 
    ggplot(aes(x = timestamp)) +
      geom_line(aes(y = ma20_pina, color = "MA20 Pina")) +
      geom_line(aes(y = ma20_coco, color = "MA20 Coco")) +
      geom_line(aes(y = ma200_avg, color = "Averaged MA200")) +
      # Widening Gap
      geom_rect(
        aes(xmin = 3296500, xmax = 3298000, ymin = -4.7, ymax = -2.7), 
        alpha = 0.4, fill = "gray70"
      ) +
      geom_text(
        aes(x = 3293000, y = -3.8, label = "Widening Gap > 0.3"),
        size = 3.5, vjust = 0, hjust = 0, color = "gray50"
      ) +
      # Narrowing Gap
      geom_rect(
        aes(xmin = 3316500, xmax = 3318000, ymin = -4.7, ymax = -2.7), 
        alpha = 0.4, fill = "gray70"
      ) + 
      geom_text(
        aes(x = 3322000, y = -3.3, label = "Narrowing Gap < 0.05"),
        size = 3.5, vjust = 0, hjust = 0, color = "gray50"
      ) +
      # Additional features
      scale_color_manual(
        name = "",
        values = c("MA20 Pina" = '#D39615', 'MA20 Coco' = '#1B8292')
      ) +
      theme_bw() +
      labs(title = "MA20 with Widening and Narrowing Gaps") +
      ylab("")

ggplotly(p1)



### Visual actual buying and selling points (figure 2) =================

# Obtain simulated trading results
orders <- read_csv2('data/outputPINA-COCO.csv', col_names = FALSE)
colnames(orders) = c(
  'timestamp', 
  "pina_price", "pina_quant", "pina_profit", 
  "coco_price", "coco_quant", "coco_profit"
)
orders <- orders %>% 
  mutate(timestamp = timestamp + 2000000,
         pina_price = pina_price/10,
         coco_price = coco_price/10)

# Combine with original data
data_orders <- scaled_data %>% 
  left_join(
    y = orders,
    by = 'timestamp'
  ) %>% 
  mutate(
    pina_quant = as.numeric(pina_quant),
    coco_quant = as.numeric(coco_quant)
  )

# Plotting
p2 <- data_orders %>%
  mutate(
    pina_buy = ifelse(pina_quant > 0, PINA_COLADAS, NA),
    pina_sell = ifelse(pina_quant < 0, PINA_COLADAS, NA),
    coco_buy = ifelse(coco_quant > 0, COCONUTS, NA),
    coco_sell = ifelse(coco_quant < 0, COCONUTS, NA)
  ) %>% 
  filter(timestamp >= 3290000) %>% 
  filter(timestamp <= 3325000) %>% 
  ggplot(aes(x = timestamp)) +
    geom_line(aes(y = PINA_COLADAS, color = 'PINA_COLADAS')) +
    geom_line(aes(y = COCONUTS, color = 'COCONUTS')) +
    geom_point(aes(y = pina_buy, color = 'Buying point')) +
    geom_point(aes(y = coco_buy, color = 'Buying point')) +
    geom_point(aes(y = pina_sell, color = 'Selling point')) +
    geom_point(aes(y = coco_sell, color = 'Selling point')) +
    scale_color_manual(
      name = "",
      values = c(
        'PINA_COLADAS' = '#D39615', 'COCONUTS' = '#1B8292', 
        'Buying point' = '#008000', 'Selling point' = '#800000'
      )
    ) +
    labs(title = "Actual Price Action with Buying and Selling Points") +
    theme_bw() +
    ylab("")

ggplotly(p2)

