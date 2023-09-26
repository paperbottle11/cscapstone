# Capstone Logbook
[GitHub Repo](https://github.com/paperbottle11/cscapstone)

<h2>Entries:</h2>
<h3>9/25/23</h3>
<h4>WebGen:</h4>
I added a loading icon that pops up when the model is generating.
Then, I restructured the GPT function from just a general "code" argument that would output a full html file to three arguments: html, css, and js.  This allows me to split the HTML, CSS, and JavaScript code into separate files and makes the model's outputs more reliable and capable.  So far, the websites generated after this change have had better styling, functionality, and general completion of the request.  The bug where it would return the prompt in restated in plaintext instead of actual code has not showed up ever since this change as well.
<h4>TicTacToe:</h4>
No changes.