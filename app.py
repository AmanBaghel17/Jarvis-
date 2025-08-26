from flask import Flask, render_template, request
import main  # Import your assistant logic (processCommand)

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    response = ""
    if request.method == 'POST':
        user_input = request.form['command']
        # Call your assistant logic and capture the response
        # If processCommand returns None, set a default response
        result = main.processCommand(user_input)
        response = result if result else "Command processed. Check for audio or other output."
    return render_template('index.html', response=response)

if __name__ == '__main__':
    app.run(debug=True)
