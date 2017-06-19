# README.md
Patrick Coakley   
Udacity P6  
May 21st, 2017

## Summary

The visualization created for this project was done in order to show that there is a relationship between the handedness of baseball players and their home run performance. The data set used as the basis for this visualization contains 1,157 baseball players' statistics, including weight, height, handedness, and home runs. The final visualization shows that left-handed players were outperforming both right-handed and ambidextrous players by rate of home runs during the period in which this data was being collected. 

## Design
Originally, for this data visualization I wanted to try and do a simple stacked bar chart, but decided that a scatter plot would be more interest to visually see the differences between weight and home runs. I did a bit of prototyping in Tableau, having found it to be a useful tool at the start of this class for learning what you can do with data in a short amount of time. 

When I first began working on the actual first draft, I started using only d3.js. I quickly found that Dimple is much easier to use for this kind of visualization, and switched over using the [example](http://dimplejs.org/examples_viewer.html?id=scatter_standard) found here as the basis for what I wanted to create.

In taking some feedback I received, and through my own personal choices, the design evolved first into a line chart and then an area chart. I chose an area chart design because I think it fits well with the data being explained. The peaks and drops of the lines are more visually pleasing than a simple bar chart, and the opaque backgrounds behind the lines make it easier to distinguish between players' handedness than using straight lines. 

After receiving more feedback and thinking about what I wanted to accomplish, I played around with the idea of a scatter plot and then evolved that design into a bar chart with two ring charts on the side. I felt that this was the best way to easy show the effect of players' handedness and their performance, show both the average home runs per hand, the total home runs per hand, and the total number of players by hand. 

Aside from the data itself, I wanted to make sure my color choices extend to the look of the web page itself, as well as the visualization. I try to avoid using pure black or pure white, and instead chose colors that I feel are pleasurable to look at. Based on some research prior to starting this project, many web designers seem to recommend using off-white or off-black where possible, and I find the results to be much cleaner looking. 

The colors used in the visualization are ones that I felt worked very well together, and in particular I chose all three because the red and the blue can be combined to purple; purple represents the ambidextrous players, who use both their right and left hands. 

## Feedback
	Note: I have included a few previous designs to give an idea of the advancement of this project. 
	
#### Feedback A
* There is no pre-text, so there is no way to understand the narrative trying to be told
* The bins are too narrow

#### Feedback B
* The size of the visualization is quite large
* The formatting of the page looks nice
* Nice color choices

#### Feedback C
* The type of graph is not appropriate for the data being displayed
* The x-axis spacing is not consistent
* Why was this data chosen?

#### Revision A Based On Udacity Reviewer Feedback
After submitting a better version of the area chart, I took the feedback from the reviewer into consideration and decided to change my visualization entirely. As area charts are generally only acceptable for time-oriented visualizations, I played around with the idea of a normal scatter plot, and instead went with a bar chart and two ring charts to focus on the handedness of players. While the bar chart itself is much simpler than the previous designs, I feel that in conjunction with the ring charts it is an easy way to visually understand the differences between the data.

Other parts of the project that were fixed were also spacing issues in my code, as the alignment was off in some areas. 

#### Revision B Based On Udacity Reviewer Feedback
Upon receiving some more feedback after my last submission, I made sure to fix any remaining code quality and formatting issues, the bulk of which were simply inconsistent use of tabs/spaces and spacing issues. Some of the positive feedback received included good commenting in the code, appropriate use of chart type for the visualization, and design choices. I also had to tweak the overall message of the project, making sure that it fit the criteria of being explanatory rather than exploratory. 

### Resources

[Dimple](http://dimplejs.org/)  
[Dimple Scatter Plot Example](http://dimplejs.org/examples_viewer.html?id=scatter_standard)  
[d3](https://d3js.org/)  
[Udacity Forums](https://discussions.udacity.com/c/nd002-data-visualization-with-d3-js)
