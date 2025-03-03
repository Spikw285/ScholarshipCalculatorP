import logging

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

def input_score(prompt):
    score_input = input(prompt).strip()
    try:
        return float(score_input) if score_input else None
    except ValueError:
        return None

def calculate_composite_score(component_name):
    """
    Calculates a composite score (e.g., for RegMid or RegEnd).
    The user can either enter a single final score or break it down into several components with specified weights.
    Normalization is applied if the total weight does not equal 100%.
    """
    while True:
        mode = input(f"Do you want to enter a single final score for {component_name}? (y/n): ").strip().lower()
        if mode in ['y', 'n']:
            break
        else:
            print("Invalid input. Please enter 'y' or 'n'.")

    if mode == 'y':
        while True:
            score = input_score(f"Enter the score for {component_name} (0-100): ")
            if score is not None:
                if 0 <= score <= 100:
                    return score
                else:
                    print("Score must be between 0 and 100. Please try again.")
            else:
                print("Score cannot be empty. Please enter a value between 0 and 100.")
    else:
        # Ask for number of components
        while True:
            n_input = input(f"How many components does {component_name} include?: ")
            if not n_input:
                print("Number of components cannot be empty. Please enter a positive integer.")
                continue
            try:
                n = int(n_input)
                if n > 0:
                    break
                else:
                    print("Number of components must be a positive integer. Please try again.")
            except ValueError:
                print("Invalid input. Please enter a positive integer.")

        total_weight = 0
        weighted_sum = 0
        for i in range(n):
            print(f"\nComponent {i + 1}:")
            # Input weight for this component
            while True:
                weight_input = input("  Enter the weight of the component (in percent): ")
                if not weight_input:
                    print("Weight cannot be empty. Please enter a positive number.")
                    continue
                try:
                    weight = float(weight_input)
                    if weight > 0:
                        break
                    else:
                        print("Weight must be a positive number. Please try again.")
                except ValueError:
                    print("Invalid input. Please enter a number.")
            # Input score for this component
            while True:
                score = input_score("  Enter the score for the component (0-100): ")
                if score is not None:
                    if 0 <= score <= 100:
                        break
                    else:
                        print("Score must be between 0 and 100. Please try again.")
                else:
                    print("Score cannot be empty. Please enter a value between 0 and 100.")
            total_weight += weight
            weighted_sum += score * weight

        if total_weight != 100:
            print(f"\nThe total weight is {total_weight}%, expected 100%. Normalizing the score.")
            composite_score = weighted_sum / total_weight
        else:
            composite_score = weighted_sum / 100
        logging.info(f"{component_name} composite score: {composite_score:.2f}")
        return composite_score

def calculate_required_regfinal(regterm, target):
    required = (target - 0.6 * regterm) / 0.4
    return required
