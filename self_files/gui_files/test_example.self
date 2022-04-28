_AddSlots: (| testContainer = container wcopy. 
			  subContainer = container wcopy. 
			  spacingContainer = container wcopy. 
			  testScrollable = scrollableContainer wcopy. 
			  specialLabel = (label clone text: '5') setSizeWidth: 1 Height: 0.3.
			  specialButton = (button clone text: '6') setSizeWidth: 1 Height: 0.3|).
testContainer setSizeWidth: 0.25 Height: 0.4.
testContainer addWidget: 
	((((subContainer setOrientationIsVertical: false) setSizeWidth: 1 Height: 0.2)
		addWidget: ((label clone text: '1') setSizeWidth: 1 Height: 1))
		addWidget: ((button clone text: '2') setSizeWidth: 1 Height: 1)).
testContainer addWidget: testScrollable.
testScrollable addWidget: ((label clone text: '1') setSizeWidth: 1 Height: 1).
testScrollable addWidget: ((label clone text: '1') setSizeWidth: 1 Height: 0.3).
testScrollable addWidget: ((label clone text: '1') setSizeWidth: 1 Height: 0.3).
testScrollable addWidget: ((label clone text: '1') setSizeWidth: 1 Height: 1).
testScrollable addWidget: ((label clone text: '1') setSizeWidth: 1 Height: 0.3).
testScrollable addWidget: specialLabel.
testScrollable addWidget: specialButton.
subContainer setColorR: 0.4 G: 0.1 B: 0.3 A: 1.
spacingContainer setColorR: 0.1 G: 0.2 B: 0.5 A: 1.
specialLabel setColorR: 0.1 G: 0.2 B: 0.5 A: 1.
specialButton setColorR: 0.1 G: 0.7 B: 0.5 A: 1.
testContainer addWidget: (textInput clone text: '3').

canvas addWidget: testContainer

'Containers are always filled in one axis. If horizontal, their subwidgets will fill their entire width, If vertical, their height will be filled'.
'To create empty space in a filled axis, add an empty container'.