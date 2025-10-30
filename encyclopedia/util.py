import re
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
import html

def list_entries():
    """
    Returns a list of all names of encyclopedia entries.
    """
    _, filenames = default_storage.listdir("entries")
    return list(sorted(re.sub(r"\.md$", "", filename)
                for filename in filenames if filename.endswith(".md")))

def save_entry(title, content):
    """
    Saves an encyclopedia entry, given its title and Markdown
    content. If an existing entry with the same title already exists,
    it is replaced.
    """
    filename = f"entries/{title}.md"
    if default_storage.exists(filename):
        default_storage.delete(filename)
    default_storage.save(filename, ContentFile(content))

def get_entry(title):
    """
    Retrieves an encyclopedia entry by its title. If no such
    entry exists, the function returns None.
    """
    try:
        f = default_storage.open(f"entries/{title}.md")
        return f.read().decode("utf-8")
    except FileNotFoundError:
        return None

def html_escape(text):
    # escape HTML special chars like < 
    return html.escape(text, quote=True) 

def inline_markup(text):
    '''
    Handler for links and bold text
    - links: [label](url)
    - bold: **text** or __text__
    ORDER MATTERS: links first, then bold.
    '''
    def repl_link(m):
        label = m.group(1) # extract the link label 
        url = m.group(2) # extract the URL
        safe_url = html.escape(url, quote=True) # escpape special chars in the url
        return f'<a href="{safe_url}">{label}</a>' # return the HTML anchor tag with escaped URL and label
    
    # first replace Markdown-style links with HTML <a> tags with repl_link function
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", repl_link, text)
    
    # then bold (** and __)
    text = re.sub(r"(\*\*|__)(.+?)\1", r"<strong>\2</strong>", text)  

    return text

def markdown_to_html(md):
    '''
    Markdown to hmtl converted
    '''
    if md is None:
        return "" # just in case there is no text, return "" to avoid errors, for some reason this is a thing.
    
    # split the md into individual lines
    lines = md.splitlines() 
    
    # define some empty list we will use later
    html_lines = [] 
    paragraph_lines = [] 
    
    # set this as False since at first we are not in a list
    in_list = False

    def flush_paragraph():
        nonlocal paragraph_lines
        
        if paragraph_lines:
            # join all the lines into a single string separating them with spaces (makes sense now the empty list)
            paragraph_text = " ".join(line.strip() for line in paragraph_lines).strip()
            
            if paragraph_text:
                escaped = html_escape(paragraph_text)
                # append the escaped value to the html_lines (see? we used it)
                html_lines.append(f"<p>{inline_markup(escaped)}</p>")
            
            paragraph_lines = [] # after all, empty this list

    def close_list():
        # helper to close open unordered lists
        nonlocal in_list
        if in_list:
            # adds the closing </ul> tag to the HTML output
            html_lines.append("</ul>")
            # reset the value of the variable since we left the list
            in_list = False

    for l in lines:
        line = l.rstrip() # remove trailing whitespaces from the lines

        if not line.strip(): # if the line is empty or it only has whitespaces do that...
            flush_paragraph() 
            close_list() 
            continue # and continue, this will be repetitive
        
        # header treatment
        m = re.match(r"^(#{1,6})\s+(.*)$", line) # check for headers # or ## or stuff like that
        if m: # if m exists however
            flush_paragraph() 
            close_list()
            level = len(m.group(1)) # calculates the header level, # -> 1  ## -> 2...
            text = m.group(2).strip() # extracts the header title and format it clean
            escaped = html_escape(text) 
            # Now append to html_lines with the level of the header as h(level) and the escaped text.
            html_lines.append(f"<h{level}>{inline_markup(escaped)}</h{level}>") # if for example level is 1, then <h1>
            continue

        # unordered list treatment
        m = re.match(r"^[\-\*\+]\s+(.*)$", line) # check if the line is a list item (e.g., "- item", "* item", "+ item")
        if m:
            flush_paragraph()
            if not in_list:
                html_lines.append("<ul>") # open a new unordered list
                in_list = True # important set this True since we are in a list tho
            item_text = m.group(1).strip()
            escaped = html_escape(item_text)
            html_lines.append(f"<li>{inline_markup(escaped)}</li>")
            continue

        # otherwise a normal paragraph line
        paragraph_lines.append(line)

    # end loop
    flush_paragraph()
    close_list()
    
    return "\n".join(html_lines)       
        

