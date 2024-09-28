import faiss
from sklearn.preprocessing import normalize

class VectorDB:
  # def __init__(self) -> None:
  #   self.index_file_path = '../indices/ecommerce_indice.index'
  
  # build faiss index
  def build_faiss_index(self, embeeing):
    norm_embedding = normalize(embeeing, norm='l2')
    dim = norm_embedding.shape[1]
    index = faiss.IndexFlatIP(dim)
    index.add(norm_embedding)
    return index
  
  # save faiss index
  def save_faiss_index(self, index, index_file_path):
    faiss.write_index(index, index_file_path)
  
  # load faiss index
  def load_faiss_index(self, index_file_path):
    return faiss.read_index(index_file_path)
  
vector_db = VectorDB()