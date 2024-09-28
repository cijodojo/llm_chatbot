import json
import csv

class Utility:
  
  # clean the training data
  def clear_text(self, text):
    return text.lower().strip()
  
  # load training/embedding input_file
  def load_training_file(self, file_content):
    data = json.loads(file_content)
    questions = [item['question'] for item in data]
    return questions
  
  def format_response(self, response_text):
    response_lines = response_text.split('\n')
    response_lines = [line.strip() for line in response_lines if line.strip()]
    return "\n".join(response_lines)
  
utility = Utility()