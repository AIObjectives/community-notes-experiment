
import pandas as pd
import plotly.express as px
import sys 

if __name__ == '__main__':
  folder = sys.argv[1]
  quality = pd.read_csv(f"./data/{folder}/note_quality.txt", header=None).transpose()
  quality.columns = ['quality']
  alignment = pd.read_csv(f"./data/{folder}/note_alignment.txt", header=None).transpose()
  alignment.columns = ['alignment']
  comments = pd.read_csv(f"./data/{folder}/comments.csv")[['comment-id', 'comment-body', 'agrees', 'disagrees']]
  comments = comments.merge(quality, left_on='comment-id', right_index=True)
  comments = comments.merge(alignment, left_on='comment-id', right_index=True)
  comments.sort_values(by='alignment', ascending=False, inplace=True)
  comments.to_csv(f"./data/{folder}/comments_with_quality.csv", index=False)
  fig = px.scatter(comments, x='alignment', y='quality', hover_name='comment-body')
  fig.update_layout(
      title='Polis consultation results, quality and polarization',
      xaxis_title='Polarization',
      yaxis_title='Quality'
  )
  fig.show()