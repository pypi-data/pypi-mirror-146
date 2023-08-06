import cbpro
from binance.client import Client
from binance.client import Client
import pandas as pd

def min_increments(base_increase):
    if '.' not in base_increase:
        dec = ""
    else:
        dec = base_increase.split(".")[1]
    return len(dec)


def get_min_increments(exchanges, clients):
    # get min increment information for trading sizes later

    # dictionary setup for return later
    quote_min_increments = {}
    base_min_increments = {}

    # CBPRO
    for e in exchanges:
        if 'cbpro' == e:
            # connect to exchange and make products call
            public_client = cbpro.PublicClient()
            p_data = public_client.get_products()

            # loop through each product
            qmi = {}
            bmi = {}
            for p in p_data:
                qmi[p['id']] = min_increments(p['quote_increment'])
                bmi[p['id']] = min_increments(p['base_increment'])
            quote_min_increments['cbpro'] = qmi
            base_min_increments['cbpro'] = bmi

        if 'binance' == e:
            products = clients[e].get_exchange_info()['symbols']


    # return increments
    return quote_min_increments, base_min_increments


def exchange_connections(exchanges, credentials):
    # dictionary of clients
    clients = {}

    # loop through exchange list
    for e in exchanges:
        if e == 'cbpro':
            clients[e] = cbpro.AuthenticatedClient(**credentials[e])
        if e == 'binance':
            clients[e] = Client(**credentials[e])

    return clients


def full_average_changes(hloc: pd.DataFrame, diffs: list, column="Close") -> pd.DataFrame:
    """
    function to create data frame of average changes, by looping through each row and running the average changes
    function against each sub data set. Then updating with DataFrame.update()

    :param hloc: input asset High, Low, Open, Close data set
    :param diffs: list of differences to calculate as a percentage, in 100.00 form (via average_changes function)
    :param column: which column to calculate the difference on. Default is "Close"
    :return: a dataframe with the original hloc, plus additional columns for each time peroid difference and an average
             of each column
             e.g. for two differences of 9 and 10 peroids a DataFrame with the below column index will be returned.
             Index(['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume', 9, 10, 'ave'], dtype='object')
    """

    # prepare data for calculation by taking a copy to avoid updates to the original
    md = max(diffs)
    starting_hloc = hloc.copy()

    # add in the columns which will be generated from the average function.
    for d in diffs:
        hloc[d] = ""
    hloc['ave'] = ""

    # loop through each row starting from where a full data subset is, then update with DataFrame.update()
    for i in range(md, len(hloc)):
        dif_df = average_changes(starting_hloc[i - md:i + 1], diffs, column)
        hloc.update(dif_df)

    return hloc


def average_changes(df: pd.DataFrame, diffs: list, column="Close") -> pd.DataFrame:
    """
    function for calculating the differences between two periods as a percentage.
    #1: prepare data into lists
    #2: loop through each of the difference to calculate as a percentage % (100 = 100%)
    #3: get the average of all differences (as a percentage)
    #4: get the last row name and prepare column names for return

    :param df: dataframe of HLOC values normally
    :param diffs: what are the peroids to get the difference for.
    :param column: default is "Close" peroid, so can use open, high, low or other

    :return: dataframe row of the last row i.e. the last time peroid
    """

    # 1: prepare data into lists
    data = df[column].tolist()
    new_cols = []
    data_len = len(data) - 1

    # 2: loop through each of the difference to calculate
    for d in diffs:
        new_cols.append((data[data_len] - data[data_len - d]) / data[data_len - d] * 100)

    # 3: get the average
    new_cols.append(sum(new_cols) / len(new_cols))

    # 4: get the last row name and prepare column names for return
    cols = diffs.copy()
    cols.append("ave")
    idx = [df.tail(1).index.item()]

    return pd.DataFrame([new_cols], index=idx, columns=cols)


