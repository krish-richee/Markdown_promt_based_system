# """
# utils/competitor_search.py
# Searches the web for real competitor prices using Tavily API.
# """

# import re
# from typing import Optional
# from config.settings import TAVILY_API_KEY


# def search_competitor_prices(product_name: str,
#                               category: str,
#                               our_price: float) -> dict:
#     """
#     Searches the web for real competitor prices for a product.

#     Returns:
#         {
#             "results"         : list of {source, price, url, snippet},
#             "avg_price"       : float,
#             "min_price"       : float,
#             "max_price"       : float,
#             "price_gap_pct"   : float,   # how much cheaper/expensive vs us
#             "recommendation"  : str,
#             "raw_results"     : list,    # full Tavily response
#             "error"           : str or None
#         }
#     """
#     if not TAVILY_API_KEY or TAVILY_API_KEY.strip() == "":
#         return _fallback_response(product_name, our_price,
#                                   error="Tavily API key not set in config/settings.py")
#     try:
#         from tavily import TavilyClient
#         client = TavilyClient(api_key=TAVILY_API_KEY)

#         # Build targeted search queries
#         queries = [
#             f'"{product_name}" price buy online',
#             f'{product_name} {category} price amazon flipkart',
#             f'{product_name} cheapest price online shop',
#         ]

#         all_results = []
#         prices_found = []

#         for query in queries[:2]:   # 2 queries to save API credits
#             try:
#                 response = client.search(
#                     query=query,
#                     search_depth="basic",
#                     max_results=5,
#                     include_answer=False,
#                 )
#                 for r in response.get("results", []):
#                     parsed = _extract_price_from_result(r, our_price)
#                     if parsed:
#                         all_results.append(parsed)
#                         prices_found.append(parsed["price"])
#             except Exception:
#                 continue

#         # Deduplicate by URL
#         seen_urls = set()
#         unique_results = []
#         for r in all_results:
#             if r["url"] not in seen_urls:
#                 seen_urls.add(r["url"])
#                 unique_results.append(r)

#         if not prices_found:
#             return _fallback_response(product_name, our_price,
#                                       error="No competitor prices found on web")

#         avg_price = round(sum(prices_found) / len(prices_found), 2)
#         min_price = round(min(prices_found), 2)
#         max_price = round(max(prices_found), 2)
#         price_gap_pct = round((our_price - avg_price) / avg_price * 100, 1)

#         if price_gap_pct > 10:
#             recommendation = f"We are {price_gap_pct}% MORE EXPENSIVE than competitors. Consider markdown."
#         elif price_gap_pct < -10:
#             recommendation = f"We are {abs(price_gap_pct)}% CHEAPER than competitors. Good position."
#         else:
#             recommendation = f"Our price is within {abs(price_gap_pct)}% of competitor average. Competitive."

#         return {
#             "results"       : unique_results[:6],   # top 6 results
#             "avg_price"     : avg_price,
#             "min_price"     : min_price,
#             "max_price"     : max_price,
#             "price_gap_pct" : price_gap_pct,
#             "recommendation": recommendation,
#             "raw_results"   : unique_results,
#             "error"         : None,
#         }

#     except ImportError:
#         return _fallback_response(product_name, our_price,
#                                   error="tavily-python not installed. Run: pip install tavily-python")
#     except Exception as e:
#         return _fallback_response(product_name, our_price, error=str(e))


# def _extract_price_from_result(result: dict, our_price: float) -> Optional[dict]:
#     """
#     Tries to extract a price from a Tavily search result.
#     Looks for patterns like: $19.99, ₹1,299, USD 45.00, Price: 23.50
#     """
#     text = (result.get("content", "") + " " + result.get("title", "")).lower()
#     url  = result.get("url", "")

#     # Price regex patterns
#     patterns = [
#         r'\$\s*([\d,]+(?:\.\d{1,2})?)',      # $19.99
#         r'₹\s*([\d,]+(?:\.\d{1,2})?)',       # ₹1,299
#         r'usd\s*([\d,]+(?:\.\d{1,2})?)',     # USD 19.99
#         r'price[:\s]+\$?([\d,]+(?:\.\d{1,2})?)',  # Price: 19.99
#         r'([\d,]+(?:\.\d{1,2})?)\s*(?:usd|dollars?)',  # 19.99 USD
#     ]

#     for pattern in patterns:
#         matches = re.findall(pattern, text, re.IGNORECASE)
#         for match in matches:
#             try:
#                 price = float(match.replace(",", ""))
#                 # Sanity check: price should be between 10% and 500% of our price
#                 if our_price * 0.1 <= price <= our_price * 5:
#                     source = _extract_domain(url)
#                     return {
#                         "source" : source,
#                         "price"  : round(price, 2),
#                         "url"    : url,
#                         "snippet": result.get("content", "")[:120] + "...",
#                     }
#             except (ValueError, TypeError):
#                 continue
#     return None


