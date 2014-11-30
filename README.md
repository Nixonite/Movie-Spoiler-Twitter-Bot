<h1>MovieSpoilerBot</h1>

Evil twitter bot. 

<table><h2>Requirements (free):</h2> 

<tr>
<td>SQLite</td>
<tr>
<td>MongoDB for storage of streaming tweets (not included since it's huge)</td>
</tr>
</table>

For Python:
<table>
<td>BeautifulSoup</td>
<td>sqlite3</td>
<td>pymongo</td>
</tr>
<tr>
<td>twitter app with oauth keys</td>
<td>twitter</td>
</tr>

</table>

<h2>How to Use the Bot</h2>

<ul>
<li>Use fetchSpoilers.py first to assemble a SQLite databse of movie titles and spoilers</li>
<li>Put your oauth keys into a file called moviespoilerbotkeys.py in a directory above the cloned directory (or just insert them into the appropriate places, I just made it this way to not accidentally commit keys). It is also possible to put them in the same directory as the other files, I suppose it really doesn't matter.</li>
<li>Run database_query.py (assuming it is connected to an appropriate database or feed containing twitter data (id,text). This is the main file that should start the bot and keep it running in a while loop. You can kill it with a keyboard interruption (ctrl+C).</li>
<li>Add appropriate print statements across the database_query.py to help with debugging if problems arise (they shouldn't unless it's a problem connecting to your databases).</li>

</ul>

Enjoy!