def merge_frames_drop_cols(ds: dict, drop_col='ave'):
    """
    function to merge together many dataframes which have calculated average gains

    :param ds: the data set of hlocs for many assets
    :param drop_col: what is the name of the column to NOT drop
    :return: returns a data frame which contains only the averages
    """

    full_df = pd.DataFrame(columns=ds[list(ds.keys())[0]].columns)

    for k, v in ds.items():
        full_df = full_df.join(v, how='outer', rsuffix="_" + k)

    full_df = full_df.drop(drop_col, axis=1)
    full_df = full_df.loc[:, full_df.columns.str.contains(drop_col)]

    return full_df


def full_buy_sell_signal(df_ave: pd.DataFrame, assets, top=3, col='ave'):
    """
    function to create a dataframe of buy sell signals for a time range (index of peroids)
    #1: prepare the dataframe for return, bss (buy sell signal)
    #2: loop through each time peroid, calculate the buy or sell and update the dataframe.

    :param df_ave: the dataframe of average gains
    :param assets: list of tickers which are being used
    :param top: how many assets are being traded, ie. the top 3. default 3
    :param col: what is the column prefix for the averages. default 'ave'
    :return: dataframe of buy (1.0) and sell signals (0.0)
    """

    # 1: prepare the dataframe for return, bss (buy sell signal)
    idx = df_ave.index.values
    for i in range(len(assets)):
        assets[i] = col + "_" + assets[i]
    bss = pd.DataFrame(index=idx, columns=assets)

    # 2: loop through each time peroid, calculate the buy or sell and update the dataframe.
    for i, r in df_ave.iterrows():
        bss.at[i] = buy_sell_signal(r=r, top=top)

    return bss


def buy_sell_signal(r: pd.Series, top=3, limit=0):
    """
    function to get a buy sell signal from a single time peroid, comparing the average gains of assets
    #1: sort the series by highest gains at the top
    #2: loop through each value and if the top (normally 3) and above limit (normally zero) buy, else sell.
    :param r: Series to sort and compare
    :param top: number of top assets
    :param limit: limit if below to sell
    :return: series of buy sell signals
    """

    r = r.sort_values(ascending=False)

    j = 0
    for i, v in r.iteritems():
        if v != "":
            if j < top and v > limit:
                r.update({i: int(1)})
            else:
                r.update({i: int(0)})

        j = j + 1

    return r


def returns(fdf: pd.DataFrame, funds=100, commission=0.005, bs_point="Close", coin=''):
    """
    function for calculating returns on a backtest with buy (1) or sell signals (2)

    :param fdf: full data frame for asset including signal to buy or sell
    :param funds: amount of funds to trade, default is 100
    :param commission: level of commission, default is 0.005 i.e. 0.5%
    :param bs_point: which column to buy or sell at, default is market close
    :param coin: what is the coin name. Default is null. Used in column name returns
    :return: dataframe of results:
                 Buy n Hold      Signal     Delta
        BTC-GBP   97.802091  100.875162  3.073071
    """
    # buy n hold check
    counter = 1
    bnh_funds = funds

    state = False
    for i, r in fdf.iterrows():

        # get price, used in many calcs
        price = r[bs_point]

        # buy n hold purchase
        if counter == 1:
            bnh_funds = bnh_funds - (commission * bnh_funds)
            bnh_funds = bnh_funds / price
        elif counter == len(fdf):
            bnh_funds = bnh_funds * price
            bnh_funds = bnh_funds - (commission * funds)
        counter = counter + 1

        # buy n hold strategy
        if r['signal'] == 1 and not state:
            # print("Buy")
            state = True
            funds = funds - (commission * funds)
            funds = funds / price
        elif r['signal'] == 0 and state:
            # print("Sell")
            state = False
            funds = funds * price
            funds = funds - (commission * funds)

    # close open purchase
    if state:
        funds = funds * price

    res_df = pd.DataFrame([[bnh_funds, funds, funds - bnh_funds]], index=[coin],
                          columns=['Buy n Hold', 'Signal', 'Delta'])
    # print(res_df)

    return res_df
