from sklearn.naive_bayes import BernoulliNB
from sklearn.linear_model import PassiveAggressiveClassifier , SGDClassifier

def initialize_online_ensemble():
    """
    Day 13 Core Target: Instantiate the Phase 2 Streaming Ensemble Matrix
    using the hyperparameter boundaries detailed in Sections 4.2.1 & 4.2.2.
    """
    #1. Bernoulli Naive Bayes Core Configuration
    # alpha = 0.01 provides laplace soothing for the features not available for the initial rows

    model_nb = BernoulliNB(
        alpha = 0.01,
        binarize = 0.0,
        fit_prior = False
    )

    #2. Passive Aggresive Classifier Configuration
    # C = 0.5 sets the aggressiveness penalty step multiplier during margin error

    model_pa = PassiveAggressiveClassifier(
        C = 5.0,
        fit_intercept = False,
        max_iter = 1,
        n_iter_no_change = 50,
        random_state = 42
    )

    # 3. Stochastic Gradient Descent Classifier Configuration
    # loss='log_loss' configures the estimator as an online Logistic Regression model
    model_sgd = SGDClassifier(
        loss='log_loss', 
        alpha=0.0001, 
        learning_rate='optimal',
        eta0=100.0,              # Initial multiplier step tracking parameter from the paper
        max_iter=1,              # Enforces strict 1-epoch stream-based weight updates
        n_iter_no_change=50, 
        random_state=42
    )

    # Package into an easily loopable ensemble dictionary
    ensemble_matrix = {
        'NaiveBayes' : model_nb,
        'PassiveAggressive' : model_pa,
        'SGDClassifier' : model_sgd
    }
    return ensemble_matrix

# =====================================================================
# Verification Execution
# =====================================================================
if __name__ == "__main__":
    print("=" * 65)
    print("  DAY 13: ENSEMBLE MODEL INITIALIZATION MONITOR")
    print("=" * 65)
    
    models = initialize_online_ensemble()
    
    print("  [SUCCESS] All three streaming models configured and locked!")
    for name, obj in models.items():
        print(f"    -> {name:<18} : Hyperparameters mapped to Section 4.2.")
        
    print("=" * 65)