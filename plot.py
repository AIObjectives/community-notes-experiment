
import pandas as pd
import plotly.express as px
import sys

if __name__ == '__main__':
    folder = sys.argv[1]
    votes = pd.read_csv(f"./data/{folder}/participants-votes.csv")
    comment_ids = [int(x) for x in votes.columns[7:]]

    quality = pd.read_csv(f"./data/{folder}/note_quality.txt", header=None)
    quality.columns = ['quality']
    quality['comment-id'] = comment_ids
    # quality.set_index('comment-id', inplace=True)

    alignment = pd.read_csv(f"./data/{folder}/note_alignment.txt", header=None)
    alignment.columns = ['alignment']
    alignment['comment-id'] = comment_ids
    alignment.set_index('comment-id', inplace=True)

    comments = pd.read_csv(
        f"./data/{folder}/comments.csv")[['comment-id', 'comment-body', 'agrees', 'disagrees']]

    print(comments.dtypes)
    print(quality.dtypes)

    comments = comments.merge(
        quality, left_on='comment-id', right_on='comment-id')

    comments = comments.merge(
        alignment, left_on='comment-id', right_index=True)
    comments.sort_values(by='alignment', ascending=False, inplace=True)
    comments.to_csv(f"./data/{folder}/comments_with_quality.csv", index=False)

    def label(row):
        body = row['comment-body']
        agrees = row['agrees']
        disagrees = row['disagrees']
        return f"{body} ({agrees} agrees, {disagrees} disagrees)"

    comments['label'] = comments.apply(label, axis=1)

    fig = px.scatter(comments, x='alignment', y='quality',
                     hover_name='label')
    fig.update_layout(
        title=folder,
        xaxis_title='Polarization',
        yaxis_title='Quality'
    )
    fig.show()
