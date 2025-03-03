import logging

# Set up logging for detailed output
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


def input_score(prompt):
    """
    Prompts the user for a score and returns a float if valid; returns None if empty.
    """
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
    """
    Calculates the required score on the RegFinal exam.
    Calculation: RegTotal = (RegTerm * 60%) + (RegFinal * 40%)
    => RegFinal = (target - 0.6 * regterm) / 0.4
    """
    required = (target - 0.6 * regterm) / 0.4
    return required


class Subject:
    def __init__(self):
        self.name = input("Enter subject name: ")
        self.teacher = input("Enter teacher's name: ")

        hours_input = input("Enter total hours: ")
        self.hours = float(hours_input) if hours_input else 0.0

        credits_input = input("Enter number of credits: ")
        self.credits = float(credits_input) if credits_input else 0.0

        while True:
            self.academic_period_type = input("Enter academic period type (semester/trimester): ").strip().lower()
            if self.academic_period_type in ["semester", "trimester"]:
                break
            else:
                print("Invalid academic period type. Please enter 'semester' or 'trimester'.")

        while True:
            target_input = input("Enter your target final score (70 for scholarship, 90 for increased scholarship): ")
            if not target_input:
                print("Target score cannot be empty. Please enter a value between 0 and 100.")
                continue
            try:
                self.target = float(target_input)
                if 0 <= self.target <= 100:
                    break
                else:
                    print("Invalid target. Please enter a value between 0 and 100.")
            except ValueError:
                print("Invalid input. Please enter a number.")

        self.weights = self.set_default_weights()
        self.reg_mid = None
        self.reg_end = None
        self.reg_final = None

    def set_default_weights(self):
        if self.academic_period_type == "trimester":
            # Default weights: RegMid 30%, RegEnd 30%, RegFinal 40%
            return {"reg_mid": 30, "reg_end": 30, "reg_final": 40}
        elif self.academic_period_type == "semester":
            # For semester: Midterm 40%, Final 60%
            return {"reg_mid": 40, "reg_final": 60}
        else:
            return {"reg_mid": 30, "reg_end": 30, "reg_final": 40}

    def input_scores(self):
        if self.academic_period_type == "trimester":
            self.reg_mid = calculate_composite_score("RegMid (e.g., Midterm + Assignments)")
            self.reg_end = calculate_composite_score("RegEnd (e.g., Endterm + Assignments)")
        elif self.academic_period_type == "semester":
            self.reg_mid = calculate_composite_score("Midterm (including any assignments)")
        self.reg_final = input_score("Enter your RegFinal (Final exam) score (or leave blank if unknown): ")

    def calculate_reg_term(self):
        if self.academic_period_type == "trimester":
            return (self.reg_mid + self.reg_end) / 2
        elif self.academic_period_type == "semester":
            return self.reg_mid

    def calculate_reg_total(self):
        reg_term = self.calculate_reg_term()
        if self.academic_period_type == "trimester":
            return reg_term * 0.6 + self.reg_final * 0.4
        elif self.academic_period_type == "semester":
            return self.reg_mid * (self.weights["reg_mid"] / 100) + self.reg_final * (self.weights["reg_final"] / 100)

    def display_progress(self):
        print(f"\nSubject: {self.name}")
        print(f"Teacher: {self.teacher}")
        print(f"Credits: {self.credits}, Hours: {self.hours}")
        if self.reg_mid is not None:
            print(f"RegMid: {self.reg_mid:.2f}")
        if self.academic_period_type == "trimester" and self.reg_end is not None:
            print(f"RegEnd: {self.reg_end:.2f}")

        # Calculating RegTerm
        reg_term = self.calculate_reg_term()
        print(f"\nCalculated RegTerm: {reg_term:.2f}%")

        # Printing RegFinal score
        if self.reg_final is not None:
            print(f"RegFinal (Final exam score): {self.reg_final:.2f}")
            # Calculating RegTotal
            reg_total = self.calculate_reg_total()
            print(f"Calculated RegTotal: {reg_total:.2f}%")

            if reg_total >= self.target:
                print(f"🎉 Congratulations! You have achieved your target score of {self.target:.2f}% or higher. 🎉")
            else:
                # If RegTotal is lower than target, calculating required points for Final exam
                required = calculate_required_regfinal(reg_term, self.target)
                effective_required = max(required, 50)  # Minimal requirement for passing Final exam is 50%
                print(
                    f"✅ To reach your target of {self.target:.2f}%, you need to score at least {effective_required:.2f}% on the Final Exam. ✅")
        else:
            print("RegFinal (Final exam score): Not provided")
            required = calculate_required_regfinal(reg_term, self.target)
            if required > 100:
                print(
                    f"⚠️ Unfortunately, with your current RegTerm score, it is impossible to reach your target of {self.target:.2f}% even with a perfect Final exam score. ⚠️")
            else:
                effective_required = max(required, 50)
                print(
                    f"✅ To reach your target of {self.target:.2f}%, you need to score at least {effective_required:.2f}% on the Final Exam. ✅")

        # Showcasing calculation breakdown foк clarity
        print("\nCalculation breakdown:")
        print("RegTotal = (RegTerm × 60%) + (RegFinal × 40%)")
        print(f"→ RegTerm × 60% = {reg_term:.2f} × 0.6 = {reg_term * 0.6:.2f}")
        if self.reg_final is not None:
            print(f"→ RegMid")
            print(f"→ RegFinal × 40% = {self.reg_final:.2f} × 0.4 = {self.reg_final * 0.4:.2f}")
            print(f"→ RegTotal = ({reg_term:.2f} × 60%) + ({self.reg_final:.2f} × 40%) = {reg_total}")
        else:
            print("→ RegFinal × 40%: Not provided")



def main():
    print("=== Subject Assessment & Progress Tracker ===")
    subject = Subject()
    subject.input_scores()
    subject.display_progress()


if __name__ == "__main__":
    main()
