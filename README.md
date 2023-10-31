# Community notes experiment

Idea:

- use Polis data (comments + matrix of votes)
- apply a simplified version of Community Notes algorithm (Vitalik's version)
- look at the output scores (quality and polarisation)

See also:

- https://vitalik.ca/general/2023/08/16/communitynotes.html
- https://github.com/ethereum/research/blob/master/community_notes_analysis/basic_algo.py

How to use:

- put your Polis data under `./data/some-folder`
- use `python main.py some-folder` to run the algorithm (stop it with Ctrl+C when you want to stop)
- alternatively use `node main.js some-folder` (a JS version of same algo, which is much faster)
- display with `python plot.py some-folder`
