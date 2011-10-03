Roar - Python based, easy extendable, blog aware, static site generator
=======================================================================

Roar is a static website generator, forked from
[Growl](http://github.com/xfire/growl/tree), which in turn is heavily
inspired from [Jekyll](http://github.com/mojombo/jekyll/tree/master),
and which shamelessly stole some really cool ideas from Jekyll.

Nevertheless Growl brought some nice features:

* Minimal dependencies
* Easy to install (and use? ;])
* Easy to extend

The [Growl based site of xfire's blog](http://github.com/xfire/downgrade/tree)
is also available on github.

On top, Roar departs from Growl in some aspects:

* Even less dependencies (e.g. Yaml is no longer used)
* Packaged for the PyPi
* Actively maintained


Installation
------------

### Prequisites

The following basic packages are needed:

    > apt-get install python

All other is optional depending on you own needs.

I recommend using [Jinja2][jinja2] as the templating engine. Roar will
use [Jinja2][jinja2] as default, if it is installed.

    > apt-get install python-jinja2

You are free to use some other templating engine like [Django][django],
[Mako][mako] or [Cheetah][cheetah]. for examples how to
configure them, see [extending Roar](#extending_roar).

### Finish the installation

After installing all needed packages, you can use `roar`
directly or copy it to a place which is in your `$PATH`.

    > ./roar ...
    > cp roar /usr/local/bin


Usage
-----

Simply call `roar` with the source directory:

    > roar my.site

Roar will then generate the output in the directory `my.site/_deploy`.
if you want Roar to spit the generated stuff into another directory,
simply specify this director as second parameter.

    > roar my.site /tmp/my.site.output

### options

* `--serve[:port]` (default port: 8080)

  Generate the site to the deploy directory and then start a simple
  webserver. this is intended to be used for testing purposes only.

	> roar my.site --serve 1234

* `--deploy`

  Trigger deploy process. this does nothing per default, but you can
  add actions using hooks. (see `_hooks/deploy_rsync.py`)


Input data
----------

Roar will ignore all files and directories which starts with
a `.` or a `_`. (this can be changed via `Site.IGNORE`, see
[extending Roar](#extending_roar))

All files ending with `_` or a transformer extension (`Config.transformers`)
are processed as **pages**. in these cases, the ending will be striped from
the filename. E.g.

* `index.html_`  ->  `index.html`
* `atom.xml_`  ->  `atom.xml`
* `somefile.txt.markdown`  ->  `somefile.txt`

Some directories beginning with an `_` are special to Roar:

* `_deploy/` the default deploy directory
* `_layout/` contains your site layouts
* `_posts/` contains your posts
* `_hooks/` contains all your hooks (see [extending roar](#extending_roar))
* `_libs/` contains third party code (see [extending roar](#extending_roar))

All **pages** and **posts** must have an `rfc822` header. An empty line
separates the header from the content. Example:

    layout: post
    title: my post title
    category: spam, eggs

    <html>
       <!-- more content here -->
    </html>


If no headers are needed, and *empty* `rfc822` header section consisting
of an empty line before the actual content will work.

All data defined in this header will be attached to the corresponding object
and can be accessed in your template code. an example in [Jinja2][jinja2] may
look like

    <ul>
    {% for post in site.posts|reverse %}
        <li>{{ post.title }} - {{ post.date }}</li>
    {% endfor %}
    </ul>

in the context of your template, you have access to one or more of the following
objects.

### site

This holds the site wide informations.

* `site.now`

  Current date and time when you run roar. this is a Python
  [datetime](http://docs.python.org/library/datetime.html#datetime-objects) object.

    {{ site.now.year }}-{{site.now.month}}

* `site.posts`

  Chronological list of all posts.

    {% for post in site.posts|reverse|slice(8) %}
        {{ post.content }}
    {% endfor %}

* `site.unpublished_posts`

  Chronological list of all unpublished posts. e.g. all posts which set
  `publish` to `false`.

* `site.categories`

  Dictionary mapping category <-> posts.

    <ul>
    {% for cat in site.categories %}
        <li> <stong>{{ cat }}</strong>
            <ul>
                {% for post in site.categories.get(cat) %}
                    <li><a href="{{ post.url }}">{{ post.title }}</a> - {{ post.date }}</li>
                {% endfor %}
            </ul>
        </li>
    {% endfor %}
    </ul>

### page

* `page.url`

  The relative URL to the page.

* `page.transformed`

  The transformed content. no layouts are applied here.

### post

* `post.date`

  A `datetime` object with the publish date of the post.

* `post.url`

  Relative URL to the post.

* `post.publish`

  If set to `false`, the post will be generated, but is not in the list
  of `site.posts`. Instead it's in the `site.unpublished_posts` list.

  If `publish` is not set, Roar will assume this as `true` and the post
  will be normally published.

* `post.content`

  The transformed content. Exactly the layout specified in the `rfc822`
  header is applied  (no recursive applying).

* `post.transformed`

  The transformed content. No layouts are applied here.


<a name="extending_roar"></a>
Extending Roar
--------------

Roar is very easy extendable via Python code placed in the `_hooks` and
`_libs` directory.

If the `_libs` directory exists, it is added to the Python module search path
(`sys.path`), so Python modules dropped there will be available in the code.

All files in the `_hooks` directory, which end with `.py`, are executed
directly in the global scope of the `roar` script. Thus a hook can freely
shape Roar's code at will. Roar loves that! ;)

Here are some examples of what can be done. But you sure can imagine other
cool things.


### Configuring template engines



### Register new transformers

New transformers can be registered in the `Config` class by adding a
filename extension <-> transformation function mapping to the `transformers`
attribute. here's an example for `markdown2`:

    import markdown2
    import functools

    Config.transformers['noop'] = lambda source: source
    Config.transformers['markdown2'] = functools.partial(
                markdown2.markdown,
                extras={'code-color': {"noclasses": True}})

The transformation function must return the transformed source text which is given
as the only parameter. so if you need to add more parameters to your
transformation function, best use the [functools](http://docs.python.org/library/functools.html)
module as you see in the example above.



### Change which files will be ignored

Roar decides to ignore files which filenames start with one of the tokens
defined in `Site.IGNORE`. so a hook with the following content will make
Roar ignore all files begining with `.`, `_` and `foo`.

    Site.IGNORE += ('foo',)



### Define global template context content

Simply add your content to `Site.CONTEXT` like these examples:

    Site.CONTEXT.author = 'Rico Schiekel'
    Site.CONTEXT.site = AttrDict(author = 'Rico Schiekel')

Note: `Site.CONTEXT.site` has to be an `AttrDict` instance!



### Add some verbosity

As an example, we would display the currently processed post, while
Roar chomps your input.

Create a new file (e.g. `verbose.py`) in the `_hooks` directory with the
following content:

    @wrap(Post.write)
    def verbose_post_write(forig, self):
        print 'post: %s - %s\n' % (self.date.strftime('%Y-%m-%d'), self.title)
        return forig(self)

Roar offers the helper decorator `wrap`, which wraps an existing method
of a class with a new one. the original method is given to your new function
as the first parameter (`forig`).




Bug reporting
-------------

Please report bugs [here](http://github.com/Connectical/roar/issues).


License
-------
[GPLv2](http://www.gnu.org/licenses/gpl-2.0.html)



  [jinja2]:  http://jinja.pocoo.org/2/          "jinja2"
  [django]:  http://www.djangoproject.com/      "django"
  [mako]:    http://www.makotemplates.org/      "mako"
  [cheetah]: http://www.cheetahtemplate.org/    "cheetah"

