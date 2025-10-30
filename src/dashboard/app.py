"""
Streamlit Dashboard for KOO Sentiment Analysis
"""

import streamlit as st
import pandas as pd
import json
from pathlib import Path
import sys

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent.parent))

from src.visualization.charts import SentimentCharts
from src.visualization.wordcloud_generator import WordCloudGenerator
from src.sentiment.analyzer import SentimentAnalyzer
from src.scraper.koo_scraper import KooScraper
from src.utils.config_loader import load_config


# Page configuration
st.set_page_config(
    page_title="KOO Sentiment Analysis Dashboard",
    page_icon=":bar_chart:",
    layout="wide",
    initial_sidebar_state="expanded"
)


def load_analysis_results(file_path: str):
    """Load analysis results from file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def main():
    """Main dashboard application"""

    # Title
    st.title("KOO Multilingual Sentiment Analysis Dashboard")
    st.markdown("---")

    # Sidebar
    st.sidebar.title("Navigation")
    page = st.sidebar.radio(
        "Select Page",
        ["Home", "Data Analysis", "Visualizations", "Live Analysis", "Statistics"]
    )

    # Data loading section in sidebar
    st.sidebar.markdown("---")
    st.sidebar.subheader("Data Source")

    data_source = st.sidebar.radio(
        "Choose data source:",
        ["Upload File", "Load Sample Data", "Use Existing Results"]
    )

    results = None
    df = None

    if data_source == "Upload File":
        uploaded_file = st.sidebar.file_uploader(
            "Upload JSON file with analysis results",
            type=['json']
        )
        if uploaded_file:
            results = json.load(uploaded_file)
            df = pd.DataFrame(results)

    elif data_source == "Load Sample Data":
        if st.sidebar.button("Generate Sample Data"):
            with st.spinner("Generating sample data..."):
                scraper = KooScraper()
                posts = scraper.create_sample_data(num_posts=100)

                # Analyze
                config = load_config()
                analyzer = SentimentAnalyzer(config.get('sentiment', {}))
                results = analyzer.analyze_posts(posts, show_progress=False)
                df = pd.DataFrame(results)

                st.sidebar.success(f"Generated {len(results)} sample posts!")

    elif data_source == "Use Existing Results":
        results_dir = Path("data/processed")
        if results_dir.exists():
            result_files = list(results_dir.glob("*.json"))
            if result_files:
                selected_file = st.sidebar.selectbox(
                    "Select results file:",
                    [f.name for f in result_files]
                )
                if selected_file:
                    results = load_analysis_results(results_dir / selected_file)
                    df = pd.DataFrame(results)

    # Main content
    if page == "Home":
        show_home_page()

    elif page == "Data Analysis" and results:
        show_data_analysis_page(df)

    elif page == "Visualizations" and results:
        show_visualizations_page(results, df)

    elif page == "Live Analysis":
        show_live_analysis_page()

    elif page == "Statistics" and results:
        show_statistics_page(df)

    elif results is None:
        st.info("Please load data from the sidebar to view analysis.")


def show_home_page():
    """Display home page"""
    st.header("Welcome to KOO Sentiment Analysis")

    st.markdown("""
    This dashboard provides comprehensive multilingual sentiment analysis for KOO social media posts.

    ### Features:
    - **Multilingual Support**: Analyze posts in English, Hindi, Tamil, Telugu, Bengali, and more
    - **Advanced NLP**: Uses transformer-based models (BERT) for accurate sentiment detection
    - **Rich Visualizations**: Interactive charts, word clouds, and statistical reports
    - **Real-time Analysis**: Analyze new text in real-time
    - **Export Capabilities**: Download results in JSON or CSV format

    ### How to Use:
    1. **Load Data**: Use the sidebar to upload analysis results or generate sample data
    2. **Explore**: Navigate through different pages to view analysis and visualizations
    3. **Analyze**: Use the Live Analysis page to test sentiment on new text
    4. **Export**: Download results and visualizations

    ### About:
    This tool uses state-of-the-art multilingual BERT models to analyze sentiment across
    multiple Indian languages, providing insights into public opinion and social media trends.
    """)

    # Display some metrics if possible
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Supported Languages", "10+")
    with col2:
        st.metric("Model Accuracy", "~85%")
    with col3:
        st.metric("Analysis Speed", "Fast")


def show_data_analysis_page(df):
    """Display data analysis page"""
    st.header("Data Analysis")

    # Basic statistics
    st.subheader("Dataset Overview")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Posts", len(df))
    with col2:
        st.metric("Languages", df['language'].nunique())
    with col3:
        st.metric("Avg Confidence", f"{df['confidence'].mean():.2%}")
    with col4:
        st.metric("Unique Authors", df['author'].nunique())

    # Data table
    st.subheader("Sample Data")
    display_cols = ['text', 'sentiment', 'confidence', 'language', 'likes', 'reposts']
    st.dataframe(df[display_cols].head(20), use_container_width=True)

    # Filters
    st.subheader("Filter Data")
    col1, col2 = st.columns(2)

    with col1:
        selected_sentiments = st.multiselect(
            "Filter by Sentiment",
            options=df['sentiment'].unique().tolist(),
            default=df['sentiment'].unique().tolist()
        )

    with col2:
        selected_languages = st.multiselect(
            "Filter by Language",
            options=df['language'].unique().tolist(),
            default=df['language'].unique().tolist()
        )

    # Apply filters
    filtered_df = df[
        (df['sentiment'].isin(selected_sentiments)) &
        (df['language'].isin(selected_languages))
    ]

    st.write(f"Filtered results: {len(filtered_df)} posts")
    st.dataframe(filtered_df[display_cols], use_container_width=True)


def show_visualizations_page(results, df):
    """Display visualizations page"""
    st.header("Visualizations")

    charts = SentimentCharts(results)

    # Sentiment Distribution
    st.subheader("Sentiment Distribution")
    col1, col2 = st.columns(2)

    with col1:
        st.write("**Overall Distribution**")
        fig_dist = charts.plot_sentiment_distribution(use_plotly=True)
        if fig_dist:
            st.plotly_chart(fig_dist, use_container_width=True)

    with col2:
        st.write("**By Language**")
        fig_lang = charts.plot_sentiment_by_language(use_plotly=True)
        if fig_lang:
            st.plotly_chart(fig_lang, use_container_width=True)

    # Timeline
    st.subheader("Sentiment Timeline")
    fig_timeline = charts.plot_sentiment_timeline(use_plotly=True)
    if fig_timeline:
        st.plotly_chart(fig_timeline, use_container_width=True)

    # Engagement
    st.subheader("Engagement Analysis")
    fig_engagement = charts.plot_engagement_by_sentiment(use_plotly=True)
    if fig_engagement:
        st.plotly_chart(fig_engagement, use_container_width=True)

    # Word Clouds
    st.subheader("Word Clouds")
    wc_gen = WordCloudGenerator(results)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Generate Overall Word Cloud"):
            with st.spinner("Generating..."):
                import tempfile
                with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as tmp:
                    wc_gen.generate_overall_wordcloud(save_path=tmp.name)
                    st.image(tmp.name)

    with col2:
        if st.button("Generate Hashtag Word Cloud"):
            with st.spinner("Generating..."):
                import tempfile
                with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as tmp:
                    wc_gen.generate_hashtag_wordcloud(save_path=tmp.name)
                    st.image(tmp.name)


def show_live_analysis_page():
    """Display live analysis page"""
    st.header("Live Sentiment Analysis")

    st.write("Enter text to analyze its sentiment in real-time:")

    # Text input
    user_text = st.text_area(
        "Enter text (supports multiple languages):",
        height=150,
        placeholder="Type or paste text here..."
    )

    if st.button("Analyze Sentiment", type="primary"):
        if user_text:
            with st.spinner("Analyzing..."):
                try:
                    # Load model and analyze
                    config = load_config()
                    analyzer = SentimentAnalyzer(config.get('sentiment', {}))

                    from src.scraper.data_models import KooPost
                    from datetime import datetime

                    # Create a temporary post
                    post = KooPost(
                        post_id="temp",
                        text=user_text,
                        author="user",
                        timestamp=datetime.now()
                    )

                    result = analyzer.analyze_post(post)

                    # Display results
                    st.success("Analysis Complete!")

                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Sentiment", result['sentiment'].upper())
                    with col2:
                        st.metric("Confidence", f"{result['confidence']:.2%}")
                    with col3:
                        st.metric("Language", result['language'].upper())

                    # Detailed scores
                    st.subheader("Detailed Sentiment Scores")
                    scores_df = pd.DataFrame([result['sentiment_scores']])
                    st.bar_chart(scores_df.T)

                except Exception as e:
                    st.error(f"Error during analysis: {str(e)}")
        else:
            st.warning("Please enter some text to analyze.")


def show_statistics_page(df):
    """Display statistics page"""
    st.header("Statistical Analysis")

    # Overall statistics
    st.subheader("Overall Statistics")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Posts", len(df))
        st.metric("Average Sentiment Score", f"{df['sentiment_score'].mean():.3f}")

    with col2:
        most_common_sentiment = df['sentiment'].mode()[0]
        st.metric("Most Common Sentiment", most_common_sentiment.title())
        st.metric("Average Likes", f"{df['likes'].mean():.1f}")

    with col3:
        st.metric("Average Confidence", f"{df['confidence'].mean():.2%}")
        st.metric("Average Comments", f"{df['comments'].mean():.1f}")

    # Sentiment breakdown
    st.subheader("Sentiment Breakdown")
    sentiment_dist = df['sentiment'].value_counts()
    st.bar_chart(sentiment_dist)

    # Language statistics
    st.subheader("Language Statistics")
    lang_stats = df.groupby('language').agg({
        'sentiment_score': 'mean',
        'confidence': 'mean',
        'likes': 'mean'
    }).round(3)
    st.dataframe(lang_stats, use_container_width=True)

    # Top posts
    st.subheader("Top Posts")

    col1, col2 = st.columns(2)
    with col1:
        st.write("**Most Positive Posts**")
        top_positive = df.nlargest(5, 'sentiment_score')[['text', 'sentiment_score', 'likes']]
        st.dataframe(top_positive, use_container_width=True)

    with col2:
        st.write("**Most Negative Posts**")
        top_negative = df.nsmallest(5, 'sentiment_score')[['text', 'sentiment_score', 'likes']]
        st.dataframe(top_negative, use_container_width=True)


if __name__ == "__main__":
    main()
