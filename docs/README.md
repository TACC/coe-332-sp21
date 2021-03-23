 1 ===================
  2 Tapis Documentation
  3 ===================
  4 
  5 Quickstart
  6 ----------
  7 
  8 1. Create a Python 3 environment
  9 2. Install dependencies ``pip install -r requirements.txt``
 10 3. Build using ``make html`` (Mac/Linux) or ``make.bat html`` (Windows)
 11 
 12 If you ``pip install sphinx-autobuild``, you can use ``make livehtml`` which
 13 will start a server that watches for source changes and will rebuild/refresh
 14 automatically. Go to http://localhost:7898/ to see its output.
 15 
 16 reStructuredText help
 17 ---------------------
 18 
 19 rST is a bit more onerous than Markdown, but it includes more advanced features
 20 like inter-page references/links and a suite of directives.
 21 
 22 - `Sphinx's primer <http://www.sphinx-doc.org/en/stable/rest.html>`_
 23 - `Full Docutils reference <http://docutils.sourceforge.net/rst.html>`_
 24 
 25   - also see its `Quick rST
 26     <http://docutils.sourceforge.net/docs/user/rst/quickref.html>`_ cheat sheet.
 27 
 28 - `Online rST editor <http://rst.ninjs.org/>`_ (it gets some things wrong)
 29 - Other projects that use rST/Sphinx
 30 
 31   - `Python <https://docs.python.org/3/library/index.html>`_: click the "Show
 32     Source" under "This Page" in the sidebar.
 33   - `Sphinx <http://www.sphinx-doc.org/en/stable/rest.html>`_: similar
 34   - Numpy; note that the landing pages are usually coded in HTML and can be
 35     found in the templates directory, e.g. `Numpy's landing page
 36     <https://github.com/numpy/numpy/blob/master/doc/source/_templates/indexcontent.html>`_

