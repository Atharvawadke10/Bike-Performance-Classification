🏍️ Bike Performance Classification Based on Rider Behavior
📘 Project Overview

This project aims to classify bike performance and rider behavior using Machine Learning techniques.
Rider actions such as Acceleration, Braking, and turning are analyzed using data from sensors (or simulated data) to determine whether the rider is Smooth, Aggressive, or Risky.

The goal is to help riders understand their riding style, improve safety, and optimize bike performance through intelligent insights.



🎯 Objectives

1. To classify rider behavior into categories like Smooth, Aggressive, and Risky.

2. To analyze acceleration, braking, and turning patterns to evaluate performance.

3. To develop a predictive model that identifies riding style in real-time.

4. To visualize results using an interactive dashboard.




⚙️ System Architecture

1. Data Processing & Feature Engineering:

Mean and maximum acceleration

Jerk (rate of change of acceleration)

Average speed & speed variance

Braking frequency and turn rate

2. Model Development:

Algorithms used: Random Forest, XGBoost, SVM

Data split: 80% training, 20% testing

Evaluation Metrics: Accuracy, Precision, Recall, F1-score

3. Implementation:

Python script for training and prediction

Streamlit dashboard for visualization



| Category             | Tools / Libraries                                        |
| -------------------- | -------------------------------------------------------- |
| Programming Language | Python                                                   |
| Data Processing      | pandas, numpy                                            |
| Machine Learning     | scikit-learn, xgboost                                    |
| Visualization        | matplotlib, seaborn, Streamlit                           |




📊 Results

Random Forest achieved ~92% accuracy in classifying rider behavior.

Distinct patterns were identified:

Aggressive riders → High acceleration variance & frequent braking.

Smooth riders → Consistent speed, low jerk values.

Risky riders → Extreme tilt angles and high-speed fluctuations.
