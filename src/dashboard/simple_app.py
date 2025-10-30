"""
Simplified Streamlit Dashboard for KOO Sentiment Analysis
"""

import streamlit as st
import pandas as pd
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent.parent))

# Page configuration
st.set_page_config(
    page_title="KOO Sentiment Analysis Dashboard",
    page_icon=":bar_chart:",
    layout="wide"
)

# Title
st.title("KOO Multilingual Sentiment Analysis Dashboard")
st.markdown("---")

# Sidebar
st.sidebar.title("Navigation")
page = st.sidebar.radio("Select Page", ["Home", "Generate Data", "Live Analysis"])

st.sidebar.markdown("---")
st.sidebar.info("Dashboard is running successfully!")

# Home Page
if page == "Home":
    st.header("Welcome to KOO Sentiment Analysis")

    st.markdown("""
    ### Your Dashboard is Working!

    This is a **multilingual sentiment analysis system** for social media posts.

    #### Features:
    - **Multilingual Support**: English, Hindi, Tamil, Telugu, Bengali, and more
    - **AI-Powered**: Uses BERT transformer models
    - **Real-time Analysis**: Analyze text instantly
    - **Interactive Visualizations**: Beautiful charts and graphs
    - **Data Export**: Save results in JSON/CSV

    #### Navigation:
    Use the sidebar to navigate between pages:
    - **Home**: This page
    - **Generate Data**: Create sample posts
    - **Live Analysis**: Analyze custom text

    ---

    ### 📊 Quick Stats:
    """)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Supported Languages", "10+")
    with col2:
        st.metric("Model Type", "BERT")
    with col3:
        st.metric("Status", "Ready")

    st.markdown("---")

    st.success("Dashboard loaded successfully! Use the sidebar to explore features.")

# Generate Data Page
elif page == "Generate Data":
    st.header("Generate Sample Data")

    st.info("Generate sample multilingual posts for testing")

    num_posts = st.slider("Number of posts to generate:", 5, 50, 20)

    if st.button("Generate Sample Data", type="primary"):
        with st.spinner("Generating data..."):
            try:
                from src.scraper.koo_scraper import KooScraper

                scraper = KooScraper()
                posts = scraper.create_sample_data(num_posts=num_posts)

                st.success(f"Generated {len(posts)} posts!")

                # Display sample posts
                st.subheader("Sample Posts:")

                for i, post in enumerate(posts[:5], 1):
                    with st.expander(f"Post {i} - {post.language.upper()}"):
                        st.write(f"**Text:** {post.text}")
                        st.write(f"**Author:** {post.author}")
                        st.write(f"**Likes:** {post.likes} | **Reposts:** {post.reposts} | **Comments:** {post.comments}")
                        if post.hashtags:
                            st.write(f"**Hashtags:** {', '.join(['#' + h for h in post.hashtags])}")

                # Show data as dataframe
                st.subheader("Data Table:")
                df = pd.DataFrame([{
                    'ID': p.post_id,
                    'Text': p.text[:50] + '...' if len(p.text) > 50 else p.text,
                    'Language': p.language,
                    'Likes': p.likes,
                    'Author': p.author
                } for p in posts])

                st.dataframe(df, use_container_width=True)

                # Language distribution
                st.subheader("Language Distribution:")
                lang_counts = df['Language'].value_counts()
                st.bar_chart(lang_counts)

            except Exception as e:
                st.error(f"Error generating data: {str(e)}")
                st.info("Make sure all dependencies are installed.")

# Live Analysis Page
elif page == "Live Analysis":
    st.header("Live Sentiment Analysis")

    st.info("Enter any text below to analyze its sentiment. Supports 10+ languages!")

    user_text = st.text_area(
        "Enter text to analyze:",
        height=150,
        placeholder="Type your text here in any language (English, Hindi, Tamil, etc.)"
    )

    if st.button("Analyze Sentiment", type="primary"):
        if user_text:
            with st.spinner("Analyzing sentiment... (This may take a moment on first run)"):
                try:
                    from src.sentiment.analyzer import SentimentAnalyzer
                    from src.scraper.data_models import KooPost
                    from src.utils.config_loader import load_config
                    from datetime import datetime

                    # Initialize analyzer
                    config = load_config()
                    analyzer = SentimentAnalyzer(config.get('sentiment', {}))

                    # Create temporary post
                    post = KooPost(
                        post_id="temp",
                        text=user_text,
                        author="user",
                        timestamp=datetime.now()
                    )

                    # Analyze
                    result = analyzer.analyze_post(post)

                    st.success("Analysis Complete!")

                    # Display results
                    col1, col2, col3 = st.columns(3)

                    with col1:
                        st.metric("Sentiment", result['sentiment'].upper())

                    with col2:
                        st.metric("Confidence", f"{result['confidence']*100:.1f}%")

                    with col3:
                        st.metric("Language", result['language'].upper())

                    # Detailed scores
                    st.subheader("Detailed Sentiment Scores:")
                    scores_df = pd.DataFrame([result['sentiment_scores']])
                    st.bar_chart(scores_df.T)

                    # Show sentiment score
                    st.metric("Sentiment Score", f"{result['sentiment_score']:+.3f}")
                    st.caption("Score ranges from -1 (very negative) to +1 (very positive)")

                except Exception as e:
                    st.error(f"Error during analysis: {str(e)}")
                    st.info("Note: First run downloads the AI model (~500MB). Please be patient!")
                    st.code(str(e))
        else:
            st.warning("Please enter some text to analyze.")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <p>KOO Multilingual Sentiment Analysis | Built with Streamlit</p>
    <p>Supports: English, Hindi, Tamil, Telugu, Bengali, Marathi, Kannada, Gujarati, Malayalam, Punjabi</p>
</div>
""", unsafe_allow_html=True)
