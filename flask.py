from flask import Flask, request, jsonify
from app import generate_plan

app = Flask(__name__)

@app.route('/submit', methods=['POST'])
def plan_trip():
    if request.method == 'POST':
        data = request.get_json()

        # Extract user input from request object
        budget_from = data.get('budget_from')
        budget_to = data.get('budget_to')
        preferences = data.get('preferences')
        travel_date_from = data.get('travel_date_from')
        travel_date_to = data.get('travel_date_to')
        num_travelers = data.get('num_travelers')
        fears = data.get('fears')

        try:
            # Call your Python code and generate response
            response = generate_plan(budget_from, budget_to, preferences, travel_date_from, travel_date_to, num_travelers, fears)
        except Exception as e:
            # Handle exceptions, return error message
            response = {'error': str(e)}

        # Return the generated itinerary or error message as a JSON response
        return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
