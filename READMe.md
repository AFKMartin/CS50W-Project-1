# CS50W Project 1 - Wiki Checklist

- [x] Visiting `/wiki/TITLE`, where `TITLE` is the title of an encyclopedia entry, should render a page displaying that entry’s content.  
- [x] The view should retrieve the content using the appropriate `util` function.  
- [x] If an entry does **not exist**, display an error page informing the user that the requested page was not found.  
- [x] If the entry **does exist**, show a page displaying the content of the entry, with the **page title including the entry’s name**.  

--- 
### Index
- [x] Update `index.html` so that instead of merely listing names of all pages, each entry name is a **clickable link** that leads directly to its entry page.  

---
### Search
- [x] Allow the user to type a query into the search box in the sidebar to search for encyclopedia entries.  
- [x] If the query **matches exactly** the name of an entry, redirect the user to that entry’s page.  
- [x] If the query does **not match exactly**, show a **search results page** listing all entries that contain the query as a substring.  
- [x] Each result in the search results page should be a clickable link to that entry’s page.  

---
### New
- [x] Clicking **“Create New Page”** in the sidebar should take the user to a page with a form to create a new entry.  
- [x] The form should contain:  
  - [x] A text input for the entry **title**.  
  - [x] A textarea for the entry **Markdown content**.  
- [x] When the form is submitted:  
  - [x] If an entry with the provided title already exists, show an **error message** instead of overwriting it.  
  - [x] Otherwise, save the new entry and redirect the user to the new entry’s page.  
  - [x] Make the submit buton nice and the content box smaller
---
### Edit
- [x] Each entry page should have a link to **edit** the entry.  
- [x] Clicking that link takes the user to a page with a textarea pre-populated with the entry’s existing Markdown content.  
- [x] The user can edit the content and click a button to **save** their changes.  
- [x] Upon saving, the entry should be updated and the user redirected back to the entry page.  
- [x] title should NOT be editable after creating the post

---
### Random
- [x] Clicking **“Random Page”** in the sidebar should take the user to a random encyclopedia entry.  

---
### Extra
- [x] On each entry page, the Markdown content should be **converted to HTML** before being displayed.  
- [x] Use the `markdown2` Python package (`pip install markdown2`) to perform the conversion.  

**Challenge (optional):**  
- [x] Implement your own Markdown → HTML converter without using external libraries.  
  - Support headings, bold text, unordered lists, links, and paragraphs.  
