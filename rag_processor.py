import os
import json
import pathway as pw
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import TextLoader
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class RAGProcessor:
    def __init__(self, knowledge_dir="./knowledge_base"):
        """
        Initialize the RAG processor with a knowledge base directory.
        
        Args:
            knowledge_dir: Directory containing knowledge base documents
        """
        self.knowledge_dir = knowledge_dir
        self.vector_store = None
        self.qa_chain = None
        
        # Create knowledge directory if it doesn't exist
        os.makedirs(knowledge_dir, exist_ok=True)
        
        # Initialize the knowledge base
        self._initialize_knowledge_base()
    
    def _initialize_knowledge_base(self):
        """Initialize the vector store with documents from the knowledge base."""
        try:
            # Check if we have documents in the knowledge base
            documents = []
            
            # Load documents from knowledge base directory
            for filename in os.listdir(self.knowledge_dir):
                if filename.endswith('.txt'):
                    file_path = os.path.join(self.knowledge_dir, filename)
                    loader = TextLoader(file_path)
                    documents.extend(loader.load())
            
            # If no documents found, create a sample document
            if not documents:
                print("No documents found in knowledge base. Creating sample document.")
                sample_path = os.path.join(self.knowledge_dir, "sample_translations.txt")
                with open(sample_path, "w") as f:
                    f.write("""
                    # Common Translation Examples
                    
                    ## Meeting-related terms
                    - meeting: A gathering of people for discussion or business
                    - conference: A formal meeting for discussion, exchange of information, or planning
                    - agenda: A list of items to be discussed at a meeting
                    - minutes: A written record of what was said and decided in a meeting
                    
                    ## Business terms
                    - deadline: The latest time or date by which something should be completed
                    - project: A planned piece of work with a specific purpose
                    - budget: An estimate of income and expenditure for a set period of time
                    - stakeholder: A person with an interest or concern in something, especially a business
                    
                    ## Technical terms
                    - algorithm: A process or set of rules to be followed in calculations or problem-solving
                    - database: A structured set of data held in a computer
                    - interface: A point where two systems meet and interact
                    - bandwidth: The capacity for data transfer of an electronic communications system
                    """)
                
                # Load the sample document
                loader = TextLoader(sample_path)
                documents.extend(loader.load())
            
            # Split documents into chunks
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200
            )
            texts = text_splitter.split_documents(documents)
            
            # Create vector store
            embeddings = OpenAIEmbeddings()
            self.vector_store = FAISS.from_documents(texts, embeddings)
            
            # Create QA chain
            self.qa_chain = RetrievalQA.from_chain_type(
                llm=OpenAI(),
                chain_type="stuff",
                retriever=self.vector_store.as_retriever()
            )
            
            print("Knowledge base initialized successfully")
        except Exception as e:
            print(f"Error initializing knowledge base: {e}")
    
    def process_with_rag(self, query, translation_result):
        """
        Enhance translation with RAG-based context.
        
        Args:
            query: The original query text
            translation_result: The basic translation result
            
        Returns:
            Enhanced translation with context
        """
        if not self.qa_chain:
            return translation_result
        
        try:
            # Extract the translated text
            translated_text = translation_result.get("translated_text", "")
            source_language = translation_result.get("source_language", "unknown")
            
            # Create a context query
            context_query = f"Provide context for the term '{translated_text}' in English"
            
            # Get context from RAG
            rag_response = self.qa_chain.run(context_query)
            
            # Enhance the translation result with context
            enhanced_result = {
                "translated_text": translated_text,
                "source_language": source_language,
                "context": rag_response if rag_response else "No additional context available"
            }
            
            return enhanced_result
        except Exception as e:
            print(f"Error in RAG processing: {e}")
            # Return original translation if RAG fails
            return translation_result

# Pathway integration for RAG processing
class RAGPathwayProcessor:
    def __init__(self):
        self.rag_processor = RAGProcessor()
        self.setup_pipeline()
    
    def setup_pipeline(self):
        # Define input schema for processed translations
        class TranslationSchema(pw.Schema):
            original_text: str
            timestamp: float
            session_id: str
            translation: str
        
        # Create input connector for processed translations
        self.input_stream = pw.io.fs.read(
            "./output_data",
            format="json",
            schema=TranslationSchema,
            mode="streaming"
        )
        
        # Process with RAG
        enhanced = self.input_stream.select(
            original_text=pw.this.original_text,
            timestamp=pw.this.timestamp,
            session_id=pw.this.session_id,
            translation=pw.this.translation,
            enhanced_translation=pw.apply(self._enhance_with_rag, pw.this.original_text, pw.this.translation)
        )
        
        # Output enhanced results
        enhanced.to_json("./enhanced_output")
    
    def _enhance_with_rag(self, original_text, translation_json):
        # Parse the translation JSON
        translation_result = json.loads(translation_json)
        
        # Process with RAG
        enhanced_result = self.rag_processor.process_with_rag(original_text, translation_result)
        
        # Return as JSON
        return json.dumps(enhanced_result)
    
    def run(self):
        # Run the pipeline
        pw.run()

# Main application entry point
if __name__ == "__main__":
    # Create output directory if it doesn't exist
    os.makedirs("./enhanced_output", exist_ok=True)
    
    # Initialize and run the RAG processor
    processor = RAGPathwayProcessor()
    processor.run()