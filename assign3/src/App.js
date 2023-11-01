import { useState } from 'react';

function Square({ value, onSquareClick, isSelected }) {
  const classNames = `square ${isSelected ? 'selected-square' : ''}`;

  return (
    <button className={classNames} onClick={onSquareClick}>
      {value}
    </button>
  );
}

function Board({ xIsNext, squares, onPlay, currentMove }) {
  const [selectedSquare, setSelectedSquare] = useState(null);

  function handleClick(i) {
    if (calculateWinner(squares) || (squares[i] && currentMove < 6)) {
      return;
    }

    if(currentMove > 6)
    {
      const currentPiece = xIsNext ? 'X' : 'O';

      // if you have a piece in the center and you did not click it
      if(selectedSquare == null && squares[4] != null && currentPiece == squares[4] && i != 4)
      {
        // console.log("if you have a piece in the center and you did not click it");
        return;
      }

      // if you don't have a piece in the center and you clicked a piece that is not yours
      else if(selectedSquare == null && currentPiece != squares[4] && squares[i] != currentPiece)
      {
        // console.log("if you don't have a piece in the center and you clicked a piece that is not yours");
        return;
      }

      // unselect
      else if((selectedSquare != null && i == selectedSquare))
      {
        // console.log("unselect");
        setSelectedSquare(null);
      }

      // selecting the second square and not a valid move
      else if(selectedSquare != null && !isValidMove(selectedSquare, i, squares))
      {
        // console.log("selecting the second square and not a valid move");
        return;
      }

      // assuming you have clicked a piece you are allowed to click
      // if no square is selected, set the current square as selected
      else if (selectedSquare == null) 
      {
        // console.log("selected");
        setSelectedSquare(i);
      } 
      
      // if a square is already selected, move the piece, clear the prev square, and reset selectedSquare
      else 
      {
        const nextSquares = squares.slice();
        nextSquares[selectedSquare] = null; 
        nextSquares[i] = currentPiece;
        onPlay(nextSquares);
        setSelectedSquare(null); 
      }
    }

    else 
    {
      setSelectedSquare(null);
      const nextSquares = squares.slice();
      if (xIsNext) {
        nextSquares[i] = 'X';
      } else {
        nextSquares[i] = 'O';
      }
      onPlay(nextSquares);
    }
  }

  const winner = calculateWinner(squares);
  let status;
  if (winner) {
    status = 'Winner: ' + winner;
  } else {
    status = 'Next player: ' + (xIsNext ? 'X' : 'O');
  }

  return (
    <>
      <div className="status">{status}</div>
      <div className="board-row">
        <Square value={squares[0]} onSquareClick={() => handleClick(0)} isSelected={selectedSquare == 0} />
        <Square value={squares[1]} onSquareClick={() => handleClick(1)} isSelected={selectedSquare == 1}/>
        <Square value={squares[2]} onSquareClick={() => handleClick(2)} isSelected={selectedSquare == 2}/>
      </div>
      <div className="board-row">
        <Square value={squares[3]} onSquareClick={() => handleClick(3)} isSelected={selectedSquare == 3}/>
        <Square value={squares[4]} onSquareClick={() => handleClick(4)} isSelected={selectedSquare == 4}/>
        <Square value={squares[5]} onSquareClick={() => handleClick(5)} isSelected={selectedSquare == 5}/>
      </div>
      <div className="board-row">
        <Square value={squares[6]} onSquareClick={() => handleClick(6)} isSelected={selectedSquare == 6}/>
        <Square value={squares[7]} onSquareClick={() => handleClick(7)} isSelected={selectedSquare == 7}/>
        <Square value={squares[8]} onSquareClick={() => handleClick(8)} isSelected={selectedSquare == 8}/>
      </div>
    </>
  );
}

export default function Game() {
  const [history, setHistory] = useState([Array(9).fill(null)]);
  const [currentMove, setCurrentMove] = useState(0);
  const xIsNext = currentMove % 2 === 0;
  const currentSquares = history[currentMove];

  function handlePlay(nextSquares) {
    const nextHistory = [...history.slice(0, currentMove + 1), nextSquares];
    setHistory(nextHistory);
    setCurrentMove(nextHistory.length - 1);
  }

  function jumpToStart() {
    setCurrentMove(0);
  }

  return (
    <div className="game">
      <div className="game-board">
        <Board xIsNext={xIsNext} squares={currentSquares} onPlay={handlePlay} currentMove={currentMove + 1}/>
      </div>
      <div className="game-info">
        <button onClick={jumpToStart}> Reset Game </button>
      </div>
    </div>
  );
}

function calculateWinner(squares) {
  const lines = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6],
  ];
  for (let i = 0; i < lines.length; i++) {
    const [a, b, c] = lines[i];
    if (squares[a] && squares[a] === squares[b] && squares[a] === squares[c]) {
      return squares[a];
    }
  }
  return null;
}

function isValidMove(i, j, squares)
{
  // i is the original square
  // j is the square to move to
  return (
    squares[j] == null &&
    ((i === 0 && (j === 1 || j === 3 || j === 4)) ||
    (i === 1 && (j === 0 || j === 2 || j === 3 || j === 4 || j === 5)) ||
    (i === 2 && (j === 1 || j === 4 || j === 5)) ||
    (i === 3 && (j === 0 || j === 1 || j === 4 || j === 6 || j === 7)) ||
    (i === 4 && j !== 4) ||
    (i === 5 && (j === 1 || j === 2 || j === 4 || j === 7 || j === 8)) ||
    (i === 6 && (j === 3 || j === 4 || j === 7)) ||
    (i === 7 && (j === 3 || j === 4 || j === 5 || j === 6 || j === 8)) ||
    (i === 8 && (j === 4 || j === 5 || j === 7)))
  );
}