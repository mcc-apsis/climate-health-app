import dash_core_components as dcc

relevance_explanation = '''
Documents were included on the basis of a machine-learning algorithm which
was trained using documents labelled by hand to predict the relevance of documents.
There is therefore some uncertainty about whether they are relevant to climate and
health or not. Scores range from 0 to 1 and are to be understood as the probability
that they are relevant.
Documents with higher scores are more likely to be relevant, and
documents with scores lower than 0.35 were not included in the map.
'''

graph_instructions = dcc.Markdown('''
The map on the left shows the places mentioned in climate and health studies,
the bar chart on the right shows the topics mentioned in those studies.
Concretely, the height of the bar shows the share of documents in the region mentioning each topic
divided by the share of global documents mentioning each topic.
The documents are listed in the table below.

Documents were included on the basis of a machine-learning algorithm which
was trained using documents labelled by hand to predict the relevance of documents.
There is therefore some uncertainty about whether they are relevant to climate and
health or not. Scores range from 0 to 1 and are to be understood as the probability
that they are relevant.
Documents with higher scores are more likely to be relevant, and
documents with scores lower than 0.35 were not included in the map.

You can **filter** this data in the following ways

- Filter by relevance score using the slider at the top of the page. Only documents with
a predicted relevance value greater than that selected will be shown.
- Use the dropdown menu to select the region of interest
- Select places on the map by clicking, or clicking and dragging. This will
update the topic distribution on the right and the document table below
- Double click inside the map to reset your selection
- Topics are grouped into types: click on the coloured buttons to filter
the topics displayed in the bar chart
- Click on a bar to filter documents mentioning that topic. These documents
will be highlighted in green in the map, and will appear, sorted by their relevance
to the topic, in the table below.
- Clicking multiple bars will filter for documents containing all of the selected
topics (there may not be any for all combinations), clicking on the same bar twice
will deselect the topic.
- The selected topics are displayed below the graphs on the right hand side.
There is a "Clear topics" button which will deselect all topics.

It is also possible to focus on different parts of each figure.
- Click and drag to zoom in on an area of the bar chart, double click to zoom out again
- If you hover over the map, a toolbar will appear in the top right-hand corner.
Select the "Pan" button to move around the map and zoom in and out.
''')

heatmap_instructions = dcc.Markdown('''
Each cell in the heatmap below shows the number of documents that are linked to
both the category in the cell's row and the category in the cell's column.

Clicking on a cell will fill the table below the heatmap with the documents in
that cell's categories.

By default, cells with higher numbers are darker colours, but you can use the
**normalisation** buttons to adjust how cells are coloured. Normalising by
column sum colours by the cell value divided by the sum of all cells in that column.
This helps to highlight which rows (sums) are particularly relevant to a specific
column (row).

Use the dropdown to switch between types of categories to combine.


''')

topic_instructions = dcc.Markdown('''
Each dot in the map below represents a document related to climate and health.
Hover over it, to see the document's title

Each document is a mixture of different topics, and the map below attempts to show
the topical structure of the list of documents.

The dots are laid out in a 2-dimensional representation of their topical content.
In simple language, this means that documents with similar topics will appear closer together.

The buttons on the right-hand side of the screen give further options for filtering
and displaying the data.

- **World View** (green tab) shows the same documents on a geographical map of the world. Hovering and clicking works in the same way
- **Draw labels** (blue tab) draws labels for each topic that point to clusters of documents related to the topic
- **Continent Filter** (yellow tab) lets you filter the data by continent
- **Topic selector** (red tab) shows a hierarchy of topics. Deselect topics you wish to hide
- **Document filter** (three black lines) lets you filter by searching the document titles.
''')
