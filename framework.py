import numpy as np
import pandas as pd
from scipy.stats import zscore

# ======================
# 1. 因子计算核心逻辑
# ======================
def calculate_factor(data: pd.DataFrame, 
                    lookback: int = 20,
                    volatility_adj: bool = True) -> pd.Series:
    """
    示例：动量因子 (过去N日收益率)
    
    参数：
    data: 包含['close']列的DataFrame
    lookback: 回溯周期
    volatility_adj: 是否做波动率调整
    
    返回：
    factor_values: 因子值Series
    """
    # 基础因子计算
    returns = data['close'].pct_change(lookback)
    
    # 波动率调整 (降低极端值影响)
    if volatility_adj:
        vol = data['close'].pct_change().rolling(60).std()
        factor = returns / (vol + 1e-6)  # 避免除零
    else:
        factor = returns
        
    # 标准化处理 (使因子符合标准正态分布)
    factor = factor.groupby(data.index.date).apply(zscore)
    
    return factor.dropna()

# ======================
# 2. 回测引擎对接模板
# ======================
class FactorBacktester:
    def __init__(self, data, factor_name, cost_rate=0.001):
        self.data = data
        self.factor = calculate_factor(data)  # 调用因子计算
        self.cost_rate = cost_rate  # 单边交易成本
        
    def generate_signals(self, threshold: float = 0.5):
        """生成交易信号：1=做多, -1=做空, 0=空仓"""
        signals = pd.Series(0, index=self.factor.index)
        signals[self.factor > threshold] = 1
        signals[self.factor < -threshold] = -1
        return signals.shift()  # 避免前向引用
        
    def run_backtest(self):
        signals = self.generate_signals()
        returns = self.data['close'].pct_change()
        
        # 计算策略收益 (考虑交易成本)
        strategy_returns = signals.shift(1) * returns
        trade_days = signals.diff().abs() > 0  # 换仓日标记
        strategy_returns[trade_days] -= self.cost_rate  # 扣除交易成本
        
        return strategy_returns.cumsum()  # 累计收益曲线
    
# ======================
# 3. 核心指标计算函数
# ======================
def calculate_metrics(returns: pd.Series) -> dict:
    """计算关键评估指标"""
    # 年化收益率
    annual_return = returns.iloc[-1] * 252 / len(returns)
    
    # 夏普比率 (假设无风险利率=0)
    sharpe = np.sqrt(252) * returns.mean() / returns.std()
    
    # 最大回撤
    cum_returns = (1 + returns).cumprod()
    peak = cum_returns.expanding().max()
    drawdown = (cum_returns - peak) / peak
    max_drawdown = drawdown.min()
    
    # 换手率估算
    turnover = (returns.diff().abs() > 0).mean() * 252
    
    return {
        "Annual Return": annual_return,
        "Sharpe Ratio": sharpe,
        "Max Drawdown": max_drawdown,
        "Turnover": turnover
    }

# ======================
# 4. 主执行流程
# ======================
if __name__ == "__main__":
    # 加载数据 (示例)
    data = pd.read_csv("price_data.csv", index_col=0, parse_dates=True)
    
    # 运行回测
    backtester = FactorBacktester(data, factor_name="momentum")
    equity_curve = backtester.run_backtest()
    
    # 输出结果
    metrics = calculate_metrics(equity_curve.pct_change().dropna())
    print("=== 回测结果 ===")
    for k, v in metrics.items():
        print(f"{k}: {v:.4f}")
