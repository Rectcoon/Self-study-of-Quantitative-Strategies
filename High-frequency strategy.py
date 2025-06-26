def intraday_momentum(ticks: pd.DataFrame):
    """
    高频策略：开盘30分钟方向决定当日趋势
    """
    # 计算开盘区间
    open_range = ticks.between_time('9:30','10:00')
    range_high = open_range['high'].max()
    range_low = open_range['low'].min()
    
    # 突破交易信号
    long_signal = ticks['last'] > range_high
    short_signal = ticks['last'] < range_low
    
    # 尾盘平仓
    signals = long_signal.astype(int) - short_signal.astype(int)
    signals[ticks.index.time >= pd.to_datetime('15:30').time()] = 0
    
    return signals
