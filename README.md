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

**Computed Data**
  * Author affiliation statement x
  * Time differences x
  * Timelines
  * Formatted emails
  * Turn email into a standard template
  * Meeting minutes
  * Topic annotation linked to meeting transcript
    * i.e. last week you had a meeting with x and y where you mentioned a, b, and c
      * click b for transcript pertaining to b
    * Train model to detect topic after a few labellings
  * Investigations through data

### Ideas

Computed data can come from Python scripts with type property annotations
A parser can transform any recognised file type (JSON / csv) into a semantic graph
Then the annotated script can be pointed at the file and the script will identify the information it is supposed to use
Imagine:
  `plot_covid_cases.py` -> Date, Observation.reportedDiseaseCases -> plots cases
  `publication_authorship.py` -> Groups.AuthorGroup -> creates text for an author list and affiliation information

#### 29-03-2022
Would be nice to express approximate dates somehow.

Pretty fucking cool.

Would be nice to give a better indication of which types are expected

Gen random data from schema for testing and checking that all compute works on current schema

Add @type and `schema.jsonx` and check that all types comply with schema. No qualifiers, just additional types. Type can but does not have to have all properties.


Schema:

No docs for now
