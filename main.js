const fs = require("fs");

function loadMatrix(folder) {
  const filePath = `./data/${folder}/participants-votes.csv`;
  const fileContent = fs.readFileSync(filePath, "utf8");
  const lines = fileContent.trim().split("\n").slice(1);
  const matrix = lines.map((line) =>
    line
      .split(",")
      .slice(7)
      .map((x) => parseInt(x === "" ? "0" : x))
  );
  const people = matrix.length;
  const notes = matrix[0].length;
  console.log(`Loaded ${people} people, ${notes} notes`);
  return matrix;
}

function cost(
  matrix,
  intercept,
  userFriendliness,
  noteQuality,
  userAlignment,
  noteAlignment
) {
  const people = matrix.length;
  const notes = matrix[0].length;
  let total = 0;
  for (let i = 0; i < people; i++) {
    for (let j = 0; j < notes; j++) {
      const expectedValue =
        intercept +
        userFriendliness[i] +
        noteQuality[j] +
        userAlignment[i] * noteAlignment[j];
      const incr = Math.pow(matrix[i][j] - expectedValue, 2);
      if (isNaN(incr)) {
        console.log({ i, j, m: matrix[i][j], e: expectedValue });
        throw new Error("Incr is NaN");
      }
      total += incr;
    }
  }
  total +=
    0.15 *
    [
      ...Array(people + 1).fill(intercept),
      ...userFriendliness,
      ...noteQuality,
    ].reduce((acc, val) => acc + Math.pow(val, 2), 0);
  total +=
    0.05 *
    [...userAlignment, ...noteAlignment].reduce(
      (acc, val) => acc + Math.pow(val, 2),
      0
    );
  return total;
}

function naiveDescent(matrix, folder) {
  const people = matrix.length;
  const notes = matrix[0].length;
  let intercept = [Math.random()];
  let userFriendliness = Array.from({ length: people }, () => Math.random());
  let noteQuality = Array.from({ length: notes }, () => Math.random());
  let userAlignment = Array.from({ length: people }, () => Math.random());
  let noteAlignment = Array.from({ length: notes }, () => Math.random());

  let score = cost(
    matrix,
    intercept[0],
    userFriendliness,
    noteQuality,
    userAlignment,
    noteAlignment
  );
  let improvements = 0;
  let timeStart = Date.now();
  for (let round = 0; round < 9 ** 99; round++) {
    const roundDelta = Math.max(0.001, 0.1 / Math.sqrt(round + 1));
    const startRoundScore = score;

    for (const [index, varArray] of [
      [0, intercept],
      [1, userFriendliness],
      [2, noteQuality],
      [3, userAlignment],
      [4, noteAlignment],
    ]) {
      for (let i = 0; i < varArray.length; i++) {
        for (const delta of [roundDelta, -roundDelta]) {
          varArray[i] += delta;
          const newScore = cost(
            matrix,
            intercept[0],
            userFriendliness,
            noteQuality,
            userAlignment,
            noteAlignment
          );
          if (score < newScore) {
            varArray[i] -= delta;
          } else {
            improvements++;
            score = newScore;
            if (improvements % 50 === 0) {
              const elapsed = (Date.now() - timeStart) / 1000;
              console.log(
                `Round ${round}, improvements ${improvements}, cost: ${score}, elapsed: ${elapsed} seconds`
              );
              fs.writeFileSync(
                `./data/${folder}/note_alignment.txt`,
                noteAlignment.join(",")
              );
              fs.writeFileSync(
                `./data/${folder}/note_quality.txt`,
                noteQuality.join(",")
              );
            }
          }
        }
      }
    }

    if (score === startRoundScore) {
      console.log("Finished descending");
      break;
    }
  }

  return noteQuality;
}

const folder = process.argv[2];
const matrix = loadMatrix(folder);
naiveDescent(matrix, folder);