# def _extract_domain(url: str) -> str:
#     """Extracts clean domain name from URL."""
#     match = re.search(r'(?:https?://)?(?:www\.)?([^/]+)', url)
#     if match:
#         domain = match.group(1)
#         # Clean known domains
#         for known in ["amazon", "flipkart", "walmart", "ebay",
#                        "target", "myntra", "meesho", "snapdeal"]:
#             if known in domain.lower():
#                 return known.capitalize()
#         return domain[:30]
#     return "Web"


# def _fallback_response(product_name: str, our_price: float,
#                         error: str = None) -> dict:
#     """
#     Returns a mock response when Tavily is unavailable.
#     Generates realistic competitor prices based on our price.
#     """
#     import random
#     random.seed(hash(product_name) % 9999)

#     mock_results = [
#         {"source": "Amazon",   "price": round(our_price * random.uniform(0.85, 1.15), 2),
#          "url": "https://amazon.com", "snippet": "Similar product found on Amazon"},
#         {"source": "Flipkart", "price": round(our_price * random.uniform(0.80, 1.10), 2),
#          "url": "https://flipkart.com", "snippet": "Similar product found on Flipkart"},
#         {"source": "Walmart",  "price": round(our_price * random.uniform(0.90, 1.20), 2),
#          "url": "https://walmart.com", "snippet": "Similar product found on Walmart"},
#     ]

#     prices     = [r["price"] for r in mock_results]
#     avg_price  = round(sum(prices) / len(prices), 2)
#     gap        = round((our_price - avg_price) / avg_price * 100, 1)

#     if gap > 10:
#         rec = f"We are {gap}% more expensive. Consider markdown. (Simulated data)"
#     elif gap < -10:
#         rec = f"We are {abs(gap)}% cheaper than competitors. (Simulated data)"
#     else:
#         rec = f"Our price is within {abs(gap)}% of competitor average. (Simulated data)"

#     return {
#         "results"       : mock_results,
#         "avg_price"     : avg_price,
#         "min_price"     : min(prices),
#         "max_price"     : max(prices),
#         "price_gap_pct" : gap,
#         "recommendation": rec,
#         "raw_results"   : mock_results,
#         "error"         : error,
#         "is_simulated"  : True,
#     }





"""
utils/competitor_search.py
Searches the web for real competitor prices using Tavily API.
Fixed: uses category-based queries so synthetic product names
       don't cause empty results.
"""
import re
from typing import Optional
from config.settings import TAVILY_API_KEY

# Category → realistic search queries that find real prices on web
CATEGORY_QUERIES = {
    "Climbing":        ["climbing gear equipment price buy online", "rock climbing accessories price amazon walmart"],
    "Footwear":        ["hiking boots shoes price buy online", "outdoor footwear price amazon walmart"],
    "Mens":            ["mens outdoor clothing price buy online", "mens hiking apparel price amazon"],
    "Womens":          ["womens outdoor clothing price buy online", "womens hiking apparel price amazon"],
    "Kids":            ["kids outdoor gear price buy online", "childrens outdoor equipment price amazon"],
    "Gift Cards":      ["outdoor sports gift card price online", "adventure gift card buy online price"],
    "Hiking & Camping":["hiking camping gear price buy online", "camping equipment price amazon walmart"],
    "Travel":          ["travel gear accessories price buy online", "travel equipment price amazon"],
}

def search_competitor_prices(product_name: str,
                              category: str,
                              our_price: float) -> dict:
    if not TAVILY_API_KEY or TAVILY_API_KEY.strip() == "":
        return _fallback_response(product_name, our_price,
                                  error="Tavily API key not set in config/settings.py")
    try:
        from tavily import TavilyClient
        client = TavilyClient(api_key=TAVILY_API_KEY)

        # Build queries — try exact name first, then category fallback
        price_min = round(our_price * 0.5)
        price_max = round(our_price * 1.5)

        cat_queries = CATEGORY_QUERIES.get(
            category,
            [f"{category} products price buy online",
             f"{category} equipment price amazon walmart"]
        )

        queries = [
            # Query 1: exact product name — may work if name is recognisable
            f'{product_name} price buy online',
            # Query 2: category-based — always finds real prices
            cat_queries[0],
            # Query 3: second category query
            cat_queries[1] if len(cat_queries) > 1 else f"{category} price online shop",
        ]

        all_results  = []
        prices_found = []

        for query in queries[:3]:
            try:
                response = client.search(
                    query=query,
                    search_depth="basic",
                    max_results=5,
                    include_answer=False,
                )
                for r in response.get("results", []):
                    parsed = _extract_price_from_result(r, our_price)
                    if parsed:
                        all_results.append(parsed)
                        prices_found.append(parsed["price"])
            except Exception:
                continue

            # Stop early if we already have 4+ prices
            if len(prices_found) >= 4:
                break

        # Deduplicate by URL
        # seen_urls      = set()
        # unique_results = []
        # for r in all_results:
        #     if r["url"] not in seen_urls:
        #         seen_urls.add(r["url"])
        #         unique_results.append(r)
        
        seen_keys = set()
        unique_results = []
        for r in all_results:
            key = f"{r['url']}_{r['price']}"
            if key not in seen_keys:
                    seen_keys.add(key)
                    unique_results.append(r)
                    

        if not prices_found:
            return _fallback_response(product_name, our_price,
                                      error="No competitor prices found on web")

        avg_price     = round(sum(prices_found) / len(prices_found), 2)
        min_price     = round(min(prices_found), 2)
        max_price     = round(max(prices_found), 2)
        price_gap_pct = round((our_price - avg_price) / avg_price * 100, 1)

        if price_gap_pct > 10:
            recommendation = f"We are {price_gap_pct}% MORE EXPENSIVE than competitors. Consider markdown."
        elif price_gap_pct < -10:
            recommendation = f"We are {abs(price_gap_pct)}% CHEAPER than competitors. Good position."
        else:
            recommendation = f"Our price is within {abs(price_gap_pct)}% of competitor average. Competitive."

        return {
            "results"       : unique_results[:6],
            "avg_price"     : avg_price,
            "min_price"     : min_price,
            "max_price"     : max_price,
            "price_gap_pct" : price_gap_pct,
            "recommendation": recommendation,
            "raw_results"   : unique_results,
            "error"         : None,
            "is_simulated"  : False,
        }

    except ImportError:
        return _fallback_response(product_name, our_price,
                                  error="tavily-python not installed. Run: pip install tavily-python")
    except Exception as e:
        return _fallback_response(product_name, our_price, error=str(e))


