import pandas as pd
import os
#Change this directory to wherever netflix_titles.csv is saved
os.chdir(r'')
df = pd.read_csv('netflix_titles.csv')
# Prints null values
print(df.isnull().sum())
# Replaced null values with unknown
df['director'].fillna('Unknown', inplace=True)
df['cast'].fillna('Unknown', inplace=True)
# Drop empty rows where applicable along with duplicate showid
df.dropna(subset=['title', 'show_id', 'type', 'date_added', 'rating', 'duration'], inplace=True)
df.drop_duplicates(subset='show_id', inplace=True)
# Converts date_added to datetime
df['date_added'] = pd.to_datetime(df['date_added'], errors='coerce')
# Filter to create 2 new columns each with duration of seasons and minutes
df['duration_minutes'] = df['duration'].apply(lambda x: float(x.split()[0]) if isinstance(x, str) and 'min' in x else 0)
df['duration_seasons'] = df['duration'].apply(lambda x: float(x.split()[0]) if isinstance(x, str) and 'Season' in x else 0)
df.drop(['duration'], axis=1, inplace=True)
# Create binary movie/tv show check
df['isMovie'] = df['type'].apply(lambda x: 1 if x == 'Movie' else 0)
df['isTVShow'] = df['type'].apply(lambda x: 1 if x == 'TV Show' else 0)
# Adjust country cateogry
df['country'] = df['country'].astype('category')
df['rating'] = df['rating'].astype('category')
# Create function to filter between children/teen/adult
def categorize_rating(rating):
    if rating in ['G', 'PG', 'TV-Y', 'TV-G', 'TV-Y7', 'TV-Y7-FV']:
        return 'Children'
    elif rating in ['PG-13', 'TV-PG', 'TV-14']:
        return 'Teen'
    elif rating in ['R', 'NC-17', 'TV-MA']:
        return 'Adult'
    return 'Unrated'
df['adjusted_rating'] = df['rating'].apply(categorize_rating)
# Output csv
df.to_csv('netflix_cleaned.csv', index=False)

# THis cfreates the country count 
df = pd.read_csv('netflix_titles.csv')
df['country'] = df['country'].fillna('Unknown')
df['country'] = df['country'].replace('', 'Unknown')
countries_split = df['country'].str.split(',', expand=True).stack().reset_index(level=1, drop=True)
countries_df = countries_split.to_frame(name='country')
countries_df['country'] = countries_df['country'].str.strip()  
country_count = countries_df['country'].value_counts().reset_index()
country_count.columns = ['country', 'count']
country_count.to_csv('country_count.csv', index=False)