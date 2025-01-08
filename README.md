# Financial QA RAG System

This project implements a **Financial Question-Answering System** using a Retrieval-Augmented Generation (RAG) architecture with Google's Vertex AI, LangChain, and the SEC Filings Data API. It allows users to input natural language queries and retrieves precise answers sourced from financial filings (10-K reports) of 5 major companies: Apple, Microsoft, Meta, Google, Amazon.

---

## How the System Works

1. **Data Retrieval**: 
   - SEC Filings are fetched using the SEC API.
   - Filings are cleaned, parsed, and broken into smaller, meaningful chunks.

2. **Vector Indexing**:
   - Document chunks are converted to embeddings using Google's **text embedding models**.
   - These embeddings serve as the basis for a high-performance **Vector Search Index** created with Vertex AI Matching Engine.

3. **Question-Answer System**:
   - Questions from users are processed by LangChain's Retrieval-Aware Generation (RAG) models.
   - The context is retrieved from the custom Vector Store.
   - Responses are generated using Google's **Gemini 1.5 Pro Model**.

4. **Deployment**:
   - A fully deployed system indexed on Google Cloud enables fast retrieval, context parsing, and answer generation.

Here is an example of how the system works in action:

---

### Example 1:

**Your Question**: What was Apple’s revenue in 2021?

**Answer**:
```json
{
  "query": "What was Apple's revenue in 2021?",
  "result": "Apple's total net sales in 2021 were **$365.817 billion**.\n\nThis figure is derived by summing the net sales of all product categories in the \"Products and Services Performance\" table of Apple's 2022 Form 10-K:\n\n- iPhone: $191.973 billion\n- Mac: $35.190 billion\n- iPad: $31.862 billion\n- Wearables, Home and Accessories: $38.367 billion\n- Services: $68.42 billion"
}
```

---

### Example 2:

**Your Question**: Which Apple product made the most money in 2022?

**Answer**:
```json
{
  "query": "Which Apple product made the most money in 2022?",
  "result": "The iPhone generated the most revenue for Apple in 2022, with net sales of $205.489 billion."
}
```

---

## Features

- **Real-Time Answer Generation**: Get precise answers extracted from financial filings.
- **Scalable Vector Search**: Efficient information retrieval with Google's Vertex AI Matching Engine.
- **Financial Focus**: Tailored to answer finance-related questions about publicly traded companies using verified filings.
- **Interactive Chat**: A user-friendly interactive terminal-based interface (can be extended to a web-based or app-based UI).
- **End-to-End Processing**: From 10-K scraping to GCP-based deployment and live query answering.

---

## Project Structure

```plaintext
.
├── config/                # Project configuration (env variables, constants, etc.)
│   └── config.py          
├── data/                  # Data handlers for parsing and processing financial data
│   └── data_handler.py    # Fetching 10-K filings and splitting documents into chunks
├── model/                 # Core classes for index creation and question-answering
│   ├── index_retrieval.py # Index creation and vector store handling
│   └── qa_system.py       # Retrieval-based Question Answering System
├── storage/               # Google Cloud Storage interaction modules
│   └── storage_handler.py # Save and retrieve files (chunks, metadata) on GCP
├── data_pipeline.py       # Pipeline to process and upload filings to GCP
├── main.py                # Main script to run the system interactively
├── README.md              # Project documentation (this file)
└── requirements.txt       # Python dependencies
```

---

## Setup Instructions

### Prerequisites

- Python 3.11+
- A Google Cloud Project with:
  - Vertex AI and Matching Engine APIs enabled
  - Cloud Storage Bucket created
- SEC API Key [Get Here](https://sec-api.io/)
- `pip` installed for Python package management.

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/Luka-Lukacevic/RAG-Financial-QA-system.git
   cd rag-financial-qa-system
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:

   Copy the `.env` template provided and update it with your configuration:

   ```plaintext
   SEC_API_KEY=<your-sec-api-key>
   PROJECT_ID=<gcp-project-id>
   REGION=<gcp-region>
   BUCKET_NAME=<gcp-bucket-name>
   ```

4. Ensure GCP credentials are available locally (e.g., a JSON key for your GCP Service Account).

### Running the System

1. **Data Pipeline**: Run the `data_pipeline.py` to collect, parse, and upload filings to Google Cloud:

   ```bash
   python data_pipeline.py
   ```

2. **Interactive Chat**: Start the interactive QA session:

   ```bash
   python main.py
   ```

---

## Dependencies

The project relies on the following tools and libraries:

- **Python Core**:
  - `pickle`, `os`, `logging`, `time`
- **Google Cloud**:
  - `google-cloud-storage`, `google-cloud-aiplatform`
- **LangChain**:
  - `langchain`, `langchain_google_vertexai`, `langchain_text_splitters`
- **Web Scraping**:
  - `BeautifulSoup`, `request`
- **SEC API**:
  - `sec-api`

Install them via `requirements.txt`.

---

## Future Work

- Extend QA to broader domains (beyond financial data or these 5 companies).
- Develop a front-end interface for improved user interaction.
- Automate retraining and index updates for dynamic filings.
