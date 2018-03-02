Syncing books between repository, website and pagebrowser
------------------------------------------------------------

The workflow is like this:

 1. Books are created (in the form of archivefile) in the repository (using the scanstore)
 2. Books are published on the dasa site
 3. Books are published in the pagebrowser
 
 The idea is to make a little "administration hub" on the dasa website.
 
 This hub:
 
     1. reads books from the repository
     2. syncs information in the django database with the respository
     3. syncs this info with the pagebrowser

The scanstore, on each change, calls the 'hub', which will sync teh necessary data

-----



