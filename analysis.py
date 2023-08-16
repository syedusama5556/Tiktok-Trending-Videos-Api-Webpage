import math
import pandas as pd
import seaborn as sns
from sklearn.feature_extraction.text import TfidfVectorizer
from gensim.models import Word2Vec
from nltk.tokenize import word_tokenize
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from db_stuff import VideoDatabase
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score

# Load data from the database and preprocess
db = VideoDatabase()
db.connect()
video_data = []

selected_data = db.select_all()
if selected_data:
    for row in selected_data:
        if row:
            json_data = {
                'video_id': row[1],
                'username': row[2],
                'likes': row[3],
                'shares': row[4],
                'plays': row[5],
                'thumbnail': row[6],
                'description': row[7],
                'hashtags': ','.join([tag.strip() for tag in row[8].split(',') if tag.strip()]),
                'region': row[9],
                'timestamp': row[10]
            }
            video_data.append(json_data)
else:
    video_data = []

db.close()

plt.rcParams["font.family"] = "DejaVu Sans"

# Convert data into a pandas DataFrame
df = pd.DataFrame(video_data)

# Preprocess timestamp column
df['timestamp'] = pd.to_datetime(df['timestamp'])

# Preprocess hashtags column
df['hashtags'] = df['hashtags'].apply(lambda x: x.split(','))

# EDA: Summary Statistics
summary_stats = df.describe()
print(summary_stats)


# Popular Hashtags
all_hashtags = [tag for tags in df['hashtags'] for tag in tags]
top_hashtags = pd.Series(all_hashtags).value_counts().head(10)
plt.figure(figsize=(10, 6))
top_hashtags.plot(kind='bar')
plt.title('Top 10 Popular Hashtags in the WORLD')
plt.xlabel('Hashtag')
plt.ylabel('Frequency')
plt.xticks(rotation=40)
plt.show()


# Iterate through regions and create plots for top hashtags
regions = df['region'].unique()

for region in regions:
    region_df = df[df['region'] == region]
    
    all_hashtags = [tag for tags in region_df['hashtags'] for tag in tags]
    top_hashtags = pd.Series(all_hashtags).value_counts().head(10)
    
    plt.figure(figsize=(10, 6))
    top_hashtags.plot(kind='bar')
    plt.title(f'Top 10 Popular Hashtags in {region}')
    plt.xlabel('Hashtag')
    plt.ylabel('Frequency')
    plt.xticks(rotation=40)
    plt.tight_layout()
    plt.show()

# Region-Based Analysis
region_data = df.groupby('region').agg({'likes': 'sum', 'shares': 'sum', 'plays': 'sum'})
plt.figure(figsize=(10, 6))
region_data.plot(kind='bar')
plt.title('Metrics by Region')
plt.xlabel('Region')
plt.ylabel('Count')
plt.xticks(rotation=45)
plt.legend()
plt.show()

# Iterate through regions and perform analysis
regions = df['region'].unique()

for region in regions:
    region_df = df[df['region'] == region]
    
    X = region_df[['shares', 'plays']]  # Features
    y = region_df['likes']  # Target
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = LinearRegression()
    model.fit(X_train, y_train)
    
    y_pred = model.predict(X_test)
    
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    # Calculate target range as difference between max and min actual 'likes' in testing set
    target_range = y_test.max() - y_test.min()

    rmse = math.sqrt(mse) / target_range
    rmse_percentage = rmse * 100

    result_value = abs(r2 )

    print(f"Region: {region}")
    print(f"RMSE(accuracy of a models predictions) Percentage: {rmse_percentage:.2f}%")
    print(f"R-squared: {result_value:.2f}")
    print("=" * 60)

