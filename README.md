<h1>MovieSpoilerBot</h1>
===============

Evil twitter bot. 


<table><h2>Requirements:</h2> (all free)

<td>SQLite</td>
<td>MongoDB for storage of streaming tweets (not included since it's huge)</td>

For Python:
<tr>BeautifulSoup</tr>
<tr>sqlite3</tr>
<tr>nltk</tr>
<tr>pymongo</tr>
<tr>twitter app with oauth keys</tr>
<tr>urllib2</tr>
<tr>httplib</tr>
<tr>twitter</tr>

</table>

<table>
<h2>How to use: (not functioning YET)</h2>

<tr>Use fetchSpoilers.py first to assemble a SQLite databse of movie titles and spoilers</tr>
<tr>Put your oauth keys into a file called moviespoilerbotkeys.py in a directory above the cloned directory (or just insert them into the appropriate places, I just made it this way to not accidentally commit keys)</tr>
<tr>Run bot_template.py (assuming it is connected to an appropriate database or feed containing twitter data (id,text).</tr>

</table>
