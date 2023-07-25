library(tidyverse)
library(zoo)
library(plotly)

data <- read_csv2('data/data_round_1/island-data-bottle-round-1/prices_round_1_day_-1.csv')

# Visualise pearls graph
ggplotly(
    data %>% 
        filter(timestamp < 15000) %>% 
        filter(product == 'PEARLS') %>% 
        ggplot(aes(x = timestamp)) +
        geom_line(aes(y = ask_price_1, color = 'Ask Price')) +
        geom_line(aes(y = bid_price_1, color = 'Bid Price')) +
        theme_bw()+
        ylab(NULL)+
        labs(title = "Pearls Price Action")
)

# Generating Simple Exponential Smoothing function
generate_sem <- function(data, alpha, level_0) {
    # Set up vector for the response with initial values set to 0
    data <- data %>% 
    mutate(sem = 0)
    data <- bind_rows(
    data.frame(day = -1, timestamp = -100, product = "BANANAS", sem = level_0),
    data
    )
    # Generate remaining observations
    for(i in seq(2, length = nrow(data) - 1)) {
    data$sem[i] <- alpha * data$mid_price[i] + (1-alpha) * data$sem[i-1]
    }
    return(data)
}

# Visualise bananas graph
data_b_em <- generate_sem(
    data %>% 
        filter(product == 'BANANAS') %>% 
        mutate(mid_price = mid_price/10),
                0.077,
                4950
    )
ggplotly(
    data_b_em %>% 
    filter(timestamp >= 30000 & timestamp <= 60000) %>% 
    ggplot(aes(x = timestamp)) +
        geom_line(aes(y = ask_price_1, color = 'Ask Price')) +
        geom_line(aes(y = bid_price_1, color = 'Bid Price')) +
        geom_line(aes(y = sem, color = 'SEM'), size = 0.7) +
        theme_bw()+
        ylab(NULL)+
        labs(title = "Bananas Price Action, with Simple Exponential Smoothing")
)
