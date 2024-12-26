from fastapi import FastAPI, Query
from typing import Optional
import matplotlib.pyplot as plt

def score_metric(data, thresholds, reverse=False):
    """
    Assigns a normalized score (1-5) based on defined thresholds.
    Args:
        data: The value to be scored.
        thresholds: A list of thresholds for scoring. Example: [50, 100, 500, 1000]
        reverse: If True, reverse the scoring logic (lower is better).
    Returns:
        A score between 1 and 5.
    """
    if reverse:
        thresholds = thresholds[::-1]

    if data >= thresholds[-1]:
        return 5
    elif data >= thresholds[-2]:
        return 4
    elif data >= thresholds[-3]:
        return 3
    elif data >= thresholds[-4]:
        return 2
    else:
        return 1


def fetch_real_time_data(metric, company_symbol):
    """
    Fetches real-time data for a given metric and company symbol.
    ** Note: Replace with actual API integration. This is a placeholder. **
    Args:
        metric: The metric for which to fetch data.
        company_symbol: The stock symbol of the company.
    Returns:
        Simulated real-time data for the given metric.
    """
    # Simulated data for demonstration (replace with API calls)
    simulated_data = {
        "AI R&D Spending": 750_000_000,  # Example: $750 million
        "Acquisitions of AI Companies": 3,
        "Dedicated AI Budgets": 500_000_000,
        "Number of AI Experts": 1500,
        "Hiring Trends": 50,
        "Academic Partnerships": 10,
        "AI Patents Filed": 250,
        "Research Publications": 100,
        "Open-Source Contributions": 50,
        "AI-Driven Products": 5,
        "Customer Use Cases": 20,
        "AI Research Partnerships": 10,
        "Industry Leadership Roles": 5,
        "Reputation in AI": 4,
        "Media Coverage": 4,
        "Stock Performance Tied to AI": 4,
        "AI Investment Narratives": 4
    }
    return simulated_data.get(metric, None)


def score_ai_company(company_symbol, custom_weights=None):
    """
    Scores an AI-dedicated company based on a multi-faceted rubric.

    Args:
        company_symbol: The stock symbol of the company to be scored (e.g., 'TSLA').
        custom_weights: Optional dictionary to override default weights.
    
    Returns:
        A dictionary containing the scores for each category and the overall score.
    """
    # Default rubric with weights
    default_rubric = {
        "Financial Metrics": {
            "AI R&D Spending": 0.1,
            "Acquisitions of AI Companies": 0.1,
            "Dedicated AI Budgets": 0.1
        },
        "Workforce and Talent": {
            "Number of AI Experts": 0.0667,
            "Hiring Trends": 0.0333,
            "Academic Partnerships": 0.0333
        },
        "Intellectual Property and Research": {
            "AI Patents Filed": 0.0667,
            "Research Publications": 0.0333,
            "Open-Source Contributions": 0.0333
        },
        "Product and Service Offerings": {
            "AI-Driven Products": 0.075,
            "Customer Use Cases": 0.075
        },
        "Partnerships and Collaborations": {
            "AI Research Partnerships": 0.05,
            "Industry Leadership Roles": 0.05
        },
        "Market Perception": {
            "Reputation in AI": 0.025,
            "Media Coverage": 0.025
        },
        "Stock Market and Investor Sentiment": {
            "Stock Performance Tied to AI": 0.025,
            "AI Investment Narratives": 0.025
        }
    }

    rubric = custom_weights or default_rubric

    # Scoring thresholds (examples; adjust based on industry knowledge)
    scoring_thresholds = {
        "AI R&D Spending": [50_000_000, 100_000_000, 500_000_000, 1_000_000_000],
        "Acquisitions of AI Companies": [1, 2, 5, 10],
        "Dedicated AI Budgets": [50_000_000, 100_000_000, 500_000_000, 1_000_000_000],
        "Number of AI Experts": [100, 500, 1000, 2000],
        "Hiring Trends": [10, 20, 50, 100],
        "Academic Partnerships": [1, 5, 10, 20],
        "AI Patents Filed": [10, 50, 100, 500],
        "Research Publications": [5, 20, 50, 100],
        "Open-Source Contributions": [1, 10, 25, 50],
        "AI-Driven Products": [1, 3, 5, 10],
        "Customer Use Cases": [5, 10, 20, 50],
        "AI Research Partnerships": [1, 5, 10, 20],
        "Industry Leadership Roles": [1, 3, 5, 10],
        "Reputation in AI": [1, 2, 3, 5],
        "Media Coverage": [1, 2, 3, 5],
        "Stock Performance Tied to AI": [1, 2, 3, 5],
        "AI Investment Narratives": [1, 2, 3, 5]
    }

    # Fetch and score data
    scores = {}
    category_scores = {}
    for category, metrics in rubric.items():
        category_score = 0
        scores[category] = {}
        for metric, weight in metrics.items():
            data = fetch_real_time_data(metric, company_symbol)
            if data is not None:
                metric_score = score_metric(data, scoring_thresholds[metric])
                scores[category][metric] = metric_score
                category_score += metric_score * weight
            else:
                print(f"Warning: Missing data for {metric}.")
        category_scores[category] = category_score

    # Normalize category scores to sum to 1
    total_weight = sum(rubric[cat][metric] for cat in rubric for metric in rubric[cat])
    normalized_scores = {k: v / total_weight for k, v in category_scores.items()}
    overall_score = sum(normalized_scores.values())

    return {
        "Category Scores": normalized_scores,
        "Overall Score": overall_score,
        "Detailed Scores": scores
    }


def plot_scores(scores):
    """
    Plots a radar chart of the scores for each category.
    Args:
        scores: Dictionary containing scores for each category.
    """
    categories = list(scores.keys())
    values = list(scores.values())

    # Radar chart requires values to be a circular list
    values += values[:1]
    categories += categories[:1]

    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
    ax.fill(categories, values, color='blue', alpha=0.25)
    ax.plot(categories, values, color='blue', linewidth=2)
    ax.set_yticks([0.2, 0.4, 0.6, 0.8, 1.0])
    ax.set_title("Normalized AI Company Category Scores", size=16)
    plt.show()


# Example usage:
company_symbol = "TSLA"
result = score_ai_company(company_symbol)
print(f"Scores for {company_symbol}: {result}")

# Plot the results
plot_scores(result["Category Scores"])

# Create a FastAPI app
app = FastAPI()

@app.get("/score_ai_company")
def handle_score_request(ticker: str = Query(..., description="The stock ticker of the company to analyze")):
    """
    Endpoint to process stock ticker and return AI company scores.
    """
    try:
        # Call the scoring function with the provided ticker
        result = score_ai_company(ticker)
        return {
            "success": True,
            "ticker": ticker,
            "category_scores": result["Category Scores"],
            "overall_score": result["Overall Score"],
            "detailed_scores": result["Detailed Scores"]
        }
    except Exception as e:
        return {"error": str(e)}


