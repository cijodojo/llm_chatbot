import os
import json
import tqdm
import numpy as np
from db import vector_db
from sklearn.preprocessing import normalize
from fastapi import UploadFile
from utlis import utility
from sentence_transformers import SentenceTransformer

class ChatBot:
  def __init__(self) -> None:
    self.embeddings = []
    self.threshold = 0.4
    self.qa_answers = []
    self.load_answers()
    self.model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2')
    
  # load answer when the application starts
  def load_answers(self):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    data_file = os.path.join(BASE_DIR, '../dataset/ecommerce-dataset.json')
    with open(data_file, 'r') as f:
      qa_data = json.load(f)
    self.qa_answers = [items['response'] for items in qa_data]
    
  async def genrate_embedding(self, file: UploadFile):
    index_file_path = '../app/indices/ecommerce_indice.index'
    file_contents = await file.read()
    questions = utility.load_training_file(file_contents)
    if os.path.exists(index_file_path):
      return "Already Index Present..!!!"
    else:
      for question in tqdm.tqdm(questions, desc="embedding"):
        embedding = self.model.encode([utility.clear_text(question)], convert_to_tensor=False)
        self.embeddings.append(embedding[0])
      index = vector_db.build_faiss_index(np.array(self.embeddings))
      vector_db.save_faiss_index(index, index_file_path)
      
  def chatbot(self, query):
    index_file_path = '../app/indices/ecommerce_indice.index'
    query_embedding = self.model.encode([utility.clear_text(query.query)], convert_to_tensor=False)
    norm_query_embedding = normalize(np.array(query_embedding), norm='l2')
    index = vector_db.load_faiss_index(index_file_path)
    similiarty_score, indices = index.search(norm_query_embedding, k=1)
    closest_question_idx = indices[0][0]
    print("similiarty_score:", similiarty_score[0])
    print("closest_question_idx:", closest_question_idx)
    if similiarty_score[0][0] > self.threshold:
      response_text = self.qa_answers[closest_question_idx]
    else:
      response_text = 'Sorry, Please re-pharse your answer'
    
    # final_answer = utility.format_response(response_text) 
    final_answer = response_text
    return final_answer
        
chatbotcontroller = ChatBot()
  