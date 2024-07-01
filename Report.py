import pandas as pd
import glob


path = 'C:\\Users\\ASUS\\OneDrive\\Desktop\\Kalvium Task\\Report\\csvfiles\\'
all_files = glob.glob(path + "/*.csv")

dfs = []
for filename in all_files:
    df = pd.read_csv(filename)
    df.columns = [col.strip().lower().replace(' ', '_') for col in df.columns]
    state = filename.split("\\")[-1].replace('_Election_Results.csv', '')
    df['state'] = state
    dfs.append(df)


df = pd.concat(dfs, ignore_index=True)


df.columns = ['s.no', 'candidate', 'party', 'evm_votes', 'postal_votes', 'total_votes', 'percentage_of_votes', 'state']

# Analyze top 5 candidates who received the highest number of votes
top_5_candidates = df.nlargest(5, 'total_votes')[['candidate', 'party', 'total_votes']]
print("Top 5 Candidates:\n", top_5_candidates)

# Party Performance
party_votes = df.groupby('party')['total_votes'].sum().sort_values(ascending=False)
print("Party Performance:\n", party_votes.head())

# Winning Margins
df['winning_margin'] = df['total_votes'] - df['total_votes'].shift(-1)
top_5_margins = df.nlargest(5, 'winning_margin')[['candidate', 'party', 'winning_margin']]
print("Top 5 Winning Margins:\n", top_5_margins)

# Voter Turnout
state_turnout = df.groupby('state')['total_votes'].sum().sort_values(ascending=False)
print("State-wise Voter Turnout:\n", state_turnout)

# Percentage of Votes for NOTA
nota_votes = df[df['candidate'].str.contains('NOTA', case=False, na=False)]['total_votes'].sum()
total_votes = df['total_votes'].sum()
nota_percentage = (nota_votes / total_votes) * 100
print("Percentage of Votes for NOTA: {:.2f}%".format(nota_percentage))

# Postal Votes Contribution
df['postal_votes_percentage'] = (df['postal_votes'] / df['total_votes']) * 100
print("Postal Votes Contribution:\n", df[['candidate', 'party', 'postal_votes_percentage']].head())

# Candidates with Lowest Votes
lowest_votes = df.nsmallest(5, 'total_votes')[['candidate', 'party', 'total_votes']]
print("Candidates with Lowest Votes:\n", lowest_votes)

# Party-wise Seat Distribution
seat_distribution = df.groupby('party').size().sort_values(ascending=False)
print("Party-wise Seat Distribution:\n", seat_distribution)

# State-wise Analysis
state_winners = df.loc[df.groupby('state')['total_votes'].idxmax()][['state', 'candidate', 'party', 'total_votes']]
print("State-wise Winning Candidates and Their Parties:\n", state_winners)

# Regional Performance Analysis

# Top Performing Regions
top_5_regions = df.groupby('state')['total_votes'].sum().sort_values(ascending=False).head(5)
print("Top 5 Performing Regions:\n", top_5_regions)

# Region-wise Party Performance
region_party_performance = df.groupby(['state', 'party'])['total_votes'].sum().unstack().fillna(0)
print("Region-wise Party Performance:\n", region_party_performance.head())

# Regional Voter Turnout Comparison
voter_turnout_comparison = df.groupby('state')['total_votes'].sum().sort_values(ascending=False)
print("Regional Voter Turnout Comparison:\n", voter_turnout_comparison)

# Dominant Parties by Region
dominant_party_by_region = df.loc[df.groupby('state')['total_votes'].idxmax()][['state', 'party', 'total_votes']]
print("Dominant Parties by Region:\n", dominant_party_by_region)
