## Ulysses-Clean-Sheet

Developed by RoyRogers56.

### Ulysses III: *Dirty sheets?*
Sometimes, after copying from web-pages and pasting with Ulysses excellent "Paste from Rich Text", you get too few or too many blank lines. This script cleans and irons out the wrinkles. Test it out!

Does not change your original sheet, just opens a cleaned copy in the Inbox (iCloud)

**Drag sheet** from Ulysses III's sheet list **to Ulysses-Clean-Sheet folder** on Desktop.  
**Python script fixes blank lines and double spaces**, and deliver **clean sheet back in Inbox.**

Use Hazel for smooth laundry service :)

### Need RegEx Find & Replace?
Add two lines at top of sheet in UL codeblocks:  
**'' find:**_regex-pattern_  
**'' repl:**_replace-pattern_  

Then drag sheet as above.

Attributes (in link, image, and video) and Attachments are left untouched.

#### Example:
_Change to US date format (2014-05-09 -> 05/09/2014):_  
**'' find:(\d{4})-(\d{2})-(\d{2})**  
**'' repl:\2/\3/\1** 

For info on RegEx patterns, see: [Python 3.3 RegEx](https://docs.python.org/3.3/howto/regex.html)

**Note:** Does either Clean Blank Lines or RegEx, not both in the same run.
