# Self-study-of-Quantitative-Strategies
Original Reference: Quantitative Strategy Evaluation Metrics: From Sharpe to Fitness, Turnover, and 6 Key Metrics - CSDN Blog
## Core Metrics Explained
### 1. Sharpe Ratio
- Purpose: Measures risk-adjusted returns, quantifying excess return per unit of total risk (volatility).
- Formula:
Sharpe = √252 × (Avg_Daily_PnL / StdDev_Daily_PnL)
(252 ≈ trading days/year)
- Interpretation: Higher is better. Indicates superior returns for the same risk level or lower risk for the same returns. Key metric for strategy efficiency and stability.
- Limitation: Assumes normal return distribution (often violated); equally penalizes upside/downside volatility (addressed by Sortino Ratio).
### 2. Annualized Returns
- Purpose: Quantifies absolute profitability, representing expected annual profit.
- Formula (Platform-Specific):
Returns = Annualized_PnL / (Account_Capital / 2)
(Denominator adjusts for 2x leverage via "Booksize")
- Common Formula:
(1 + Total_Return)^(252/Trading_Days) - 1
- Interpretation: Higher is better. Most intuitive profit metric. Must be evaluated alongside risk and costs (e.g., turnover impact).
### 3. Turnover
- Purpose: Reflects trading activity & implied costs, defined as total traded value relative to capital employed.
- Formula:
Turnover = Total_Traded_Value / Booksize
- Interpretation: Typically lower is better. High turnover increases transaction costs (commissions, fees, slippage), eroding net profits. High-frequency strategies require sufficient returns to justify turnover.
- Critical Note: Always evaluate performance using net PnL (after realistic cost simulation).
### 4. Maximum Drawdown (MDD)
- Purpose: Measures extreme downside risk tolerance – the largest peak-to-trough decline in strategy net value (%).
- Formula:
Drawdown = (Peak_Value - Trough_Value) / Peak_Value
- Interpretation: Lower is better. Indicates resilience during adverse conditions and risk control effectiveness. Deep/prolonged drawdowns risk strategy termination.
- Context: Consider both depth and duration of drawdowns.
### 5. Fitness (Platform-Specific Metric)
- Purpose: Composite score evaluating overall strategy quality (implementation varies by platform).
- Example Formula:
Fitness = Sharpe × √(|Returns| / max(Turnover, 0.125))
- Interpretation: Higher is better. Balances returns (Sharpe, Returns) against costs/activity (Turnover). Reflects holistic strategy performance.
- Important: Understand the specific components and weighting of the Fitness metric on your platform.
### 6. Supplementary Metrics (Mentioned)
- PnL (Profit/Loss): Absolute monetary gain/loss. Higher is better.
- Per Dollar Profit: Net profit per $1 traded. Measures trading efficiency. Higher is better.
- Autocorrelation: Measures similarity of strategy returns/positions over time or between strategies. High autocorrelation may indicate lack of diversity or overfitting risk. Context-dependent.
---
## Key Takeaways from Reference
- Target Higher Values: Sharpe, Returns, Fitness, PnL
- Target Lower Values: Turnover, Drawdown
- Essential Trade-offs: Returns (Sharpe/Returns) vs. Risk (Drawdown) vs. Cost (Turnover). Fitness provides one framework for balancing.
- Out-of-Sample (OS) Validation is Paramount: Tests generalizability and robustness, guarding against overfitting. True viability is proven on unseen data.
---
## Additional Critical Metrics
### 1. Sortino Ratio
- Purpose: Downside risk-adjusted returns. Sharpe enhancement focusing only on "bad" volatility (below target return, e.g., risk-free rate or zero).
- Formula:
Sortino = (Annualized_Return - Risk_Free_Rate) / Downside_Deviation
- Interpretation: Higher is better. Particularly relevant for strategies prioritizing capital preservation (e.g., absolute return). More precise than Sharpe when return distributions are skewed.
### 2. Calmar Ratio
- Purpose: Return vs. maximum pain balance, measuring annualized return per unit of maximum drawdown.
- Formula:
Calmar = |Annualized_Return| / |Max_Drawdown| (Absolute values common)
- Interpretation: Higher is better. Directly quantifies compensation for enduring the worst historical loss. Valuable for drawdown-sensitive investors.
### 3. Information Ratio (IR)
- Purpose: Gauges active management skill / excess return consistency relative to a benchmark per unit of active risk (tracking error).
- Formula:
IR = (Portfolio_Return - Benchmark_Return) / Tracking_Error
Tracking Error = StdDev(Portfolio_Return - Benchmark_Return)
- Interpretation: Higher is better. Core metric for active managers (Alpha strategies). High IR signifies persistent benchmark outperformance.
### 4. Win Rate & Profit Factor
- Win Rate: % of profitable trades. Higher generally better, but not definitive.
- Profit Factor:
Profit Factor = Gross_Profits / Gross_Losses
>1 = Profitable, higher is better.
- Payoff Ratio:
Avg_Win / Avg_Loss
Higher is better.
- Interpretation: Reveals profit generation mechanics. High win rates often pair with moderate payoff ratios; low win rates require high payoff ratios (e.g., trend following). Calculate Expected Return per Trade.
### 5. Beta (β)
- Purpose: Measures systematic market risk exposure (sensitivity to benchmark movements).
- Formula: β = Covariance(Strategy_Returns, Benchmark_Returns) / Variance(Benchmark_Returns) (Regression slope).
- Interpretation:
    - β = 1: Market-average volatility.
    - β > 1: Higher volatility than market (aggressive).
    - β < 1: Lower volatility than market (defensive).
    - β ≈ 0: Low market correlation (e.g., market neutral).
