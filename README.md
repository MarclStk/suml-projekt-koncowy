---
title: LapiMate
emoji: 🚀
colorFrom: red
colorTo: red
sdk: docker
app_file: app.py
pinned: false
license: apache-2.0
tags:
  - streamlit
---

# LapiMate 💻

LapiMate is a laptop price prediction application built with Streamlit that helps users estimate laptop prices based on specifications and find similar models within their budget.

## Features

- **Price Prediction**: Predict laptop prices based on detailed specifications
- **Laptop Recommendations**: Get recommendations for similar laptops based on your preferences
- **Price Comparison**: Compare different laptop models to make an informed purchase decision
- **PDF Export**: Export prediction results to PDF for sharing or reference
- **Multiple Currency Support**: View prices in different currencies
- **Laptop Categorization**: Understand which segment a laptop belongs to (budget, premium, gaming, etc.)
- **History Tracking**: Keep track of previous predictions for easy reference

## Getting Started

### Prerequisites

- Python 3.9+
- pip (Python package installer)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/lapimate.git
cd lapimate
```

2. Create a virtual environment and activate it:
```bash
python -m venv .venv
# On Windows
.venv\Scripts\activate
# On macOS/Linux
source .venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
streamlit run app.py
```

The application will be available at `http://localhost:8501`

## Running with Docker

1. Build and run the Docker container:
```bash
docker-compose up -d
```

2. Access the application at `http://localhost:8501`

## Project Structure

```
LapiMate/
├── app.py                  # Main application entry point
├── laptop_price.csv        # Dataset file
├── requirements.txt        # Python dependencies
├── Dockerfile              # Docker configuration
├── docker-compose.yml      # Docker Compose configuration
├── models/                 # Directory for saved ML models
├── outputs/                # Directory for generated PDFs
├── src/
│   ├── backend/
│   │   ├── data/           # Data loading and preprocessing
│   │   ├── domain/         # Domain models (DDD)
│   │   ├── services/       # Business logic services
│   │   └── infrastructure/ # External services integration
│   ├── frontend/
│   │   ├── components/     # UI components
│   │   └── main_app.py     # Main Streamlit UI logic
│   ├── tests/              # Unit and integration tests
│   └── utils/              # Utility functions
└── .github/
    └── workflows/          # CI/CD workflows
```

## Development

### Running Tests

```bash
pytest
```

### CI/CD Pipeline

The project includes a GitHub Actions workflow for continuous integration and deployment. It:

1. Runs tests
2. Builds a Docker image
3. Pushes the image to Docker Hub
4. Deploys to a cloud platform (configuration required)

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- Dataset source: [Kaggle - Laptop Price](https://www.kaggle.com/datasets/muhammetvarl/laptop-price)
