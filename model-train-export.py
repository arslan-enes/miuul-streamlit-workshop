# Import necessary libraries
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import plotly.express as px
import joblib

# Load Gapminder dataset from Plotly Express
df = px.data.gapminder()

# Select features (X) and target variable (y)
X = df[['year', 'pop', 'gdpPercap']]
y = df['lifeExp']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create and train the model (Random Forest Regressor in this case)
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Make predictions on the test set
y_pred = model.predict(X_test)

# Evaluate the model
mse = mean_squared_error(y_test, y_pred)
print(f'Mean Squared Error: {mse}')

# Export the trained model using joblib
model_filename = 'gapminder_model.joblib'
joblib.dump(model, model_filename)
print(f'Model saved as {model_filename}')
