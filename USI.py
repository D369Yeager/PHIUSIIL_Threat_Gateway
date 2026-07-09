# This is URL Similarity Index Calculation Program : 
# It calculated the similarity between URL's (The source (to be check) and the target (real legit ones))

def get_min(src : str , tar : str):
    if len(src) <= len(tar):
        return src , tar  , len(src)
    else:
        return tar , src , len(tar)

def url_similarity_index(src : str , tar : str):
    if(src == tar):   #The edge case.
        return 100.0
    X , Y , n = get_min(src , tar)
    
    N = max(len(src) , len(tar))
    SI = 0.0
    base_value = 50/N
    nsum = N*(N+1)/2

    i = 0
    while i<n and i < len(X) and i < len(Y):
        if X[i] == Y[i]:
            SI += base_value + 50*(N-i)/nsum
            i+= 1
        else:
            Y = Y[:i] + Y[i+1 : ]
            X,Y,n = get_min(X,Y) 

            if len(X) == 0 or len(Y) == 0:
                break
    return SI


url1 = "google.com"
url2 = "googl1.com"

score = url_similarity_index(url1, url2)

print(f"Similarity Index = {score}")



def phase1_gateway_router(url_to_test : str , trusted_reference: str):
    #Computing the similarity index first:-
    usi_score = url_similarity_index(url_to_test , trusted_reference)
    
    #Define the payload structure to pass down the pipeline
    decision_payload = {
        'url' : url_to_test,
        'usi_score' : usi_score,
        'action' : "",
        'route to Phase-2' : False,
        'log_message' : ""
    }

    # Applying the PHIUSIIL decision boundaries
    if usi_score == 100:
        decision_payload['action'] = "ALLOW"
        decision_payload['log_message'] = "SAFE : Exact domain registry matched."
    elif 80 <= usi_score < 100:
        decision_payload['action'] = "Blocked"
        decision_payload['log_message'] = f"Critical Security ALert : Visula clone isolated {usi_score:.2f}"  
    else:
        decision_payload['action'] = "Divert"
        decision_payload['log_message'] = f"Doubtful (USI:{usi_score:.2f}. Initialising HTML Parsing and ML feature extraction)."
        
    return decision_payload

## Verification Execution:
if __name__ == "__main__":
    trusted_registry = "paypal.com"
    incoming_traffic = ['paypal.com' ,'Paypal.com' , 'paypa1.com' , 'paypal-update-login-setting.com']

    print('_'*70)
    print(f"Live Gateway firewall monitor | Reference : {trusted_registry}")
    print('_'*70)

    for incoming_url in incoming_traffic:
        result = phase1_gateway_router(incoming_url , trusted_registry)
        print(f"INCOMING : {result['url']}")
        print(f"ACTION : {result['action']}")
        print(f"MESSAGE : {result['log_message']}")
        print('+'*80)