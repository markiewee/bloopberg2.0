import numpy as np
import scipy.stats as stats
from linreg import Linreg
import pandas as pd
import pandas_market_calendars as mcal


class PortfolioStatistics:
    """
    Calculates portfolio statistics such as linear regression coefficients, average rate of return, final AUM, etc.
    """
    def __init__(self, linreg_instance):
        self.linreg = linreg_instance
        self.top_stocks = linreg_instance.perform_strategy()[1]
        self.daily_returns = self.top_stocks.groupby(pd.to_datetime(self.top_stocks['Date'])).mean()['Return_actual']
        self.start_date = pd.to_datetime(self.linreg.start_date)
        self.end_date = pd.to_datetime(self.linreg.end_date)
        self.aum = self.linreg.aum

    def adjust_dates(self) -> None:
        """
        Adjusts for trading dates based on NYSE calendar.

        This function will adjust the start_date and end_date attributes to be valid trading days.
        """
        nyse = mcal.get_calendar('NYSE')
        schedule = nyse.schedule(start_date=self.start_date, end_date=self.end_date)
        self.start_date = schedule.index[0]
        self.end_date = schedule.index[-1]

    def calculate_statistics(self):
        """
        Args: None

        Returns: A dictionary containing the statistics requested:
        - Number of calendar days between the first and last trading day.
        – Total stock return
        – Initial AUM
        – Final AUM 
        – Return
        – ARR
        – Average and Maximum AUM
        – Profit and loss
        – Daily return (Average)
        – Standard deviation
        – Sharpe ratio
        – Linear regression coefficients
        – Linear regression t-values
        """
        self.adjust_dates()
        num_days = (self.end_date - self.start_date).days
        total_return = self.top_stocks['Return_actual'].sum()
        initial_aum = self.aum
        final_aum = self.linreg.perform_strategy()[0]
        total_return_aum = final_aum - initial_aum
        annualized_rate_of_return = (final_aum / initial_aum) ** (365.0 / num_days) - 1
        avg_daily_aum = (self.daily_returns * initial_aum).mean()
        max_daily_aum = (self.daily_returns * initial_aum).max()
        pnl = total_return_aum
        avg_daily_return = self.daily_returns.mean()
        daily_std = self.daily_returns.std()
        daily_sharpe_ratio = (avg_daily_return - 0.0001) / daily_std

        # Linear regression coefficients and t-values
        model = self.linreg.predict_performance()
        coeffs = model.params
        t_values = model.tvalues

        statistics = {
            'Begin date': self.start_date,
            'End date': self.end_date,
            'Number of days': num_days,
            'Total stock return': total_return,
            'Total return (AUM)': total_return_aum,
            'Annualized rate of return (AUM)': annualized_rate_of_return,
            'Initial AUM': initial_aum,
            'Final AUM': final_aum,
            'Average daily AUM': avg_daily_aum,
            'Maximum daily AUM': max_daily_aum,
            'PnL (AUM)': pnl,
            'Average daily return of the portfolio': avg_daily_return,
            'Daily Standard deviation of the return of the portfolio': daily_std,
            'Daily Sharpe Ratio of the portfolio': daily_sharpe_ratio,
            'Coefficients of the Linear regression': coeffs,
            't-values of the Linear regression': t_values
        }

        return statistics

if __name__ == '__main__':
    tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA']
    start_date = '20210105'
    end_date = '20211228'
    days_1 = 30
    day_2 = 60
    strategy_1 = 'M'
    strategy_2 = 'R'
    top_pct = 30
    aum = 100000

    linreg = Linreg(tickers, start_date, end_date, days_1, day_2, strategy_1, strategy_2, top_pct, aum)

    linreg.perform_strategy()

    portfolio_stats = PortfolioStatistics(linreg)

    stats = portfolio_stats.calculate_statistics()

    for key, value in stats.items():
        print(f"{key}: {value}")
