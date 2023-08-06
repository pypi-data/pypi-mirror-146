# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['lcdoc',
 'lcdoc.call_flows',
 'lcdoc.mkdocs',
 'lcdoc.mkdocs.blacklist',
 'lcdoc.mkdocs.custom_dir',
 'lcdoc.mkdocs.find_pages',
 'lcdoc.mkdocs.lp',
 'lcdoc.mkdocs.lp.plugs.bash',
 'lcdoc.mkdocs.lp.plugs.chart',
 'lcdoc.mkdocs.lp.plugs.chartist',
 'lcdoc.mkdocs.lp.plugs.column',
 'lcdoc.mkdocs.lp.plugs.drawio',
 'lcdoc.mkdocs.lp.plugs.flowchart',
 'lcdoc.mkdocs.lp.plugs.kroki',
 'lcdoc.mkdocs.lp.plugs.lightbox',
 'lcdoc.mkdocs.lp.plugs.make_badges',
 'lcdoc.mkdocs.lp.plugs.make_file',
 'lcdoc.mkdocs.lp.plugs.markmap',
 'lcdoc.mkdocs.lp.plugs.mermaid',
 'lcdoc.mkdocs.lp.plugs.python',
 'lcdoc.mkdocs.lp.plugs.python.pyplugs',
 'lcdoc.mkdocs.lp.plugs.python.pyplugs.call_flow_logging',
 'lcdoc.mkdocs.lp.plugs.python.pyplugs.comments',
 'lcdoc.mkdocs.lp.plugs.python.pyplugs.convert',
 'lcdoc.mkdocs.lp.plugs.python.pyplugs.cov_report',
 'lcdoc.mkdocs.lp.plugs.python.pyplugs.data_table',
 'lcdoc.mkdocs.lp.plugs.python.pyplugs.diag_diagram',
 'lcdoc.mkdocs.lp.plugs.python.pyplugs.git_changelog',
 'lcdoc.mkdocs.lp.plugs.python.pyplugs.lprunner',
 'lcdoc.mkdocs.lp.plugs.python.pyplugs.mpl_pyplot',
 'lcdoc.mkdocs.lp.plugs.python.pyplugs.project_dependencies',
 'lcdoc.mkdocs.lp.plugs.python.pyplugs.screenshot',
 'lcdoc.mkdocs.lp.plugs.show_file',
 'lcdoc.mkdocs.lp.plugs.show_src',
 'lcdoc.mkdocs.page_tree',
 'lcdoc.mkdocs.replace',
 'lcdoc.mkdocs.stats']

package_data = \
{'': ['*'],
 'lcdoc': ['assets/mkdocs/*',
           'assets/mkdocs/lcd/partials/*',
           'assets/mkdocs/lcd/src/_snippets/*',
           'assets/mkdocs/lcd/src/md/keepachangelog/*'],
 'lcdoc.mkdocs.lp': ['assets/*',
                     'assets/arch/*',
                     'assets/css/*',
                     'assets/javascript/*',
                     'assets/plantuml/*',
                     'plugs/about/*'],
 'lcdoc.mkdocs.lp.plugs.python.pyplugs.data_table': ['assets/*'],
 'lcdoc.mkdocs.lp.plugs.python.pyplugs.git_changelog': ['assets/keepachangelog/*']}

install_requires = \
['anybadge>=1.7.0,<2.0.0',
 'coverage>=6.0.2,<7.0.0',
 'diagrams',
 'git-changelog',
 'httpx>=0.17.1,<0.18.0',
 'imagesize',
 'inflection>=0.5.1,<0.6.0',
 'markdown-include>=0.6.0,<0.7.0',
 'markupsafe==2.0.1',
 'mkdocs-exclude>=1.0.2,<2.0.0',
 'mkdocs-macros-plugin>=0.5.12,<0.6.0',
 'mkdocs-material>=8,<9',
 'mkdocs-pymdownx-material-extras>=1.1.3,<2.0.0',
 'mkdocs>=1.1.2,<2.0.0',
 'pycond',
 'pytest-cov>=2.10.1,<3.0.0',
 'pytest-randomly>=3.4.1,<4.0.0',
 'pytest-sugar>=0.9.4,<0.10.0',
 'pytest-xdist>=2.1.0,<3.0.0',
 'pytest>=6.0.1,<7.0.0',
 'toml>=0.10.1,<0.11.0']

