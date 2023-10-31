# Community notes experiment

Key idea:

- use Polis data (comments + matrix of votes)
- apply a simplified version of Community Notes algorithm (Vitalik's version)
- look at the output scores (quality and polarisation)

See also:

- https://vitalik.ca/general/2023/08/16/communitynotes.html
- https://github.com/ethereum/research/blob/master/community_notes_analysis/basic_algo.py

How to use:

- put your Polis data under `./data/some-folder`
- use `python main.py some-folder` to run the algorithm (stop it with Ctrl+C when you want to stop)
- display with `python plot.py some-folder`

Datasets included:

- `rec-public` is the Polis data from Recursuve public team (not very large, but high quality)
- `cip-anthropic` is the Polis data gathered by CIP for the [CCAI](https://www.anthropic.com/index/collective-constitutional-ai-aligning-a-language-model-with-public-input) project (larger dataset, but most of it is spam or low-quality)

For instance, `python plot.py rec-public` will produce this interactive plot:

<img width="989" alt="image" src="https://github.com/AIObjectives/community-notes-experiment/assets/3934784/386b0576-8ca1-4172-9c21-0e70f7470e8f">

## First learnings and observations

- Vitalik's original implementation was very slow but rewriting it using numpy helped make it ~10 faster.

- The outputs I got for the rec-public dataset were fairly encouraging. Looking at the polarisation axis, we can notice that the posts on the left are more libertarian/anti-regulation (promoting individualism) while the posts on the right are more authoritarian/pro-regulation (promoting collectivism).

- The quality/polarisation plot doesn't seem really well distributed. It seems that posts on the right side of the plot (the collectivist side) generally get better quality score. I wonder whether this is might be due to the fact that a large majority of participants are more on the collectivist side. Maybe the algorithm could be further improved to somehow compensate the unbalance during the training (e.g. by modifying the cost function to penalize assymetries)? Or alternatively, one might keep the grandiant descend unchanged but correct the final scores at the end (e.g. boosting the score of notes from under-represented side, or boosting the notes that are in the middle of the polarisation axis).

## Potential future technical work, if anyone wants to help?

Many things could potentially be improved in the algo:

- [ ] maybe use ML libs like autograd and/or pytorch or whatever
- [ ] come up with better cost function and/or regularisation params

We may also get better performance by addressing the fact that our Polis matrices are very sparse...

- [ ] we could cost function to treat "0" and "NaN" differently
- [ ] we could maybe drop comments with less than two votes to reduce noise
- [ ] we could try and fill the gaps using various technics (interpolation, knn, collaborative filtering...)

We could also start looking at multi-dimensional polarisation

- [ ] the user_alignment and note_alignent vectors could be replaced by matrices
- [ ] the case with two dimensions could be particularly interesting (and easy to plot)
