# tradingtools
Basic trading tools used repeatedly in algo trading applications. Setting as a package enables imports to be performed.

`pip install git+https://github.com/pedrostanton/toolbox.git`

## functions
| Function                | Description                                                                                                                                                                             |
|-------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| min_increments          | function to get and return the number of decimal places a product quotes at or base min size                                                                                            |
|get_min_increments       | function to get and return all the minimum increasements for all products on an exchange                                                                                                |
|exchange_connections     | function to get and return authorised client logins for trading exchanges                                                                                                               |            
|full_average_changes     | function to create data frame of average changes, by looping through each row and running the average changes function against each sub data set. Then updating with DataFrame.update() |
|average_changes          | function for calculating the differences between two periods as a percentage.                                                                                                           |
|merge_frames_drop_cols   | function to merge together many dataframes which have calculated average gains |
|full_buy_sell_signal     | function to create a dataframe of buy sell signals for a time range (index of peroids) |
|buy_sell_signal        | function to get a buy sell signal from a single time peroid, comparing the average gains of assets |
| returns               | function for calculating returns on a backtest with buy (1) or sell signals (2)|

## classes
| Class    | Description                                                                 |
|----------|-----------------------------------------------------------------------------|
| Consumer | class to connect to rabbit mq and start consuming from an exchange or queue |



