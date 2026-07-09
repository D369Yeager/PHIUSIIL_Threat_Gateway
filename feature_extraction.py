import re
from urllib.parse import urlparse

# Pre-calculated statistical baseline character probabilities from the paper (Section 3.1.4)
LEGIT_CHAR_PROB_MAP = {
    'a': 0.078, 'b': 0.012, 'c': 0.045, 'd': 0.031, 'e': 0.079, 'f': 0.018, 
    'g': 0.022, 'h': 0.028, 'i': 0.055, 'j': 0.005, 'k': 0.009, 'l': 0.041, 
    'm': 0.024, 'n': 0.048, 'o': 0.065, 'p': 0.029, 'q': 0.002, 'r': 0.062, 
    's': 0.052, 't': 0.063, 'u': 0.021, 'v': 0.011, 'w': 0.015, 'x': 0.004, 
    'y': 0.016, 'z': 0.003,
    '0': 0.007, '1': 0.008, '2': 0.007, '3': 0.005, '4': 0.004, '5': 0.004, 
    '6': 0.003, '7': 0.003, '8': 0.002, '9': 0.002,
    '.': 0.082, '-': 0.025, '_': 0.005, '/': 0.095
}

def extract_root_and_tld(url: str):
    """Parses out the domain host, isolated network path, and target TLD string extension."""
    parsed = urlparse(url if "://" in url else f"http://{url}")
    domain = parsed.netloc.split(':')[0].lower()
    if domain.startswith("www."):
        domain = domain[4:]
    parts = domain.split('.')
    tld = parts[-1] if len(parts) > 1 else ""
    return domain, tld

def calculate_continuation_rate(url: str) -> float:
    """Computes the continuous layout cluster weight (Section 3.1.4)."""
    if not url:
        return 0.0
    alpha_sequences = re.findall(r'[a-zA-Z]+', url)
    digit_sequences = re.findall(r'[0-9]+', url)
    special_sequences = re.findall(r'[^a-zA-Z0-9]+', url)
    
    max_alpha = max([len(s) for s in alpha_sequences]) if alpha_sequences else 0
    max_digit = max([len(s) for s in digit_sequences]) if digit_sequences else 0
    max_special = max([len(s) for s in special_sequences]) if special_sequences else 0
    
    return (max_alpha + max_digit + max_special) / len(url)

def calculate_char_prob(url: str) -> float:
    """Implements Equation 1 to evaluate string composition likelihood."""
    url_lower = url.lower()
    total_prob = sum(LEGIT_CHAR_PROB_MAP.get(char, 0.001) for char in url_lower)
    return total_prob / len(url) if url else 0.0

def extract_lexical_features(url: str) -> dict:

    # Normalize FIRST before computing any features
    if "://" not in url:
        url = "http://" + url      # ← This is the actual fix
    domain, tld = extract_root_and_tld(url)
    url_lower = url.lower()
    # ... rest of function unchanged

    """
    Day 6 & 7 Complete Upgraded Engine: Extracts lexical and calculated indicators.
    Matches the exact dataset columns layout shared in the spreadsheet.
    """
    domain, tld = extract_root_and_tld(url)
    url_lower = url.lower()
    
    features = {}
    
    # Structural metric properties
    features['URLLength'] = len(url)
    features['DomainLength'] = len(domain)
    features['IsDomainIP'] = 1 if re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", domain) else 0
    
    # TLD categorical checks matching your dataset columns
    features['TLD_com'] = 1 if tld == 'com' else 0
    features['TLD_org'] = 1 if tld == 'org' else 0
    features['TLD_net'] = 1 if tld == 'net' else 0
    features['TLD_info'] = 1 if tld == 'info' else 0
    
    # Syntactic counters
    features['NoOfSubDomain'] = max(0, domain.count('.') - 1)
    features['NoOfObfuscatedChar'] = len(re.findall(r'%[0-9a-fA-F]{2}', url))
    features['HasObfuscatedChar'] = 1 if features['NoOfObfuscatedChar'] > 0 else 0
    features['NoOfLetters'] = sum(c.isalpha() for c in url)
    features['NoOfDegits'] = sum(c.isdigit() for c in url) # Typed 'NoOfDegits' exactly to match dataset column header
    features['DegitRatio'] = features['NoOfDegits'] / len(url) if len(url) > 0 else 0
    features['NoOfQMark'] = url.count('?')
    features['NoOfEquals'] = url.count('=')
    features['NoOfAmpere'] = url.count('&') # Typed 'NoOfAmpere' exactly to match dataset column header
    features['NoOfOtherSpecialChar'] = sum(not (c.isalnum() or c in './_:-') for c in url)
    features['IsHTTPS'] = 1 if url_lower.startswith('https') else 0
    
    # Statistical derived values
    features['CharContinuationRate'] = calculate_continuation_rate(url)
    features['TLDLegitimateProb'] = LEGIT_CHAR_PROB_MAP.get(tld, 0.001)
    features['URLCharProb'] = calculate_char_prob(url)
    
    return features

# =====================================================================
# Verification Testing Block
# =====================================================================
if __name__ == "__main__":
    test_url = "https://sub.login.paypal-security-update.com/signin?session=abc%20&auth=1"
    
    print("=" * 65)
    print("  INTEGRATED URL LEXICAL FEATURE MINING ENGINE")
    print("=" * 65)
    
    lexical_data = extract_lexical_features(test_url)
    for key, val in lexical_data.items():
        print(f"    {key:<22} : {val}")
    print("=" * 65)