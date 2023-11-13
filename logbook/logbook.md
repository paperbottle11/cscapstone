# Capstone Logbook
[GitHub Repo](https://github.com/paperbottle11/cscapstone)

<h2>Entries:</h2>
<h3>9/25/23</h3>
<h4>WebGen:</h4>
I added a loading icon that pops up when the model is generating.
Then, I restructured the GPT function from just a general "code" argument that would output a full html file to three arguments: html, css, and js.  This allows me to split the HTML, CSS, and JavaScript code into separate files and makes the model's outputs more reliable and capable.  So far, the websites generated after this change have had better styling, functionality, and general completion of the request.  The bug where it would return the prompt in restated in plaintext instead of actual code has not showed up ever since this change as well.

<h4>Screenshot of a generated page about turtles after the function restructure:</h4>
<img alt="Screenshot of a generated page about turtles" src="TurtlePageGeneration.jpg" style="width: 75%">

<h4>TicTacToe:</h4>
No changes.

<h3>9/28/23</h3>
<h4>WebGen:</h4>
I added comments to the flask app code, and I also created a button that links to the last generated website.  This allows the user to see their last generation without having to type in the exact same query again.  I also fixed the fonts on the input elements and made other styling changes.

<h4>TicTacToe:</h4>
I added comments to the code and fixed the bug where the opponent would place the "O" over an already-filled space.  I solved it by checking if the space is already filled, then generating another move if it is.

<h3>10/4/23</h3>
<h4>WebGen:</h4>
I played around with using multiple responses to build up the website instead generating it all in one response.  However, this proved to create formatting and encoding issues.  Currently, the method of generating the website all at once is the best working, but the prompt has been modified.  The modifications, which primarily shortended it, led to poorer quality websites.  I may have to revert to past prompt.

<h4>TicTacToe:</h4>
This project has been terminated.

<h3>10/7/23</h3>
<h4>WebGen:</h4>
A refresh of the project has occurred since the last entry.  It now generates the full HTML for a website, and the user can select from many premade bootstrap CSS stylesheets with a small menu on the generated website.  It also has the capability to generate the images needed for the website, such as visual aids for the content in the website.

<h3>10/13/23</h3>
<h4>WebGen:</h4>
The project overall works very well, but time consumption is a minor issue as it takes quite a while to generate the images and content.  Measuring the elapsed time and comparing it to the length of the generations is one way of studying its performance and will be used to test it.  Plotting the time elapsed vs. length of content would be a great way to visualize this.

A checkbox to enable image generation was added to the home page, and a diagram of the program was also created.

<img alt="diagram of program" src="diagram.png" style="width: 75%; float: left;">