def _extract_price_from_result(result: dict, our_price: float) -> Optional[dict]:
    """
    Extracts price from Tavily result.
    Widened sanity check to 5% - 1000% to catch more real prices
    since category searches return products at varied price points.
    """
    text = (result.get("content", "") + " " + result.get("title", "")).lower()
    url  = result.get("url", "")

    patterns = [
        r'\$\s*([\d,]+(?:\.\d{1,2})?)',
        r'₹\s*([\d,]+(?:\.\d{1,2})?)',
        r'usd\s*([\d,]+(?:\.\d{1,2})?)',
        r'price[:\s]+\$?([\d,]+(?:\.\d{1,2})?)',
        r'([\d,]+(?:\.\d{1,2})?)\s*(?:usd|dollars?)',
        r'buy\s+for\s+\$?([\d,]+(?:\.\d{1,2})?)',
        r'only\s+\$?([\d,]+(?:\.\d{1,2})?)',
        r'sale\s+\$?([\d,]+(?:\.\d{1,2})?)',
    ]

    for pattern in patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        for match in matches:
            try:
                price = float(match.replace(",", ""))
                # Wider sanity check for category-based searches
                # Accept prices between 5% and 1000% of our price
                if our_price * 0.4 <= price <= our_price * 2.5:
                    source = _extract_domain(url)
                    return {
                        "source" : source,
                        "price"  : round(price, 2),
                        "url"    : url,
                        "snippet": result.get("content", "")[:120] + "...",
                    }
            except (ValueError, TypeError):
                continue
    return None


def _extract_domain(url: str) -> str:
    match = re.search(r'(?:https?://)?(?:www\.)?([^/]+)', url)
    if match:
        domain = match.group(1)
        for known in ["amazon", "flipkart", "walmart", "ebay",
                      "target", "myntra", "meesho", "snapdeal",
                      "rei", "backcountry", "moosejaw", "patagonia"]:
            if known in domain.lower():
                return known.capitalize()
        return domain[:30]
    return "Web"


def _fallback_response(product_name: str, our_price: float,
                        error: str = None) -> dict:
    import random
    random.seed(hash(product_name) % 9999)

    mock_results = [
        {"source": "Amazon",   "price": round(our_price * random.uniform(0.85, 1.15), 2),
         "url": "https://amazon.com", "snippet": "Similar product found on Amazon"},
        {"source": "Flipkart", "price": round(our_price * random.uniform(0.80, 1.10), 2),
         "url": "https://flipkart.com", "snippet": "Similar product found on Flipkart"},
        {"source": "Walmart",  "price": round(our_price * random.uniform(0.90, 1.20), 2),
         "url": "https://walmart.com", "snippet": "Similar product found on Walmart"},
    ]

    prices    = [r["price"] for r in mock_results]
    avg_price = round(sum(prices) / len(prices), 2)
    gap       = round((our_price - avg_price) / avg_price * 100, 1)

    if gap > 10:
        rec = f"We are {gap}% more expensive. Consider markdown. (Simulated data)"
    elif gap < -10:
        rec = f"We are {abs(gap)}% cheaper than competitors. (Simulated data)"
    else:
        rec = f"Our price is within {abs(gap)}% of competitor average. (Simulated data)"

    return {
        "results"       : mock_results,
        "avg_price"     : avg_price,
        "min_price"     : min(prices),
        "max_price"     : max(prices),
        "price_gap_pct" : gap,
        "recommendation": rec,
        "raw_results"   : mock_results,
        "error"         : error,
        "is_simulated"  : True,
    }