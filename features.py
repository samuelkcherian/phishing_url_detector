# features.py
import re
import tldextract
from urllib.parse import urlparse
from difflib import SequenceMatcher

# Common phishing indicators
suspicious_tlds = ['xyz', 'tk', 'ml', 'cf', 'gq', 'top', 'buzz']
known_brands = ['paypal', 'google', 'apple', 'amazon', 'facebook', 'microsoft', 'steam']

shorteners = ['bit.ly', 'tinyurl.com', 'goo.gl', 'ow.ly', 't.co', 'rebrand.ly']

def extract_features(url):
    features = {}

    # Basic features
    features['url_length'] = len(url)
    features['has_ip'] = bool(re.search(r'\d{1,3}(?:\.\d{1,3}){3}', url))
    features['has_https'] = urlparse(url).scheme == 'https'
    features['count_dots'] = url.count('.')
    features['has_at_symbol'] = '@' in url
    features['has_hyphen'] = '-' in url
    features['has_double_slash'] = url.count('//') > 1

    ext = tldextract.extract(url)
    features['count_subdomains'] = len(ext.subdomain.split('.')) if ext.subdomain else 0
    features['suspicious_tld'] = ext.suffix.lower() in suspicious_tlds

    # 🆕 Advanced features
    features['has_login'] = 'login' in url.lower() or 'signin' in url.lower()
    features['has_brand'] = any(brand in url.lower() for brand in known_brands)
    features['is_shortened'] = any(short in url for short in shorteners)
    features['digit_count'] = sum(c.isdigit() for c in url)
    features['special_char_count'] = sum(c in '@%:/?#&=+-$' for c in url)

    # Levenshtein similarity to known brands
    domain = f"{ext.domain}.{ext.suffix}"
    scores = [SequenceMatcher(None, domain, brand + ".com").ratio() for brand in known_brands]
    features['levenshtein_score'] = max(scores)

    return list(features.values())

def get_feature_names():
    return [
        'url_length', 'has_ip', 'has_https', 'count_dots',
        'has_at_symbol', 'has_hyphen', 'has_double_slash',
        'count_subdomains', 'suspicious_tld',
        'has_login', 'has_brand', 'is_shortened',
        'digit_count', 'special_char_count',
        'levenshtein_score'
    ]
