from flask import Flask, jsonify
import boto3
import pandas as pd

app = Flask(__name__)

@app.route("/")
def home():
    return "Welcome to the Flask app"
s3 = boto3.client('s3')
BUCKET_NAME = "my-data-project-bucket"  # Replace with your bucket name
FILE_NAME = "merged_dataset.csv"  # Replace with your file name

@app.route('/data', methods=['GET'])
def get_data():
    try:
        # Get the file from S3
        obj = s3.get_object(Bucket=BUCKET_NAME, Key=FILE_NAME)
        df = pd.read_csv(obj['Body'])

        # Convert to JSON
        data = df.to_dict(orient='records')
        return jsonify(data)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