entry_points = \
{'console_scripts': ['mdrun = lcdoc.lprunner:main'],
 'mkdocs.plugins': ['lcd-blacklist = lcdoc.mkdocs.blacklist:BlacklistPlugin',
                    'lcd-custom-dir = lcdoc.mkdocs.custom_dir:CustomDirPlugin',
                    'lcd-find-pages = '
                    'lcdoc.mkdocs.find_pages:MDFindPagesPlugin',
                    'lcd-lp = lcdoc.mkdocs.lp:LPPlugin',
                    'lcd-md-replace = lcdoc.mkdocs.replace:MDReplacePlugin',
                    'lcd-page-tree = lcdoc.mkdocs.page_tree:PageTreePlugin',
                    'lcd-stats = lcdoc.mkdocs.stats:StatsPlugin']}

setup_kwargs = {
    'name': 'docutools',
    'version': '2022.4.11',
    'description': 'Documentation Tools for the Mkdocs Material Framework',
    'long_description': '#  docutools\n\n<!-- badges -->\n[![docs pages][docs pages_img]][docs pages] [![gh-ci][gh-ci_img]][gh-ci] [![pkg][pkg_img]][pkg] [![code_style][code_style_img]][code_style] \n\n[docs pages]: https://axiros.github.io/docutools\n[docs pages_img]: https://axiros.github.io/docutools/img/badge_docs.svg\n[gh-ci]: https://github.com/axiros/docutools/actions/workflows/ci.yml\n[gh-ci_img]: https://github.com/axiros/docutools/actions/workflows/ci.yml/badge.svg\n[pkg]: https://pypi.org/project/docutools/2022.04.11/\n[pkg_img]: https://axiros.github.io/docutools/img/badge_pypi.svg\n[code_style]: https://pypi.org/project/axblack/\n[code_style_img]: https://axiros.github.io/docutools/img/badge_axblack.svg\n<!-- badges -->\n\n\n## [MkDocs Documentation](https://axiros.github.io/docutools/) Tools For Developers\n\nThis repo is providing a set of plugins for [mkdocs material](https://squidfunk.github.io/mkdocs-material/) compatible documentation.\n\nIt is meant to be used as a development dependency for projects, intended to be used mainly by the\ndevelopers themselves, i.e. for the more technical, code centric parts of software project documentation.\n\nMost notable feature: **[Literate Programming](https://axiros.github.io/docutools/features/lp/)**, i.e. dynamic code execution - tightly integrated within the mkdocs framework.\n\n\n> Most plugins should work in [other](https://www.mkdocs.org/dev-guide/themes/) mkdocs themes as well. No guarantees though.\n\n\n\n## [Feature](https://axiros.github.io/docutools/features/) Gallery\n\n<!-- gallery --><table id=gallery>\n<tr>\n<td style="cursor: pointer" title="features/lp/bash" class="even" onclick="window.location.href=\'features/lp/bash\'">\n<a href="https://axiros.github.io/docutools/features/lp/bash/">bash</a><br/><img onclick="event.stopPropagation();" src="https://axiros.github.io/docutools/features/lp/bash/img/gl_lp_any.png" style="display: block; padding: 3%; margin: auto; max-height: 500px"></img>\n</td>\n<td style="cursor: pointer" title="features/lp/bash" class="odd" onclick="window.location.href=\'features/lp/bash\'">\n<a href="https://axiros.github.io/docutools/features/lp/bash/">bash</a><br/><img onclick="event.stopPropagation();" src="https://axiros.github.io/docutools/features/lp/bash/img/gl_lp_async.png" style="display: block; padding: 3%; margin: auto; max-height: 500px"></img>\n</td>\n<td style="cursor: pointer" title="features/lp/bash" class="even" onclick="window.location.href=\'features/lp/bash\'">\n<a href="https://axiros.github.io/docutools/features/lp/bash/">bash</a><br/><img onclick="event.stopPropagation();" src="https://axiros.github.io/docutools/features/lp/bash/img/gl_lp_ctrl_c.png" style="display: block; padding: 3%; margin: auto; max-height: 500px"></img>\n</td>\n</tr>\n<tr>\n<td style="cursor: pointer" title="features/lp/python/call_flow_logging" class="odd" onclick="window.location.href=\'features/lp/python/call_flow_logging\'">\n<a href="https://axiros.github.io/docutools/features/lp/python/call_flow_logging/">call_flow_logging</a><br/><img onclick="event.stopPropagation();" src="https://axiros.github.io/docutools/features/lp/python/call_flow_logging/img/gl_cfl.png" style="display: block; padding: 3%; margin: auto; max-height: 500px"></img>\n</td>\n<td style="cursor: pointer" title="features/lp/python/call_flow_logging" class="even" onclick="window.location.href=\'features/lp/python/call_flow_logging\'">\n<a href="https://axiros.github.io/docutools/features/lp/python/call_flow_logging/">call_flow_logging</a><br/><img onclick="event.stopPropagation();" src="https://axiros.github.io/docutools/features/lp/python/call_flow_logging/img/gl_cfl_details.png" style="display: block; padding: 3%; margin: auto; max-height: 500px"></img>\n</td>\n<td style="cursor: pointer" title="features/lp/plugs/chart" class="odd" onclick="window.location.href=\'features/lp/plugs/chart\'">\n<a href="https://axiros.github.io/docutools/features/lp/plugs/chart/">chart</a><br/><img onclick="event.stopPropagation();" src="https://axiros.github.io/docutools/features/lp/plugs/chart/img/gl_chart.png" style="display: block; padding: 3%; margin: auto; max-height: 500px"></img>\n</td>\n</tr>\n<tr>\n<td style="cursor: pointer" title="features/lp/plugs/chartist" class="even" onclick="window.location.href=\'features/lp/plugs/chartist\'">\n<a href="https://axiros.github.io/docutools/features/lp/plugs/chartist/">chartist</a><br/><img onclick="event.stopPropagation();" src="https://axiros.github.io/docutools/features/lp/plugs/chartist/img/gl_chartist.png" style="display: block; padding: 3%; margin: auto; max-height: 500px"></img>\n</td>\n<td style="cursor: pointer" title="features/lp/plugs/column" class="odd" onclick="window.location.href=\'features/lp/plugs/column\'">\n<a href="https://axiros.github.io/docutools/features/lp/plugs/column/">column</a><br/><img onclick="event.stopPropagation();" src="https://axiros.github.io/docutools/features/lp/plugs/column/img/gl_columns.png" style="display: block; padding: 3%; margin: auto; max-height: 500px"></img>\n</td>\n<td style="cursor: pointer" title="features/lp/python/comments" class="even" onclick="window.location.href=\'features/lp/python/comments\'">\n<a href="https://axiros.github.io/docutools/features/lp/python/comments/">comments</a><br/><img onclick="event.stopPropagation();" src="https://axiros.github.io/docutools/features/lp/python/comments/img/gl_comments.png" style="display: block; padding: 3%; margin: auto; max-height: 500px"></img>\n</td>\n</tr>\n<tr>\n<td style="cursor: pointer" title="features/lp/python/convert" class="odd" onclick="window.location.href=\'features/lp/python/convert\'">\n<a href="https://axiros.github.io/docutools/features/lp/python/convert/">convert</a><br/><img onclick="event.stopPropagation();" src="https://axiros.github.io/docutools/features/lp/python/convert/img/gl_convert.png" style="display: block; padding: 3%; margin: auto; max-height: 500px"></img>\n</td>\n<td style="cursor: pointer" title="features/lp/python/convert" class="even" onclick="window.location.href=\'features/lp/python/convert\'">\n<a href="https://axiros.github.io/docutools/features/lp/python/convert/">convert</a><br/><img onclick="event.stopPropagation();" src="https://axiros.github.io/docutools/features/lp/python/convert/img/gl_convert_slides.png" style="display: block; padding: 3%; margin: auto; max-height: 500px"></img>\n</td>\n<td style="cursor: pointer" title="features/lp/python/cov_report" class="odd" onclick="window.location.href=\'features/lp/python/cov_report\'">\n<a href="https://axiros.github.io/docutools/features/lp/python/cov_report/">cov_report</a><br/><img onclick="event.stopPropagation();" src="https://axiros.github.io/docutools/features/lp/python/cov_report/img/gl_cov_backref.png" style="display: block; padding: 3%; margin: auto; max-height: 500px"></img>\n</td>\n</tr>\n<tr>\n<td style="cursor: pointer" title="features/lp/python/data_table" class="even" onclick="window.location.href=\'features/lp/python/data_table\'">\n<a href="https://axiros.github.io/docutools/features/lp/python/data_table/">data_table</a><br/><img onclick="event.stopPropagation();" src="https://axiros.github.io/docutools/features/lp/python/data_table/img/gl_data_tables.png" style="display: block; padding: 3%; margin: auto; max-height: 500px"></img>\n</td>\n<td style="cursor: pointer" title="features/lp/python/diag_diagram" class="odd" onclick="window.location.href=\'features/lp/python/diag_diagram\'">\n<a href="https://axiros.github.io/docutools/features/lp/python/diag_diagram/">diag_diagram</a><br/><img onclick="event.stopPropagation();" src="https://axiros.github.io/docutools/features/lp/python/diag_diagram/img/gl_diag.png" style="display: block; padding: 3%; margin: auto; max-height: 500px"></img>\n</td>\n<td style="cursor: pointer" title="features/lp/plugs/drawio" class="even" onclick="window.location.href=\'features/lp/plugs/drawio\'">\n<a href="https://axiros.github.io/docutools/features/lp/plugs/drawio/">drawio</a><br/><img onclick="event.stopPropagation();" src="https://axiros.github.io/docutools/features/lp/plugs/drawio/img/gl_drawio.png" style="display: block; padding: 3%; margin: auto; max-height: 500px"></img>\n</td>\n</tr>\n<tr>\n<td style="cursor: pointer" title="features/find-pages" class="odd" onclick="window.location.href=\'features/find-pages\'">\n<a href="https://axiros.github.io/docutools/features/find-pages/">find-pages</a><br/><img onclick="event.stopPropagation();" src="https://axiros.github.io/docutools/features/find-pages/img/gl_find_pages.png" style="display: block; padding: 3%; margin: auto; max-height: 500px"></img>\n</td>\n<td style="cursor: pointer" title="features/lp/plugs/flowchart" class="even" onclick="window.location.href=\'features/lp/plugs/flowchart\'">\n<a href="https://axiros.github.io/docutools/features/lp/plugs/flowchart/">flowchart</a><br/><img onclick="event.stopPropagation();" src="https://axiros.github.io/docutools/features/lp/plugs/flowchart/img/gl_flow.png" style="display: block; padding: 3%; margin: auto; max-height: 500px"></img>\n</td>\n<td style="cursor: pointer" title="features/lp/python/git_changelog" class="odd" onclick="window.location.href=\'features/lp/python/git_changelog\'">\n<a href="https://axiros.github.io/docutools/features/lp/python/git_changelog/">git_changelog</a><br/><img onclick="event.stopPropagation();" src="https://axiros.github.io/docutools/features/lp/python/git_changelog/img/gl_changel.png" style="display: block; padding: 3%; margin: auto; max-height: 500px"></img>\n</td>\n</tr>\n<tr>\n<td style="cursor: pointer" title="features/lp/plugs/kroki" class="even" onclick="window.location.href=\'features/lp/plugs/kroki\'">\n<a href="https://axiros.github.io/docutools/features/lp/plugs/kroki/">kroki</a><br/><img onclick="event.stopPropagation();" src="https://axiros.github.io/docutools/features/lp/plugs/kroki/img/gl_kroki.png" style="display: block; padding: 3%; margin: auto; max-height: 500px"></img>\n</td>\n<td style="cursor: pointer" title="features/lp/plugs/kroki" class="odd" onclick="window.location.href=\'features/lp/plugs/kroki\'">\n<a href="https://axiros.github.io/docutools/features/lp/plugs/kroki/">kroki</a><br/><img onclick="event.stopPropagation();" src="https://axiros.github.io/docutools/features/lp/plugs/kroki/img/gl_kroki_cheat.png" style="display: block; padding: 3%; margin: auto; max-height: 500px"></img>\n</td>\n<td style="cursor: pointer" title="features/lp/plugs/lightbox" class="even" onclick="window.location.href=\'features/lp/plugs/lightbox\'">\n<a href="https://axiros.github.io/docutools/features/lp/plugs/lightbox/">lightbox</a><br/><img onclick="event.stopPropagation();" src="https://axiros.github.io/docutools/features/lp/plugs/lightbox/img/gl_light.png" style="display: block; padding: 3%; margin: auto; max-height: 500px"></img>\n</td>\n</tr>\n<tr>\n<td style="cursor: pointer" title="features/lp/python/lprunner" class="odd" onclick="window.location.href=\'features/lp/python/lprunner\'">\n<a href="https://axiros.github.io/docutools/features/lp/python/lprunner/">lprunner</a><br/><img onclick="event.stopPropagation();" src="https://axiros.github.io/docutools/features/lp/python/lprunner/img/gl_lprunner.png" style="display: block; padding: 3%; margin: auto; max-height: 500px"></img>\n</td>\n<td style="cursor: pointer" title="features/lp/plugs/make_badges" class="even" onclick="window.location.href=\'features/lp/plugs/make_badges\'">\n<a href="https://axiros.github.io/docutools/features/lp/plugs/make_badges/">make_badges</a><br/><img onclick="event.stopPropagation();" src="https://axiros.github.io/docutools/features/lp/plugs/make_badges/img/gl_badges.png" style="display: block; padding: 3%; margin: auto; max-height: 500px"></img>\n</td>\n<td style="cursor: pointer" title="features/lp/plugs/markmap" class="odd" onclick="window.location.href=\'features/lp/plugs/markmap\'">\n<a href="https://axiros.github.io/docutools/features/lp/plugs/markmap/">markmap</a><br/><img onclick="event.stopPropagation();" src="https://axiros.github.io/docutools/features/lp/plugs/markmap/img/gl_mark.png" style="display: block; padding: 3%; margin: auto; max-height: 500px"></img>\n</td>\n</tr>\n<tr>\n<td style="cursor: pointer" title="features/md-replace" class="even" onclick="window.location.href=\'features/md-replace\'">\n<a href="https://axiros.github.io/docutools/features/md-replace/">md-replace</a><br/><img onclick="event.stopPropagation();" src="https://axiros.github.io/docutools/features/md-replace/img/gl_md_repl.png" style="display: block; padding: 3%; margin: auto; max-height: 500px"></img>\n</td>\n<td style="cursor: pointer" title="features/md-replace" class="odd" onclick="window.location.href=\'features/md-replace\'">\n<a href="https://axiros.github.io/docutools/features/md-replace/">md-replace</a><br/><img onclick="event.stopPropagation();" src="https://axiros.github.io/docutools/features/md-replace/img/gl_md_repl_custom_admons.png" style="display: block; padding: 3%; margin: auto; max-height: 500px"></img>\n</td>\n<td style="cursor: pointer" title="features/lp/plugs/mermaid" class="even" onclick="window.location.href=\'features/lp/plugs/mermaid\'">\n<a href="https://axiros.github.io/docutools/features/lp/plugs/mermaid/">mermaid</a><br/><img onclick="event.stopPropagation();" src="https://axiros.github.io/docutools/features/lp/plugs/mermaid/img/gl_merm.png" style="display: block; padding: 3%; margin: auto; max-height: 500px"></img>\n</td>\n</tr>\n<tr>\n<td style="cursor: pointer" title="features/page-tree" class="odd" onclick="window.location.href=\'features/page-tree\'">\n<a href="https://axiros.github.io/docutools/features/page-tree/">page-tree</a><br/><img onclick="event.stopPropagation();" src="https://axiros.github.io/docutools/features/page-tree/img/gl_tree_ex.png" style="display: block; padding: 3%; margin: auto; max-height: 500px"></img>\n</td>\n<td style="cursor: pointer" title="features/lp/python/project_dependencies" class="even" onclick="window.location.href=\'features/lp/python/project_dependencies\'">\n<a href="https://axiros.github.io/docutools/features/lp/python/project_dependencies/">project_dependencies</a><br/><img onclick="event.stopPropagation();" src="https://axiros.github.io/docutools/features/lp/python/project_dependencies/img/gl_auto_deps.png" style="display: block; padding: 3%; margin: auto; max-height: 500px"></img>\n</td>\n<td style="cursor: pointer" title="features/lp/python" class="odd" onclick="window.location.href=\'features/lp/python\'">\n<a href="https://axiros.github.io/docutools/features/lp/python/">python</a><br/><img onclick="event.stopPropagation();" src="https://axiros.github.io/docutools/features/lp/python/img/gl_lp_html.png" style="display: block; padding: 3%; margin: auto; max-height: 500px"></img>\n</td>\n</tr>\n<tr>\n<td style="cursor: pointer" title="features/lp/python/screenshot" class="even" onclick="window.location.href=\'features/lp/python/screenshot\'">\n<a href="https://axiros.github.io/docutools/features/lp/python/screenshot/">screenshot</a><br/><img onclick="event.stopPropagation();" src="https://axiros.github.io/docutools/features/lp/python/screenshot/img/gl_shots.png" style="display: block; padding: 3%; margin: auto; max-height: 500px"></img>\n</td>\n<td style="cursor: pointer" title="features/stats" class="odd" onclick="window.location.href=\'features/stats\'">\n<a href="https://axiros.github.io/docutools/features/stats/">stats</a><br/><img onclick="event.stopPropagation();" src="https://axiros.github.io/docutools/features/stats/img/gl_stats.png" style="display: block; padding: 3%; margin: auto; max-height: 500px"></img>\n</td>\n<td style="cursor: pointer" title="features/lp/xterm" class="even" onclick="window.location.href=\'features/lp/xterm\'">\n<a href="https://axiros.github.io/docutools/features/lp/xterm/">xterm</a><br/><img onclick="event.stopPropagation();" src="https://axiros.github.io/docutools/features/lp/img/gl__xterm.png" style="display: block; padding: 3%; margin: auto; max-height: 500px"></img>\n</td>\n</tr>\n<tr>\n<td style="cursor: pointer" title="" class="odd" onclick="window.location.href=\'\'">\n</td>\n<td style="cursor: pointer" title="" class="even" onclick="window.location.href=\'\'">\n</td>\n<td style="cursor: pointer" title="" class="odd" onclick="window.location.href=\'\'">\n</td>\n</tr>\n</table><!-- gallery -->',
    'author': 'Gunther Klessinger',
    'author_email': 'gkle_ss_ing_er@gmx.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://axiros.github.io/docutools/',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
