import re
from bs4 import BeautifulSoup
def extract_html_structural_features(raw_html: str, soup: BeautifulSoup) -> dict:
    """
    Day 10 & 11 Final Production Engine.
    Ensures ALL missing columns including NoOfCSS are explicitly returned.
    """
    features = {}
    
    if not raw_html or not soup:
        keys = [
            'LineLength', 'LargestLineLength', 'HasTitle', 'HasFavicon', 'Robots', 'IsResponsive',
            'NoOfURLRedirect', 'NoOfSelfRef', 'NoOfEmptyRef', 'NoOfExternalRef', 'HasDescription',
            'HasKeywords', 'HasAuthor', 'NoOfJS', 'NoOfCSS', 'NoOfPopup', 'NoOfiFrame', 
            'HasExternalFormSubmit', 'HasSocialNet', 'HasSubmitButton', 'HasHiddenFields', 
            'HasPasswordField', 'NoOfImage'
        ]
        return {k: 0.0 for k in keys}

    # 1. Line formatting structural properties
    lines = raw_html.splitlines()
    features['LineLength'] = float(len(lines))
    features['LargestLineLength'] = float(max([len(line) for line in lines]) if lines else 0)
    
    # 2. Header DOM element validation
    title_tag = soup.find('title')
    features['HasTitle'] = 1.0 if (title_tag and title_tag.text.strip()) else 0.0
    features['HasFavicon'] = 1.0 if soup.find('link', rel=lambda x: x and 'icon' in x.lower()) else 0.0
    features['Robots'] = 1.0 if soup.find('meta', attrs={"name": "robots"}) else 0.0
    
    # 3. Device visibility rules
    viewport = soup.find('meta', attrs={"name": "viewport"})
    features['IsResponsive'] = 1.0 if viewport else 0.0
    
    # 4. Page redirection triggers
    redirect_patterns = [r'window\.location\.href', r'window\.location\.replace', r'http-equiv=["\']refresh["\']']
    features['NoOfURLRedirect'] = float(sum(len(re.findall(pat, raw_html, re.IGNORECASE)) for pat in redirect_patterns))
    
    # 5. Extract reference tracking vectors
    self_ref, empty_ref, external_ref = 0, 0, 0
    for link in soup.find_all('a', href=True):
        href = link.get('href', '').strip()
        if not href or href == "#" or href.lower().startswith("javascript:"):
            empty_ref += 1
        elif href.startswith("/") or "google.com" in href:
            self_ref += 1
        else:
            external_ref += 1
            
    features['NoOfSelfRef'] = float(self_ref)
    features['NoOfEmptyRef'] = float(empty_ref)
    features['NoOfExternalRef'] = float(external_ref)
    
    # Meta tag existence verifications
    features['HasDescription'] = 1.0 if soup.find('meta', attrs={"name": "description"}) else 0.0
    features['HasKeywords'] = 1.0 if soup.find('meta', attrs={"name": "keywords"}) else 0.0
    features['HasAuthor'] = 1.0 if soup.find('meta', attrs={"name": "author"}) else 0.0
    
    # 6. Interactive components, style sheets, and scripts
    features['NoOfJS'] = float(len(soup.find_all('script')))
    
    # 🌟 CORE FIX: Explicitly assign NoOfCSS to the feature dictionary output mapping!
    features['NoOfCSS'] = float(len(soup.find_all('style')) + len(soup.find_all('link', rel='stylesheet')))
    
    features['NoOfPopup'] = float(len(re.findall(r'window\.open\s*\(', raw_html)))
    features['NoOfiFrame'] = float(len(soup.find_all('iframe')))
    
    # 7. Security form actions
    features['HasExternalFormSubmit'] = 0.0
    for form in soup.find_all('form'):
        action = form.get('action', '')
        if action.startswith('http'):
            features['HasExternalFormSubmit'] = 1.0
            break
            
    # 8. Social presence tokens
    social_links = ['facebook.com', 'twitter.com', 'linkedin.com', 'instagram.com', 'youtube.com']
    features['HasSocialNet'] = 1.0 if any(s in raw_html.lower() for s in social_links) else 0.0
    
    # 9. Form layouts matching dataset columns
    features['HasSubmitButton'] = 1.0 if (soup.find('input', type='submit') or soup.find('button', type='submit') or soup.find('input', type='button')) else 0.0
    features['HasHiddenFields'] = 1.0 if soup.find('input', type='hidden') else 0.0
    features['HasPasswordField'] = 1.0 if soup.find('input', type='password') else 0.0
    features['NoOfImage'] = float(len(soup.find_all('img')))
    
    return features