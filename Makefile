# Makefile for KOO Sentiment Analysis

.PHONY: install clean test run dashboard help

help:
	@echo "KOO Sentiment Analysis - Available Commands:"
	@echo ""
	@echo "  make install     - Install dependencies"
	@echo "  make run         - Run main analysis with sample data"
	@echo "  make dashboard   - Launch web dashboard"
	@echo "  make visualize   - Run analysis with visualizations"
	@echo "  make clean       - Clean generated files"
	@echo "  make test        - Run example scripts"
	@echo ""

install:
	pip install -r requirements.txt

run:
	python main.py --mode sample --num-posts 100

dashboard:
	streamlit run src/dashboard/app.py

visualize:
	python main.py --mode sample --num-posts 100 --visualize

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf build/ dist/

test:
	python examples/basic_usage.py
	python examples/analyze_custom_text.py
