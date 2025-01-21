# DataAnalyticsFooty

How to generate video:
  python3.11 MatchGenerator/generate_video.py MatchReports/15-16/StokeVLeicester/match_data.json

Question 1:
  populate db: python3.11 ./Questions/1/pipeline.py MatchReports/15-16/StokeVLeicester/match_data.json
  boot up website: streamlit run ./Questions/1/interface.py