<h1>MovieSpoilerBot</h1>
===============

Evil twitter bot. 


<table><h2>Requirements:</h2> (all free)

<td>SQLite</td>
<td>MongoDB for storage of streaming tweets (not included since it's huge)</td>

For Python:
<td>BeautifulSoup</td>
<td>sqlite3</td>
<td>nltk</td>
<td>pymongo</td>
<td>twitter app with oauth keys</td>
<td>urllib2</td>
<td>httplib</td>
<td>twitter</td>

</table>

<table>
<h2>How to use: (not functioning YET)</h2>

<td>Use fetchSpoilers.py first to assemble a SQLite databse of movie titles and spoilers</td>
<td>Put your oauth keys into a file called moviespoilerbotkeys.py in a directory above the cloned directory (or just insert them into the appropriate places, I just made it this way to not accidentally commit keys)</td>
<td>Run bot_template.py (assuming it is connected to an appropriate database or feed containing twitter data (id,text).</td>

</table>
