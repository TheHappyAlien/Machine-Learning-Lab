using Godot;
using System;
using System.Collections.Generic;
using System.Reflection.Metadata;
using System.Runtime.ConstrainedExecution;
using System.Xml.Serialization;

public partial class HalmaController : GridContainer
{

	# region Texture imports
	[Export] private Texture2D _0;
	[Export] private Texture2D _1;
	[Export] private Texture2D _base;
	[Export] private Texture2D _highlight;
	[Export] private Texture2D X_0;
	[Export] private Texture2D X_1;
	[Export] private Texture2D X_base;
	[Export] private Texture2D X_highlight;
	[Export] private Texture2D Black_0;
	[Export] private Texture2D Black_1;
	[Export] private Texture2D Black_base;
	[Export] private Texture2D Black_highlight;
	[Export] private Texture2D White_0;
	[Export] private Texture2D White_1;
	[Export] private Texture2D White_base;
	[Export] private Texture2D White_highlight;
	# endregion

	private const String PLAYER_WHITE = "w";
	private const String PLAYER_BLACK = "b";
	private (int, int) NO_PRESS = (-1, -1);

	private (int, int) firstPressCoords;
	private (int, int) secondPressCoords;

	private Dictionary<String, Texture2D> texturesDict = new Dictionary<String, Texture2D>();
	private String[,] gameGrid = new String[16,16];

	private String currentPlayer = PLAYER_WHITE;

	Vector2 tileSize;
	private const int GRID_SIZE = 16;
	private const int PADDING = 100;
	public override void _Ready()
	{	
		firstPressCoords = NO_PRESS;
		secondPressCoords = NO_PRESS;

		tileSize = _0.GetSize();
		initGame();
		GridToGame();
	}

	private void initGame() {
		PopulateDictionary();
		GenerateInitGrid();

		Vector2I windowSize = DisplayServer.WindowGetSize();
		this.Size = windowSize;
		int minDim = Math.Min(windowSize.X,  windowSize.Y);

		for (int row = 0; row < GRID_SIZE; row++)
		{
			for (int col = 0; col < GRID_SIZE; col++)
			{
                Button button = new()
                {
                    Name = row + "_" + col,
					Size = tileSize,
					Flat = true
                };
                button.Pressed += () => _OnButtonPressed(button.Name); // Use lambda expression
				AddChild(button);
			}
		}

		int positionX = windowSize.X == minDim ? PADDING / 2 : (windowSize.X - minDim) / 2 + PADDING;
		int positionY = windowSize.Y == minDim ? PADDING / 2 : (windowSize.Y - minDim) / 2 + PADDING;
		float scale = (minDim - PADDING * 2)/(GetChild<Button>(-1).Size.X * 16);
		GD.Print(scale + " " + windowSize.Y + " " + GetChild<Button>(-1).Size.X * 16);
		this.Position = new Vector2I(positionX, positionY);
		this.Scale = new Vector2(scale, scale);	
	}
	private void PopulateDictionary() {
		texturesDict.Add("_0", _0);
		texturesDict.Add("_1", _1);
		texturesDict.Add("_b", _base);
		texturesDict.Add("_h", _highlight);

		texturesDict.Add("x_0", X_0);
		texturesDict.Add("x_1", X_1);
		texturesDict.Add("x_b", X_base);
		texturesDict.Add("x_h", X_highlight);

		texturesDict.Add("w_0", White_0);
		texturesDict.Add("w_1", White_1);
		texturesDict.Add("w_b", White_base);
		texturesDict.Add("w_h", White_highlight);

		texturesDict.Add("b_0", Black_0);
		texturesDict.Add("b_1", Black_1);
		texturesDict.Add("b_b", Black_base);
		texturesDict.Add("b_h", Black_highlight);
	}

	private void GridToGame() {
		for (int row = 0; row < GRID_SIZE; row++) {
			for (int col = 0; col < GRID_SIZE; col++) {
				// GD.Print(row*16 + col);
				GetChild<Button>(row*16 + col).Icon = Icon(row, col);
			}
		}
	}
	
	private Texture2D Icon(int row, int col) {
		String iconKey = gameGrid[row, col] + IconSuffix(row, col);
		// GD.Print(iconKey);
		return texturesDict[iconKey];
	}

	private String IconSuffix(int row, int col) {
		if (IsHighlighted(row, col)) {
			return "_h";
		} else if (IsBase(row, col)) { 
			return "_b";
		} else if((row + col)%2 == 0) {
			return "_0";
		} else {
			return "_1";
		} 
	}

	private bool IsHighlighted(int row, int col) {
		return firstPressCoords.Item1 == row && firstPressCoords.Item2 == col 
			|| secondPressCoords.Item1 == row && secondPressCoords.Item2 == col;
	}

	private void GenerateInitGrid() {
		for (int row = 0; row < GRID_SIZE; row++) {
			for (int col = 0; col < GRID_SIZE; col++) {
				gameGrid[row, col] = InitialOccupation(row, col);
			}
		}
	}
	private String InitialOccupation(int row, int col) {
		if (IsBase(row, col)) {
			return row < 5 ? "w" : "b";
		} else {
			return ""; 
		}
	}

	private bool IsBase(int row, int col) {
		switch ((row, col))
		{
			case var _ when row < 2 && col < 5:
			case (2, _) when col < 4:
			case (3, _) when col < 3:
			case (4, _) when col < 2:
			case (11, _) when col > 13:
			case (12, _) when col > 12:
			case (13, _) when col > 11:
			case var _ when row > 13 && col > 10:
				return true;
			default: 
				return false;
		}
	}

	private void _OnButtonPressed(String buttonName)
	{
		(int row, int col) = ButtonToCoords(buttonName);

		// GD.Print($"Button: {buttonName} pressed");
		// GD.Print("Pressed coords: " + row + " - " + col);
		// GD.Print("Current coords: " + firstPressCoords);
		// GD.Print("Current player:" + currentPlayer);

		if (firstPressCoords == NO_PRESS) {
			if (gameGrid[row, col] == currentPlayer) {
				firstPressCoords = (row, col);
			}
		} else {
			if (gameGrid[row, col] == currentPlayer) {
				firstPressCoords = (row, col);
			}
		}

		// GD.Print("First press: " + firstPressCoords);
		GridToGame();
	}

	private void GeneratePotentialMoves(int row, int col, String player) {

	}
	
	private (int, int) ButtonToCoords(String buttonName) {
		String[] vals = buttonName.Split('_');
		return (int.Parse(vals[0]), int.Parse(vals[1]));
	}
	
	// Called every frame. 'delta' is the elapsed time since the previous frame.
	public override void _Process(double delta)
	{
	}
}
