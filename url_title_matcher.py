 # URL-TITLE-MATCH-SCORE : A Score that resembles how closely an url matches with the title.    

url = 'https://verify-user-payment.ru'
title = 'Paypal Login'
tset = title.split()
txt_url = url.lower()
txt_url = url.replace("https://" , "")
txt_url = url.replace("http://" , "")
txt_url = url.replace("www:" , "")
# Removing everything after /

if '/' in txt_url:
    txt_url = txt_url.split()[0]

# Removing TLD
if '.' in txt_url:
    txt_url = '.'.join(txt_url.split('.')[-1])

title = title.lower()
t_set = title.split()
def match_url_score(url , t_set):
    score = 0
    base_score = 100 / (len(txt_url))
    # compare each title word now:

    for element in t_set:

        if element in txt_url:
            score += base_score * len(element)

            # remove the matched word so it does not counted again:
            txt_url.replace(element , '' , 1)

        if score > 99.99:
            score = 100
    return round(score , 2)
if __name__ == "__main__":    
    print(match_url_score(txt_url , t_set))


