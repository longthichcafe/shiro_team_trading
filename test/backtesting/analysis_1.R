library(tidyverse)
library(zoo)
library(plotly)


data_tut_1 <- read_csv2('data/tut1.csv')

# Explore the difference bid and ask for Pearls
data_test <- data_tut_1 %>% 
  filter(product == 'PEARLS') %>% 
  pivot_longer(cols = c(bid_price_1, bid_price_2, bid_price_3),
               names_to = 'bid',
               values_to = 'bid_price') %>% 
  pivot_longer(cols = c(ask_price_1, ask_price_2, ask_price_3),
               names_to = 'ask',
               values_to = 'ask_price')

data_test %>% 
  count(bid_price)

data_test %>% 
  count(ask_price)



data_tut_1 <- data_tut_1 %>% 
  filter(product == 'BANANAS') %>% 
  mutate(mid_price = mid_price/10) %>% 
  mutate(ma20 = rollmean(mid_price, k = 20, align = "right", fill = NA),
         ma100 = rollmean(mid_price, k = 100, align = "right", fill = NA))



# Graph the bid ask order
ggplotly(
data_tut_1 %>% 
  filter(product == 'BANANAS') %>% 
  ggplot(aes(x = timestamp)) +
    geom_line(aes(y = ask_price_1, color = 'red')) +
    geom_line(aes(y = bid_price_1, color = 'blue'))
)

ggplotly(
  data_tut_1 %>% 
    filter(product == 'PEARLS') %>% 
    ggplot(aes(x = timestamp)) +
      geom_line(aes(y = ask_price_1, color = 'blue')) +
      geom_line(aes(y = bid_price_1, color = 'red'))
)

# Graph delta log 

# ggplotly(
#   data_tut_1 %>% 
#     filter(product == "BANANAS") %>% 
#     mutate(pct_delta_bid = (bid_price_1 / lag(bid_price_1) - 1)*100,
#            pct_delta_ask = (ask_price_1 / lag(ask_price_1) - 1)*100,
#            pct_delta_mid = (mid_price / lag(mid_price) - 1)*100) %>%
#     ggplot(aes(x = timestamp, y = pct_delta_mid, color = 'blue')) +
#       geom_line() +
#       geom_line(aes(y = mid_price/10, color = 'red')) +
#       scale_y_continuous(
#         name = "First Axis",
#         sec.axis = sec_axis(~./2, name="Second Axis", limits= c(min(mid_price/10), max(mid_price/10)))
#     )
# ) 
  
  
# Graph moving average

ggplotly(
  data_tut_1 %>% 
    filter(product == 'BANANAS') %>% 
    mutate(ma20 = rollmean(mid_price, k = 20, align = "right", fill = NA),
           ma100 = rollmean(mid_price, k = 100, align = "right", fill = NA)) %>% 
    ggplot(aes(x = timestamp)) +
      geom_line(aes(y = ask_price_1, color = 'ask')) +
      geom_line(aes(y = bid_price_1, color = 'bid')) +
      geom_line(aes(y = ma20, color = 'ma20')) 
      # geom_line(aes(y = ma100, color = 'ma100')) +
      # geom_line(aes(y = mid_price))
)





### TREND IDENTIFIER
data_trend_iden <- data_tut_1

for (i in c(1,2,3,5,10,15,20,30)) {
  col_name <- paste0("ma100_chg_", i)

  data_trend_iden <- data_trend_iden %>% 
    mutate(!!col_name := (ma100 / lag(ma100, i) - 1) * 100)
}


# create a column of 0
data_trend_iden <- data_trend_iden %>% 
  mutate(n_increase = 0,
         n_decrease = 0)



for (i in c(130:nrow(data_trend_iden))) {
  
  count_up <- 0
  count_down <- 0
  
  for (j in c(1,2,3,5,10,15,20,30)) {
    
    col_name <- paste0("ma100_chg_", j)
  
    if (data_trend_iden[i, col_name] > 0){
      count_up <- count_up + 1
    }
    if (data_trend_iden[i, col_name] < 0){
      count_down <- count_down + 1
    }    
    
    data_trend_iden[i, "n_increase"] <- count_up
    data_trend_iden[i, "n_decrease"] <- count_down
  }
}

data_trend_iden <- data_trend_iden %>% 
  mutate(trend = ifelse(n_increase >= 6, "up",
                        ifelse(n_decrease >= 6, "down", "undefined")
                        )
  )

# ggplotly(
  data_trend_iden %>% 
    filter(product == 'BANANAS') %>% 
    mutate(ma20 = rollmean(mid_price, k = 20, align = "right", fill = NA),
           ma100 = rollmean(mid_price, k = 100, align = "right", fill = NA)) %>% 
    
    ggplot(aes(x = timestamp)) +
      geom_line(aes(y = ask_price_1), color = '#800000') +
      geom_line(aes(y = bid_price_1), color = '#008000') +
      geom_line(aes(y = ma100, color = ifelse(trend == 'up', '#000080',
                                             ifelse(trend == 'down', '#800080',
                                                    '#008080')
                                             )
                    )
                ) +
      geom_line(aes(y = ma20), color = 'grey')
# )

p <- data_trend_iden %>% 
  filter(product == 'BANANAS') %>% 
  ggplot(aes(x = timestamp, y = ma100, color = trend)) +
  geom_line(aes(group = 1)) +
  guides(color = FALSE)

ggplotly(p)





data_trend_iden %>% 
  filter(product == 'BANANAS') %>% 
  slice(500: 1200) %>% 
  ggplot(aes(x = timestamp, y = ma100, color = trend)) +
  geom_line(aes(group = 1), size = 1)




