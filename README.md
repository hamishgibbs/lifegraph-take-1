# lifegraph

A graph of useful information for getting things done.

### The graph

A series of json files providing data on useful things for getting stuff done.

Git version the data to understand changes over time.

Some ideas:

**Basic Data**
  * People
  * Institutions
  * Email templates
  * Author groups
  * Funder statement
  * People's resumes
  * Address history
  * Deadlines
  * Repetitive personal admin tasks
  * Entire project templates
  * Citations & literature review
  * Literature groups
  * Data collection for projects (like agriculture)
  * Mythology

**Computed Data**
  * Author affiliation statement x
  * Time differences x
  * Timelines x
  * Formatted emails x
  * Turn email into a standard template
  * Meeting minutes
  * Topic annotation linked to meeting transcript
    * i.e. last week you had a meeting with x and y where you mentioned a, b, and c
      * click b for transcript pertaining to b
    * Train model to detect topic after a few labellings
  * Investigations through data
  * Retelling of Greek and Roman stories (and comparison between)
  * vis of entire graph
  * models to extract facts
  * Tag emails, chats, meeting minutes with "topics" and generate summaries about your information on specific topics

### Ideas

Computed data can come from Python scripts with type property annotations
A parser can transform any recognised file type (JSON / csv) into a semantic graph
Then the annotated script can be pointed at the file and the script will identify the information it is supposed to use
Imagine:
  `plot_covid_cases.py` -> Date, Observation.reportedDiseaseCases -> plots cases
  `publication_authorship.py` -> Groups.AuthorGroup -> creates text for an author list and affiliation information

#### 29-03-2022
Would be nice to express approximate dates somehow.

Gen random data from schema for testing and checking that all compute works on current schema

All compute snippets could be automatically tested to ensure that they comply with a certain schema and in many cases they could be automatically updated to comply with a new schema

For automated testing - the thing should be flagged as a compute snippet and must take IDs of annotated type as input
- gen arbitrary data X
- with genned data - unit test graph audit x

- run the compute snippets against the generated data and check for failure x
- if no failure - this snippet will still work with current schema x
- run automated test where keys are either singular or multiple x

- Audit for shadowed inherited properties
- Audit for duplicated entity IDs

- figure out how to package this and use in any project directory

#### 30-03-2022
Zaifen family tree & email templates x
Story about 15 battles

#### Notes
Pretty fucking cool.
It is very easy to update broken code after schema changes and get it working with new schema

Don't completely trust the automated testing yet but is it pretty cool
