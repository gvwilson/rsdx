# A Static Web Site

-   Sharing knowledge is the last and most important step of scientific research
-   Journals may require a PDF, but a website will get more readers
-   Use a [static](g:ssg)e generator" %] to create one
-   We will use [Ark][ark] (the same tool used to create this site)

## Site Elements {: #website-elements}

-   Configuration file `config.py` in root directory
    -   Some SSGs use YAML files, then need workarounds for conditionals etc.

[%inc ../example_site/config.py %]

-   [Theme](g:ssg_theme) lives in <code>lib/<em>theme</em></code>
    -   `extensions`: Python to add features (discussed below)
    -   `resources`: CSS and image files copied over as-is
    -   `templates`: for controlling page layout

-   Markdown files with `.md` extension are turned into HTML

[%inc ../example_site/src/index.md %]

-   Transformation relies on a [template](g:ssg_template)
-   We use [Jinja][jinja]

[%inc ../example_site/lib/snails/templates/node.jinja %]

-   `@root` is turned into the path to the root of the generated site
-   <code>{{<em>variable</em>}}</code> is [interpolated](g:interpolation)
    -   <code>site.<em>name</em></code> picks up variables from site configuration
    -   <code>page.<em>name</em></code> picks up variables from page header
    -   <code>{% if <em>condition</em> %}…{% endif %}</code> is conditional

[%inc ../example_site/src/credits.md %]

## Customizing {: #website-customize}

-   SSGs weren't designed with researchers' needs in mind
-   Write our own extensions for things we need and register them as [shortcodes](g:shortcode)
-   What we want:

[%inc ../example_site/src/result.md %]

-   Code for the extension

[%inc ../example_site/lib/snails/extensions/codes.py keep=display_csv %]

[% figure
   id="webiste_screenshot"
   src="website_screenshot.svg"
   alt="screenshot of generated page"
   caption="Generated page."
%]
