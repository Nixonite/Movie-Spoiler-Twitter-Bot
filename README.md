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
<td>nltk</td>
<td>pymongo</td>
</tr>
<tr>
<td>twitter app with oauth keys</td>
<td>urllib2</td>
<td>httplib</td>
<td>twitter</td>
</tr>

</table>

<h2>How to use: (not functioning YET)</h2>

<ul>
<li>Use fetchSpoilers.py first to assemble a SQLite databse of movie titles and spoilers</li>
<li>Put your oauth keys into a file called moviespoilerbotkeys.py in a directory above the cloned directory (or just insert them into the appropriate places, I just made it this way to not accidentally commit keys)</li>
<li>Run bot_template.py (assuming it is connected to an appropriate database or feed containing twitter data (id,text).</li>

</ul>