- Utility: Crucial for understanding risk drivers and portfolio construction.
### 6. Alpha (α)
- Purpose: Risk-adjusted excess return above the return predicted by market exposure (CAPM). Reports manager skill.
- Formula:
α = Strategy_Return - [Risk_Free_Rate + β × (Benchmark_Return - Risk_Free_Rate)]
- Interpretation: Higher (positive) is better. The holy grail of active management, signifying value-add beyond market risk.
### 7. Tail Risk Metrics
- Value at Risk (VaR): Maximum potential loss ($or %) over a set period at a given confidence level (e.g., 95%). *Example: 95% 1-day VaR =$100k → 95% confidence daily loss ≤ $100k.*
- Conditional VaR (CVaR) / Expected Shortfall: Average loss magnitude when losses exceed the VaR threshold. Measures severity of extreme losses.
- Interpretation: VaR/CVaR lower is better (at same confidence). Assesses black swan event vulnerability.
### 8. Slippage
- Purpose: Quantifies execution price deviation (difference between intended trade price and actual fill price).
- Measurement: Average slippage per trade or slippage cost as % of trade value.
- Interpretation: Lower is better. Significant impact on HFT/large orders. Net PnL after realistic slippage is crucial for credible backtests.
---
## Conclusion & Best Practices
1. Master Fundamentals: Sharpe, Returns, Turnover, Drawdown, and Fitness (or equivalent composites) are essential for all strategy evaluation.
2. Select Metrics Strategically: Augment core metrics based on strategy goals:
    - Downside Focus? → Sortino, CVaR
    - Benchmark-Relative? → IR, Beta, Alpha
    - Trade Mechanics? → Win Rate, Profit Factor
    - Extreme Events? → VaR, CVaR
    - High-Frequency/Large Size? → Rigorous Slippage Analysis
3. Holistic Assessment: Never rely on a single metric! High Sharpe can mask low returns; high returns can hide crippling drawdowns; low turnover can signal missed opportunities. Multi-dimensional analysis and trade-off management are imperative.
4. Out-of-Sample is King: Strong In-Sample (IS) performance is necessary but insufficient. Robust Out-of-Sample (OS) results are the primary evidence of strategy validity and resistance to overfitting.
5. Model Costs Realistically: Backtests must incorporate realistic estimates of transaction costs (commissions, fees, slippage) to avoid inflated performance.
6. Verify Formula Details: Metric calculations can vary across platforms/research. Always confirm the precise definition and formula used in your context.
