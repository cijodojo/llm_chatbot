# How to run the files

Prerequisites:
  Python 3.10 or higher must be installed.

Steps:

1. Clone the Repository:
  git clone <repository_url>

2. Set Up a Virtual Environment (Recommended): For better isolation and dependency management, it's recommended to create a Python virtual environment:

  # python -m venv venv

  Activate the virtual environment:
  On macOS/Linux
    # source </path/to/venv>/bin/activate
  On Windows
    # .\venv\Scripts\activate

  Once the virtual environment is activated, install the required packages by running:
  pip install -r requirements.txt

3. Start the Application: To start the application, run the following command:
  python server.py

4. Generate Training Data: To create the training data, which will train the model based on user queries, use any REST client (e.g., Postman) to hit the following API:

  POST http://0.0.0.0:3333/generate_embedding

  a. This is a POST request with a multipart/form-data content type.
  b. In Postman (or similar clients), select form-data under the Body tab.
  c. The payload key should be file, and you will need to upload a training file in .json format from the /dataset folder.
  
  ## Notes:-
    a. The time required to generate indices depends on your CPU. For high-performance CPUs, this process takes approximately 15-20 minutes; for lower configurations, it may take longer.
    b. To skip this process, you can download pre-generated indices from the following link:
      https://drive.google.com/drive/folders/1XYr4QD9hhxRRuJOOskr_TA42mbZQhLiE?usp=drive_link
    c. Download the files and place them inside the /indices folder to proceed with the search functionality.

5. Update Dataset for Chatbot Testing:
  Update the app/controllers/chatbot_controller.py file with the dataset you want to test (currently supports insurance and e-commerce datasets). Modify the following variables:
  
  a. "index_file_path": Set this to the desired .index file located in the /indices directory.
  a. "data_file": Set this to the desired .json file located in the /dataset directory.

6. Interact with the Chatbot: To interact with the chatbot and get the desired output, use the following API:

  POST http://0.0.0.0:3333/chatbot

  a. This is a POST request with application/json as the content type.
  b. The payload format is as follows
    {
      "query":"<your question>"
    }

7. If you want to run it with UI, Please load the index.html file present in frontend directory.



# Flow Of the Code: - 


Technology Used: - 

I have used the below technology for building this "question-answering system" 

  1. Python as the main programming language,  
  2. Fast API for building the rest Apis,
  3. Used normalize function form sklearn library to normalized vector for FAISS-DB 
  4. Sentence-transformer is used as the LLM model here specially I have used hugging face "all-mpnet-base-v2" model. 
  5. FAISS is used as vector DB 
  6. Vanilla JS for building simple web Ui for asking the question-answer 

 

The code is structed into two parts Backend and Frontend: - 

  
## Backend:-(containing all the backend logic), this contained many different directory 

1. requirement.txt -> this file contains all the necessary packages required by the backend application 

2. server.py -> this is the starting point of my backend application. in this file I have initialized the fast Api and included the router. The router handles all the incoming requests and passes it to the necessary controller to give the response. in this I have also used "Cors middleware" to allow this backend application to interact with the frontend Ui. 

3. dataset -> this directory contains the dataset which is required for question and answer 

  The dataset is converted from .csv to. Json format. Since our data was well structed with proper level of question and answer. it is better to work with Json. Also, when we have such well structed data the Json format is considered better for training the model where we can properly pass all the required data for model training and embeddings. 

  for this I have used python script of converting csv to Json. The script is attached with the name of csv_to_json.py. It is a simple script where I have loaded the required package (csv and Json) and there is one function named "csv_to_json" which accepts two parameters which are input “csv file path” and output “Json file path.” Then using the open method, we open the csv file and using “csv.DictReader()” method read the content of csv file one by one and store it in a list. Once all data is stored in the list then using “json.dumps()” method we dump all data into Json format with proper indentation. 


4. db. -> this directory contains all the vector db. (Faiss) related function. 

  The reason I have used Faiss as vector db. is, since our data is well structured, I have used the "semantic-search" approach which is based on similarity-based retrieval of answers.
  also, it is designed to handle efficient similarity search in high-dimensional spaces, in our case the "all-mpnet-bave-v2" model is 768 dims, so it is again a desirable choice. 

  ###The db_config.py file handles all building, saving, and loading of Faiss db. 

    the “build_faiss_index” function takes embedding as input. embeddings are the vector data generated by the model which in our case is a 2D array of vectors. Since Faiss by default does not offer cosine similarity function, we normalize the embedding so that inner product search behaves like cosine similarity. Then we set the dimensions of our Faiss index. Here I have used “IndexFlatIP()” index of Faiss, this is optimized for fast similarity searches using inner product similarity which we are using as cosine to get more accurate result. 

    the “save_faiss_index,” save our created index into the desired location that can be loaded in future, so we do not create indexing repeatedly

    the “load_faiss_index,” does what it says, it loads the created Faiss index to perform the similarity semantic search. 


5. indices -> this directory is especially important; this contains our main vector index. This is the place where we store our Faiss index. 


6. routes -> this directory contains all the routes used in the application. This is one centralized part where we define our whole route.  

  the first route: “genrate_embedding”:
  This route is used to generate the embedding of the given data, which we can also say is responsible for training of our model, so it can understand the context of asked question in any other different form. here we are using FastApi UploadFile functionality, where we directly upload the .Json file for training and this Api does the training, generate embedding, and create Faiss index. 

  second route: "chatbot":
  This is the main route to give answers to the question. here we have also used pydantic validator for creating a simple scheme for our input body type that should be a proper string. 


7. utlis -> this directory contains some helper functions. in this the utility.py file contains some helper function, like loading of file and pre-processing of data. 


8. controllers -> inside this I have my main controller that is “chatbot_controller”: 

  This “chatbot_controller” used class-based structure so that all the functions can be used as method and can be properly imported in other files when required.The class chatbot is initialized with some values and models. 

  The first “load_answers” function, loads the dataset in the memory for performing the sematic search, so once the similarly question is detected by the model, this helps is to get the correct answer directly from the loaded memory data. 

  The second “genrate_embedding” function, as discussed earlier this function helps us in creating the embedding. So firstly, it loads the dataset file and checks if there is already an index present or not. for new embedding and tracking the progress I have used  tqdm.

  "embedding = self.model.encode([utility.clear_text(question)], convert_to_tensor=False)" this particular line is where our data is passed to the model for its understanding and then generating the embedding, "convert_to_tensor=False", this is set false because we are not dealing with Py Torch tensor. We want our data to be in the form of a list or NumPy Array.  

  Rest is simple loading the required function and building the index. and saving it to the location 

  The main chatbot function. This is a function which handles the main question and answering. First, we calculate the embedding of the user input query. and again, this query is also normalized for better search. Then we load our vector db. and pass this user embedded query into the db. and look for the most similar question based on the user query. here basically we do sematic Search, using cosine similarity of use asked query with all the data stored in the db. (k=1) this tell we are only considering top 1 match. Once we have the match, we look for its index value and that index value is passed to the already loaded dataset in the memory to retrieve the answer for that query. and we have our answer. 


## Frontend: - has the basic web Ui, created using vanilla JS.  

  Index.html -> this file has loading point of the Ui and has external import of JS and CSS file. 

  Style.css -> this contains the required style of the Ui 

  Script.js -> handle Api response and rendering the response on the Ui 


This is the basic flow of the code. 